import os
import os.path as osp

# Create your views here.
from typing import List

import sh
from django.http import HttpRequest
from login.models import User
from utils.info_port import Port
from utils.info_env import get_cache_dir, get_host_ip

from .models import TDB


def create_tdb(parent: User, paths: List[str]) -> TDB:
    cache_root = get_cache_dir()
    port = Port.get_avaliable_port()
    cache_dir = osp.join(cache_root, f"tdb:{port}")
    if osp.isdir(cache_dir):
        print("remove", cache_dir)
        sh.rm("-rf", cache_dir)
    os.mkdir(cache_dir)
    name = "<br>".join(osp.basename(p) for p in paths)
    link = f"{get_host_ip()}:{port}"
    for path in paths:
        sh.ln("-s", path, osp.join(cache_dir, osp.basename(path)))
    p = sh.tensorboard(
        f"--logdir={cache_dir}",
        "--bind_all",
        "--samples_per_plugin=images=1000",
        f"--port={port}",
        _bg=True,
    )
    tdb = parent.tdb_set.create(
        port=port, pid=p.pid, name=name, link=link, cache_dir=cache_dir
    )
    tdb.save()
    return tdb


def close_tdb(port):
    if TDB.objects.filter(port=port).exists():
        TDB.objects.filter(port=port).first().delete()


def close_all_user_tdb(user):
    for q in user.tdb_set.all():
        q.delete()


def view_tdb(request: HttpRequest, user: User):
    if "close_all" in request.POST:
        close_all_user_tdb(user)
    tdbs = user.tdb_set.all()
    return {"TDBs": tdbs}
