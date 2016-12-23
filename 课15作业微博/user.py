from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import Blueprint
from flask import session
from flask import abort

from models import User

main = Blueprint('user', __name__)

def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)

        return u

@main.route('/')
def login_view():
    u = current_user()
    if u is not None:
        return redirect('/weibo')
    else:
        return render_template('login.html')

@main.route('/register', methods=['POST'])
def register():
    form = request.form
    u = User(form)
    if u.valid(u):
        u.save()
    else:
        abort(410)
    return redirect(url_for('.login_view'))

@main.route('/login', methods=['post'])
def login():
    form = request.form
    u = User(form)
    user = User.query.filter_by(username= u.username).first()
    if u.validate_login(user):
        session['user_id'] = user.id
        print('登入成功')
        return redirect('/weibo')
    else:
        print('登入失败')
    return redirect(url_for('.login_view'))

@main.route('/update_password', methods=['POST'])
def update_password():
    u = current_user()
    password = request.query.get('password', '')
    if u.change_password(password):
        print('更改密码成功')
    else:
        print('密码必须大于3位')
    return redirect('/profile')

@main.route('/profile')
def profile():
    u = current_user()
    if u is not None:
        print('profile', u.id, u.content, u.created_time)
        return render_template('profile.html', user=u)
    else:
        return redirect(url_for('.login_view'))