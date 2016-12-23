import socket

host = ''
port = 3000
s = socket.socket()
s.bind((host, port))


def read_form_file(filename):
    with open(filename, 'rb') as f:
        return f.read()
while True:
    s.listen(3)
    connection, address = s.accept()
    request = connection.recv(1024)
    request = request.decode('utf-8')
    if len(request) == 0:
        continue
    print('ip and request.{}\n{}'.format(address, request))
    line = request.split('\n')[0]
    # print('line =', line)
    path = line.split()[1]
    print('path =', path)
    response = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nchenchao!<img src="img/doge0.gif"><img src="img/doge1.gif">'
    if path == '/doge':
        r = response
    elif path == '/img/doge0.gif':
        r = read_form_file('doge0.gif')
    elif path == '/img/doge1.gif':
        r = read_form_file('doge1.gif')
    else:
        r = b'404 NOT FOUND'
    connection.sendall(r)
    connection.close()