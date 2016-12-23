from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import time

app = Flask(__name__)
app.secret_key = 'secret key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATEBASE_URI'] = 'sqlite:///todos.db'

db = SQLAlchemy(app)

class ModelHelper(object):
    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}:{}'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '{}\n{}\n\n'.format(classname, s)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Todo(db.Model, ModelHelper):
      __tablename__ = 'todos'
      id = db.Column(db.Integer, primary_key = True)
      task = db.Column(db.String())
      created_time = db.Column(db.Integer, default=0)
      user_id = db.Column(db.Integer)

      def __init__(self, form):
          format =  '%Y/%M/%D %H:%M:%S'
          v = int(time.time()) + 3600 * 8
          value = time.gmtime(v)
          dt = time.strftime(format, value)
          self.task = form.get('task', '')
          self.created_time = dt
      def valid(self):
          return len(self.task) > 0

class User(db.Model, ModelHelper):
      __tablename__ = 'users'
      id = db.Column(db.Integer, primary_key = True)
      username = db.Column(db.String())
      password = db.Column(db.String())
      created_time = db.Column(db.Integer, default= 0)

      def __init__(self, form):
          format = '%Y/%M/%D %h:%M:%s'
          v = int(time.time()) + 3600 * 8
          value = time.gmtime(v)
          dt = time.strftime(format, value)
          self.username = form.get('username', '')
          self.password = form.get('password', '')
          self.created_time = dt

      def validate_login(self, u):
          return u.username == self.username and u.password == self.password
      def change_password(self, password):
          if len(password) > 2:
              self.password = password
              self.save()
              return True
          else:
              return False


      def valid(self):
          return len(self.username) > 2 and len(self.password) > 2

def init_db():
      db.drop_all()
      db.create_all()
      print('rebulid database')

if __name__ == '__main__':
    init_db()
