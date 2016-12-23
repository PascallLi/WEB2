from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import  Blueprint
from flask import abort

from user import current_user
from models import Todo

main = Blueprint('todo', __name__)

@main.route('/todo',)
def index():
    todo_list = Todo.query.all()
    return render_template('todo.html', todos=todo_list)

@main.route('/add', methods=['POST'])
def add():
    form = request.form
    t = Todo(form)
    #  从前端task=XX&time=XX 的数据放到Todo的model中解析，保存到服务器中
    if t.valid():
        t.save()
    else:
        abort(400)
    return redirect(url_for('todo.index'))

@main.route('/delete/<int:todo_id>')
def delete(todo_id):
    t = Todo.query.get(todo_id)
    t.delete()
    return redirect(url_for('.index'))