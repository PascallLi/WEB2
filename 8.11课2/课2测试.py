import socket

def log(*args, **kwargs):
    print(log, *args, **kwargs)
class Request(object):
    def __init__(self):
        self.methed = 'GET'


def route_index():
    header = 'HTTP/1.X 200 OK\r\nContent-Type = text/html\r\n'
    body = '<h1>Hello World</h1><img src = "doge.gif"/>'
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

def response_for_path(path):
    r = {
    '/':route_index(),
    '/doge.gif':route_image(),
    }
    response = r.get(path, error)
    return response

def run(host='', port = 3000):
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(3)
            connection, address = s.accept()
            request = connection.recv(1024)
            request = request.decode('utf-8')
            log('requset = ', request)
            try:
                path = request.split()[1]
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