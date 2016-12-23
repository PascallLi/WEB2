# 作业 2.5
#
"""
豆瓣电影 Top250 页面链接如下
https://movie.douban.com/top250
我们的 client 已经可以获取 https 的内容了
这页一共有 25 个条目
通过在浏览器页面中访问 豆瓣电影 top250 可以发现
1, 每页 25 个条目
2, 下一页的 URL 如下
https://movie.douban.com/top250?start=25
因此可以用循环爬出豆瓣 top250 的所有网页
所以现在的程序就只剩下了解析 HTML

请观察页面的规律，解析出
1，电影名
2，分数
3，评价人数
4，引用语（比如第一部肖申克的救赎中的「希望让人自由。」）

解析方式可以用任意手段，如果你没有想法，用字符串查找匹配比较好
"""
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
import  ssl
import  socket

def log(*args):
    print(*args)
def parsed_url(url):
    protocol = 'http'
    if url[:7] == 'http://':
        u = url.split('//', 1)[1]
    elif url[:8] == 'https://':
        protocol = url.split('://', 1)[0]
        u = url.split('//', 1)[1]
    else:
        u = url

    i = u.find('/')
    if i == -1:
        host = u
        path = '/'
    else:
        host = u[:i]
        path = u[i:]

    port_dict= {
        'http':80,
        'https':443,
    }
    port = port_dict.get(protocol)
    if host.find(':') != -1:
        h =  host.split(':')
        host = h[0]
        port = int(h[1])

    # log(protocol, host, port, path)
    return protocol, host, port, path
def test_parsed_url():
    http = 'http'
    https = 'https'
    host = 'g.cn'
    path = '/'
    test_items = [
        ('g.cn', (http, host, 80, path)),
        ('g.cn/', (http, host, 80, path)),
        ('g.cn:3000', (http, host, 3000, path)),
        ('g.cn:3000/search', (http, host, 3000, '/search')),
        ('http://g.cn:90/', (http, host, 90, path)),
        ('https://g.cn', (https, host, 443, path)),
        ('https://g.cn:233/', (https, host, 233, path)),
    ]
    for t in test_items:
        url, expected = t
        log('链接', url)
        u = parsed_url(url)
        e = "parsed_url ERROR, ({}) ({}) ({})".format(url, u, expected)
        assert u == expected, e
# test_parsed_url()
def socket_by_protocol(protocol):
    if protocol == 'http':
        s = socket.socket()
    else:
        s = ssl.wrap_socket(socket.socket())
    return s
def response_by_socket(s):
    response = b''
    while True:
        request = s.recv(1024)
        if  len(request) == 0:
            break
        response += request
    return response.decode('utf-8')
def parsed_response(r):
    header, body = r.split('\r\n\r\n', 1)
    h = header.split('\r\n')
    header_first_line = h[0]
    log('头的第一行', header_first_line)
    status_code = header_first_line.split()[1]
    status_code = int(status_code)
    # log('status =', status_code)
    headers = {}
    for line in h[1:]:
        k, v = line.split(': ')
        headers[k] = v
    return status_code, headers, body
def test_parsed_response():
    response = 'HTTP/1.1 301 Moved Permanently\r\n' \
               'Content-Type: text/html\r\n' \
               'Location: https://movie.douban.com/top250\r\n' \
               'Content-Length: 178\r\n\r\n' \
               'test body'
    status_code, header, body = parsed_response(response)
    assert status_code == 301
    assert len(list(header.keys())) == 3
    assert body == 'test body'
# test_parsed_response()
def get(url):
    protocol, host, port, path = parsed_url(url)
    s = socket_by_protocol(protocol)
    s.connect((host, port))
    http_request = 'GET {} HTTP/1.1\r\nhost:{}\r\nConnection: close\r\n\r\n'.format(path, host)
    request = http_request.encode('utf-8')
    s.send(request)
    response = response_by_socket(s)
    status_code, headers, body = parsed_response(response)
    if status_code == 301:
        url = headers.get('Location')
        return get(url)
    return response, status_code, headers, body
def test_get():
    urls = [
        'http://movie.douban.com/top250',
        'https://movie.douban.com/top250',
    ]
    for u in urls:
        get(u)
# test_get()
def main():
    url = 'http://movie.douban.com/top250'
    # url = 'https://movie.douban.com/subject/1295644/'
    response, status_code, headers, body = get(url)
    log(response)
if __name__ == '__main__':
     main()

# --------------------------------------------------------
