# import socket
# def log(*args):
#     print(*args)
#
# s = socket.socket()
# host = 'www.baidu.com'
# port = 80
# s.connect((host, port))
#
# ip, port = s.getsockname()
# log('本机IP：{}和本机端口号：{}'.format(ip, port))
#
# request = 'GET / http/1.1\r\nhost:{}\r\nConnection:close\r\n\r\n'.format(host)
# log('请求', request)
# request_send = request.encode('utf-8')
# s.send(request_send)
#
# response = b''
# while True:
#     r = s.recv(1024)
#     if len(r) == 0:
#         break
#     response += r
#
# log("响应", response.decode('utf-8'))
#


# split() 函数测试
str = "Line1-abcdef Line2-abc\nLine4-abcd"
print(str.split())
print(str.split('\n'))