# Create your models here.
import re
from django.db import models
from login.models import User
import sh
import os
import os.path as osp
from utils import get_cache_dir, get_gpu_simple_info
from utils.info_port import Port
import tdb
import torch
from utils import debug_port
import time

pid_pool = dict()


def check_pid(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


class Runner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gpus = models.CharField(max_length=20)
    pid = models.IntegerField()
    port = models.IntegerField()
    config = models.CharField(max_length=200)
    log_dir = models.CharField(max_length=200)
    cache_file = models.CharField(max_length=200)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.user.name}:{self.port}"

    def delete(self, using=False, keep_parents=False):
        self.stop()
        return super().delete(using=using, keep_parents=keep_parents)

    def get_pids_by_port(self):
        pids = []
        try:
            pids = sh.lsof(f"-i:{int(self.port)}", "-t")
        except:
            pids = self.pid
        return pids

    def stop(self):
        try:
            for tdb in self.tdb_set.all():
                tdb.delete()
        except:
            pass
        try:
            if self.pid != 0:
                os.system(f"kill -9 {self.pid}")
            pids = self.get_pids_by_port()
            for pid in pids:
                pid: str
                pid = pid.strip("\n")
                os.system(f"kill -9 {pid}")
            os.remove(self.cache_file)
        except:
            pass
        finally:
            print(f"stop success")

    def get_context(self, short_line=-1):
        context = {}
        if osp.isfile(self.cache_file):
            with open(self.cache_file, "r", encoding="utf-8") as f:
                try:
                    lines = f.readlines()
                    if len(lines) > 400:
                        lines = lines[10:300] + lines[-100:]
                    context["log"] = "".join(lines)
                    result = re.match(
                        r".*\[(\d+/\d+)\].*eta:(.*), time(.*), data_time", lines[-1]
                    )
                    if result:
                        try:
                            short_text = f"Iter: {result.group(1)}, ETA: {result.group(2)}, AVG: {result.group(3)}"
                        except:
                            short_text = "<br>".join(lines[short_line:])
                    else:
                        short_text = "<br>".join(lines[short_line:])
                    context["simple_log"] = "*" + short_text
                except IOError as e:
                    context["log"] = str(e)
                    context["simple_log"] = str(e)
                except:
                    context["log"] = "code error"
                    context["simple_log"] = "code error"
        context["gpus"] = "\n".join(
            get_gpu_simple_info(int(gpu))["text"] for gpu in self.gpus if gpu.isdigit()
        )
        context["pid"] = self.pid
        context["port"] = self.port

        context["root_dir"] = osp.relpath(
            osp.dirname(self.config), self.user.get_info().config_dir
        )
        context["config"] = osp.basename(self.config)
        context["alive"] = check_pid(self.pid)
        context["buttons"] = self.get_buttons()["context"]
        context["jump_button"] = self.log_dir
        if len(self.tdb_set.all()) > 0:
            tdb = self.tdb_set.all().first()
            context["link"] = tdb.link

        return context

    def get_buttons(self):
        pass

    def jump_log_dir(self):
        print("enter jump")
        from filelist.views import get_filelist

        filelist = get_filelist(self.user, "record")
        filelist.current_dir = self.log_dir


class TrainRunner(Runner):
    resume_from = models.CharField(max_length=200)
    load_from = models.CharField(max_length=200)

    def get_buttons(self):
        if not hasattr(self, "buttons"):
            buttons = [
                ["delete", self.delete],
                ["debug", self.debug],
                ["retry", self.retry],
                ["resume", self.resume],
                ["pause", self.stop],
                ["single test", self.single_test],
                ["multi test", self.multi_test],
            ]
            context = {}
            callback = {}
            for button in buttons:
                key = f"{self.pk}_{button[0]}"
                context[key] = button[0]
                callback[key] = button[1]
            self.buttons = dict(
                context=context,
                callback=callback,
            )
        return self.buttons

    def get_context(self):
        context = super().get_context()
        if len(self.resume_from) > 1:
            context["resume_from"] = self.resume_from
        if len(self.load_from) > 1:
            context["load_from"] = self.load_froms
        context["pid"] = self.pid
        return context

    def retry(self):
        self.stop()
        self.startup()
        return self

    def resume(self):
        self.stop()
        self.startup(resume=True)
        return self

    def debug(self):
        self.stop()
        self.startup(debug=True)
        return self

    def get_weights(self):
        latest = osp.join(self.log_dir, "latest.pth")
        meta = torch.load(latest, map_location=torch.device("cpu"))["meta"]
        hook_msgs = meta["hook_msgs"]
        best = ""
        if "best_ckpt" in hook_msgs:
            best_weight = hook_msgs["best_ckpt"]
            if osp.isfile(best_weight):
                best = best_weight
        return latest, best

    def single_test(self):
        latest, best = self.get_weights()
        test(self.user, self.config, self.gpus, latest)
        test(self.user, self.config, self.gpus, best)

    def multi_test(self):
        latest, best = self.get_weights()
        test(self.user, self.config, self.gpus, latest, aug_test=True)
        test(self.user, self.config, self.gpus, best, aug_test=True)

    def startup(self, resume=False, debug=False):
        if debug:
            assert len(self.gpus) == 1
        # need parameters
        user = self.user
        config = self.config
        gpus = self.gpus

        # startup
        python = sh.Command(user.interpreter_path)
        train_script = user.get_info().train_script
        if len(self.gpus) > 2:
            port = Port.get_avaliable_port()
        else:
            port = int(time.time()) % 1000
        cache_file = osp.join(get_cache_dir(), f"{port}.log")
        log_dir = osp.join(
            user.get_info().work_dir,
            osp.basename(osp.dirname(config)),
            osp.splitext(osp.basename(config))[0],
        )
        args = []
        if len(self.gpus) > 2:
            args.extend(
                [
                    "-m",
                    "torch.distributed.launch",
                    f'--nproc_per_node={len(gpus.split(","))}',
                    f"--master_port={port}",
                ]
            )
        if debug:
            args.extend(
                [
                    "-m",
                    "debugpy",
                    "--listen",
                    debug_port,
                ]
            )
        args.extend(
            [
                train_script,
                config,
                f"--work-dir={log_dir}",
            ]
        )
        if len(self.gpus) > 2:
            args.extend(
                [
                    "--launcher",
                    "pytorch",
                ]
            )
        if resume:
            latest, _ = self.get_weights()
            args.extend(
                [
                    f"--resume-from={latest}",
                ]
            )

        p = python(
            *args,
            _env={"CUDA_VISIBLE_DEVICES": gpus},
            _bg=True,
            _out=cache_file,
            _err_to_out=True,
        )
        print(" ".join(args))
        self.pid = p.pid
        self.port = port
        self.log_dir = log_dir
        self.cache_file = cache_file
        tdb.views.create_tdb(self, [log_dir])
        self.save()

    def get_latest_weight(self):
        return osp.join(self.log_dir, "latest.pth")


class TestRunner(Runner):
    weight = models.CharField(max_length=200)
    aug_test = models.BooleanField()

    def get_buttons(self):
        if not hasattr(self, "buttons"):
            buttons = [
                ["delete", self.delete],
                ["single test", self.retry_for_single_test],
                ["multi test", self.retry_for_aug_test],
                ["pause", self.stop],
            ]
            context = {}
            callback = {}
            for button in buttons:
                key = f"{self.pk}_{button[0]}"
                context[key] = button[0]
                callback[key] = button[1]
            self.buttons = dict(
                context=context,
                callback=callback,
            )
        return self.buttons

    def get_context(self):
        context = super().get_context(short_line=-5)
        context["root_dir"] = osp.relpath(
            osp.dirname(self.config), self.user.get_info().work_dir
        )
        context["weight"] = osp.basename(self.weight)
        context["aug_test"] = self.aug_test
        return context

    def startup(self, aug_test=False):
        user = self.user
        test_script = user.get_info().test_script
        config = self.config
        gpus = self.gpus
        aug_test = aug_test
        weight = self.weight
        python = sh.Command(user.interpreter_path)
        port = Port.get_avaliable_port()
        cache_file = osp.join(get_cache_dir(), f"{port}.log")
        log_dir = osp.dirname(weight)
        if aug_test:
            p = python(
                test_script,
                config,
                weight,
                f"--work-dir={log_dir}",
                "--eval=mIoU",
                "--aug-test",
                _env={"CUDA_VISIBLE_DEVICES": gpus},
                _bg=True,
                _out=cache_file,
                _err_to_out=True,
            )
        else:
            p = python(
                test_script,
                config,
                weight,
                f"--work-dir={log_dir}",
                "--eval=mIoU",
                _env={"CUDA_VISIBLE_DEVICES": gpus},
                _bg=True,
                _out=cache_file,
                _err_to_out=True,
            )
        self.pid = p.pid
        self.port = port
        self.log_dir = log_dir
        self.cache_file = cache_file
        self.weight = weight
        self.aug_test = aug_test
        self.save()

    def retry_for_aug_test(self):
        self.stop()
        self.startup(aug_test=True)
        return self

    def retry_for_single_test(self):
        self.stop()
        self.startup(aug_test=False)
        return self


def train(
    user: models.Model, config, gpus, load_from=None, resume_from=None, debug=False
):
    port = Port.get_avaliable_port()
    cache_file = osp.join(get_cache_dir(), f"{port}.log")
    # stream = open(cache_file, "w")
    log_dir = osp.join(user.get_info().work_dir, osp.splitext(osp.basename(config))[0])

    runner = user.trainrunner_set.create(
        gpus=gpus,
        pid=0,
        port=port,
        config=config,
        log_dir=log_dir,
        cache_file=cache_file,
        resume_from="",
        load_from="",
    )
    runner.startup(debug=debug)
    runner.save()
    return runner


def test(user: models.Model, config, gpus, weight, aug_test=False):
    port = Port.get_avaliable_port()
    cache_file = osp.join(get_cache_dir(), str(port))
    log_dir = osp.join(user.get_info().work_dir, osp.splitext(osp.basename(config))[0])
    runner = user.testrunner_set.create(
        gpus=gpus,
        pid=0,
        port=port,
        config=config,
        log_dir=log_dir,
        cache_file=cache_file,
        weight=weight,
        aug_test=aug_test,
    )
    runner.startup(aug_test)
    runner.save()
    return runner


def close_all_runner(user):
    for t in user.testrunner_set.all():
        t.delete()
    for t in user.trainrunner_set.all():
        t.delete()
