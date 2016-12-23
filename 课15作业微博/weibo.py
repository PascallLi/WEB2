from flask import render_template
from flask import abort
from flask import url_for
from flask import redirect
from flask import request
from flask import Blueprint


from models import Weibo
from models import Comment
from user import current_user

main = Blueprint('weibo', __name__)

@main.route('/weibo')
def index():
    # print('form===', request.form)
    u  = current_user()
    if u is None:
        return redirect(url_for('user.login_view'))
    else:
        weibo_list = Weibo.query.order_by(Weibo.id.desc()).all()
        for i in weibo_list:
            i.comment = i.comments()
        return render_template('weibo.html', weibos=weibo_list)

@main.route('/weibo/add', methods=['POST'])
def add():
    u = current_user()
    # print('测试')
    form = request.form
    w = Weibo(form)
    if w.valid():
        w.name = u.username
        w.save()
    # return  redirect(url_for('.index'))
    return w.json()

@main.route('/comment/add', methods=['POST'])
def comment_add():
    u = current_user()

    form = request.form
    print('添加评论测试')
    c = Comment(form)
    c.name = u.username
    print('c.comment==', c.comment)
    c.save()
    return redirect(url_for('.index'))

@main.route('/delete/<int:weiboId>', methods=['POST'])
def delete(weiboId):
    print('weiboId', weiboId)
    w = Weibo.query.get(weiboId)
    print('w=', w)
    if w is None :
        return redirect(url_for('.index'))
    else:
        w.delete()
    return w.json()