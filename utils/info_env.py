import os
import os.path as osp
from typing import Tuple
import socket


def get_env_list() -> Tuple[str]:
    scanned = [".conda", "anaconda3"]
    env_list = []
    home = osp.abspath("/home")
    for user in os.listdir(home):
        user = osp.abspath(osp.join(home, user))
        for p in scanned:
            conda_envs = osp.abspath(osp.join(user, p, "envs"))
            if not osp.isdir(conda_envs):
                continue
            env_list.extend(
                osp.abspath(osp.join(conda_envs, env)) for env in os.listdir(conda_envs)
            )
    if osp.isdir("/opt/anaconda3"):
        env_list.append("/opt/anaconda3")
    return tuple(osp.abspath(osp.join(env, "bin/python")) for env in env_list)


host_ip = None


def get_host_ip():
    """
    查询本机ip地址
    :return:
    """
    global host_ip
    if host_ip is None:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        finally:
            host_ip = ip
            s.close()
    else:
        ip = host_ip
    return ip


def get_cache_dir():
    cache_root = osp.abspath(osp.join(__file__, "..", "..", ".cache"))
    if not osp.isdir(cache_root):
        os.mkdir(cache_root)
    return cache_root


if __name__ == "__main__":
    print(get_env_list())
    print(get_host_ip())
    print((get_cache_dir()))
