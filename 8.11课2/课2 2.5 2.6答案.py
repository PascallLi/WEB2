import socket
import ssl


# 输入要搜索的字符串，以及开始和结束字符串，便可以列表返回所有开始和结束字符串之间的字符串
def findall_in_html(html, startpart, endpart):
    all_strings = []
    start = html.find(startpart) + len(startpart)
    end = html.find(endpart, start)
    #  end 从start开始搜寻endpart字符串，返回endpart的起始位置
    string = html[start:end]
    while html.find('</html>') > start > html.find('<html'):
        # 切出一个页面返回的Body中需要查找的内容，找到之后都放在一个List里面，跳出条件是：最后一个start只有len(startpart)-1了小于html.find('<html')的长度
        all_strings.append(string)
        start = html.find(startpart, end) + len(startpart)
        end = html.find(endpart, start)
        string = html[start:end]
    return all_strings


# 得到豆瓣电影top250的html，以列表形式保存，列表中每个元素用字符串保存一个页面
def htmls_from_douban():
    index = 0
    html = []
    url = """https://movie.douban.com/top250?start={}&filter="""
    for index in range(0, 250, 25):
        url.format(index)
        r = get(url)
        html.append(r)
    return html


# 得到页面中所有的影片名字，以列表形式返回
def movie_name(html):
    name = findall_in_html(html, '<span class="title">', '</span>')
    for i in name:
        if 'bsp' in i:
            name.remove(i)
    return name


# 得到页面中所有电影的打分，以列表形式返回
def movie_score(html):
    score = findall_in_html(html, '<span class="rating_num" property="v:average">', '</span>')
    return score


# 得到页面中所有电影的引言， 以列表形式返回
def movie_infq(html):
    infq = findall_in_html(html, '<span class="inq">', '</span>')
    return infq


#得到页面中的评价人数
def number_comment(html):
    temp = findall_in_html(html,'<div class="star">', '</div>' )
    num = []
    for item in temp:
        start = item.find('<span>') + len('<span>')
        end = item.find('</span>', start)
        n = item[start:end]
        num.append(n)
    return num

# 分析页面， 打包返回电影的名字、打分、引言
def movie_data_from_html(htmls):
    movie = []
    score = []
    inq = []
    number = []
    for h in htmls:
        m = movie_name(h)
        s = movie_score(h)
        i = movie_infq(h)
        n = number_comment(h)
        movie.extend(m)
        score.extend(s)
        inq.extend(i)
        number.extend(n)
    data = zip(movie, score, inq, number)
    return data


# 分析响应，得到重定向的url
def redirect_url(response):
    start = response.find('Location: ') + len('Location: ')
    end = response.find('\n', start)
    url = response[start:end]
    return url


# 分析状态码
def status_code(response):
    part = 'HTTP/1.1 '
    start = response.find(part) + len(part)
    end = response.find(' ', start)
    status = response[start:end]
    return status


# 分析响应，根据状态码重新发送响应
def anylise_response(response, url):
    status = status_code(response)
    while status != '200':
        if status == '301':
            url = redirect_url(response)
            response = get(url)
            status = status_code(response)
        else:
            response = get(url)
            status = status_code(response)
    return response


# 发请求，得响应
def get(url):
    print('URL:', url)
    u = url.split('://')[1]
    protocol = url.split('://')[0]
    i = u.find('/')
    host = u[:i]
    path = u[i:]

    # https 的默认端口是 443
    # 端口换成 443
    # port = 443

    # 用这一行就可以进行 https 请求
    if protocol == 'https':
        s = ssl.wrap_socket(socket.socket())
        port = 443
        print('use https')
    else:
        s = socket.socket()
        port = 80
        print(protocol)
    s.connect((host, port))

    request = 'GET {} HTTP/1.1\r\nhost:{}\r\n\r\n'.format(path, host)
    print('request', request)
    encoding = 'utf-8'
    s.send(request.encode(encoding))

    response = b''
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        response += r
        if len(r) < buffer_size:
            break

    response = response.decode(encoding)
    return response


def main():
    # 请求页面
    htmls = htmls_from_douban()
    # 分析页面，得到电影数据
    movie_data = movie_data_from_html(htmls)
    # 打印电影数据
    counter = 0
    for item in movie_data:
        counter = counter + 1
        print("No." + str(counter))
        print('电影名:', item[0])
        print('打分:', item[1])
        print('引用语:', item[2])
        print("评价人数:", item[3],'\n\n')


if __name__ == '__main__':
    main()

