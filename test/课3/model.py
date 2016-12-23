import json

def save(data, path):
        print('save')
        s = json.dumps(data, indent=2, ensure_ascii=False)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(s)
def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        return json.loads(s)

class Model(object):
    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = '{}.txt'.format(classname)
        return path
    @classmethod
    def all(cls):
        method = cls.db_path()
        model = load(method)
        ms = [cls(m) for m in model]  # m 是一个dict， cls(m)表示类的实例，相当于request = Request(m)
        return ms
    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}:{}\n'.format(k, v) for k,v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '{}'.format(s)

    def save(self):   # self = request.query()
        print('request.save')
        models = self.all()
        models.append(self)
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)
class User(Model):
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self):
        return self.username == 'gua' and self.password == '123'
    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2