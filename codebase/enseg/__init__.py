import os.path as osp

"""
startup_train
in: interpreter: str,
    gpus: str,
    config: str,
    port: str,
    cache_dir: str,
    seed=42,
    log_dir=None,
    resume_from=None,
    load_from=None,
out:
    pid
startup_test
in:
    interpreter: str,
    gpus: str,
    config: str,
    weight: str,
    port: str,
    cache_dir: str,
    log_dir=None,
    ms_test=False,
out:
    pid
"""


class MMsegStruct:
    def __init__(self, project_dir) -> None:
        self.config_dir = osp.join(project_dir, "configs")
        self.work_dir = osp.join(project_dir, "work_dirs")
        self.tools_dir = osp.join(project_dir, "tools")
        self.train_script = osp.join(self.get_tools_dir(), "train.py")
        self.test_script = osp.join(self.get_tools_dir(), "test.py")

    def get_work_dir(self):
        return self.work_dir

    def get_config_dir(self):
        return self.config_dir

    def get_tools_dir(self):
        return self.tools_dir
