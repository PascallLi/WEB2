from flask import Flask


from todo import main as todo_routes
from user import main as user_routes

app = Flask(__name__)

app.secret_key = 'sda sa da dsad sa dsa d'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.register_blueprint(todo_routes)
app.register_blueprint(user_routes)


# @app.errorhandler(404)
# def error404(e):
#     return render_template('404.html')

if __name__ == '__main__':
    config = dict(
        port= 3000,
        host = '127.0.0.1',
        threaded = True,
        debug = True,

    )
    app.run(**config)