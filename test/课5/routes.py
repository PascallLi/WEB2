from utils import log
from models import Message
from models import User

import random


# 这个函数用来保存所有的 messages
message_list = []
session = {}


def random_str():
    seed = 'abcdefjsad89234hdsfkljasdkjghigaksldf89weru'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


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

def current_user(request): # 必须是先得到请求后回复响应，第二次才能用到
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '游客')
    return username


def route_index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.x 210 VERY OK\r\nContent-Type: text/html\r\n'

    username = current_user(request)
    # body = body.replace('{{username}}', username)
    body = template('index.html', username=username)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def response_with_headers(headers, status_code=200):
    """
Content-Type: text/html
Set-Cookie: user=gua
    """
    header = 'HTTP/1.x {} VERYOK\r\n'.format(status_code)
    header += ''.join(['{}: {}\r\n'.format(k, v) for k, v in headers.items()])

    return header


def route_login(request):
    """
    登录页面的路由函数
    """
    headers = {
        'Content-Type': 'text/html',
        # 'Set-Cookie': 'height=169; gua=1; pwd=2; Path=/',
    }
    # log('login, headers', request.headers)
    # log('login, cookies', request.cookies)
    username = current_user(request)
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_login():
            session_id = random_str()
            session[session_id] = u.username  # session是一个list,每次登入成功都会重新生成新的对应关系。cookie用来免登陆的，然后失效了就要重新登陆然后是随机生成的
            headers['Set-Cookie'] = 'user={}'.format(session_id)
            # 增加到header中，发送给客户端
            result = '登录成功'
        else:
            result = '用户名或者密码错误'
    else:
        result = ''
    body = template('login.html', result=result, username=username)
    # body = body.replace('{{result}}', result)
    # body = body.replace('{{username}}', username)
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    # log('login', r)
    return r.encode(encoding='utf-8')


def route_register(request):
    """
    注册页面的路由函数
    """
    header = 'HTTP/1.x 210 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_register():
            u.save()
            result = '注册成功<br> <pre>{}</pre>'.format(User.all())
        else:
            result = '用户名或者密码长度必须大于2'
    else:
        result = ''
    body = template('register.html',result=result)
    # body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


# 写一个函数 redirect , 可以直接 redirect('/') 来得到重定向响应
def redirect(location):
    headers = {}
    headers['Location'] = location  # header设置Location来指定获取页面
    header = response_with_headers(headers, 302)
    r = header + '\r\n' + ''
    return r.encode(encoding='utf-8')
def route_message(request):
    """
    消息页面的路由函数
    """
    headers = {'Content-Type':'text/html',
               }
    log('本次请求的 method', request.method)
    username = current_user(request)
    if username == '游客':
        # 没登录 不让看 重定向到 /
        # return redirect('/')
        return redirect('/')
    else:
        header = response_with_headers(headers, 302)
    if request.method == 'POST':
        form = request.form()
        msg = Message(form)
        message_list.append(msg)

    msgs = '<br>'.join([str(m) for m in message_list])
    # body = body.replace('{{messages}}', msgs)
    body = template('html_basic.html',messgae=msgs)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')

def route_profile(request):
    headers = {
        'Content-Type': 'text/html',
    }
    username = current_user(request)
    if username == '游客':
        return redirect('/')

    else:
        header = response_with_headers(headers)
    u = User.find_by(username=username)
    log('u.id', u.id)
    body = template('profile.html', id=u.id, username=u.username, note=u.note)
    # body = body.replace('{{id}}', str(u.id))
    # body = body.replace('{{username}}', u.username)
    # body = body.replace('{{note}}', u.note)
    r = header + '\r\n' + body
    return r.encode('utf-8')




def route_static(request):
    """
    静态资源的处理函数, 读取图片并生成响应返回
    """
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.x 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img


# 路由字典
# key 是路由(路由就是 path)
# value 是路由处理函数(就是响应)
route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
    '/messages': route_message,
    '/profile': route_profile,
}
