# @Time    : 2019/4/2 15:14
# @Author  : SuanCaiYu
# @File    : run.py
# @Software: PyCharm
import asyncio
import time

from Base import GetIPBase
from config import inspect_threads, pool_size, PROXY_SOURCE_CLASS
from inspect_ip import InspectIP
from pool import Pool
from web_server import run_web_server


async def source_add(ipool: Pool, source: GetIPBase):  #
    task_queue = asyncio.Queue()
    inspect = InspectIP(ipool)
    while True:
        if ipool.size >= pool_size:
            await asyncio.sleep(30)
            continue
        await inspect.create_session()
        result = await source.get_ip()
        [task_queue.put_nowait(ip) for ip in result]
        await asyncio.wait([inspect.handle_tasks(task_queue) for _ in range(inspect_threads)])
        await inspect.session.close()
        await asyncio.sleep(30)


async def inspect_all(ipool: Pool):
    inspect = InspectIP(ipool)
    task_queue = asyncio.Queue()
    await asyncio.sleep(60)
    while True:
        await inspect.create_session()
        pool_data = await ipool.get_inspect_data()
        [task_queue.put_nowait(ip) for ip in pool_data.values()]
        print('开始测试代理是否可用')
        await asyncio.wait([inspect.handle_tasks(task_queue, True) for _ in range(inspect_threads)])
        await inspect.session.close()
        await asyncio.sleep(60 * 5)


def init_porxy_source():
    objs = []
    for cls in PROXY_SOURCE_CLASS:
        if not isinstance(cls, str):
            continue
        clss = cls.split('.')
        exec('from {} import {}'.format('.'.join(clss[:-1]), clss[-1]))
        obj = eval("{}()".format(clss[-1]))
        if isinstance(obj, GetIPBase):
            objs.append(obj)
    return objs


if __name__ == '__main__':
    print('启动代理ip池...')
    proxy_sources = init_porxy_source()
    pool = Pool()
    tasks = [
        inspect_all(pool),
        run_web_server(pool)
    ]
    tasks.extend([source_add(pool, x) for x in proxy_sources])
    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
