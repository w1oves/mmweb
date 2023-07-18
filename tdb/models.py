from django.db import models

# Create your models here.
import os

import shutil

from runner.models import TrainRunner, TestRunner
import sh
from django.db import models


from login.models import User
# from port.models import Port


# Create your models here.
class TDB(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    TrainRunner = models.ForeignKey(TrainRunner, on_delete=models.CASCADE, null=True)
    TestRunner = models.ForeignKey(TestRunner, on_delete=models.CASCADE, null=True)
    port = models.IntegerField(unique=True)
    pid = models.IntegerField()
    name = models.CharField(max_length=200)
    link = models.URLField()
    cache_dir = models.CharField(max_length=200)

    def delete(self, using=False, keep_parents=False):
        print("Delete tensorboard", self.port)
        os.system(f"kill -9 {self.pid}")
        shutil.rmtree(self.cache_dir)
        return super().delete(using=using, keep_parents=keep_parents)
