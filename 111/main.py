from flask import Flask
from flask import render_template

from user import main as user_routes
from weibo import main as weibo_routes


app = Flask(__name__)
app.secret_key = 'random string'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'sadadsasadas.243434'


app.register_blueprint(user_routes)


app.register_blueprint(weibo_routes)




@app.errorhandler(404)
def error404(e):
    return render_template('404.html')

@app.errorhandler(410)
def error410(e):
    return render_template('410.html')

if __name__ == '__main__':
    config = dict(
        host='127.0.0.1',
        port=3000,
        debug=True,
        threaded=True,

    )
    app.run(**config)
