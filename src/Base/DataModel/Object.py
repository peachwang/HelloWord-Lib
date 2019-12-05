# -*- coding: utf-8 -*-  
import sys, os; sys.path.append(os.path.realpath(__file__ + '/../'));
from functools import wraps, partial
from shared import ensureArgsType, Optional, Union

class Object() :

    _id_list = [ ]
    
    def __init__(self) :
        from List import List
        from Dict import Dict
        object.__setattr__(self, '_data', Dict())
        object.__setattr__(self, '_property_name_list', List())
        object.__setattr__(self, '_property_default_list', Dict())

    @ensureArgsType
    def _registerProperty(self, property_name_list: list) :
        pnl = self.__getattribute__('_property_name_list')
        pdl = self.__getattribute__('_property_default_list')
        for name in property_name_list :
            if isinstance(name, str) :
                pnl.append(name)
            elif isinstance(name, tuple) :
                pnl.append(name[0])
                pdl[name[0]] = name[1]
            else :
                raise Exception(f'Unexpected {type(name)=} of {name=}')

    def _hasProperty(self, name) :
        return self._has(f'_{name}')

    def _hasNotProperty(self, name) :
        return not self._hasProperty(name)

    def _ensureHasProperty(self, name) :
        if _hasNotProperty(name) :
            raise Exception(f'{self}必须拥有属性{name}.')
        return self

    def _setProperty(self, name, value) :
        self._data[f'_{name}'] = value
        return self

    def _appendProperty(self, name, value_or_generator_or_iterator, filter_none = True) :
        from List import List
        from inspect import isgenerator
        name = f'_{name}'
        def appendValue(value) :
            if filter_none and value == None : return
            if self._data.hasNot(name) :
                self._data[name] = List()
            self._data[name].append(value)
        if isgenerator(value_or_generator_or_iterator) or '__next__' in dir(value_or_generator_or_iterator) :
            for value in value_or_generator_or_iterator :
                appendValue(value)
        else : appendValue(value_or_generator_or_iterator)
        return self

    def __getattr__(self, name) :
        from Str import Str
        if name == '_data' : return self.__getattribute__('_data')
        if name == '__class__' : return self.__getattribute__('__class__')
        if name in dir(self) : return self.__getattribute__(name)
        pnl = self.__getattribute__('_property_name_list')
        pdl = self.__getattribute__('_property_default_list')
        if name in pnl : name = f'_{name}'
        if name[0] == '_' and name[1:] in pnl :
            if self._data.hasNot(name) and name[1:] in pdl :
                return pdl[name[1:]]
        if self._data.has(name) : return self._data[name]

        def generatePartial(prefix):
            l = len(prefix)
            suffix = ('List' if prefix == 'append' else '')
            if name[:l] == prefix and (Str(name[l]).isUpper() or name[l] == '_')\
                and ((idx1 := pnl.index(name1 := Str(name[l:]).toPascalCase() + suffix)) is not None 
                    or (idx2 := pnl.index(name2 := Str(name[l:]).toSnakeCase() + suffix)) is not None) :
                if idx1 is not None :
                    return partial(self.__getattribute__(f'_{prefix}Property'), str(name1))
                elif idx2 is not None :
                    return partial(self.__getattribute__(f'_{prefix}Property'), str(name2))
            return None

        for prefix in [ 'has', 'hasNot', 'ensureHas', 'set', 'append' ] :
            if (p := generatePartial(prefix)) is not None :
                return p

        from util import P, E
        raise Exception(f'Object{P}{type(self)}{E}中无{P}{name}{E}属性或方法, 只有这些属性: {(self._data.keys() + dir(self)).filter(lambda name : name not in dir(Object))}; {pnl=}; {pdl=}')

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
        from util import j
        _ = self._data.jsonSerialize()
        _['__instance__'] = f'<{self.__class__} at {self.getId()}>'
        return _

    # 可读化
    def j(self) :
        from util import j
        return j(self.jsonSerialize())

    def json(self) :
        from Dict import Dict
        return Dict((name, value.json() if 'json' in dir(value := self.__getattr__(name)) else value)
            for name in self.__getattribute__('_property_name_list') if self._data.has(f'_{name}') or name in dir(self))

    def print(self, color = '', json = False) :
        from util import E
        if json :
            print(color, self.json().j(), E if color != '' else '')
        else :
            print(color, self.j(), E if color != '' else '')
        return self

    def __format__(self, code) :
        # 防止自嵌套死循环
        if self.getId() in Object._id_list :
            return object.__str__(self)
        Object._id_list.append(self.getId())
        result = f'{self._data}'
        Object._id_list.remove(self.getId())
        return result

    def __str__(self) :
        return f'<{self.__class__} at {self.getId()}>{str(self._data)}'

    def _update(self, mapping) :
        self._data.update(mapping)
        return self

    def _warnNonPrivateName(func) :
        @wraps(func)
        def wrapper(self, *args, **kwargs) :
            from util import Y, E
            if isinstance(args[0], str) and args[0][0] != '_' :
                print(Y, f'Object {self.__class__}\'s method {func.__name__} is handling non-private name: {args[0]}', E)
            elif isinstance(args[0], list) and (len(args[0]) == 0 or not isinstance(args[0][0], str) or args[0][0][0] != '_') :
                print(Y, f'Object method {func.__name__} is handling non-private name in name_list: {args[0]}', E)
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
