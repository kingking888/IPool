# @Time    : 2019/4/2 19:42
# @Author  : SuanCaiYu
# @File    : inspect_ip.py
# @Software: PyCharm
import asyncio

import aiohttp

from Structure import IP
from config import inspect_threads
from pool import Pool


class InspectIP:

    def __init__(self, ip_pool: Pool):
        """
        代理池检测
        :param ip_pool: 操作的代理池
        """
        self.max_threads = inspect_threads
        self.ip_pool = ip_pool

    async def handle_tasks(self, work_queue: asyncio.Queue, check: bool = False):
        """
        任务检测
        :param work_queue:检测的队列
        :param check: 是否是定期检测
        :return:
        """
        while not work_queue.empty():
            task = await work_queue.get()
            try:
                await self.protocol(task, check)
            except Exception as e:
                pass

    async def protocol(self, task: IP, check: bool = False):
        """
        实际检测方法
        :param task:需要检测的任务
        :param check: 是否为定期检测，如果为定期检测，未成功需要从代理池中删除对应的代理，
                        如果为初次添加检测代理，未成功不做反应，成功则添加进入代理池
        :return:
        """
        if task.protocol == 'https':
            url = 'https://www.baidu.com'
            proxy = f"https://{task.ip}:{task.port}"
        else:

            url = 'http://2019.ip138.com/ic.asp'
            proxy = f"http://{task.ip}:{task.port}"
        try:
            async with self.session.get(url, proxy=proxy, timeout=20, allow_redirects=False) as resp:
                if (not check) and (resp.status == 200):
                    await self.ip_pool.insert(task)
                if check and (resp.status != 200):
                    await self.ip_pool.remove(task.ip)
                resp.close()
        except Exception as e:
            if check:
                await self.ip_pool.remove(task.ip)

    async def create_session(self, **kwargs):
        self.session = await aiohttp.ClientSession(**kwargs).__aenter__()
