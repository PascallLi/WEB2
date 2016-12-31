from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


from models import db
# 这里 import 具体的 Model 类是为了给 migrate 用
# 如果不 import 那么无法迁移
# 这是 SQLAlchemy 的机制
from models.todo import Todo
from models.user import User
from models.node import Node
from models.topic import Topic

from routes.todo import main as routes_todo
from routes.node import main as routes_node
from routes.topic import main as routes_topic

# from routes.admin_views import admin
# from routes.chest_views import chest
# from routes.question_views import question
# from routes.topic_views import topic

app = Flask(__name__)
db_path = 'todo.sqlite'
manager = Manager(app)


def configure_app():
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = 'secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
    db.init_app(app)
    app.register_blueprint(routes_todo, url_prefix='/todo')
    app.register_blueprint(routes_node, url_prefix='/node')
    app.register_blueprint(routes_topic, url_prefix='/topic')

def configured_app():
    configure_app()
    return app


# 自定义的命令行命令用来运行服务器
@manager.command
def server():
    app = configured_app()

    config = dict(
        debug=True,
        host='127.0.0.1',
        port=3000,
    )
    app.run(**config)


def configure_manager():
    """
    这个函数用来配置命令行选项
    """
    Migrate(app, db)
    manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    configure_manager()
    configure_app()
    manager.run()
