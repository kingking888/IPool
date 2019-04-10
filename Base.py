# @Time    : 2019/4/2 15:19
# @Author  : SuanCaiYu
# @File    : Base.py
# @Software: PyCharm
from abc import ABCMeta, abstractmethod


class GetIPBase(metaclass=ABCMeta):

    @abstractmethod
    async def get_ip(self) -> list:
        """
        获取到ip，返回代理ip列表
        :return:
        """
        pass
