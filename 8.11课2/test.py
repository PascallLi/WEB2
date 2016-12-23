import urllib.parse
print(urllib.parse.unquote("%E6%B5%8B%E8%AF%95abc"))

# find函数测试
str1 = '1234567890'
str2 = '45'

print(str1.find(str2))
print(str1.find(str2, 1))
print(str1.find(str2, 3))

#  3表示从第3个数开始，也就是'4'开始搜寻str2，返回'45'的第一个位置输出3

print('{:0>10}\n{:1}'.format(str2, str1))

print('{:10}{:5}'.format('hello', 'gua'))

# 输出helloXXXXXgua X为空格，个数为5

# zip函数测试
x = [1, 2, 3]
y = [4, 5, 6]
a = zip(x, y)
# 直接输出a，会返回一个对象
for i in a:
    c = i[0]
    d = i[1]
    print(c, d)
# 返回 [1, 4] [2, 5] [3, 6]


class Model(object):
    @classmethod
    def db_path(cls):
        # classmethod 有一个参数是class
        # 　所以我们可以得到class的名字
        classname = cls.__name__
        print('classname', classname)
        path = '{}.txt'.format(classname)
        return path

    @classmethod
    def all(cls):
        path = cls.db_path()
        models = print(path)
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
class Users(Model):
    def show(self):
        return print('引用')

Users().show()
