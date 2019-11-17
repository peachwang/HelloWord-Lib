# -*- coding: utf-8 -*-  
import sys, os; sys.path.append(os.path.realpath(__file__ + '/../'));
from functools import wraps
from shared import ensureArgsType

class Object() :

    _id_list = [ ]
    
    def __init__(self) :
        from Dict import Dict
        object.__setattr__(self, '_data', Dict())

    # @
    # def _registerProperty(self, property_name_list) :
    #     if 

    def __getattr__(self, name) :
        if name == '_data' : return self.__getattribute__('_data')
        if name == '__class__' : return self.__getattribute__('__class__')
        return self._data[name]

    def _wrapValue(self, value) :
        from Dict import Dict
        from List import List
        from Str import Str
        from DateTime import DateTime, datetime
        if isinstance(value, list)        : return List(value)
        elif isinstance(value, dict)      : return Dict(value)
        elif isinstance(value, str)       : return Str(value)
        elif isinstance(value, bytes)     : return Str(value.decode())
        elif isinstance(value, tuple)     : return tuple([ self._wrapValue(_) for _ in value ])
        elif isinstance(value, set)       : return set([ self._wrapValue(_) for _ in value ])
        elif isinstance(value, datetime)  : return DateTime(value)
        else : return value

    def __setattr__(self, name, value) :
        self._data[name] = self._wrapValue(value)
        return value

    def getId(self) :
        '''id(object) -> integer
        Return the identity of an object.  This is guaranteed to be unique among
        simultaneously existing objects.  (Hint: it's the object's memory address.)'''
        return hex(id(self))

    def getRaw(self) :
        return self._data

    def jsonSerialize(self) :
        return '<{} at {}>{}'.format(self.__class__, self.getId(), self._data.j())

    # 可读化
    def j(self) :
        from util import j
        return j(self.jsonSerialize())

    def print(self, color = '') :
        from util import E
        print(color, self.j(), E if color != '' else '')
        return self

    def __format__(self, code) :
        # 防止自嵌套死循环
        if self.getId() in Object._id_list :
            return object.__str__(self)
        Object._id_list.append(self.getId())
        result = '{}'.format(self._data)
        Object._id_list.remove(self.getId())
        return result

    def __str__(self) :
        return '<{} at {}>{}'.format(self.__class__, self.getId(), self._data)

    def _update(self, mapping) :
        self._data.update(mapping)
        return self

    def _warnNonPrivateName(func) :
        @wraps(func)
        def wrapper(self, *args, **kwargs) :
            from util import Y, E
            if isinstance(args[0], str) and args[0][0] != '_' :
                print(Y, 'Object {}\'s method {} is handling non-private name: {}'.format(self.__class__, func.__name__, args[0]), E)
            elif isinstance(args[0], list) and (len(args[0]) == 0 or not isinstance(args[0][0], str) or args[0][0][0] != '_') :
                print(Y, 'Object method {} is handling non-private name in name_list: {}'.format(func.__name__, args[0]), E)
            return func(self, *args, **kwargs)
        return wrapper

    @_warnNonPrivateName
    def _get(self, name_list, default = None) : 
        return self._data.get(name_list, default) # 字段可以不存在

    @_warnNonPrivateName
    def _getMulti(self, name_list) :
        return self._data.getMulti(name_list, de_underscore = True) # 字段可以不存在

    def _has(self, name_list) :
        if self._get(name_list) is None : return False
        else : return True
        # return self._data.has(name_list)

    def _hasNot(self, name_list) :
        return not self._has(name_list)
