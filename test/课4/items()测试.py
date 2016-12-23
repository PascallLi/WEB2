

m= {
    'username':'123',
    'password': '235',
    }

properties = ['{}:{}'.format(k, v) for k, v in m.items()]
properties_1 = m.items()  #　处理字典变成List,拆解字典
s = '\n'.join(properties)

# print('{}'.format(s))
# 'password:235'
# 'username:123'

# print(properties_1)
# dict_items([('username', '123'), ('password', '235')])

models = {'password:123' 'username:123',},{'password:3333' 'username:1233',}

l = models.__dict__.items()

print('__dict__方法 = ', l)