# -*- coding: utf-8 -*-  

class Object() :
    
    def __init__(self, obj = None) :
        if obj is None :
            object.__setattr__(self, 'obj', None)
        elif type(obj) is dict :
            object.__setattr__(self, 'obj', Dict({ k : Object(obj[k]) for k in obj }))
        elif type(obj) is list :
            object.__setattr__(self, 'obj', List([ Object(item) for item in obj ]))
        elif type(obj) is Object :
            object.__setattr__(self, 'obj', obj.obj)
        else : 
            object.__setattr__(self, 'obj', obj)

    def __getattr__(self, name) :
        # print('__getattr__', self.obj, name)
        if name in dir(list) and type(self.obj) in [ list, List ] :
            if type(self.obj) is not List : 
                object.__setattr__(self, 'obj', List(self.obj))
            return self.obj.__getattribute__(name)
        elif name in dir(dict) and type(self.obj) in [ dict, Dict ] :
            if type(self.obj) is not Dict :
                object.__setattr__(self, 'obj', Dict(self.obj))
            return self.obj.__getattribute__(name)
        elif name in dir(list) or name in dir(dict) :
            print(ERROR, '__call__ Error 01: self.obj(', self.obj, ') has no method(', name, ')', END)
            raise Exception('__call__ Error 01')
        elif type(self.obj) is not Dict :
            print(ERROR, '__getattr__ Error 02: self.obj(', self.obj, ')[', name, ']', END)
            raise Exception('__getattr__ Error 02')
        if self.obj.get(name) is None :
            # print('init', name)
            print(ERROR, '__getattr__ Error 03: self.obj(', self.obj, ')[', name, ']', END)
            raise Exception('__getattr__ Error 03')
            # self.obj[name] = Object()
        return self.obj[name]

    def __setattr__(self, name, value) :
        # print('__setattr__', self.obj, name, value)
        if type(self.obj) is Dict :
            self.obj[name] = Object(value)
        else :
            print(ERROR, '__setattr__ Error 01: self.obj(', self.obj, ')[', name, '] =', value, END)
            raise Exception('__setattr__ Error 01')
        return value

    def __delattr__(self, name) :
        del self.obj[name]

    def __getitem__(self, key) :
        # print('__getitem__', key)
        if type(self.obj) not in [ List, Dict ]  :
            print(ERROR, '__getitem__ Error 01: self.obj(', self.obj, ')[', key, '] is not list or dict', END)
            raise Exception('__getitem__ Error 01')
        else :
            try :
                return self.obj[key]
            except Exception as e :
                if key != len(self.obj) :
                    print(ERROR, '__getitem__ Error 02: self.obj(', self.obj, ')[', key, ']', END)
                raise e

    def __setitem__(self, key, value) :
        # print('__setitem__', key, value)
        if type(self.obj) not in [ List, Dict ] :
            print(ERROR, '__setitem__ Error 01: self.obj(', self.obj, ')[', key, '] is not list or dict', END)
            raise Exception('__setitem__ Error 01')
        else :
            self.obj[key] = Object(value)
            return value

    def __repr__(self) :
        return str(self.obj)

if __name__ == '__main__':
    pass