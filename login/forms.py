from django.forms import ModelForm
from .models import User
import os.path as osp

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = "__all__"