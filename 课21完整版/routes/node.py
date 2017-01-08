#从todo.py复制后修改相应选项
from models.node import Node
from models.topic import Topic
from routes import *


# for decorators
from functools import wraps


main = Blueprint('node', __name__)

Model = Node

# 验证登入是否合法机制（管理员权限才能增加node板块）
def admin_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        # your code
        print('admin required')
        if request.args.get('uid') != '1':
            print('not admin')
            abort(404)
        return f(*args, **kwargs)
    return function


@main.route('/')
def index():
    ms = Model.query.all()
    return render_template('node_index.html', node_list=ms)

# 　显示板块中发帖的选项，　node.html页面
@main.route('/<int:id>')
def show(id):
    m = Model.query.get(id)
    return render_template('node.html', node=m)

# @main.route('/<int:id>')
# def todo(id):
#     m = Model.query.get(id)
#     return render_template('todo_index.html', node=m)

@main.route('/edit/<id>')
# @admin_required
def edit(id):
    t = Model.query.get(id)
    return render_template('node_edit.html', todo=t)


@main.route('/add', methods=['POST'])
# @admin_required
def add():
    form = request.form
    m = Model(form)
    m.save()
    return redirect(url_for('.index'))


@main.route('/update/<int:id>', methods=['POST'])
def update(id):
    form = request.form
    t = Model.query.get(id)
    t.update(form)
    return redirect(url_for('.index'))


@main.route('/delete/<int:id>')
# @admin_required
def delete(id):
    t = Model.query.get(id)
    t.delete()
    return redirect(url_for('.index'))
