# 8.15
# 实现1优化 request全局变量
# 实现2  静态路径绑定和图片绑定（用字典）  route_static(request)
# 实现3 登入界面 route_login(request)
# 实现4 response_for_path 实现字典寻找路径
# 实现5 注册界面（与登入界面类似）
# 实现6 如何用JSON格式保存数据
# JSON 就是一个存储dict或者List的数据格式（现在的通用格式）
# 是dict和list的字符串存储格式，把数据转换为字符串的格式叫做序列化，反之叫做反序列化

# 这节课更新的地方：原来request是手动生成发给服务器的，现在因为Set-Cookie的存在，
# 通过add_headers解析成字典拼接字符串去解决这个问题
# 添加session防止User被窜改
# 共享session服务


# 定义一个 class 用于保存请求的数据
import socket
import urllib.parse

from utils import log
from routes import route_index
# from routes import route_message
# from routes import route_static
# from routes import route_login
from routes import route_dict

class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}  #  从URL分析来看刚好？后面的 message = hello author = gua对应一个字典
        self.body = ''
        self.headers = {}
        self.cookies = {}

        # 新增add_cookies, 目的是将self.headers中获得并切割处理更新cookie
    def add_cookies(self):
        """
        height = 169
        user = gua
        :return:
        """
        cookies = self.headers.get('Cookie', '')
        kvs = cookies.split('; ')
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=')
                self.cookies[k] = v
        # return self.cookies
    # 新增add_headers， 目的是将下列的字符串更新到self.headers中
    def add_headers(self, header):
        """
        header打印出来如下，分割生成字典
        Accept-Language: zh-CN,zh;q=0.8
        Cookie: height=169; user=gua
        """
        # lines = header.split('\r\n')
        # 在run函数中通过切割Header把第一行请求命令删除，结果直接是一个列表
        lines = header
        for line in lines:
            k, v = line.split(': ', 1)
            self.headers[k] = v
        self.add_cookies()
        # return self.add_cookies()

    def form(self):
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        log('读取body中数据', args)
        f = {}
        # 返回f的字典
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        return f
request = Request()


def error(request, code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    # 之前上课我说过不要用数字来作为字典的 key
    # 但是在 HTTP 协议中 code 都是数字似乎更方便所以打破了这个原则
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')



def parsed_path(path):  # 处理过的路径
    """
    message=hello&author=gua
    {
        'message': 'hello',
        'author': 'gua',
    }
    """
    index = path.find('?')
    if index == -1:
        return path, {}
    else:
        path, query_string = path.split('?', 1)
        # query_string ： message=hello&author=gua 需要转换成字典
        args = query_string.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return path, query


def response_for_path(path):
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    # log('path and query', path, query)
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """

    # 简化这里的代码，注册一个字典
    r = {
        '/': route_index,
        # 改成静态路由了
        # '/static': route_static,
        # '/login': route_login,
        # '/messages': route_message,
    }
    r.update(route_dict)
    response = r.get(path, error)
    return response(request)


def run(host='', port=3000):
    """
    启动服务器
    """
    # 初始化 socket 套路
    # 使用 with 可以保证程序中断的时候正确关闭 socket 释放占用的端口
    log('start at', '{}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        # 无限循环来处理请求
        while True:
            # 监听 接受 读取请求数据 解码成字符串
            s.listen(3)
            connection, address = s.accept()
            r = connection.recv(1000)
            r = r.decode('utf-8')
            # log('ip and request, {}\n{}'.format(address, request))
            if len(r.split()) < 2:
                continue
            path = r.split()[1]
            request.method = r.split()[0]
            # 新增
            log('头部等于', r)
            # header =
            """
            GET /favicon.ico HTTP/1.1
            Host: 127.0.0.1:3000
            Connection: keep-alive
            User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36
            Accept: */*
            Referer: http://127.0.0.1:3000/login
            Accept-Encoding: gzip, deflate, sdch
            Accept-Language: zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,fr;q=0.2
            Cookie: user=gua
            """
            # 需要把第一行的请求命令去除
            request.add_headers(r.split('\r\n\r\n', 1)[0].split('\r\n')[1:])


            request.body = r.split('\r\n\r\n', 1)[1]
            response = response_for_path(path)
            connection.sendall(response)
            connection.close()


if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='',
        port=3000,
    )
    # 如果不了解 **kwargs 的用法, 上过基础课的请复习函数, 新同学自行搜索
    run(**config)
