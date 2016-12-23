
session = {}

def error(request, code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    # 之前上课我说过不要用数字来作为字典的 key
    # 但是在 HTTP 协议中 code 都是数字似乎更方便所以打破了这个原则
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def response_with_headers(headers, status_code=200):
    """
Content-Type: text/html
Set-Cookie: user=gua
    """
    header = 'HTTP/1.x {} VERYOK\r\n'.format(status_code)
    header += ''.join(['{}: {}\r\n'.format(k, v) for k, v in headers.items()])

    return header


def template(name,**kwargs):
    """
    根据名字读取 templates 文件夹里的一个文件并返回
    """
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        for k,v in kwargs.items():
            s = s.replace('{{' + k + '}}', str(v))
    return s

# 写一个函数 redirect , 可以直接 redirect('/') 来得到重定向响应
def redirect(location):
    headers = {}
    headers['Location'] = location  # header设置Location来指定获取页面
    header = response_with_headers(headers, 302)
    r = header + '\r\n' + ''
    return r.encode(encoding='utf-8')