# IPool
基于Python3的异步ip代理池
## 使用说明

安装依赖

```
 > pip install requirements.txt
```

编写代理获取源类

```python
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
```

编写配置文件(config.py)

```python
# 同时执行检测方法的个数
inspect_threads = 30

# 代理池最大长度
pool_size = 1000

# 获取代理源的类声明
PROXY_SOURCE_CLASS = [
    # 'GetIP.GetIPWithWeb',
    # 'GetIP.GetIPWithTest',
]
```

运行程序

```
> python run.py
```

## 获取服务

api

```
http://127.0.0.1:8000/proxy
```
---

GET（从代理池中获取代理）

参数

- limit 整数，获取代理的数量，如果代理池中不足，有多少返回多少，默认1
- protocol 取值为 http|https,代理协议，默认不限制
- area 地区名字(如:成都市),默认不限制
- category 匿名度，取值为 普匿|高匿，默认不限制

---

POST（往代理池中写代理,常用于代理循环复用）

参数

- ip 代理的host，必选
- port 代理port，必选
- protocol 代理协议，可选，默认空字符串
- area 代理地区，可选，默认空字符串
- category 代理匿名度，可选，默认空字符串

