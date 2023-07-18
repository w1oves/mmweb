from django.db import models
from utils import get_env_list
import os
import os.path as osp
from codebase.enseg import MMsegStruct
from codebase.darkseg import DarksegStruct
from codebase.vit_adapter import VitAdapterStruct

env_list = tuple((env, env) for env in get_env_list())


class User(models.Model):
    code_bases = (("mmseg", "mmseg"), ("darkseg", "darkseg"),('vit-adapter','vit-adapter'))
    name = models.CharField(max_length=256, unique=True)
    project_dir = models.CharField(max_length=256)
    interpreter_path = models.CharField(max_length=256, choices=env_list)
    code_base = models.CharField(max_length=32, choices=code_bases, default="mmseg")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._meta.get_field("interpreter_path").choices = tuple(
            (env, env) for env in get_env_list()
        )

    def __str__(self) -> str:
        return f"name: {self.name}\nproject dir: {self.project_dir}\ninterpreter path: {self.interpreter_path}\n code base: {self.code_base}"

    def get_info(self) -> MMsegStruct:
        if self.code_base == "mmseg":
            return MMsegStruct(self.project_dir)
        elif self.code_base == "darkseg":
            return DarksegStruct(self.project_dir)
        elif self.code_base=='vit-adapter':
            return VitAdapterStruct(self.project_dir)
        else:
            raise NotImplementedError(f"No code_base implement {self.code_base}")
