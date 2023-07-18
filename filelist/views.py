# Create your views here.

from django.http import HttpRequest
from login.models import User
from tdb.views import create_tdb
from utils.info_gpu import get_gpu_simple_info
import os
from .models import FileList
from runner.models import train, test


def get_gpus_and_paths(request):
    try:
        choice_paths = request.POST.getlist("choice_multiple_paths")
        gpus = ",".join(request.POST.getlist("choice_gpus"))
    except:
        raise RuntimeError("can not get gpus and paths")
    return choice_paths, gpus


def train_interface(request, user):
    paths, gpus = get_gpus_and_paths(request)
    configs = list(filter(lambda x: x[-3:] == ".py", paths))
    if len(configs) != 1:
        raise RuntimeError("Need exactly one config py")
    if len(gpus) == 0:
        raise RuntimeError("Too less gpu")
    config = configs[0]
    train(user, config, gpus)
    # print(f"{config},{gpus}")


def debug_interface(request, user):
    paths, gpus = get_gpus_and_paths(request)
    configs = list(filter(lambda x: x[-3:] == ".py", paths))
    if len(configs) != 1:
        raise RuntimeError("Need exactly one config py")
    if len(gpus) == 0:
        raise RuntimeError("Too less gpu")
    config = configs[0]
    train(user, config, gpus, debug=True)


def delete_interface(request, user):
    paths, gpus = get_gpus_and_paths(request)
    for path in paths:
        try:
            os.remove(path)
        except:
            continue


def test_interface(request, user, aug_test=False):
    paths, gpus = get_gpus_and_paths(request)
    configs = list(filter(lambda x: x[-3:] == ".py", paths))
    if len(configs) != 1:
        raise RuntimeError("Need exactly one config py")
    weights = list(filter(lambda x: x[-4:] == ".pth", paths))
    if len(weights) != 1:
        raise RuntimeError("Need exactly one model .pth")
    if len(gpus) == 0:
        raise RuntimeError("Too less gpu")
    config = configs[0]
    weight = weights[0]
    test(user, config, gpus, weight, aug_test)
    print(f"{config},{gpus},{weight}")


def multi_test_interface(request, user):
    test_interface(request, user, True)


def button_tdb(request, user):
    choice_paths = request.POST.getlist("choice_multiple_paths")
    create_tdb(user, choice_paths)


def get_filelist(user, type) -> FileList:
    try:
        filelist = user.filelist_set.get(type=type)
    except:
        print("create filelist")
        if type == "config":
            origin_dir = user.get_info().get_config_dir()
        elif type == "record":
            origin_dir = user.get_info().get_work_dir()
        filelist = user.filelist_set.create(
            type=type,
            origin_dir=origin_dir,
            current_dir=origin_dir,
            current_file="is not file",
        )
    return filelist


def view_filelist(request: HttpRequest, user: User, type: str):
    filelist: FileList
    context = {}
    context["gpus"] = get_gpu_simple_info()
    if type == "config":
        buttons = {
            "filelist_train": [
                "训练",
                train_interface,
            ],
            "filelist_delete": [
                "删除",
                delete_interface,
            ],
            "filelist_debug": [
                "调试",
                debug_interface,
            ],
        }
    elif type == "record":
        buttons = {
            "filelist_create_tdb": [
                "创建Tensorboard",
                button_tdb,
            ],
            "filelist_test": [
                "单尺度测试",
                test_interface,
            ],
            "filelist_multi_test": [
                "多尺度测试",
                multi_test_interface,
            ],
        }
    context["filelist_buttons"] = {k: v[0] for k, v in buttons.items()}
    filelist = get_filelist(user, type)
    if request.method == "POST":
        if "choice_path" in request.POST:
            filelist.change_path(request.POST["choice_path"])
        elif "submit_operate" in request.POST and request.POST["operate"]:
            operate = request.POST["operate"]
            buttons[operate][1](request, user)
        elif "text_save" in request.POST and "text_path" in request.POST:
            content = request.POST["text_content"]
            with open(request.POST["text_path"], "w") as f:
                f.write(content)
        elif "close_text" in request.POST:
            print("close_text")
            filelist.current_file = "None"
    filelist.save()
    user.save()
    context.update(filelist.get_context())
    return context
