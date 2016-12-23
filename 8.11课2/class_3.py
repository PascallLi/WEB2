# 2016/8/12
#
# ========
# 作业 (会更新)
#
# 注意, 作业会在这里更新, 对作业有问题请评论
# 注意, 登录论坛后才有评论功能
# ========
# 更新 2.1
#
#
# 请直接在我的代码中更改/添加, 不要新建别的文件

import class2client_ssl

c = class2client_ssl


# 定义我们的 log 函数
def log(*args, **kwargs):
    print(*args, **kwargs)


# 作业 2.1
#
# 实现函数
def path_with_query(path, query):
    '''
    path 是一个字符串
    query 是一个字典

    返回一个拼接后的 url
    详情请看下方测试函数
    '''
    url = path + '?'
    for (key_, value_) in query.items():
        url += key_ + '=' + str(value_) + '&'
    return url


def test_path_with_query():
    # 注意 height 是一个数字
    path = '/'
    query = {
        'name': 'gua',
        'height': 169,
    }
    expected = [
        '/?name=gua&height=169',
        '/?height=169&name=gua',
    ]
    # NOTE, 字典是无序的, 不知道哪个参数在前面, 所以这样测试
    assert path_with_query(path, query) in expected


# 作业 2.2
#
# 为作业1 的 get 函数增加一个参数 query
# query 是字典
def parsed_path(path):
    index = path.find('?')
    if index == -1:
        # 就是没有 query
        return path, {}
    else:
        path, query_string = path.split('?', 1)
        args = query_string.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return query


def get_2(url, query={}):
    protocol, host, port, path = c.parsed_url(url)
    path = path_with_query(path, query)

    s = c.socket_by_protocol(protocol)
    s.connect((host, port))

    request = 'GET {} HTTP/1.1\r\nhost: {}\r\nConnection: close\r\n\r\n'.format(path, host)
    encoding = 'utf-8'
    s.send(request.encode(encoding))

    response = c.response_by_socket(s)
    r = response.decode(encoding)

    status_code, headers, body = c.parsed_response(r)
    if status_code == 301:
        url = headers['Location']
        return get(url)

    return status_code, headers, body


# u = 'https://movie.douban.com/subject/1292052/'
# log('test_2 : ', get_2(u))

# 作业 2.3
#
# 实现函数
def header_from_dict(headers):
    '''
    headers 是一个字典
    范例如下
    对于
    {
        'Content-Type': 'text/html',
        'Content-Length': 127,
    }
    返回如下 str
    'Content-Type: text/html\r\nContent-Length: 127\r\n'
    '''
    s = ''
    for (key_, value_) in headers.items():
        s += key_ + ': ' + str(value_) + '\\r\\n'
    return s


# 作业 2.4
#
# 为作业 2.3 写测试
def test_header_from_dict():
    test_items = [
        ({
             'Content-Type': 'text/html',
             'Content-Length': 127,
         },
         'Content-Type: text/html\r\nContent-Length: 127\r\n')
    ]
    for t in test_items:
        str_, expect = t
        s = header_from_dict(str_)
        e = 'header_from_dict ERROR, ({})({})'.format(str_, s, expect)
        assert s == expect, e


# 作业 2.5
#
"""
豆瓣电影 Top250 页面链接如下
https://movie.douban.com/top250
我们的 client 已经可以获取 https 的内容了
这页一共有 25 个条目

所以现在的程序就只剩下了解析 HTML

请观察页面的规律，解析出
1，电影名
2，分数
3，评价人数
4，引用语（比如第一部肖申克的救赎中的「希望让人自由。」）

解析方式可以用任意手段，如果你没有想法，用字符串查找匹配比较好
"""


# def tup_to_str(url):
#     l = ''
#     for arg in c.get(url):
#         l += str(arg)
#     return l

class Movies(object):
    def __init__(self):
        self.sequence = ''
        self.name = ''
        self.othername = ''
        self.score = ''
        self.number = ''
        self.cite = ''

    def __repr__(self):
        return '{:5}\n{:13}\n{:13}\n{:13}\n{:20}\n{}\n'.format(
            self.sequence, self.name, self.othername, self.score, self.number, self.cite)


def get_element(body):
    body = body.split('<ol class="grid_view"')[1]
    body = body.split('</ol>')[0]
    message = body.split('<div class="item')[1:]
    l = []
    for i in message:
        m = Movies()
        m.sequence = i.split('<em class="">')[1].split('</em>')[0]
        m.name = i.split('<span class="title">')[1].split('</span>')[0]
        m.othername = i.split('<span class="other">&nbsp;/&nbsp;')[1].split('</span>')[0]
        m.score = i.split('property="v:average">')[1].split('</span>')[0]
        m.number = i.split('<span>')[1].split('</span>')[0]
        if '<span class="inq">' in i:
            m.cite = i.split('<span class="inq">')[1].split('</span>')[0]
        l.append(m)
    return l


# 作业 2.6
#
"""
通过在浏览器页面中访问 豆瓣电影 top250 可以发现
1, 每页 25 个条目
2, 下一页的 URL 如下
https://movie.douban.com/top250?start=25

因此可以用循环爬出豆瓣 top250 的所有网页

于是就有了豆瓣电影 top250 的所有网页

由于这 10 个页面都是一样的结构，所以我们只要能解析其中一个页面就能循环得到所有信息

所以现在的程序就只剩下了解析 HTML

请观察规律，解析出
1，电影名
2，分数
3，评价人数
4，引用语（比如第一部肖申克的救赎中的「希望让人自由。」）

解析方式可以用任意手段，如果你没有想法，用字符串查找匹配比较好
"""


def get_all_movies(url):
    l = []
    query = {
        'start': 0,
    }
    while query['start'] < 250:
        status_code, headers, body = get_2(url, query)
        l += get_element(body)
        query['start'] += 25
        # log(query['start'])
    return l


def main():
    url = 'https://movie.douban.com/top250'
    l = get_all_movies(url)
    for i in l:
        log(i)


if __name__ == '__main__':
    main()
