# encoding: utf-8

import socket
import ssl
import requests
from lxml import html
from utils import log


class Model(object):
    def __repr__(self):
        class_name = self.__class__.__name__
        log('class_name=', class_name)
        properties = ('{} = ({})'.format(k, v) for k, v in self.__dict__.items())
        r = '\n<{}:\n  {}\n>'.format(class_name, '\n  '.join(properties))
        return r

class Movie(Model):
    def __init__(self):
        self.ranking = 0
        self.cover_url = ''
        self.name = ''
        self.staff = ''
        self.publish_info = ''
        self.rating = 0
        self.quote = ''
        self.number_of_comments = 0

def parsed_url(url):
    """
    解析 url 返回 (protocol host port path)
    有的时候有的函数, 它本身就美不起来, 你要做的就是老老实实写
    """
    # 检查协议
    protocol = 'http'
    if url[:7] == 'http://':
        u = url.split('://')[1]
    elif url[:8] == 'https://':
        protocol = 'https'
        u = url.split('://')[1]
    else:
        # '://' 定位 然后取第一个 / 的位置来切片
        u = url

    # 检查默认 path
    i = u.find('/')
    if i == -1:
        host = u
        path = '/'
    else:
        host = u[:i]
        path = u[i:]

    # 检查端口
    port_dict = {
        'http': 80,
        'https': 443,
    }
    # 默认端口
    port = port_dict[protocol]
    if host.find(':') != -1:
        h = host.split(':')
        host = h[0]
        port = int(h[1])

    return protocol, host, port, path


def socket_by_protocol(protocol):
    """
    根据协议返回一个 socket 实例
    """
    if protocol == 'http':
        s = socket.socket()
    else:
        # HTTPS 协议需要使用 ssl.wrap_socket 包装一下原始的 socket
        # 除此之外无其他差别
        s = ssl.wrap_socket(socket.socket())
    return s


def response_by_socket(s):
    """
    参数是一个 socket 实例
    返回这个 socket 读取的所有数据
    """
    response = b''
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        if len(r) == 0:
            break
        response += r
    return response


def parsed_response(r):
    """
    把 response 解析出 状态码 headers body 返回
    状态码是 int
    headers 是 dict
    body 是 str
    """
    header, body = r.split('\r\n\r\n', 1)
    h = header.split('\r\n')
    status_code = h[0].split()[1]
    status_code = int(status_code)

    headers = {}
    for line in h[1:]:
        k, v = line.split(': ')
        headers[k] = v
    return status_code, headers, body


# 复杂的逻辑全部封装成函数
def get(url):
    """
    用 GET 请求 url 并返回响应
    """
    protocol, host, port, path = parsed_url(url)

    s = socket_by_protocol(protocol)
    s.connect((host, port))

    request = 'GET {} HTTP/1.1\r\nhost: {}\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36\r\nConnection: close\r\n\r\n'.format(
        path, host)
    # 如果需要爬知乎主页，需要登入之后输入cookie才能爬，User-Agent是为了显示登入浏览器（解决反爬虫）
    encoding = 'utf-8'
    s.send(request.encode(encoding))

    response = response_by_socket(s)
    # log('response', response)
    r = response.decode(encoding)
    status_code, headers, body = parsed_response(r)
    # log('body=', body)
    if status_code == 301:
        url = headers['Location']
        return get(url)
    return status_code, headers, body


def movie_from_div(div):
    movie = Movie()
    movie.ranking = div.xpath('.//div[@class="pic"]/em')[0].text
    movie.cover_url = div.xpath('.//div[@class="pic"]/a/img/@src')
    # names = div.xpath('.//span[@class="title"]')[0].text  如果这样写只能显示：肖申克的救赎
    names = div.xpath('.//span[@class="title"]/text()')
    movie.name = ''.join(names)
    movie.rating = div.xpath('.//span[@class="rating_num"]')[0].text
    # log('类型是啥', typeof(div.xpath('.//span[@class="inq"]')[0].text))
    if div.xpath('.//span[@class="inq"]'): # 判断该list为不空
        movie.quote = div.xpath('.//span[@class="inq"]')[0].text
    else:
        movie.quote = '消失的爱人是坑货'
        # log('type=', type(div.xpath('.//span[@class="inq"]')))
    infos = div.xpath('.//div[@class="bd"]/p/text()')
    movie.staff, movie.publish_info = [i.strip() for i in infos[:2]]
    movie.number_of_comments = div.xpath('.//div[@class="star"]/span')[-1].text[:-3]
    return movie


def movies_from_url(url):
    _, _, page = get(url)
    root = html.fromstring(page)  # fromstring方法：把字符串转换成树形结构
    movie_divs = root.xpath('//div[@class="item"]') # xpath找到相应数据生成一个List,每一部电影从item开始
    movies = [movie_from_div(div) for div in movie_divs]
    return movies


def download_covers(movies):
    for m in movies:
        image_url = m.cover_url[0]
        r = requests.get(image_url)
        path = 'covers/' + m.rating + m.name.split('/')[0] + '.jpg'
        with open(path, 'wb') as f:
            f.write(r.content) # content是写入了body


def main():
    # 豆瓣电影 top250  # 'https://movie.douban.com/top250?start=25&filter='
    index = 'http://movie.douban.com/top250'
    for i in range(0, 250, 25):
        url = index + '?start={}&filter='.format(i)
        movies = movies_from_url(url)
        log('movies', movies[0])
        # download_covers(movies)

    # download_covers(movies)

    # 以下为验证ID：134 没有quote的消失的爱人写的测试代码

    # url = index + '?start={}&filter='.format(134)
    # movies = movies_from_url(url)
    # log('movies', movies[0])

if __name__ == '__main__':
    main()



