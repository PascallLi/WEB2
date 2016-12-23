from models import User
from models import Weibo
from models import Comments

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
    # current_username = current_user(request)
    # u = User.find_by(username=current_username)

    if user_id is None:
        return redirect('/login')
    def comment_tag(c):
        comment_list = Comments.find_all(weibo_id= c.id)
        comments = '<br>'.join([c.content for c in comment_list])
        # 每次增加新的评论放在微博的内容当中
        c = {
            "id": c.id,
            "user_id": user_id,
            "created_time": c.created_time,
            "content": c.content,
            "comments": comments,
            "username": user.username,

        }
        return """
               <p>{content} from {username}@{created_time}
                <a href="/weibo/delete?id={id}">删除</a>
                <a href= "/weibo/edit?id={id}"> 编辑</a></p>
                <button class="gua-show-comment gua-hide" data-id="{id}">评论</button>
                <div>
                        {comments}
                </div>
                <div id= "id-div-comment-{id}" class="gua-comment-form gua-hide">
                <form action='/weibo/comment/add' method = "post">
                    <input name="weibo_id" value = "{id}" type= "hidden">
                    <input name="user_id" value = "{user_id}" type= "hidden">
                    <textarea name= "content"></textarea>
                    <button type="submit">添加评论</button>
                </form>
                </p>
                """.format(**c)

    w = [comment_tag(c) for c in weibos]
    weibos = '\n'.join(w) # 每一个str之间都有空格

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

def route_comment_add(request):
    # username = current_user(request)
    # u = User.find_by(username=username)
    form = request.form()
    c = Comments(form)
    log('c==', c)
    c.save()
    w = Weibo.find(c.weibo_id)
    # 重定向到用户的主页
    return redirect('/weibo?user_id={}'.format(w.user_id))
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
    '/weibo/comment/add': login_required(route_comment_add),
    # '/weibo/new': route_weibo_new,
    # '/weibo/add': route_weibo_add,
    # '/weibo/delete': route_weibo_delete,
    # '/weibo/edit': route_weibo_edit,
    # '/weibo/update': route_weibo_update,
}
