from utils import log
from models import Message
from models import User

message = []


def template(name):
    # 将index.html和html_basic.html放入一个叫templates的文件中，需要修改路径
    path = 'templates/' + name
    with open(path, 'r', encoding ='utf-8') as f:  # 默认在中文windows下面打开的编码格式是gbk,所以需要utf-8
        return f.read()


def route_index(request):  # 这里的request是传到主页函数中的 response_for_path(path)
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.x 210 VERY OK\r\nContent-Type: text/html\r\n'
    # body = '<h1>Hello World</h1><img src="doge.gif"/>'
    # 给 index 增加一个HTML文件
    body = template('index.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_login(request):
    header = 'HTTP/1.x 210 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_login():
            result = '登入成功'
        else:
            result = '用户名或者密码错误'
    else:
        result = ''
    body = template('login.html')
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_register(request):
    header = 'HTTP/1.x 210 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_register():
            u.save()
            result = '注册成功<br>' + str(User.all())
        else:
            result = '用户名或者密码长度必须大于3'
    else:
        result = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_static(request):
    '''
    静态资源的处理函数，读取图片并生成响应返回
    '''
    filename = request.query.get('file', '')
    path = 'static/' + filename
    log('路径等于', path)
    # 这个路径是static文件夹下面的文件路径
    # log = static/doge.gif
    with open(path, 'rb') as f:
        # Contene-Type : Content-Type 这些都是给浏览器的提示，没有提示也是可以的
        header = b'HTTP/1.x 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img


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


route_dict = {
    '/static': route_static,
    '/login': route_login,
    '/messages': route_message,
    '/register': route_register,
}
