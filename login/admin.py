import imp
from django.contrib import admin
from filelist.models import FileList
from runner.models import TestRunner
from runner.models import TrainRunner
from .models import User
# from port.models import Port
from tdb.models import TDB

# Register your models here.
admin.site.register(FileList)
admin.site.register(TrainRunner)
admin.site.register(TestRunner)
admin.site.register(User)
# admin.site.register(Port)
admin.site.register(TDB)
