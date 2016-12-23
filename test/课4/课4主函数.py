import socket
import urllib.parse
from model import User
import  random

# 功能实现：注册用户第一次赋值ID，已经存在ID值的用户替换内容，重复ID无效
session = {}

class Request(object):
    def __init__(self):
        self.body = ''
        self.path = ''
        self.query = {}
        self.body = ''
        self.headers = {}
        self.cookies = {}

    def form(self):
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        query = {}
        for arg in args:
            k ,v = arg.split('=')
            query[k] = v
        return query
    def add_headers(self, header):
        lines = header
        for line in lines:
            k, v  = line.split(': ', 1)
            self.headers[k] = v
        self.add_cookies()
    def add_cookies(self):
        cookies = self.headers.get('Cookie', '')
        kvs = cookies.split(';')
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=')
                self.cookies[k]= v


request =  Request()

def template(name):
    path = 'templates/'+ name
    with open(path, 'r', encoding= 'utf-8') as f:
        return f.read()

def response_with_headers(headers):
    header = 'HTTP/1.x 200 Ok\r\n'
    header += ''.join(['{}: {}\r\n'.format(k, v) for k, v in headers.items()])
    return header

def random_str():
    seed = 'asddaskfdfjkjkndsldsdddss'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) -1 )
        s += seed[random_index]
    return s

def currenet_user(request):
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '游客')

def route_login(request):
    headers = {
        'Content-Type': 'text/html',
    }
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_login():
            seesion_id = random_str()
            session[seesion_id] = u.username
            headers['Set-Cookie']= 'user= {}'.format(seesion_id)
            result  = '登入成功'
        else:
            result = '账号或者密码错误'
    else:
        result = ''
    body = template('login.html')
    body = body.replace('{{result}}', result)
    header = response_with_headers(headers)
    response = header + '\r\n'+ body
    return response.encode('utf-8')


def route_register(request):
    header = 'HTTP/1.x 200 OK\r\nContent-Type: Text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        print('form=', form)
        #  {'password': '123', 'username': '123'}
        u = User(form)
        if u.validate_register():
             result = '注册成功<br> <pre>{}</pre>'.format(User.all())
             u.save()
        else:
            result = '账号或者密码少于2位'
    else:
        result = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
    response = header + '\r\n' + body
    return response.encode('utf-8')

def error(request, code= 404):
    r = {
        404:b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
        }
    return r.get(code, b'')

def response_for_path(path):
    print(path)
    r = {}
    r.update(route_dict)
    response = r.get(path, error)
    return response(request)


def run(host = '', port = 3000):
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(3)
            connection, address = s.accept()
            r = connection.recv(1000)
            r = r.decode('utf-8')
            if len(r.split()[0]) < 2:
                continue
            path = r.split()[1]
            request.method = r.split()[0]
            request.body = r.split('\r\n\r\n')[1]
            request.add_headers(r.split('\r\n\r\n',1)[0].split('\r\n')[1:])
            response = response_for_path(path)
            # print(r)
            connection.sendall(response)
            connection.close()

route_dict = {
    '/register': route_register,
    '/login': route_login,
}

def test():
    form = dict(
        username='newgua',
        password='123'
    )
    u = User(form)
    u.save()
    # print('u.id=', u.id) # 第一次save的时候已经带了id 后面的save就没有任何意义了

    # 实现原来ID被替换数据
    form2 = dict(
        id=1,
        username='power',
        password='power',
    )
    u.save()
    User(form2).save()
    u3 = u.find(1)
    print('u3=', u3)
if __name__ == '__main__':
    config = dict(
        host='',
        port=3000,
    )
    run(**config)
#     test()
    # 为了测试相同账户是否给了ID