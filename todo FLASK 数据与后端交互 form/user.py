from models import User
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import Blueprint
from flask import abort
from flask import session

main = Blueprint('user', __name__)

def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        return u

@main.route('/')
def login_view():
    print('success')
    u = current_user()
    if u is not None:
        return redirect('/todo')
    return render_template('login.html')
# 如果没有存在此用户的话，跳转到登入注册页面

@main.route('/login', methods=['POST'])
def login():
    form = request.form
    u = User(form)
    user = User.query.filter_by(username=u.username).first()
    if user is not None and user.validate_login(u):
        print('登入成功')
        # 登入完之后从这里加密
        session['user_id'] = user.id
    else:
        return redirect(url_for('.login_view'))
    return redirect(url_for('.login_view'))

@main.route('/register', methods=['POST'])
def register():
    form = request.form
    u = User(form)
    if u.valid():
        u.save()
    else:
        abort(400)
    return redirect(url_for('user.login_view'))

























