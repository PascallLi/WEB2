from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import time
import json
app = Flask(__name__)
app.secret_key = 'secret key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db = SQLAlchemy(app)

# 显示函数 保存到数据库+ 在数据库中删除数据
class ModelHelper(object):
    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}:{}'.format(k,v) for k,v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '{}\n{}\n'.format(classname, s)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



# 用户函数 包含用户名密码和生成时间，注册 登入验证 和 更改密码
class User(db.Model, ModelHelper):
      __tablename__ = 'users'
      id = db.Column(db.Integer, primary_key=True)
      username = db.Column(db.String())
      password = db.Column(db.String())
      created_time = db.Column(db.Integer, default=0)

      def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.created_time = int(time.time())

      def valid(self, u):
          user = User.query.filter_by(username=self.username).first()
          if user is not None:
              return False
          else:
                return True
      def validate_login(self, u):
          return u.username == self.username and u.password == self.password

      def change_password(self, password):
          if len(password) > 3:
              self.password = password
              self.save()
              return True
          else:
              return False

class Weibo(db.Model, ModelHelper):
    __tablename__ = 'weibo'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer)
    comments_num = db.Column(db.Integer)
    name = db.Column(db.Integer)

    def __init__(self, form):
        format = '%Y/%m/%d %H:%M:%S'
        v = int(time.time()) + 3600 * 8
        valuegmt = time.gmtime(v)
        dt = time.strftime(format, valuegmt)
        self.content = form.get('content', '')
        self.name = form.get('name', '')
        self.created_time = dt
        self.comments_num = 0
        self.comments = []

    def comments(self):
        self.comments = Comment.query.filter_by(weibo_id=self.id)

    def valid(self):
        return  len(self.content) > 3

    def json(self):
        d = {
            'id': self.id,
            'content': self.content,
            'created_time': self.created_time,
            'comments_num':self.comments_num,
        }
        return json.dumps(d, ensure_ascii=False)


class Comment(db.Model, ModelHelper):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)
    name = db.Column(db.Integer)
    weibo_id = db.Column(db.Integer)

    def __init__(self, form):
        format = '%Y/%m/%d %H:%M:%S'
        v = int(time.time()) + 3600 * 8
        valuegmt = time.gmtime(v)
        dt = time.strftime(format, valuegmt)
        self.comment = form.get('comment', '')
        self.created_time = dt
        self.name = form.get('name', '')
        self.weibo_id = int(form.get('weibo_id', -1))



# 重置数据库
def init_db():
    db.drop_all()
    db.create_all()
    print('rebuild database successful')

if __name__ == '__main__':
    init_db()