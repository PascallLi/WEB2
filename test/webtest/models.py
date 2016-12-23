#    放class类, Controller 控制器

# form在这里添加，简化全局中的route_message代码
import json
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
class Model(object):
    @classmethod
    def db_path(cls):
        # classmethod 有一个参数是class
        # 　所以我们可以得到class的名字
        classname = cls.__name__
        # print('classname', classname)
        path = '{}.txt'.format(classname)
        return path
    @classmethod
    def all(cls):
        path = cls.db_path()
        models = load(path)
        # print('models等于', models)
        # models = [{'password': '2222', 'username': '2222'}]
        ms = [cls(m) for m in models]
        # print('ms=', ms)
        return ms
        # [User
        # password: (12222)
        # username: (12333)]

    def __repr__(self):
        # 此函数是用来打印存入的数据（username, password这些），用到了魔法方法
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '{}\n{}'.format(classname, s)
    def save(self):
        models = self.all()
        models.append(self)
        l = [m.__dict__ for m in models]  #  包含了所有的数据
        print('l=', l)
        # l = [{'password': '2222', 'username': '2222'}]
        path = self.db_path()
        save(l, path)
class User(Model):
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self): # 预存账号密码便于验证
        return self.username == 'gua' and self.password == '123'

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2


class Message(Model):
    def __init__(self, form):
        self.message = form.get('author', '')
        self.author = form.get('message', '')

