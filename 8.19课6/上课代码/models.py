import json
import time
from utils import log


def save(data, path):
    """
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        # log('save', path, s, data)
        f.write(s)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        # log('load', s)
        return json.loads(s)


class Model(object):
    """
    Model 是所有 model 的基类
    @classmethod 是一个套路用法
    例如
    user = User()
    user.db_path() 返回 User.txt
    """
    @classmethod
    def db_path(cls):
        """
        cls 是类名, 谁调用的类名就是谁的
        classmethod 有一个参数是 class(这里我们用 cls 这个名字)
        所以我们可以得到 class 的名字
        """
        classname = cls.__name__
        path = '{}.txt'.format(classname)
        return path
    @classmethod
    # 创建Load的目的是为了实现每次发微博的时间显示不一样（默认created_time每次初始化都被覆盖了）
    def load(cls, d):
        m = cls({})
        for k, v in d.items():
            setattr(m, k, v) # 'm.k=v' 构建dict
            # log('m==', m)
        return m

    @classmethod
    def all(cls):
        """
        all 方法(类里面的函数叫方法)使用 load 函数得到所有的 models
        """
        path = cls.db_path()
        models = load(path)
        # 这里用了列表推导生成一个包含所有 实例 的 list
        # m 是 dict, 用 cls(m) 可以初始化一个 cls 的实例
        # 不明白就 log 大法看看这些都是啥
        ms = [cls.load(m) for m in models]
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        """
        用法如下，kwargs 是只有一个元素的 dict
        u = User.find_by(username='gua')
        """
        # log('kwargs, ', kwargs)
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                return m # 只返回第一个数据
        return None

    @classmethod
    def find_all(cls, **kwargs):
        # 返回所有数据生成一个List
        # log('kwargs, ', kwargs)
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        models = []
        for m in all:
            if v == m.__dict__[k]:
                models.append(m)
        return models

    @classmethod
    def find(cls, id):
        return cls.find_by(id=id)

    def __repr__(self):
        """
        __repr__ 是一个魔法方法
        简单来说, 它的作用是得到类的 字符串表达 形式
        比如 print(u) 实际上是 print(u.__repr__())
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

    def save(self):
        """
        用 all 方法读取文件中的所有 model 并生成一个 list
        把 self 添加进去并且保存进文件
        """
        # log('debug save')
        models = self.all()
        # log('models', models)
        # 如果没有 id，说明是新添加的元素
        if self.id is None:
            # 设置 self.id
            # 先看看是否是空 list
            if len(models) == 0:
                # 我们让第一个元素的 id 为 1（当然也可以为 0）
                self.id = 1
            else:
                m = models[-1]
                # log('m', m)
                self.id = m.id + 1
            models.append(self)
        else:
            # index = self.find(self.id)
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            log('debug', index)
            models[index] = self  #　如果原来的ＩＤ存在，将新的数据与老ＩＤ对应替换
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    def delete(self):  #实例方法 不是类的方法，需要得到实例的属性
        models = self.all()  # 先把所有数据得出来
        index = -1
        for i, m in enumerate(models):
            if self.id == m.id:
                index = i
                # log('index ==', index)
                break
        del models[index]
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)




class User(Model):
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """
    def __init__(self, form):
        self.id = form.get('id', None)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.note = form.get('note', '')
    def validate_login(self):
        # return self.username == 'gua' and self.password == '123'
        u = User.find_by(username=self.username)
        return u is not None and u.password == self.password
    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2


class Message(Model):
    """
    Message 是用来保存留言的 model
    """
    def __init__(self, form):
        self.id = None
        self.author = form.get('author', '')
        self.message = form.get('message', '')

class Weibo(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        self.content = form.get('content', '')
        self.created_time = int(time.time())
        self.user_id = form.get('user_id', None)
def test():

    weibo_form = {
        'content':'POWER',
    }
    w = Weibo(weibo_form)
    log(w.id, w.content, w.created_time)
# if __name__ == '__main__':
#     test()
