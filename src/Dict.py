# -*- coding: utf-8 -*-  
from shared import *

class Dict(dict) :

    _has_imported_types = False
    NV = V_NON_VACANCY = 'V_NON_VACANCY'

    @classmethod
    def _importTypes(cls) :
        if cls._has_imported_types : return
        from Str      import Str;             cls._Str       = Str
        from DateTime import timedelta_class; cls._timedelta = timedelta_class
        from DateTime import TimeDelta;       cls._TimeDelta = TimeDelta
        from DateTime import date_class;      cls._date      = date_class
        from DateTime import Date;            cls._Date      = Date
        from DateTime import time_class;      cls._time      = time_class
        from DateTime import Time;            cls._Time      = Time
        from DateTime import datetime_class;  cls._datetime  = datetime_class
        from DateTime import DateTime;        cls._DateTime  = DateTime
        from DateTime import DateRange;       cls._DateRange = DateRange
        from List     import List;            cls._List      = List
        cls._Dict                                            = Dict
        from Object   import Object;          cls._Object    = Object
        from File     import File;            cls._File      = File
        from Folder   import Folder;          cls._Folder    = Folder
        cls._raw_types_tuple = (type(None), str, bytes, int, float, bool, tuple, range, zip, cls._timedelta, cls._date, cls._time, cls._datetime, type)
        cls._types_tuple     = (cls._Str, cls._TimeDelta, cls._Date, cls._Time, cls._DateTime, cls._DateRange, cls._List, cls._Dict, cls._Object, cls._File, cls._Folder)
        # 如果不赋值到self中，本装饰器无效，原因：locals() 只读, globals() 可读可写。https://www.jianshu.com/p/4510a9d68f3f
        cls._has_imported_types = True

    # @Timer.timeitTotal('_wrapValue')
    def _wrapValue(self, value, /) :
        self._importTypes()
        if isinstance(value, (self._Str, self._List, self._Dict)) : return value
        elif isinstance(value, str)                               : return self._Str(value)
        elif isinstance(value, bytes)                             : return self._Str(value.decode())
        elif isinstance(value, self._timedelta)                   : return self._TimeDelta(value)
        elif isinstance(value, self._date)                        : return self._Date(value)
        elif isinstance(value, self._time)                        : return self._Time(value)
        elif isinstance(value, self._datetime)                    : return self._DateTime(value)
        elif isinstance(value, list)                              : return self._List(value)
        elif isinstance(value, dict)                              : return self._Dict(value)
        elif isinstance(value, tuple)                             : return tuple([ self._wrapValue(_) for _ in value ])
        elif isinstance(value, set)                               : return set([ self._wrapValue(_) for _ in value ])
        else                                                      : return value

    # Initialize self.  See help(type(self)) for accurate signature.
    def __init__(self, *args, **kwargs) :
        if len(args) == 0   : dict.__init__(self, {})
        elif len(args) == 1 :
            if isinstance(args[0], Dict)                   : dict.__init__(self, args[0]._getData())
            elif isinstance(args[0], dict)                 :
                for key in args[0] : dict.__setitem__(self, key, self._wrapValue(args[0][key]))
            elif isinstance(args[0], (zip, GeneratorType)) : self.__init__(dict(args[0]))
            else                                           : raise UserTypeError(args)
        else                : raise UserTypeError(args)
        if len(kwargs) > 0  : dict.update(self, Dict(kwargs))

    # Returns a new dict with keys from iterable and values equal to value.
    # IN PLACE
    def fromkeys(self, key_list: list, value = None, /) :
        if isinstance(value, list) :
            if len(value) == len(key_list) : self.__init__(zip(key_list, value)); return self
            else                           : raise Exception(f'key_list 和 value 长度不匹配\n{key_list=}\n{value=}')
        else                       : self.__init__(zip(key_list, [value] * len(key_list))); return self

    # D.copy() -> a shallow copy of D
    def copy(self) : return Dict(self)

    # id(object) -> integer
    # Return the identity of an object.  This is guaranteed to be unique among
    # simultaneously existing objects.  (Hint: it's the object's memory address.)
    def getId(self) -> int : return hex(id(self))

    # 去除最外层封装，用于原生对象初始化：list/dict.__init__()/.update()
    def _getData(self) -> dict : return { key : self[key] for key in self }

    # 原生化 list, dict, str, Object._data, timedelta, date, time, datetime
    # NOT IN PLACE
    # else 可能是 int, float, bool, tuple, set, range, zip, object，不可能是 list. dict, str, bytes, timedelta, date, time, datetime
    def getRaw(self) -> dict : self._importTypes(); return { key : self[key].getRaw() if isinstance(self[key], self._types_tuple) else self[key] for key in self }

    @print_func
    def printLen(self) : return f'{self.len()}个键值', False

    @print_func
    def printLine(self) : return self.keys().mapped(lambda key, index : f'{index + 1} {key}: {self[key]}').join('\n'), True

    # default object formatter
    def __format__(self, code) :
        return "{{{}}}".format(
            self.keys()
                .map(lambda key : '{} : {}'.format(
                        '"{}"'.format(key) if isinstance(key, (str, bytes)) else '{}'.format(key),
                        '"{}"'.format(self[key]) if isinstance(self[key], (str, bytes)) else '{}'.format(self[key])
                    )
                ).join(', ')
        )

    @print_func
    def printFormat(self) : return self.keys().mapped(lambda key : f'{key}: {self[key]}').join('\n'), True

    # Return str(self).
    def __str__(self) :
        return 'Dict{{{}}}'.format(
            self.keys()
                .map(lambda key : '{} : {}'.format(
                        '"{}"'.format(key) if isinstance(key, (str, bytes)) else str(key),
                        '"{}"'.format(self[key]) if isinstance(self[key], (str, bytes)) else str(self[key])
                    )
                ).join(', ')
        )

    @print_func
    def printStr(self) : return self.keys().mapped(lambda key : f'{str(key)}: {str(self[key])}').join('\n'), True

    # NOT IN PLACE
    # else 可能是 int, float, bool, tuple, set, range, zip, object，不可能是 list. dict, str, bytes, timedelta, date, time, datetime
    def jsonSerialize(self) :
        self._importTypes()
        return { json_serialize(key) : (self[key].jsonSerialize() if isinstance(self[key], self._types_tuple) else json_serialize(self[key])) for key in self }

    # 可读化
    # NOT IN PLACE
    def j(self, *, indent = True) : return j(self.jsonSerialize(), indent = 4 if indent else None)

    @print_func
    def printJ(self) : return f'{self.j()}', True

    # 带有业务逻辑，与 j 不同
    # NOT IN PLACE
    def json(self) : return Dict((key, self[key].json()) if 'json' in dir(self[key]) else (key, self[key]) for key in self)

    @print_func
    def printJson(self) : return f'{self.json().j()}', False

    def inspect(self, **kwargs) : from Inspect import Inspect; return Inspect(self, **kwargs)

    # other: Union[dict, Dict]
    def diff(self, other) : from Inspect import Diff; return Diff(self, other)

    def isList(self) : return False

    def isDict(self) : return True

    # Return self==value.
    def __eq__(self, other) :
        if not isinstance(other, Dict) or self.len() != other.len() : return False
        return self.j() == other.j()

    # Return self!=value.
    def __ne__(self, other) : return not self.__eq__(other)

    # Return self>=value.
    def __ge__(self, other) : raise NotImplementedError

    # Return self>value.
    def __gt__(self, other) : raise NotImplementedError

    # Return self<=value.
    def __le__(self, other) : raise NotImplementedError

    # Return self<value.
    def __lt__(self, other) : raise NotImplementedError

    # Return len(self).
    def __len__(self) : return dict.__len__(self)

    def len(self) : return dict.__len__(self)

    def isEmpty(self) : return self.len() == 0

    def isNotEmpty(self) : return not self.isEmpty()

    # D.__contains__(k) -> True if D has a key k, else False.
    def __contains__(self, key, /) : return dict.__contains__(self, key)

    def has(self, key_list, /) :
        self._importTypes()
        if isinstance(key_list, self._raw_types_tuple) : return dict.__contains__(self, key_list)
        elif isinstance(key_list, list)                :
            if len(key_list) == 0 : raise Exception(f'非法{key_list=}')
            now = self
            for key in key_list :
                if not dict.__contains__(now, key) : return False
                now = now[key]
            return True
        else                                           : raise UserTypeError(key_list)

    def hasNo(self, key_list, /) : return not self.has(key_list)

    def hasAnyOf(self, key_list_list, /) : return any(self.has(key_list) for key_list in key_list_list)

    def hasAllOf(self, key_list_list, /) : return all(self.has(key_list) for key_list in key_list_list)

    def hasNoneOf(self, key_list_list, /) : return all(self.hasNo(key_list) for key_list in key_list_list)

    # D.keys() -> a set-like object providing a view on D's keys
    def keys(self) : self._importTypes(); return self._List(list(dict.keys(self)))
    
    # D.values() -> an object providing a view on D's values
    def values(self) : self._importTypes(); return self._List(list(dict.values(self)))

    # D.items() -> a set-like object providing a view on D's items
    def items(self) : self._importTypes(); return self._List(list(dict.items(self)))

    # Implement iter(self).
    # iter(iterable) -> iterator
    # iter(callable, sentinel) -> iterator
    # Get an iterator from an object.  In the first form, the argument must
    # supply its own iterator, or be a sequence.
    # In the second form, the callable is called until it returns the sentinel.
    def __iter__(self) : self._importTypes(); return self.keys().iter()

    def iter(self) : return self.__iter__()

    # Return getattr(self, name).
    # def __getattribute__(self, key) :
        # if key in ('List', 'Dict', 'Str', 'Object') : print(f'__getattribute__ {key=}')
        # return dict.__getattribute__(self, key)

    # D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None.
    def get(self, key_list, /, default = None) :
        self._importTypes()
        if isinstance(key_list, self._raw_types_tuple) :
            if default == self.NV and not dict.__contains__(self, key_list) : raise Exception(f'键 {key_list} 不能为空\n{self.keys()=}')
            return dict.get(self, key_list, self._wrapValue(default))
        elif isinstance(key_list, list)                :
            if self.hasNo(key_list) :
                if default == self.NV : raise Exception(f'键 {key_list} 不能为空\n{self=}')
                return self._wrapValue(default)
            else                    :
                now = self
                for key in key_list : now = now[key]
                return now
        else                                           : raise UserTypeError(key_list)

    # x.__getitem__(y) <==> x[y]
    def __getitem__(self, key) : return self.get(key, self.NV)

    # getattr(object, name[, default]) -> value
    # Get a named attribute from an object; getattr(x, 'y') is equivalent to x.y.
    # When a default argument is given, it is returned when the attribute doesn't
    # exist; without it, an exception is raised in that case.
    def __getattr__(self, key) : return self.__getitem__(key)
        # if key in ('List', 'Dict', 'Str', 'Object') : print(f'__getattr__ {key=}')

    # operator.attrgetter(*attrs)
    # [ (key1,), (key2, None), key3 ]
    def getMulti(self, key_list: list, /, *, de_underscore: bool = False) :
        def deUnderscoure(key: str) :
            if de_underscore and key[0] == '_' : return key[1:]
            else                               : return key
        result = Dict()
        for key in key_list :
            if isinstance(key, tuple) :
                if len(key) not in (1, 2) : raise Exception(f'非法{key_list=}')
                elif len(key) == 1        :
                    if self.has(key[0]) : result[deUnderscoure(key[0])] = self[key[0]]
                elif len(key) == 2        :
                    if self.has(key[0]) : result[deUnderscoure(key[0])] = self[key[0]]
                    else                : result[deUnderscoure(key[0])] = key[1]
            elif isinstance(key, str) :
                result[deUnderscoure(key)] = self[key]
            else                      : raise UserTypeError(key_list)
        return result

    # Set self[key] to value.
    # IN PLACE
    def __setitem__(self, key, value) : dict.__setitem__(self, key, self._wrapValue(value)); return value

    # Implement setattr(self, name, value).
    # Sets the named attribute on the given object to the specified value.
    # setattr(x, 'y', v) is equivalent to ``x.y = v
    # IN PLACE
    def __setattr__(self, key, value) : return self.__setitem__(key, value)

    # D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D
    # def setdefault(self) :

    # IN PLACE
    def set(self, key_list, value, /) :
        self._importTypes()
        if isinstance(key_list, self._raw_types_tuple) : self[key_list] = value
        elif isinstance(key_list, list)                :
            if len(key_list) == 0 : raise Exception(f'非法{key_list=}')
            now = self
            for index, key in enumerate(key_list) :
                if key in now : now = now[key]
                else          :
                    if index < len(key_list) - 1 : now[key] = Dict(); now = now[key]
                    else                         : now[key] = value
        else                                           : raise UserTypeError(key_list)
        return self

    # NOT IN PLACE
    def setted(self, key_list, value, /) : return self.copy().set(key_list, value)

    # D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.
    # If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]
    # If E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v
    # In either case, this is followed by: for k in F:  D[k] = F[k]
    # IN PLACE
    def update(self, mapping: dict, /, **kwargs) :
        if isinstance(mapping, dict)   : dict.update(self, Dict(mapping))
        elif isinstance(mapping, Dict) : dict.update(self, mapping)
        else                           : raise UserTypeError(mapping)
        if len(kwargs) > 0             : dict.update(self, Dict(kwargs))
        return self

    # NOT IN PLACE
    def updated(self, mapping: dict, /, **kwargs) : return self.copy().update(mapping, **kwargs)

    # IN PLACE
    def __iadd__(self, mapping: dict) : return self.update(mapping)

    # NOT IN PLACE
    def __add__(self, mapping: dict) : return self.updated(mapping)

    # Delete self[key].
    # IN PLACE
    def __delitem__(self, key) : dict.__delitem__(self, key); return self

    # Implement delattr(self, name).
    # Deletes the named attribute from the given object.
    # delattr(x, 'y') is equivalent to ``del x.y''
    # IN PLACE
    def __delattr__(self, key) : return self.__delitem__(key)

    # D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
    # If key is not found, d is returned if given, otherwise KeyError is raised
    # IN PLACE
    def popKey(self, key_list, /, default = NV) :
        self._importTypes()
        if isinstance(key_list, self._raw_types_tuple) :
            if default == self.NV : return dict.pop(self, key_list)
            else                  : return dict.pop(self, key_list, self._wrapValue(default))
        elif isinstance(key_list, list)                :
            if self.hasNo(key_list) :
                if default == self.NV : raise KeyError(key_list)
                else                  : return self._wrapValue(default)
            else                    :
                now = self
                for key in key_list[ : -1] : now = now[key]
                if default == self.NV : return dict.pop(now, key_list[-1])
                else                  : return dict.pop(now, key_list[-1], self._wrapValue(default))
        else                                           : raise UserTypeError(key_list)

    # NOT IN PLACE
    def poppedKey(self, key_list, /, default = NV) : return self.copy().popKey(key_list, default)

    # IN PLACE
    def dropKey(self, key_list, /, default = NV) : self.popKey(key_list, None); return self

    # NOT IN PLACE
    def droppedKey(self, key_list, /, default = NV) : self.copy().dropKey(key_list, default); return self

    # D.popitem() -> (k, v), remove and return some (key, value) pair as a
    # 2-tuple; but raise KeyError if D is empty.
    # IN PLACE
    def popitem(self) : return dict.popitem(self)

    def _stripValue(self, value, string, /) :
        self._importTypes()
        if isinstance(value, (self._List, self._Dict, self._Str)) : return value.strip(string) # can't be list, dict, str
        elif isinstance(value, tuple)                             : return (self._stripValue(_, string) for _ in value)
        elif isinstance(value, set)                               : return set([self._stripValue(_, string) for _ in value])
        elif isinstance(value, object)                            :
            if 'strip' in dir(value) : value.strip(string)
            return value
        elif isinstance(value, self._raw_types_tuple)             : return value
        else                                                      : raise UserTypeError(value)

    # IN PLACE
    def strip(self, string = ' \t\n', /) :
        for key in self : self[key] = self._stripValue(self[key], string)
        return self

    # NOT IN PLACE
    def stripped(self, string = ' \t\n', /) : return self.copy().strip(string)

    # NOT IN PLACE
    def forEach(self, func, /, *args, **kwargs) :
        for key, value in self.items() : func(key, value, *args, **kwargs)
        return self

    # D.clear() -> None.  Remove all items from D.
    # IN PLACE
    def clear(self) : dict.clear(self); return self

    def writeToFile(self, file, /, *, indent = True) : file.writeData(self, indent = indent); return self

    # python2
    # '__class__', '__cmp__', '__contains__', '__delattr__', '__delitem__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'clear', 'copy', 'fromkeys', 'get', 'has_key', 'items', 'iteritems', 'iterkeys', 'itervalues', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values', 'viewitems', 'viewkeys', 'viewvalues'
    # 
    # python3
    # '__class__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'clear', 'copy', 'fromkeys', 'get', 'items', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values'

    # ===============================================================

    # dict() -> new empty dictionary
    # dict(mapping) -> new dictionary initialized from a mapping object's
    #     (key, value) pairs
    # dict(iterable) -> new dictionary initialized as if via:
    #     d = {}
    #     for k, v in iterable:
    #         d[k] = v
    # dict(**kwargs) -> new dictionary initialized with the name=value pairs
    #     in the keyword argument list.  For example:  dict(one=1, two=2)
    # def __class__(self) :

    # __dir__() -> list
    # default dir() implementation
    # def __dir__(self) :

    # None
    # def __hash__(self) :

    # This method is called when a class is subclassed.
    # The default implementation does nothing. It may be
    # overridden to extend subclasses.
    # def __init_subclass__(self) :

    # Create and return a new object.  See help(type) for accurate signature.
    # def __new__(self) :

    # helper for pickle
    # def __reduce__(self) :

    # helper for pickle
    # def __reduce_ex__(self) :

    # Return repr(self).
    # def __repr__(self) :

    # D.__sizeof__() -> size of D in memory, in bytes
    # def __sizeof__(self) :

    # Abstract classes can override this to customize issubclass().
    # This is invoked early on by abc.ABCMeta.__subclasscheck__().
    # It should return True, False or NotImplemented.  If it returns
    # NotImplemented, the normal algorithm is used.  Otherwise, it
    # overrides the normal algorithm (and the outcome is cached).
    # def __subclasshook__(self) :

if __name__ == '__main__':
    # print(hasattr(Dict({'a':'b',3:4}), 'getMulti'))
    # print(getattr(Dict({'a':'b',3:4}), 'getMulti'))
    # print(Dict({'a':'b',3:4}).getMulti)
    # # print(Dict({'a':'b',3:4}).__getattr__('getMulti'))
    # print(Dict({'a':'b',3:4}).__getattribute__('getMulti'))
    a = {'b' : [1,2,3]}
    # b = a['b']
    d = Dict(a)
    d.b.append(4)
    print(a)
    print(d)

    a = {'b' : [1,2,3]}
    e = dict(a)
    e['b'].append(4)
    print(a)
    print(e)

    print(Dict)
    print(type(Dict()) is Dict)