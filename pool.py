# @Time    : 2019/4/3 15:58
# @Author  : SuanCaiYu
# @File    : pool.py
# @Software: PyCharm
import threading
from copy import deepcopy

from Structure import IP

"""
    代理ip主要用内存(dict结构)来存放代理ip，毕竟量级不大，做的比较简单，在扩展性方面还可以优化
"""


class Pool:
    def __init__(self):
        """
        代理ip的存储方式为，以host为key，ip对象为val存在dict中
        """
        self.__pool = {}
        self.__pool_lock = threading.Lock()

    async def insert(self, ip: IP):
        """
        往池子里写入代理ip
        :param ip: IP对象
        :return:
        """
        if ip.ip not in self.__pool.keys():
            self.__pool[ip.ip] = ip
            print(f'添加代理ip:{ip} 当前代理池:{len(self.__pool.items())}')
        else:
            print('已存在的ip')

    async def get(self, limit: int = 1, **kwargs) -> list:
        """
        获取代理ip
        :param limit:获取的个数
        :param kwargs:条件参数
        :return:
        """
        with self.__pool_lock:
            tmp_list = []
            for ip in self.__pool.values():
                if not isinstance(ip, IP):
                    continue
                valid_ip = await self.__protocol(ip, **kwargs)
                if valid_ip:
                    tmp_list.append(valid_ip)
                if len(tmp_list) >= limit:
                    break
            for ip in tmp_list:
                self.__pool.pop(ip.ip)
        return tmp_list

    async def __protocol(self, ip: IP, **kwargs):
        if kwargs.get('protocol'):
            if ip.protocol == kwargs.get('protocol'):
                return await self.__area(ip, **kwargs)
            else:
                return None
        return await self.__area(ip, **kwargs)

    async def __area(self, ip: IP, **kwargs):
        if kwargs.get('area'):
            if ip.area == kwargs.get('area'):
                return await self.__category(ip, **kwargs)
            else:
                return None
        return await self.__category(ip, **kwargs)

    async def __category(self, ip: IP, **kwargs):
        if kwargs.get('category'):
            if ip.category == kwargs.get('category'):
                return ip
            else:
                return None
        return ip

    async def get_inspect_data(self):
        """
        用于获取代理ip拿去定期测试
        :return:
        """
        return deepcopy(self.__pool)

    async def remove(self, key):
        """
        对于测试不合格的代理ip，需要删除
        :param key: 代理ip的host
        :return:
        """
        with self.__pool_lock:
            try:
                self.__pool.pop(key)
            except Exception as e:
                pass
            finally:
                print(f'清除代理ip:{key} 当前代理池:{len(self.__pool.items())}')

    @property
    def size(self):
        """
        定义一个属性,返回当前代理池中代理的数量
        :return:
        """
        with self.__pool_lock:
            return len(self.__pool.items())