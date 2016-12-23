from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import Blueprint
from flask import abort
from flask import session

from models import Weibo
from models import User
from models import Comment

# 创建一个 蓝图对象 并且路由定义在蓝图对象中
# 然后在 flask 主代码中「注册蓝图」来使用
# 第一个参数是蓝图的名字，第二个参数是套路
main = Blueprint('weibo', __name__)


@main.route('/<username>/weibo')
def index(username):
    # 查找所有的 weibo 并返回 加入user_id 的话就可以显示该用户下所有微博了
    u = User.query.filter_by(username=username).first()
    # print('u===', u)
    if u is None:
        abort(404)
    else:
        weibo_list = Weibo.query.filter_by(user_id=u.id).all()
        for w in weibo_list:
            w.load_comments() # 需要每一个微博把comments显示出来
        # print('weibo_list=', weibo_list)
        return render_template('weibo.html', weibos=weibo_list)

def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        return u

@main.route('/add', methods=['POST'])
def add():
    u = current_user()
    # print('weibo add', u.id, u.username, u.password)
    form = request.form
    w = Weibo(form)
    if w.valid():
         w.user_id = u.id
         w.save()
    # 蓝图中的 url_for 需要加上蓝图的名字，这里是 weibo
    return redirect(url_for('weibo.index', username=u.username))


@main.route('/delete/<int:weibo_id>')
def delete(weibo_id):
    u = current_user()
    # # 通过 id 查询 weibo 并返回
    w = Weibo.query.get(weibo_id)
    # print('w======', w)
    # print('weibo_id====', weibo_id)
    # # 删除
    w.delete()
    # 引用蓝图内部的路由函数的时候，可以省略名字只用 .


    w.delete()
    return redirect(url_for('.index', username= u.username))

@main.route('/edit/<int:weibo_id>', methods=['POST'])
def edit(weibo_id):
    u = current_user()
    form = request.form
    # print(form)
    w = Weibo.query.get(weibo_id)
    # print('w=', w)
    w.content = form.get('content','')
    # print('w.content=', w.content)
    return redirect(url_for('weibo.index',username= u.username))

@main.route('/comment/add', methods=['post'])
def comment():
    u = current_user()
    if u is not None:
        print('commente_add', u.id, u.username)
        form = request.form
        c = Comment(form)
        c.user_id = u.id
        c.weibo_id = int(form.get('weibo_id', -1))
        c.save()
        return redirect(url_for('weibo.index', username= u.username))
    else:
        abort(400)
