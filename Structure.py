# @Time    : 2019/4/2 15:24
# @Author  : SuanCaiYu
# @File    : Structure.py
# @Software: PyCharm


import attr
from attr.validators import instance_of


@attr.s(slots=True)
class IP:
    ip = attr.ib(validator=instance_of(str))
    port = attr.ib(validator=instance_of(int))
    # 协议
    protocol = attr.ib(validator=instance_of(str), default='')
    # 地区
    area = attr.ib(validator=instance_of(str), default='')
    # 匿名度
    category = attr.ib(validator=instance_of(str), default='')

    def get_dict(self):
        return {
            'ip': self.ip,
            'port': self.port,
            'protocol': self.protocol,
            'area': self.area,
            'category': self.category
        }
