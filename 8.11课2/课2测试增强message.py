import socket

# 新增加,用于实现留言板功能，需要定义一个class用于保存请求的数据
class Request(object):
    def __init__(self):
        self.path = ''
        self.query = ''


# 新增加,用于保存message
class Message(object):
    def __init__(self):
        self.message = ''
        self.author = ''

    def __repr__(self):
        return '{}:{}'.format(self.author, self.message)

# 定义全局变量
message_list = []
request = Request()


def log(*args, **kwargs):
    print(log, *args, **kwargs)

def route_index():
    header = 'HTTP/1.X 200 OK\r\nContent-Type = text/html\r\n'
    body = '<h1>Hello World</h1><img src = "doge.gif"/>'
    r = header + '\r\n' + body
    return r.encode('utf-8')


# -----新加
def template(name):
    with open(name, 'r', encoding='utf-8') as f:
        return f.read()
        # 直接运行会显示 error 'gbk' codec can't decode byte 0xaf in position 30: illegal multibyte sequence
        # 因为默认是GBK编码格式,需要encoding='utf-8'

# -----新加
def route_message():  # 称为模板

    msg = Message()
    msg.message = request.query.get('message', '')
    msg.author = request.query.get('author', '')
    message_list.append(msg)
    header = 'HTTP/1.X 200 OK\r\nContent-Type = text/html\r\n'
    # body = '<h1>消息版</h1>'
    body = template('html_basic.html')
    msgs = '<br>'.join([str(m) for m in message_list])#  这里只是单一实现hello:gua 这个功能，需要在模板中塞进去我们要的东西，通过给模板加参数替换
    # <br>在HTML中就是回车
    body = body.replace('{{messages}}', msgs)
    r = header + '\r\n' + body
    return r.encode('utf-8')


def route_image():
    with open('doge.gif', 'rb') as f:
        header = b'HTTP/1.x 200 OK\r\nContent-Tye = /image/doge\r\n\r\n'
        img = header + f.read()
        return img
def error(code=404):
    e = {
        404: b'HTTP/1.x 404 NOT FOUND<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


# 新添加的,处理PATH路径
def parsed_path(path):
    index = path.find('?')
    if index == -1:
        return path, {}
    else:
        # return path.split('?', 1)
        path, query_string = path.split('?', 1)
        # 实现功能：message = hello & author = gua
        # 转换成 {
        #   'message' = 'hello'
        #   'author' = 'gua'
        # }
        args = query_string.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=', 1)
            query[k] = v
        return path, query

def response_for_path(path):
    path, query = parsed_path(path)
    request.path = path   # 相当于全局变量
    request.query = query  # 相当于全局变量
    log('path and query', path, request.query)
    # path : /messages
    # query : message=hello&author=gua 这个时候可以把query做成一个字典再拆分
    r = {
        '/': route_index(),
        '/doge.gif': route_image(),
        '/messages': route_message()  # 新添加的
    }
    response = r.get(path, error())
    return response


def run(host='', port=3000):
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(3)
            connection, address = s.accept()
            r = connection.recv(1024)
            r = r.decode('utf-8')
            log('r = ', r)
            try:
                path = r.split()[1]  # 对PATH的处理是不完善的，因为输出会得到请求为：GET /？message=%E4%BD....空格字符都会被转码
# 实际上request.split()[1]是整一个/？message=%E4%BD....而我们只希望是‘？’这个参数之前的，所以需要增加path = parsed_path(path)
                response = response_for_path(path)
                connection.sendall(response)
            except Exception as e:
                log('error', e)
                connection.close()


if __name__ == '__main__':
    config = dict(
        host='',
        port=3000,
    )
    run(**config)
