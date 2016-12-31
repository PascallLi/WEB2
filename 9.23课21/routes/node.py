from models.node import Node
from routes import *
from models.topic import Topic

# 装饰器
from functools import wraps

main = Blueprint('node', __name__)

# 修饰器，加admin_required的话可以增加管理员权限
def admin_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        print('admin required')
        # 看看后缀有没有?uid=1 有是admin才会删除
        if request.args.get('uid') != '1':
            abort(404)
        return f(*args, **kwargs)
    return function

@main.route('/')
def index():
    ms = Node.query.all()
    return render_template('node_index.html', node_list=ms)

# 单独板块, 显示板块，里面才有发帖选项
@main.route('/<int:id>')
def show(id):
     m = Node.query.get(id)
     return render_template('node.html', node=m)

@main.route('/edit/<id>')
def edit(id):
    # t = Node.query.filter_by(id=id).first()
    n = Node.query.get(id)
    return render_template('node_edit.html', todo=n)


@main.route('/add', methods=['POST'])
@admin_required
def add():
    form = request.form
    t = Node(form)
    t.save()
    return redirect(url_for('.index'))


@main.route('/update/<int:id>', methods=['POST'])
def update(id):
    form = request.form
    # t = Todo.query.filter_by(id=id).first()
    n = Node.query.get(id)
    n.update(form)
    return redirect(url_for('.index'))


@main.route('/delete/<id>')
@admin_required
def delete(id):
    t = Node.query.filter_by(id=id).first()
    t.delete()
    return redirect(url_for('.index'))