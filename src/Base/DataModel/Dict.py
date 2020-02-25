# -*- coding: utf-8 -*-  
import sys, os; sys.path.append(os.path.realpath(__file__ + '/../'))
from types import BuiltinFunctionType, FunctionType, BuiltinMethodType, MethodType, LambdaType, GeneratorType
from shared import ensureArgsType, Optional, Union, UserTypeError, _print
# from Timer import Timer

class Dict(dict) :

    _has_imported_types = False
    NV = V_NON_VACANCY = 'V_NON_VACANCY'

    def _importTypes(self) :
        if self.__getattribute__('_has_imported_types') : return
        from List import List; dict.__setattr__(self, '_List', List)
        dict.__setattr__(self, '_Dict', Dict)
        from Str import Str; dict.__setattr__(self, '_Str', Str)
        from Object import Object; dict.__setattr__(self, '_Object', Object)
        from DateTime import DateTime, datetime; dict.__setattr__(self, '_DateTime', DateTime); dict.__setattr__(self, '_datetime', datetime)
        from File import File; dict.__setattr__(self, '_File', File)
        from Folder import Folder; dict.__setattr__(self, '_Folder', Folder)
        from Audio import Audio; dict.__setattr__(self, '_Audio', Audio)
        # 如果不赋值到self中，本装饰器无效，原因：locals() 只读, globals() 可读可写。https://www.jianshu.com/p/4510a9d68f3f
        dict.__setattr__(self, '_has_imported_types', True)

    def _wrapValue(self, value, /) :
        self._importTypes()
        if isinstance(value, list)        : return self._List(value)
        elif isinstance(value, dict)      : return self._Dict(value)
        elif isinstance(value, str)       : return self._Str(value)
        elif isinstance(value, bytes)     : return self._Str(value.decode())
        elif isinstance(value, tuple)     : return tuple([ self._wrapValue(_) for _ in value ])
        elif isinstance(value, set)       : return set([ self._wrapValue(_) for _ in value ])
        elif isinstance(value, self._datetime)  : return self._DateTime(value)
        else : return value

    def __init__(self, *args, **kwargs) :
        '''Initialize self.  See help(type(self)) for accurate signature.'''
        if len(args) == 0 :
            dict.__init__(self, {})
        elif len(args) == 1 :
            if isinstance(args[0], dict) :
                for key in args[0] :
                    dict.__setitem__(self, key, self._wrapValue(args[0][key]))
            elif isinstance(args[0], (zip, GeneratorType)) :
                self.__init__(dict(args[0]))
            elif isinstance(args[0], Dict) :
                dict.__init__(self, args[0]._getData())
            else :
                raise UserTypeError(args)
        else :
            raise UserTypeError(args)
        if len(kwargs) > 0 : dict.update(self, Dict(kwargs))

    # @ensureArgsType
    def fromkeys(self, key_list: list, value = None, /) :
        '''Returns a new dict with keys from iterable and values equal to value.'''
        '''IN PLACE'''
        if isinstance(value, list) :
            if len(value) == len(key_list) :
                self.__init__(zip(key_list, value))
                return self
            else :
                raise Exception(f'key_list 和 value 长度不匹配\n{key_list=}\n{value=}')
        else :
            self.__init__(zip(key_list, [value] * len(key_list)))
            return self

    def copy(self) :
        '''D.copy() -> a shallow copy of D'''
        return Dict(self)

    def getId(self) :
        '''
        id(object) -> integer
        Return the identity of an object.  This is guaranteed to be unique among
        simultaneously existing objects.  (Hint: it's the object's memory address.)
        '''
        return hex(id(self))

    def iter(self) :
        '''
        Implement iter(self).
        iter(iterable) -> iterator
        iter(callable, sentinel) -> iterator
        Get an iterator from an object.  In the first form, the argument must
        supply its own iterator, or be a sequence.
        In the second form, the callable is called until it returns the sentinel.
        '''
        return dict.__iter__(self)

    # 去除最外层封装，用于原生对象初始化：list/dict.__init__()/.update()
    def _getData(self) :
        return { key : self[key] for key in self }

    # 原生化 list, dict, str, Object._data, datetime
    def getRaw(self) :
        '''NOT IN PLACE'''
        self._importTypes()
        from util import json_serialize
        _ = {}
        for key in self :
            if isinstance(self[key], (self._List, self._Dict, self._Str, self._Object, self._DateTime, self._File, self._Folder, self._Audio)) :
                _[json_serialize(key)] = self[key].jsonSerialize()
            else :
                _[json_serialize(key)] = json_serialize(self[key]) # 可能是int, float, bool, tuple, set, range, zip, object，不可能是list. dict, str, bytes, datetime
        return _

    def toMongoDoc(self) :
        from bson import ObjectId
        self._importTypes()
        for key, value in self.items() :
            if isinstance(value, self._Dict) :
                if value.has('$id') :
                    self[key] = ObjectId(value['$id'])
                elif value.has('sec') and value.has('usec') :
                    self[key] = self._DateTime(value.sec + value.usec / 1000000).getRaw()
                else :
                    self[key].toMongoDoc()
            elif isinstance(value, self._List) :
                self[key].toMongoDoc()
        return self

    @_print
    def printLen(self) :
        return f'{self.len()}个键值', False

    @_print
    def printLine(self) :
        return self.keys().mapped(lambda key : f'{key}: {self[key]}').join('\n'), True

    def __format__(self, code) :
        '''default object formatter'''
        return "{{{}}}".format(
            self.keys()
                .map(lambda key : '{} : {}'.format(
                        '"{}"'.format(key) if isinstance(key, (str, bytes)) else '{}'.format(key),
                        '"{}"'.format(self[key]) if isinstance(self[key], (str, bytes)) else '{}'.format(self[key])
                    )
                )
                .join(', ')
        )

    @_print
    def printFormat(self) :
        return self.keys().mapped(lambda key : f'{key}: {self[key]}').join('\n'), True

    def __str__(self) :
        '''Return str(self).'''
        return 'Dict{{{}}}'.format(
            self.keys()
                .map(lambda key : '{} : {}'.format(
                        '"{}"'.format(key) if isinstance(key, (str, bytes)) else str(key),
                        '"{}"'.format(self[key]) if isinstance(self[key], (str, bytes)) else str(self[key])
                    )
                )
                .join(', ')
        )

    @_print
    def printStr(self) :
        return self.keys().mapped(lambda key : f'{str(key)}: {str(self[key])}').join('\n'), True

    def jsonSerialize(self) :
        '''NOT IN PLACE'''
        self._importTypes()
        from util import json_serialize
        _ = {}
        for key in self :
            if isinstance(self[key], (self._List, self._Dict, self._Str, self._Object, self._DateTime, self._File, self._Folder, self._Audio)) :
                _[json_serialize(key)] = self[key].jsonSerialize()
            else :
                _[json_serialize(key)] = json_serialize(self[key]) # 可能是int, float, bool, tuple, set, range, zip, object，不可能是list. dict, str, bytes, datetime
        return _

    # 可读化
    def j(self, *, indent = True) :
        '''NOT IN PLACE'''
        from util import j
        return j(self.jsonSerialize(), indent = 4 if indent else None)

    @_print
    def printJ(self) :
        return f'{self.j()}', True

    def json(self) :
        '''带有业务逻辑，与 j 不同'''
        '''NOT IN PLACE'''
        return Dict((key, self[key].json()) if 'json' in dir(self[key]) else (key, self[key]) for key in self)

    @_print
    def printJson(self) :
       return f'{self.json().j()}', False

    def inspect(self, **kwargs) :
        from Inspect import Inspect
        return Inspect(self, **kwargs)

    def diff(self, other, /) :
        from Inspect import Diff
        return Diff(self, other)

    def isList(self) :
        return False

    def isDict(self) :
        return True

    def __eq__(self, other, /) :
        '''Return self==value.'''
        if not isinstance(other, Dict) or self.len() != other.len() : return False
        return self.j() == other.j()

    def __ne__(self, other, /) :
        '''Return self!=value.'''
        return not self.__eq__(other)

    def __ge__(self, other, /) :
        '''Return self>=value.'''
        raise NotImplementedError

    def __gt__(self, other, /) :
        '''Return self>value.'''
        raise NotImplementedError

    def __le__(self, other, /) :
        '''Return self<=value.'''
        raise NotImplementedError

    def __lt__(self, other, /) :
        '''Return self<value.'''
        raise NotImplementedError

    def __len__(self) :
        '''Return len(self).'''
        return dict.__len__(self)

    def len(self) :
        return dict.__len__(self)

    def isEmpty(self) :
        return self.len() == 0

    def isNotEmpty(self) :
        return not self.isEmpty()

    def __contains__(self, key, /) :
        '''D.__contains__(k) -> True if D has a key k, else False.'''
        return dict.__contains__(self, key)

    def has(self, key_list, /) :
        self._importTypes()
        if isinstance(key_list, (type(None), str, bytes, int, float, bool, tuple, range, zip, self._datetime, type)) :
            return dict.__contains__(self, key_list)
        elif isinstance(key_list, list) :
            if len(key_list) == 0 :
                raise Exception(f'非法{key_list=}')
            now = self
            for key in key_list :
                if not dict.__contains__(now, key) : return False
                now = now[key]
            return True
        else :
            raise UserTypeError(key_list)

    def hasNot(self, key_list, /) :
        return not self.has(key_list)

    def hasAnyOf(self, key_list_list, /) :
        return any(self.has(key_list) for key_list in key_list_list)

    def hasAllOf(self, key_list_list, /) :
        return all(self.has(key_list) for key_list in key_list_list)

    def hasNoneOf(self, key_list_list, /) :
        return all(self.hasNot(key_list) for key_list in key_list_list)

    def keys(self) :
        '''D.keys() -> a set-like object providing a view on D's keys'''
        self._importTypes()
        return self._List(list(dict.keys(self)))
    
    def values(self) :
        '''D.values() -> an object providing a view on D's values'''
        self._importTypes()
        return self._List(list(dict.values(self)))

    def items(self) :
        '''D.items() -> a set-like object providing a view on D's items'''
        self._importTypes()
        return self._List(list(dict.items(self)))

    # def __getattribute__(self, key) :
        '''
        Return getattr(self, name).
        '''
        # if key in ('List', 'Dict', 'Str', 'Object') :
            # print(f'__getattribute__ {key=}')
        # return dict.__getattribute__(self, key)

    def __getattr__(self, key) :
        '''
        getattr(object, name[, default]) -> value
        
        Get a named attribute from an object; getattr(x, 'y') is equivalent to x.y.
        When a default argument is given, it is returned when the attribute doesn't
        exist; without it, an exception is raised in that case.
        '''
        # if key in ('List', 'Dict', 'Str', 'Object') :
            # print(f'__getattr__ {key=}')
        return self[key]

    def __getitem__(self, key) :
        '''x.__getitem__(y) <==> x[y]'''
        return self.get(key, self.NV)

    def get(self, key_list, /, default = None) :
        '''D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None.'''
        self._importTypes()
        if isinstance(key_list, (type(None), str, bytes, int, float, bool, tuple, range, zip, self._datetime, type)) :
            if default == self.NV and not dict.__contains__(self, key_list) :
                raise Exception(f'键 {key_list} 不能为空\n{self.keys()=}')
            return dict.get(self, key_list, self._wrapValue(default))
        elif isinstance(key_list, list) :
            if self.hasNot(key_list) :
                if default == self.NV :
                    raise Exception(f'键 {key_list} 不能为空\n{self=}')
                return self._wrapValue(default)
            else :
                now = self
                for key in key_list :
                    now = now[key]
                return now
        else :
            raise UserTypeError(key_list)

    # operator.attrgetter(*attrs)
    # [ (key1,), (key2, None), key3 ]
    # @ensureArgsType
    def getMulti(self, key_list: list, /, *, de_underscore: bool = False) :
        # @ensureArgsType
        def deUnderscoure(key: str) :
            if de_underscore and key[0] == '_' : return key[1:]
            else : return key
        result = Dict()
        for key in key_list :
            if isinstance(key, tuple) :
                if len(key) not in (1, 2) :
                    raise Exception(f'非法{key_list=}')
                elif len(key) == 1 :
                    if self.has(key[0]) : result[deUnderscoure(key[0])] = self[key[0]]
                elif len(key) == 2 :
                    if self.has(key[0]) : result[deUnderscoure(key[0])] = self[key[0]]
                    else                : result[deUnderscoure(key[0])] = key[1]
            elif isinstance(key, str) :
                result[deUnderscoure(key)] = self[key]
            else : raise UserTypeError(key_list)
        return result

    def __setattr__(self, key, value) :
        '''
        Implement setattr(self, name, value).
        Sets the named attribute on the given object to the specified value.
        setattr(x, 'y', v) is equivalent to ``x.y = v
        '''
        '''IN PLACE'''
        self.__setitem__(key, value)
        return value

    def __setitem__(self, key, value) :
        '''Set self[key] to value.'''
        '''IN PLACE'''
        dict.__setitem__(self, key, self._wrapValue(value))
        return value

    # def setdefault(self) :
        '''
        D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D
        '''

    def set(self, key_list, value, /) :
        '''IN PLACE'''
        self._importTypes()
        if isinstance(key_list, (type(None), str, bytes, int, float, bool, tuple, range, zip, self._datetime, type)) :
            self[key_list] = value
        elif isinstance(key_list, list) :
            if len(key_list) == 0 :
                raise Exception(f'非法{key_list=}')
            now = self
            for index, key in enumerate(key_list) :
                if key in now :
                    now = now[key]
                else :
                    if index < len(key_list) - 1 :
                        now[key] = Dict()
                        now      = now[key]
                    else :
                        now[key] = value
        else :
            raise UserTypeError(key_list)
        return self

    def setted(self, key_list, value, /) :
        '''NOT IN PLACE'''
        return self.copy().set(key_list, value)

    # @ensureArgsType
    def update(self, mapping: dict, /, **kwargs) :
        '''
        D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.
        If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]
        If E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v
        In either case, this is followed by: for k in F:  D[k] = F[k]
        '''
        '''IN PLACE'''
        if isinstance(mapping, dict) :
            dict.update(self, Dict(mapping))
        elif isinstance(mapping, Dict) :
            dict.update(self, mapping)
        else : raise UserTypeError(mapping)
        if len(kwargs) > 0 : dict.update(self, Dict(kwargs))
        return self

    def updated(self, mapping, /, **kwargs) :
        '''NOT IN PLACE'''
        return self.copy().update(mapping, **kwargs)

    def __iadd__(self, mapping) :
        '''IN PLACE'''
        return self.update(mapping)

    def __add__(self, mapping) :
        '''NOT IN PLACE'''
        return self.updated(mapping)

    def popKey(self, key_list, /, default = 'NONE') :
        '''
        D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
        If key is not found, d is returned if given, otherwise KeyError is raised
        '''
        '''IN PLACE'''
        self._importTypes()
        if isinstance(key_list, (type(None), str, bytes, int, float, bool, tuple, range, zip, self._datetime, type)) :
            if default == 'NONE' :
                return dict.pop(self, key_list)
            else :
                return dict.pop(self, key_list, self._wrapValue(default))
        elif isinstance(key_list, list) :
            if self.hasNot(key_list) :
                if default == 'NONE' :
                    raise KeyError(key_list)
                else :
                    return self._wrapValue(default)
            else :
                now = self
                for key in key_list[ : -1] :
                    now = now[key]
                if default == 'NONE' :
                    return dict.pop(now, key_list[-1])
                else :
                    return dict.pop(now, key_list[-1], self._wrapValue(default))
        else :
            raise UserTypeError(key_list)

    def poppedKey(self, key_list, /, default = 'NONE') :
        '''NOT IN PLACE'''
        return self.copy().popKey(key_list, default = default)

    def dropKey(self, key_list, /, default = 'NONE') :
        '''IN PLACE'''
        self.popKey(key_list, default = None)
        return self

    def droppedKey(self, key_list, /, default = 'NONE') :
        '''NOT IN PLACE'''
        self.copy().dropKey(key_list, default = default)
        return self

    def popitem(self) :
        '''
        D.popitem() -> (k, v), remove and return some (key, value) pair as a
        2-tuple; but raise KeyError if D is empty.
        '''
        '''IN PLACE'''
        return dict.popitem(self)

    def _stripValue(self, value, string, /) :
        self._importTypes()
        if value is None or isinstance(value, (int, float, bool, range, bytes, zip, self._datetime, type)):
            return value
        elif isinstance(value, (self._List, self._Dict, self._Str)) : # can't be list, dict, str
            return value.strip(string)
        elif isinstance(value, tuple) :
            return (self._stripValue(_, string) for _ in value)
        elif isinstance(value, set) :
            return set([self._stripValue(_, string) for _ in value])
        elif isinstance(value, object) :
            if 'strip' in dir(value) : value.strip(string)
            return value
        else :
            raise UserTypeError(value)

    def strip(self, string = ' \t\n', /) :
        '''IN PLACE'''
        for key in self :
            self[key] = self._stripValue(self[key], string)
        return self

    def stripped(self, string = ' \t\n', /) :
        '''NOT IN PLACE'''
        return self.copy().strip(string)

    def forEach(self, func, /, *args, **kwargs) :
        '''NOT IN PLACE'''
        for key, value in self.items() :
            func(key, value, *args, **kwargs)
        return self

    def clear(self) :
        '''D.clear() -> None.  Remove all items from D.'''
        '''IN PLACE'''
        dict.clear(self)
        return self

    def writeToFile(self, file, /, *, indent = True) :
        file.writeString(self.j(indent = indent))
        return self

    # python2
    # '__class__', '__cmp__', '__contains__', '__delattr__', '__delitem__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'clear', 'copy', 'fromkeys', 'get', 'has_key', 'items', 'iteritems', 'iterkeys', 'itervalues', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values', 'viewitems', 'viewkeys', 'viewvalues'
    # 
    # python3
    # '__class__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'clear', 'copy', 'fromkeys', 'get', 'items', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values'

    # ===============================================================

    # def __class__(self) :
        '''
        dict() -> new empty dictionary
        dict(mapping) -> new dictionary initialized from a mapping object's
            (key, value) pairs
        dict(iterable) -> new dictionary initialized as if via:
            d = {}
            for k, v in iterable:
                d[k] = v
        dict(**kwargs) -> new dictionary initialized with the name=value pairs
            in the keyword argument list.  For example:  dict(one=1, two=2)
        '''

    # def __delattr__(self) :
        '''
        Implement delattr(self, name).

        Deletes the named attribute from the given object.

        delattr(x, 'y') is equivalent to ``del x.y''
        '''

    # def __delitem__(self) :
        '''
        Delete self[key].
        '''

    # def __dir__(self) :
        '''
        __dir__() -> list
        default dir() implementation
        '''

    # def __hash__(self) :
        '''
        None
        '''

    # def __init_subclass__(self) :
        '''
        This method is called when a class is subclassed.

        The default implementation does nothing. It may be
        overridden to extend subclasses.

        '''

    # def __new__(self) :
        '''
        Create and return a new object.  See help(type) for accurate signature.
        '''

    # def __reduce__(self) :
        '''
        helper for pickle
        '''

    # def __reduce_ex__(self) :
        '''
        helper for pickle
        '''

    # def __repr__(self) :
        '''
        Return repr(self).
        '''

    # def __sizeof__(self) :
        '''
        D.__sizeof__() -> size of D in memory, in bytes
        '''

    # def __subclasshook__(self) :
        '''
        Abstract classes can override this to customize issubclass().

        This is invoked early on by abc.ABCMeta.__subclasscheck__().
        It should return True, False or NotImplemented.  If it returns
        NotImplemented, the normal algorithm is used.  Otherwise, it
        overrides the normal algorithm (and the outcome is cached).

        '''
