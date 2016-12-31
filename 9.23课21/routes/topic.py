from models.topic import Topic
from routes import *


main = Blueprint('topic', __name__)


@main.route('/')
def index():
    tc=Topic.query.all()
    return render_template('topic_index.html', topic_list=tc)

@main.route('/<int:id>')
def show(id):
    ms = Topic.query.get(id)
    return render_template('topic.html', topic=ms)


@main.route('/edit/<id>')
def edit(id):
    t = Topic.query.filter_by(id=id).first()
    return render_template('topic_edit.html', topic=t)


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    t = Topic(form)
    t.node_id = int(form.get('node_id'))
    t.save()
    return redirect(url_for('.index'))


@main.route('/update/<int:id>', methods=['POST'])
def update(id):
    form = request.form
    # t = Todo.query.filter_by(id=id).first()
    t  = Topic.query.get(id)
    t.update(form)
    return redirect(url_for('.index'))


@main.route('/delete/<id>')
def delete(id):
    t = Topic.query.filter_by(id=id).first()
    t.delete()
    return redirect(url_for('.index'))
