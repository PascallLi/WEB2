class User(object):
    def __init__(self, form):
        self.id = form.get('id', None)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.note = form.get('note', '')

m =  {
            "note": "power",
            "id": 1,
            "password": "123",
            "username": "123"
        }
u = User(m)

properties = ['{}: ({})'.format(k, v) for k, v in u.__dict__.items()]
s = '\n'.join(properties)
print('{}\n'.format(s))

