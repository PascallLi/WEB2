import socket
import urllib.parse
from model import User


class Request(object):
    def __init__(self):
        self.body = ''
        self.path = ''
        self.query = {}
        self.body = ''

    def form(self):
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        query = {}
        for arg in args:
            k ,v = arg.split('=')
            query[k] = v
        return query




request =  Request()

def template(name):
    path = 'templates/'+ name
    with open(path, 'r', encoding= 'utf-8') as f:
        return f.read()

def route_register(request):
    header = 'HTTP/1.x 200 OK\r\nContent-Type: Text/html\r\n'
    if request.method == 'POST':
        form = request.form()
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



def error(code= 404):
    r = {   404:b'HTTP/1.x 404 NOT FOUND\r\n<h1>NOT FOUND</h1>',}
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
            response = response_for_path(path)
            print(r)
            connection.sendall(response)
            connection.close()

route_dict = {
    '/register': route_register
}

if __name__ == '__main__':
    config = dict(
        host='',
        port=3000,
    )
    run(**config)