import json

def save(data, path):
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
        ms = [cls(m) for m in model]  # m 是一个dict， 传递进类方法的是类，先对类处理后，再调用类的对象
        # 返回的ms是一个初始化cls的实例
        # print('model', model) # model = [{'':'','':'','':''},{'':'','':'','':''}]
        print('ms=', ms)  # ms = ['{}:{}'\n\n] 经过self.__dict__items()处理过后
        # print('type=', type(ms))
        return ms
    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}:{}\n'.format(k, v) for k,v in self.__dict__.items()]
        # print('properties = ', properties)
        # ['username:power\n', 'id:1\n', 'password:power\n']
        s = '\n'.join(properties)
        return '{}'.format(s)
    @classmethod
    def find_by(cls, **kwargs):
        k, v = '', ''
        for key, value in kwargs.items():
            k ,v = key, value
            print('v= ', value) # k = 'username'
        all = cls.all()
        for m in all:
           if v == m.__dict__[k]:
                print('m=', m)
                # m = id:X\n\nusername:''\n\npassword:''\n\n,ms（list）中的第一组数据
                return m
        return None
    @classmethod
    def find(cls, id):
        return cls.find_by(id=id)  # 输出的是cls.all中的元素
    def save(self):   # self = request.query()
        # print('request.save')
        models = self.all()
        if self.id is None:
            if len(models) == 0:
                self.id = 1
            else:
                self.id = models[-1].id + 1 # self.all().id 这里all(）为类方法
            models.append(self)  # models 是一个列表
        else:
            index = -1
            for i,m  in enumerate(models):
                index = i  # i = 0 1 2...
                if m.id == self.id:  # 如果是相同的username，直接跳出
                    break
                print('debug', index)
            models[index] = self   # 如果原来就带了ID，ID下替换成新的数据
            print('self=', self) # self = username:newgua password:123
        l = [m.__dict__ for m in models]
        #　l =  [{'password': '123', 'username': '123'}, {'password': '3333', 'username': '1233'}］
        # print('l = ', l)
        path = self.db_path()
        save(l, path)
class User(Model):
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.id = form.get('id', None)
    def validate_login(self):
        # return self.username == 'gua' and self.password == '123'
        # print(self.username)
        u = User.find_by(username = self.username)
        # return u.password == self.password and u is not None
        return u is not None
    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2