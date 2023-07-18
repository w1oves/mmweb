import socket
import os
import os.path as osp
import logging
import sh
from . import port_available

logging.basicConfig(level=logging.INFO)


def _net_is_used(port: int) -> bool:
    """
    判断端口port是否在使用中
    """
    try:
        str(sh.lsof(f"-i:{port}"))
        return True
    except:
        return False


def _collect_port():
    """
    从[10000,11000)的范围内获取可用端口
    """
    while True:
        for p in range(*port_available):
            print("Is available?", p)
            if _net_is_used(p):
                print("Not", p)
            else:
                print("Yes", p)
                yield p


collecter = _collect_port()


class Port:
    cur_port_id = port_available[0]

    @staticmethod
    def get_avaliable_port() -> int:
        if _net_is_used(Port.cur_port_id + 1):
            Port.cur_port_id = next(collecter)
            return Port.cur_port_id
        else:
            Port.cur_port_id = Port.cur_port_id + 1
            return Port.cur_port_id

        # 错误的判断方式
        # ip = ip_address
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # try:
        #     s.connect((ip, port))
        #     s.shutdown(2)
        #     return True
        # except:
        #     return False
