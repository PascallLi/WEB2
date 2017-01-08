from flask import render_template
from flask import abort
from flask import url_for
from flask import redirect
from flask import request
from flask import Blueprint

import  json
from models import Weibo
from models import Comment
from user import current_user

main = Blueprint('weibo', __name__)

# 新建一个函数使用统一字典构造
def api_response(success, data=None, message=''):
    r = {
        'success': success,
        'data': data,
        'message': message,
    }
    return json.dumps(r, ensure_ascii=False)



@main.route('/weibo')
def index():
    # print('form===', request.form)
    u  = current_user()
    if u is None:
        return redirect(url_for('user.login_view'))
    else:
        weibo_list = Weibo.query.order_by(Weibo.id.desc()).all()
        # 以Weibo.id逆序查找将所有的微博数据显示出来
        for i in weibo_list:
            i.comment = i.comments()
        return render_template('weibo.html', weibos=weibo_list)

@main.route('/weibo/add', methods=['POST'])
# @main.route('/weibo/add')
def add():
    u = current_user()
    # print('测试')
    # form = request.form
    # 获取字符串形式数据，手动处理如下
    # data = request.get_data()
    # get_data() 得到原始的Body数据，需要转换成json格式，下面是手动转换格式
    # json_str = data.decode('utf-8')
    # form = json.loads(json_str)
    # print('form没数据了', data, form)

    # json有默认的解析格式
    # form = request.json
    #  前端通过ajax发送过来的请求中数据格式为json格式字符串，所以需要解析
    form = request.get_json()
    print('add weibo', form)
    w = Weibo(form)
    w.name = u.username
    # r = {
    #     'data': []
    # }
    if w.valid():
        w.save()
        return  api_response(True, data=w.json())
    else:
        return api_response(False, message=w.error())
    #     r['data'] = w.json()
    #     r['success'] = True
    # else:
    #     r['success'] = False
    #     r['message'] = w.error()
        # 如果失败发送失败的具体信息
    # return json.dumps(r, ensure_ascii=False)

@main.route('/comment/add', methods=['POST'])
#  评论在这里没有使用json字符串传
def comment_add():
#     u = current_user()
    form = request.form
#     print('添加评论测试')
#     c = Comment(form)
#     c.name = u.username
#     print('c.comment==', c.comment)
#     c.save()
#     return redirect(url_for('.index'))
# def comment_add():
    u = current_user()
    # form1 = request.form
    # print(form1)
    # form = request.get_json()
    print('commet_form=', form)
    c  = Comment(form)
    c.name = u.username
    c.user_id = u.id
    c.save()
    return api_response(True, data=c.json())

@main.route('/delete/<int:weiboId>', methods=['POST'])
def delete(weiboId):
    print('weiboId', weiboId)
    w = Weibo.query.get(weiboId)
    # print('w=', w)
    if w is None :
        return redirect(url_for('.index'))
    else:
        w.delete()
        return api_response(True, data=w.json())
    #     r = {
    #         'success': True,
    #         'data': w.json(),
    #
    #     }
    # return json.dumps(r, ensure_ascii=False)