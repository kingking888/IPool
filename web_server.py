# @Time    : 2019/4/8 10:31
# @Author  : SuanCaiYu
# @File    : web_server.py
# @Software: PyCharm
import json

import tornado.ioloop
import tornado.web
import tornado.options
from tornado import gen

from Structure import IP
from pool import Pool

web_server_pool = None


class PoolServer(tornado.web.RequestHandler):

    @gen.coroutine
    def get(self):
        limit = int(self.get_argument('limit', 1))
        protocol = self.get_argument('protocol', None)
        area = self.get_argument('area', None)
        category = self.get_argument('category', None)
        result = yield web_server_pool.get(limit=limit, protocol=protocol, area=area, category=category)
        json_data = {
            'status': 'ok' if result else 'error',
            'size': len(result) if result else 0,
            'proxy': [ip.get_dict() for ip in result] if result else []
        }
        self.write(json.dumps(json_data))
        self.finish()

    @gen.coroutine
    def post(self):
        ip = self.get_argument('ip')
        port = int(self.get_argument('port'))
        protocol = self.get_argument('protocol', '')
        area = self.get_argument('area', '')
        category = self.get_argument('category', '')
        if (not ip) or (not port):
            self.write({
                'status':'error',
                'msg':'not fund ip or port'
            })
            self.finish()
        try:
            yield web_server_pool.insert(IP(ip, port, protocol, area, category))
        except Exception as e:
            self.write({
                'status': 'error',
                'msg': repr(e)
            })
            self.finish()
        else:
            self.write({
                'status': 'ok',
                'msg': f'current pool size is :{web_server_pool.size}'
            })
            self.finish()


def make_app():
    return tornado.web.Application([
        (r"/proxy", PoolServer),
    ], autoreload=True)


async def run_web_server(pool: Pool):
    global web_server_pool
    web_server_pool = pool
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    pass
