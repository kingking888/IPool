# @Time    : 2019/4/2 15:18
# @Author  : SuanCaiYu
# @File    : GetIP.py
# @Software: PyCharm

import requests

from Structure import IP
from Base import GetIPBase


# 测试类，实现代理源类就是继承GetIPBase，然后实现get_ip方法，返回一个元素都是IP对象的列表就行
class GetIPWithTest(GetIPBase):

    async def get_ip(self) -> list:
        proxys = [
            IP(ip='182.61.101.84', port=443, protocol='http', area='北京市', category='普匿'),
            IP(ip='178.128.116.43', port=8000, protocol='http', area='希腊', category='普匿'),
            IP(ip='159.192.101.8', port=80, protocol='http', area='泰国', category='普匿'),
            IP(ip='212.83.142.185', port=54321, protocol='http', area='法国', category='普匿'),
            IP(ip='188.166.231.141', port=3128, protocol='http', area='新加坡', category='普匿'),
        ]
        return proxys


# 本类为我司的代理商获取代理类，仅作参考
class GetIPWithWeb(GetIPBase):
    def __init__(self):
        self.api = 'http://vtp.daxiangdaili.com/ip/'
        self.args = {
            'tid': 111,
            'num': 500,
            'format': 'json',
            'show_area': 'true',
        }

    async def get_ip(self) -> list:
        ip_list = []
        for protocol in ['http', 'https']:
            for category in [0, 2]:  # 普匿(0) / 高匿(2)
                tmp_args = {
                    'protocol': protocol,
                    'category': category
                }
                tmp_args.update(self.args)
                try:
                    resp = requests.get(self.api, params=tmp_args)
                    data = resp.json()
                    for row in data:
                        ip_list.append(
                            IP(row.get('host'), row.get('port'), protocol, row.get('area'),
                               '普匿' if category == 0 else '高匿'))
                except Exception as e:
                    print(repr(e))
        return ip_list
