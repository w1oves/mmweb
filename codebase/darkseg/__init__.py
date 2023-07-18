import os.path as osp


class DarksegStruct:
    def __init__(self, project_dir) -> None:
        self.config_dir = osp.join(project_dir, "custom-configs")
        self.work_dir = osp.join(project_dir, "work_dirs")
        self.tools_dir = osp.join(project_dir, "custom-tools")
        self.train_script = osp.join(self.get_tools_dir(), "train.py")
        self.test_script = osp.join(self.get_tools_dir(), "test.py")

    def get_work_dir(self):
        return self.work_dir

    def get_config_dir(self):
        return self.config_dir

    def get_tools_dir(self):
        return self.tools_dir
