# @Time    : 2019/4/2 15:18
# @Author  : SuanCaiYu
# @File    : config.py
# @Software: PyCharm


# 同时执行检测方法的个数
inspect_threads = 30

# 代理池最大长度
pool_size = 1000

# 获取代理源的类声明
PROXY_SOURCE_CLASS = [
    'GetIP.GetIPWithWeb',
    'GetIP.GetIPWithTest',
]
