from utils import log
from models import Message
from models import User
import random
message = []

session = {} # session的目的：添加随机数组保存username，防止被窜改
# 新增函数，随机字符串
# 函数目的： 生成session
def random_str():
    seed = 'ssssa123ssdadddssdadas'
    s = ''
    for i in range(6):
        random_index = random.randint(0, len(seed) -1)
        s += seed[random_index]
    return s

def current_user(request):
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '游客')
    return  username
def template(name):
    # 将index.html和html_basic.html放入一个叫templates的文件中，需要修改路径
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:  # 默认在中文windows下面打开的编码格式是gbk,所以需要utf-8
        return f.read()


def route_index(request):  # 这里的request是传到主页函数中的 response_for_path(path)
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.x 210 VERY OK\r\nContent-Type: text/html\r\n'
    # body = '<h1>Hello World</h1><img src="doge.gif"/>'
    # 给 index 增加一个HTML文件
    body = template('index.html')
    username = current_user(request)
    body = body.replace('{{username}}', username)

    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')

# 新增函数，转换route_login
def response_with_headers(headers):
    """
    Content-Type: text/html,
    Set-Cookie: user=gua,
    """
    header = 'HTTP/1.x 210 VERY OK\r\n'
    header += ''.join(['{}: {}\r\n'.format(k, v) for k, v in headers.items()])
    # 相当于 HTTP/1.x 210 VERY OK\r\n + {}:{}\r\n，通过join函数和items方法将其中的命令添加并且在末尾增加一个\r\n
    # items()方法返回字典的(键，值)元组对的列表
    # log('properties =', properties)
    # log结果 ['password: 1234', 'username: 1234']
    return header


def route_login(request):
    headers = {
        'Content-Type': 'text/html',
        # 'Set-Cookie': "user=gua",
    }
    log('login, cookies', request.cookies)
    # 原先给header发送命令没有自动，现在改为字典，直接调用
    # header = 'HTTP/1.x 210 VERY OK\r\nContent-Type: text/html\r\n'
    username = current_user(request)
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_login():  # 告诉我登入成功还是失败
            # 随机生成一串数据，让session_id生成一个字典保存，读取的时候读取key
            session_id = random_str()
            session[session_id] = u.username
            log('加密数据', session_id)
            headers['Set-Cookie'] = 'user={}'.format(session_id)
            # headers['Set-Cookie'] = 'user={}'.format(u.username)
            result = '登入成功'
        else:
            result = '用户名或者密码错误'
    else:
        result = ''
    body = template('login.html')
    body = body.replace('{{result}}', result)
    body = body.replace('{{username}}', username)
    # header 放在这里是因为需要在登入之后再存入cookie
    header = response_with_headers(headers)

    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_register(request):
    header = 'HTTP/1.x 210 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_register():
            u.save()
            result = '注册成功<br> <pre>{}</pre>'.format(User.all())
            # pre是为了user的完整性，每次都另起一行
        else:
            result = '用户名或者密码长度必须大于3'
    else:
        result = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')

def route_message(request):
    """
    主页的处理函数, 返回主页的响应
    """
    log('本次请求的 method', request.method)
    if request.method == 'POST':
        form = request.form()
        msg = Message(form)
        log('post', form)
        # 每次请求 route_message 都会将query中的数据append到message_list中
        message.append(msg)
        # 应该在这里保存 message_list
    header = 'HTTP/1.x 200 OK\r\nContent-Type: text/html\r\n'
    # body = '<h1>消息版</h1>'
    body = template('html_basic.html')  # 直接从HTML文件中读取
    msgs = '<br>'.join([str(m) for m in message])  # str(m)一下然后回车，遍历list然后生成一个新的字符串
    # br是HTML中的回车
    body = body.replace('{{messages}}', msgs)  # 在HTML中生成一个特殊标记，每次用append新生成的message_list去替换他
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')

# 简化路径用的，就不需要成天import了
route_dict = {
    '/login': route_login,
    '/messages': route_message,
    '/register': route_register,
    '/': route_index,
}
