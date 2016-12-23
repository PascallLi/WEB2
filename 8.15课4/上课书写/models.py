#    放class类, Controller 控制器
# 如何用JSON保存数据，JSON是一个存储dict或者List的数据格式，把数据转换为字符串的过程教程序列化
# form在这里添加，简化全局中的route_message代码
import json
from utils import log
# save保存注册的数据


def save(data, path):
    """
    data 是dict 或者List
    path 是保存文件的路径
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)  # indent为缩进， ensure_ascii 将中文转化成ascii编码
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(s)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        return json.loads(s)
# load载入数据，将字符串转换成列表或者字典


# 列表推导
# def all_users():
#     path = 'User.txt.txt'
#     users = load(path)
#     us = [User.txt(u) for u in users]
#     return us
class Model(object):
    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = '{}.txt'.format(classname)
        return path
    @classmethod
    def all(cls):
        # classmethod 有一个参数是class
        # 　所以我们可以得到class的名字
        path = cls.db_path()
        models = load(path)
        ms = [cls(m) for m in models]
        return ms
    @classmethod
    # 下列函数目的：通过字典的Key或者value来查询数据
    def find_by(cls, **kwargs):
        k ,v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                return m
        return None
    def __repr__(self):  # 定义对类的实例调用 repr() 时的行为，此函数的作用是自动输出字段（username ,password....）
        classname = self.__class__.__name__  # 此魔法方法和魔方属性是为了获得class的名字
        # log('类的名字', classname)  # classname = User
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]# 对字典来说，还需要调用items
        # 万一是三个空格，无法分辨，所以第二个{}加上（），将self.dict字典中的元素拼接得到properties的这样一个列表
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)
    def save(self):
        models = self.all()
        models.append(self)
        l = [m.__dict__ for m in models]  # 包含了所有的数据，将每个Models转成字典
        path = self.db_path()
        save(l, path)
class User(Model):

    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self):   # 预存账号密码便于验证
        # 这里需要的功能为无论任何用户登入都是成功的
        u = User.find_by(username = self.username)
        return u is not None and u.password == self.password


    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2


class Message(Model):
    def __init__(self, form):
        self.message = form.get('author', '')
        self.author = form.get('message', '')


# 通过查询User.txt中的用户名和密码
def test():
    users = User.all()
    u = User.find_by(username = 'gua')
    log('users', u)
if __name__ == '__main__':
    test()


