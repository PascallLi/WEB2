class data_test(object):
    day = 0
    month = 0
    year = 0
    def __init__(self, year=0, month=0, day=0):
        self.day= day
        self.month=month
        self.year=year
    @classmethod
    def get_date(cls,string_date):
        year, month, day = map(int, string_date.split('-'))
        date = cls(year,month,day)
        return date
    def out_date(self):
        print('year:')
        print(self.year)
        print('month')
        print(self.month)
        print('day')
        print(self.day)

a = data_test()

print('{}'.format(a.get_date('2016-9-25').year))

# @classmethod传递的是类，也就是data_test, 不是实例data_test()。先对类进行处理，然后再调用类的实例，初始化，输出