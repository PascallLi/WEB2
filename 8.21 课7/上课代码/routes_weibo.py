from models import User
from models import Weibo

from response import session
from response import template
from response import response_with_headers
from response import redirect
from response import error
from utils import log


#---------------------------------- cookie
def current_user(request): # 必须是先得到请求后回复响应，第二次才能用到
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '游客')
    return username
#------------------------------------------------

# -------------------------------------------------------------
# 增加微博功能
def route_weibo_new(request):
    # 增加数据
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(headers)
    body = template('weibo_new.html')
    r = header + '\r\n' + body
    return r.encode('utf-8')

def route_weibo_add(request):  # 处理请求数据
    username = current_user(request)
    u = User.find_by(username=username)
    form = request.form()
    w = Weibo(form)
    w.user_id = u.id
    w.save()
    return redirect('/weibo?user_id={}'.format(u.id))

def route_weibo_index(request):
    # 处理route_weibo_add输出的数据，显示微博发布内容
    headers={'content-type':'text/html',}
    header = response_with_headers(headers)

    # log('request.query===', request.query)
    # request.query = {'user_id': '1'}
    user_id = request.query.get('user_id', -1)
    user_id = int(user_id)
    user = User.find(user_id)
    if user is None:
        return error(request)
    # 找到user发布的所有的微博
    # user_id 必须是int型
    weibos = Weibo.find_all(user_id=user_id)
    log('weibos', weibos)
    # log(weibos)
    # 直接这样显示 [< Weibo created_time: (1475073909) user_id: (1) content: (222) id: (1) >]
    # 增加这个子函数是为了遍历weibos，输出整齐
    def weibo_tag(weibo):
        # return '<p>{} from {}@{}</p>'.format(weibo.content, user.username, weibo.created_time,)
        return '<p>{} from {}@{} <a href="/weibo/delete?id={}">删除</a>' \
               '<a href= "/weibo/edit?id={}"> 编辑</a></p>'.format(weibo.content,
                                                                user.username,
                                                                weibo.created_time,
                                                                weibo.id, weibo.id)
    weibos = [weibo_tag(w) for w in weibos]
    weibos = '\n'.join(weibos) # 每一个str之间都有空格

    body = template('weibo_index.html', weibos= weibos, edit= user.id)
    r = header + '\r\n' + body
    return r.encode('utf-8')

def route_weibo_delete(request):  # 处理请求数据
    username = current_user(request)
    u = User.find_by(username=username)
    # 删除微博
    weibo_id = request.query.get('id', None)
    weibo_id = int(weibo_id)
    w = Weibo.find(weibo_id)
    w.delete()
    log('id==', u.id)
    return redirect('/weibo?user_id={}'.format(u.id))

def route_weibo_edit(request):
    headers = {'Content-Type': 'text/html'}
    header = response_with_headers(headers)
    body = template('weibo_edit.html')
    r = header + '\r\n' + body
    return r.encode('utf-8')

def route_weibo_update(request):
    username = current_user(request)
    u = User.find_by(username=username)
    form = request.form()
    weibo_id = form.get('id',None)
    weibo_id = int(weibo_id)
    log('weibo_id=', weibo_id)
    if  Weibo.find(weibo_id):
        w1 = Weibo.find(weibo_id)
    else:
        return error(request)
    w1.content = form.get('content')
    w1.save()
    log('w1==', w1)
    return redirect('/weibo?user_id={}'.format(u.id))
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
    '/weibo':route_weibo_index,
    '/weibo/new': login_required(route_weibo_new),
    '/weibo/add': login_required(route_weibo_add),
    '/weibo/delete': login_required(route_weibo_delete),
    '/weibo/edit': login_required(route_weibo_edit),
    '/weibo/update': login_required(route_weibo_update),
    # '/weibo/new': route_weibo_new,
    # '/weibo/add': route_weibo_add,
    # '/weibo/delete': route_weibo_delete,
    # '/weibo/edit': route_weibo_edit,
    # '/weibo/update': route_weibo_update,
}
