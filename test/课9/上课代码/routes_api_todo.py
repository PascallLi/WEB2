from models import User
from models import Weibo
from models import Todo

from response import session
from response import template
from response import response_with_headers
from response import redirect
from response import error
from utils import log

import random
#---------------------------------- cookie
def current_user(request): # 必须是先得到请求后回复响应，第二次才能用到
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '游客')
    return username

def random_str():
    seed = 'abcdefjsad89234hdsfkljasdkjghigaksldf89weru'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s
#------------------------------------------------

def route_todo_add(request):  # 处理请求数据
    headers = {'content-type': 'text/html', }
    header = response_with_headers(headers)
    # username = current_user(request)
    # u = User.find_by(username=username)
    form = request.form()
    log('用JQuery之后的form', form)
    t = Todo(form)
    # t.user_id = u.id
    t.save()
    body = t.json_str() # 写在Model里面
    r = header + '\r\n' + body
    # return redirect('/todo?user_id={}'.format(u.id))
    # 这里return的不应该是一个链接，而是一个字符串
    return r.encode('utf-8')

def route_todo_index(request):
    # 此函数在用JQuery利用API中没有什么意义
    headers={'content-type':'text/html',}
    header = response_with_headers(headers)
    user_id = request.query.get('user_id', -1)
    log('user_id====', user_id)
    user_id = int(user_id)
    todos = Todo.find_all(user_id=user_id)
    log('todos====', todos)
    # todos = Todo.all()
    def todo_tag(t):
        return '<p class="{}">{} from {}@{} <a href="/todo/complete?id={}">完成</a>'.format(t.status(),
                                                                t.content,
                                                                t.id,
                                                                t.created_time,
                                                                t.id)
    todo_html = [todo_tag(t) for t in todos]
    todos_html = '\n'.join(todo_html) # 每一个str之间都有空格

    body = template('todo_index.html',todos=todos_html)
    r = header + '\r\n' + body
    return r.encode('utf-8')

def route_todo_complete(request):
    todo_id = request.query.get('id', -1)
    todo_id = int(todo_id)
    o = Todo.find(todo_id)
    o.togglecomplete()
    o.save()
    return redirect('/todo?user_id={}'.format(todo_id))


#-----------------------------------------------------------------


def login_required(route_function):
    def func(request):
        username = current_user(request)
        log('登入鉴定', username)
        if username == '游客':
            return redirect('/login')
        return  route_function(request)
    return func

# 路由字典
# key 是路由(路由就是 path)
# value 是路由处理函数(就是响应)
route_dict = {
    # '/todo':login_required(route_todo_index),
    # '/todo/add': login_required(route_todo_add),
    # '/todo/complete': login_required(route_todo_complete),
    '/api/todo':route_todo_index,
    '/api/todo/add': route_todo_add,
    '/api/todo/complete': route_todo_complete,
}
