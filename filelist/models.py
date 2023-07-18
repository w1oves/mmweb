from django.db import models
import json
import pandas as pd
from json import JSONDecodeError

# Create your models here.
import os
import os.path as osp
from collections import OrderedDict
from typing import Dict

from django.db import models
from django.forms import ModelForm
from login.models import User
from mdeditor.fields import MDTextField


class Editor(models.Model):
    text_path = models.CharField(max_length=256)
    text_content = MDTextField()


class EditorForm(ModelForm):
    class Meta:
        model = Editor
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text_path"].widget.attrs.update(size="60")


# Create your models here.
class FileList(models.Model):
    valid_type = (
        ("record", "record"),
        ("config", "config"),
        ("code", "code"),
        ("data", "data"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=16, choices=valid_type)
    origin_dir = models.CharField(max_length=256)
    current_dir = models.CharField(max_length=256)
    current_file = models.CharField(max_length=256)

    def __str__(self) -> str:
        return f"""
        user:{self.user}
        type:{self.type}
        origin_dir:{self.origin_dir}
        current_dir:{self.current_dir}
        current_file:{self.current_file}
        """

    def get_context(self) -> Dict[str, str]:
        context = dict(default_paths=OrderedDict())        
        context["default_paths"]["origin"] = self.origin_dir
        context["default_paths"][".."] = osp.abspath(osp.join(self.current_dir, ".."))
        context["default_paths"][f"{self.current_dir}"] = self.current_dir
        if not osp.isdir(self.current_dir) and self.current_dir != self.origin_dir:
            self.change_path(self.origin_dir)
            return self.get_context()
        paths = {
            path: osp.join(self.current_dir, path)
            for path in sorted(os.listdir(self.current_dir))
        }
        context["files"] = {
            path: abs_path for path, abs_path in paths.items() if osp.isfile(abs_path)
        }
        context["dirs"] = {
            path: abs_path for path, abs_path in paths.items() if osp.isdir(abs_path)
        }
        if osp.isfile(self.current_file):
            context["current_file"] = self.current_file
            self.deal_file(self.current_file, context)
        else:
            context["current_file"] = "no  file"
        return context

    def get_json_content(self, file_path: str):
        try:
            with open(file_path, "rt") as f:
                try:
                    content = json.load(f)
                except JSONDecodeError:
                    f.seek(0, 0)
                    content = [json.loads(line) for line in f.readlines()]
            df = pd.DataFrame(content[1:])
            text = ["Json Content"]
            try:
                if "mIoU" in df:
                    text.append(
                        f"mIoU: latest:{df['mIoU'][df['mIoU'].last_valid_index()]} best:{df['mIoU'].max()}, mean:{df['mIoU'].mean()}"
                    )
                if "0_mIoU" in df:
                    text.append(
                        f"0_mIoU: latest:{df['0_mIoU'][df['0_mIoU'].last_valid_index()]}, best:{df['0_mIoU'].max()}, mean:{df['0_mIoU'].mean()}"
                    )
                if "1_mIoU" in df:
                    text.append(
                        f"1_mIoU: latest:{df['1_mIoU'][df['1_mIoU'].last_valid_index()]}, best:{df['1_mIoU'].max()}, mean:{df['1_mIoU'].mean()}"
                    )
                if "aAcc" in df:
                    text.append(
                        f"aAcc: max:{df['aAcc'].max()}, mean:{df['aAcc'].mean()}"
                    )
                if "mAcc" in df:
                    text.append(
                        f"mAcc: max:{df['mAcc'].max()}, mean:{df['mAcc'].mean()}"
                    )
                if "psnr" in df:
                    text.append(
                        f"psnr: max:{df['psnr'].max()}, mean:{df['psnr'].mean()}"
                    )
                if "memory" in df:
                    text.append(f"memory: mean:{df['memory'].mean()}")
                if "data_time" in df:
                    text.append(f"data_time: mean:{df['data_time'].mean()}")
                if "time" in df:
                    text.append(f"time: mean:{df['time'].mean()}")
            except:
                pass
            return "\n".join(text)
        except:
            return self.get_txt_content(file_path)

    def get_txt_content(self, file_path):
        try:
            with open(self.current_file, "r") as f:
                return "".join(f.readlines())
        except:
            return f"read {self.current_file} fail"

    def deal_file(self, file_path: str, context: dict):
        if file_path.endswith(".json"):
            context["file_content"] = self.get_json_content(file_path)
        elif file_path.endswith(".pth"):
            context["file_content"] = f"read {self.current_file} fail"
        else:
            context["file_content"] = self.get_txt_content(file_path)
        editor = Editor(
            text_path=self.current_file, text_content=context["file_content"]
        )
        form = EditorForm(instance=editor)
        context["editor_form"] = form
        return form

    def change_path(self, path: str) -> None:
        print("from", self.current_dir)
        if osp.isfile(path):
            self.current_file = path
        else:
            self.current_dir = path
        print("change to", self.current_dir)
