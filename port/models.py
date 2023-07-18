from django.db import models

# Create your models here.

import socket
import os
import os.path as osp
import logging
import sh
from utils import port_available

logging.basicConfig(level=logging.INFO)


def _collect_port():
    """
    从[10000,11000)的范围内获取可用端口
    """
    while True:
        for p in range(*port_available):
            print(p)
            if not Port._net_is_used(p):
                try:
                    port = Port.objects.get(port_id=p)
                    port.used = False
                    port.save()
                except:
                    port = Port(port_id=p, used=False)
                    port.save()
                yield


collecter = _collect_port()


class Port(models.Model):
    port_id = models.IntegerField(unique=True)
    used = models.BooleanField()

    def __str__(self) -> str:
        return f"{self.port_id}_{self.used}"

    def avaliable_port() -> list:
        return list(Port.objects.filter(used=False).all())

    @staticmethod
    def port_pop() -> int:
        """
        从数据库获取一个可用端口
        """
        if not Port.objects.filter(used=False).exists():
            next(collecter)
        port = Port.objects.filter(used=False).first()
        if Port._net_is_used(port.port_id):
            port.delete()
            return Port.port_pop()
        else:
            port.used = True
            port.save()
            return port.port_id

    @staticmethod
    def port_push(port_id: int):
        """
        将使用过的端口添加进数据库
        """
        try:
            pid = sh.lsof(f"-i:{port_id}", "-t")
            os.system(f"kill -9 {pid}")
        except:
            pass
        try:
            port = Port.objects.get(port_id=port_id)
        except:
            port = Port(port_id=port_id, used=False)
        print(f"delete {port}")
        port.used = False
        port.save()

    @staticmethod
    def _net_is_used(port: int) -> bool:
        """
        判断端口port是否在使用中
        """
        try:
            str(sh.lsof(f"-i:{port}"))
            return True
        except:
            return False
        # 错误的判断方式
        # ip = ip_address
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # try:
        #     s.connect((ip, port))
        #     s.shutdown(2)
        #     return True
        # except:
        #     return False
