import socket

"""
作业 1
8.10

请参考上课板书内容
"""
def log(*args):
    print(*args)

# 1
# 补全函数 parsed_url
def path1(url):
    for i, c in enumerate(url):
        if c == '/':
            return url[i:]
    else:
        return ' '
def host1(url):
    for i, e in enumerate(url):
        if e == '/' or e == ':':
            return url[:i]
    else:
        return url
def parsed_url(url):
    '''
    url 可能的值如下
    g.cn
    g.cn/
    g.cn:3000
    g.cn:3000/search
    http://g.cn
    https://g.cn
    http://g.cn/

	NOTE:
    没有 protocol 时, 默认协议是 http

    在 http 下 默认端口是 80
    在 https 下 默认端口是 443
    :return : tuple, 内容如下 (protocol, host, port, path)
    '''
    pass
    protocol = ''
    host = ''
    port = ''
    path = ''
    # url = url.decode('utf-8')  # 先转换bytes为str
    if url[:5] == 'https':
        protocol = 'https'
        host = host1(url[8:])
        port = 443
        path = path1(url[8:])
    elif url[:4] == 'http':
        protocol = 'http'
        port = 80
        host = host1(url[7:])
        path = path1(url[7:])
    elif url[:4] != 'http' and url[:5] != 'https':
        protocol = 'http'
        host = host1(url)
        for i, c in enumerate(url):
            if c == ':':
                url_new = url[(i + 1):]
                for j in range(len(url_new)):
                    if url_new[j] == '/':
                        path = url_new[j:]
                        port = url_new[:j]
                        # log(path, port)
                        break
                    if j == len(url_new) - 1:
                        path = ' '
                        port = url_new[:]
                        # log(path, port)
                break
            if url[-1] == '/':
                path = '/'
                port = 80
            if url[-1] != '/':
                path = ' '
                port = 80
    return protocol, host, port, path
    # log('protocol {}\nhost {}\nport {}\npath {}'.format(protocol, host, port, path))

# parsed_url(b'g.cn:3000/search')

# 2
# 把向服务器发送 HTTP 请求并且获得数据这个过程封装成函数
# 定义如下
def get(url):
    '''
    返回的数据类型为 bytes
    '''
    pass
    protocol, host, port, path = parsed_url(url)
    s = socket.socket()
    s.connect((host, port))
    http_request = 'GET {} HTTP/1.1\r\nhost:{}\r\nConnection: close\r\n\r\n'.format(path, host)
    request = http_request.encode('utf-8')
    log('请求', request)
    s.send(request)
    response = b''
    while True:
        r = s.recv(1024)
        if len(r) == 0:
            break
        response += r
    return response.decode('utf-8')

"""
资料:
在 Python3 中，bytes 和 str 的互相转换方式是
str.encode('utf-8')
bytes.decode('utf-8')

send 函数的参数和 recv 函数的返回值都是 bytes 类型
"""
def parse_url_test():
    print(parsed_url('g.cn0'))
    print(parsed_url('g.cn/'))
    print(parsed_url('g.cn:3000'))
    print(parsed_url('g.cn:3000/search'))
    print(parsed_url('http://g.cn'))
    print(parsed_url('https://g.cn'))
    print(parsed_url('http://g.cn/'))

# 使用
def main():
    # parse_url_test()
    url1 = 'http://movie.douban.com/top250'
    r = get(url1)
    log(r)


if __name__ == '__main__':
    main()
