import socket
import urllib.parse
def log(*args, **kwargs):
    print(log, *args, **kwargs)

class Request(object):
    def __init__(self):
        self.query = ''
        self.path = ''
        self.body = ''
        self.query = {}
        self.method = ''
    def form(self):
        query = {}
        body = urllib.parse.unquote(self.body)
        # query_string = message=hello&author=gua
        query_string = body.split('&')
        for args in query_string:
            k, v = args.split('=')
            query[k] = v
        log('query=', query)
        return query

class Message(object):
    def __init__(self):
        self.message = ''
        self.author = ''
    def __repr__(self):
        return '{}:{}'.format(self.message, self.author)

request =  Request()
message_list = []



def route_index():
    header = 'HTTP/1.x 200 OK\r\nContent-Type: text/html\r\n\r\n'
    body = '<h1>Hi POWER</h1><image src = "doge.gif"/>'
    html = header + body
    return html.encode('utf-8')

def route_image():
    with open('doge.gif', 'rb') as f:
        header = b'HTTP/1.x 200 ok\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img

def template(name):
    with open(name, 'r', encoding= 'utf-8') as f:
        return f.read()

def route_message():
    log('向服务器使用{}方法'.format(request.method))
    if request.method == 'POST':
        msg = Message()
        msg.author = request.form().get('author')
        msg.message = request.form().get('message')
        log('msg', msg)
        message_list.append(msg)
    header = 'HTTP/1.x 200 OK\r\nContent-Type: text/html\r\n\r\n'
    body = template('html_basic.html')
    msgs = '<br>'.join([str(m) for m in message_list])
    body = body.replace('{{messages}}', msgs)
    html = header + body
    return html.encode('utf-8')

def error(code = 404):
    e = {

        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>404 NOT FOUND</h1>',
    }
    return e.get(code, b'')

def response_for_path(path):
    r = {
        '/': route_index(),
        '/doge.gif': route_image(),
        '/messages': route_message(),
    }
    response = r.get(path, error())
    return response



def run(host='', port= 3000):
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(3)
            connection, address = s.accept()
            r = connection.recv(1024)
            r = r.decode('utf-8')
            path = r.split()[1]
            request.method = r.split()[0]
            request.body = r.split('\r\n\r\n', 1)[1]
            # path = /messages?message=hello&author=gua
            response = response_for_path(path)

            connection.sendall(response)
            connection.close()
if __name__ == '__main__':
    config = dict(
        host='',
        port=3000,
    )
    run(**config)