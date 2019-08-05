
import sys, os; sys.path.append(os.path.realpath(__file__ + '/../../'));
from List import List
from Dict import Dict
from Str import Str
from Object import Object
from util import str_object

# =============== Str ===================

class A(Object) :

    def __init__(self) :
        super().__init__()
        self.key1 = 0
    
    # def __eq__(self, o) :
    #     return self.key1 == o.key1
    
    # def __getattr__(self, key) :
    #     print('A.__getattr__()')
    #     return self.__getattribute__(key)

    @property
    def key1(self):
        print('A.key1()')
        self._key1 += 1
        return self._key1

    @key1.setter
    def key1(self, value) :
        self._key1 = value

a = A()
print(a.key1)
# print(a.key1)
# print(a._key1)
# print(a._key1)
exit()

class B(Dict, Object) :
    pass

a1 = A()
a1.key1 = 1
a1.key2 = 2
print('{}'.format(a1))
print(a1)
print(hex(id(a1)))

a2 = A()
a2.key1 = 1
a2.key2 = 3
print('{}'.format(a2))
print(a2)

a3 = A()
a3.key1 = 2
a3.key2 = 2
print('{}'.format(a3))
print(a3)

print(a1 == a2)
print(a2 == a3)
print(a3 == a1)

l = List([a2, a3])

print(a1 in l)
# print(l.index(a1))
# print(l.count(a2))
print(l)
print(l.unique())

exit()


a = A()
a.c = 1

b = B()
b.d = 2


exit()

a = List([1,2,3])
# b = List([1,2,3])
b = a
a += a
print(a)
print(b)
print(a is b)
exit()
a = Str('abc')
b = a
# a += 'def'
# print(a)
# print(type(a))
# print(b)
# print(type(b))
# print(a is b)
print(a.strip('c'))
print(a)
print(b)
print(a is b)
exit()


a = List(1,2,3)
b = a
print(b is a)
a.append(4)
print(b is a)
print(a)
print(b)

st = Str('123.123.123')
print(type(st.strip('3')))
print(st.strip('3'))
exit()


# print(Str('{:07.1f}').format(123.444))
# print(type(Str('{:07.1f}').format(123.444)))
# print(Str('123') == '123')

# a = Dict({'1' : {2 : {'3' : ['4', '5', '6']}}, 'pop' : 11})
class A :
    pass
a = {'1' : {2 : {'3' : ['4', '5', '6']}}, 'pop' : datetime.strptime('201908011200', '%Y%m%d%H%M%S'), 'A' : A()}
print(a['pop'])
print(str(a['pop']))
print('{}'.format(a['pop']))
print(str_object(a))
print(type(str_object(a)))
print(j(str_object(a)))
# print(j(a))
exit()
print('{}'.format(a))
print(str(a))
exit()
st = Str(List(['1',2,3]))
# print('{}'.format(st))
print(st)
exit()
a = Str('123')
# print(type(a + '456'))
# print(type(a.getRaw()))
# print(a)
# print(a.getRaw())

a = Dict({Str('c') : 'b'})
print(a)
print(a.has(Str('c')))
print(a.get(Str('c')))
print(a.get('c'))
print('c' in a)
print(Str('c') in a)

exit()
print(str(List(1,2,3)))
s = Str(List(['.']))
print(type(s))
s += '123'
print(s)
print(type(s))
t = s.join(List(Str('1'),'2','3'))
print(t)
print(type(t))
print(t.split('.'))
print(type(t.split('.')))
print(type(t.split('.')[0]))
st1 = Str('regurgitate')
st2 = Str('apple')
print(type(st1), st1)
print(type(st2), st2)
# st = st1 + st2
st = 'regurgitate ' + st2
# st = st1 + ' apple'
st = Str(st)
print(type(st), st)
print('regurgitate apple' == st)

# =============== List ===================

# a = List([[1,2],[3,4]])
# a = List(List([5,4,3]), List(6,7,8,4))
a = [1,2,3]
# a = List([1,2,3])
# a = List(1,2,3)
# a = List(List())
# b = List([4,5,6])
b = List([4,5,6])
# print(type(a+b))
# print(a+b)
# print(a)
print(b)
a+=b
print(a)
print(b)
# b = List(a)
# b.append(5)
# c = b.filter(lambda x, i : x % 2 == 0)
print('{}'.format(a))
print(type(a))
print(b)
print(type(b))
# print(c)
# print(type(c))
print(a is b)
# print(b==c)
# print(a==c)
print(a.count(4))

# =============== Dict ===================

a = Dict({'1' : {2 : {'3' : ['4', '5', '6']}}, 'pop' : 11})
# a = Dict({'1' : 2})
a.set(['apple', 'peach'], {})
# import json
# print(json.dumps(a.items()))
# print(a.items())
# print('{}'.format(a))
# print(a)
from List import List
b = List([1,2,3])
print(b)

# print(json.dumps(a))
# print('apple{0:\n},{1:a}'.format(a, a))
# print(a)
# print(type(a))
# print(a[1])
# print(type(a[1][2][3]))