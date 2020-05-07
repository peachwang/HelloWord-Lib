# -*- coding: utf-8 -*-  
from ..shared import *

@add_print_func
class Dict(dict) :

    _has_imported_types = False
    _no_value           = object()

    @classmethod
    def _import_types(cls) :
        if cls._has_imported_types : return
        from .ObjectId import ObjectId;        cls._ObjectId  = ObjectId
        from .Str      import Str;             cls._Str       = Str
        from .DateTime import timedelta_class; cls._timedelta = timedelta_class
        from .DateTime import TimeDelta;       cls._TimeDelta = TimeDelta
        from .DateTime import date_class;      cls._date      = date_class
        from .DateTime import Date;            cls._Date      = Date
        from .DateTime import time_class;      cls._time      = time_class
        from .DateTime import Time;            cls._Time      = Time
        from .DateTime import datetime_class;  cls._datetime  = datetime_class
        from .DateTime import DateTime;        cls._DateTime  = DateTime
        from .DateTime import DateList;        cls._DateList  = DateList
        from .DateTime import DateRange;       cls._DateRange = DateRange
        from .DateTime import Year;            cls._Year      = Year
        from .DateTime import Month;           cls._Month     = Month
        from .DateTime import Week;            cls._Week      = Week
        from .List     import List;            cls._List      = List
        cls._Dict                                             = Dict
        from .Object   import Object;          cls._Object    = Object
        from .File     import File;            cls._File      = File
        from .Folder   import Folder;          cls._Folder    = Folder
        cls._raw_type_tuple = (type(None), str, bytes, int, float, bool, tuple, range, zip, cls._timedelta, cls._date, cls._time, cls._datetime, type)
        cls._type_tuple     = (cls._ObjectId, cls._Str, cls._TimeDelta, cls._Date, cls._Time, cls._DateTime, cls._DateList, cls._DateRange, cls._Year, cls._Month, cls._Week, cls._List, cls._Dict, cls._Object, cls._File, cls._Folder)
        # 如果不赋值到self中，本装饰器无效，原因：locals() 只读, globals() 可读可写。https://www.jianshu.com/p/4510a9d68f3f
        cls._has_imported_types = True

    # @Timer.timeit_total('_wrap_value')
    @classmethod
    def _wrap_value(cls, value, /) :
        if isinstance(value, (cls._ObjectId, cls._Str, cls._List, cls._Dict)) : return value
        elif isinstance(value, str)                                           : return cls._Str(value)
        elif isinstance(value, dict)                                          : return cls._Dict(value)
        elif isinstance(value, list)                                          : return cls._List(value)
        elif isinstance(value, tuple)                                         : return tuple([ cls._wrap_value(_) for _ in value ])
        elif isinstance(value, cls._timedelta)                                : return cls._TimeDelta(value)
        elif isinstance(value, cls._date)                                     : return cls._Date(value)
        elif isinstance(value, cls._time)                                     : return cls._Time(value)
        elif isinstance(value, cls._datetime)                                 : return cls._DateTime(value)
        elif isinstance(value, set)                                           : return set([ cls._wrap_value(_) for _ in value ])
        else                                                                  : return value

    @staticmethod
    def _wrap_str(_, func) : return '"{}"'.format(_) if isinstance(_, str) else func(_)
    
    @staticmethod
    def _wrap_str_or_type(_, func) : return '"{}"'.format(_) if isinstance(_, str) else (str(_).split("'")[1] if isinstance(_, type) else func(_))

    # Create and return a new object.  See help(type) for accurate signature.
    # def __new__(self) :

    # Initialize self.  See help(type(self)) for accurate signature.
    # dict() -> new empty dictionary
    # dict(mapping) -> new dictionary initialized from a mapping object's (key, value) pairs
    # dict(iterable) -> new dictionary initialized as if via:
    #     d = {}
    #     for k, v in iterable:
    #         d[k] = v
    # dict(**kwargs) -> new dictionary initialized with the name=value pairs in the keyword argument list.  For example:  dict(one=1, two=2)
    def __init__(self, *args, **kwargs) :
        self._import_types()
        if len(args) == 0   : dict.__init__(self, {})
        elif len(args) == 1 :
            if isinstance(args[0], Dict)       : dict.__init__(self, args[0]._get_data())
            elif isinstance(args[0], dict)     :
                for key in args[0] :
                    dict.__setitem__(
                        self,
                        eval(key) if isinstance(key, str) and key[ : 2] == "b'" and key[-1] == "'" else key,
                        self._wrap_value(args[0][key])
                    )
            elif isinstance(args[0], Iterable) : self.__init__(dict(args[0]))
            else                               : raise CustomTypeError(args)
        else                : raise CustomTypeError(args)
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
    # Return the identity of an object.  This is guaranteed to be unique among simultaneously existing objects.  (Hint: it's the object's memory address.)
    def get_id(self) -> int : return hex(id(self))

    # 去除最外层封装，用于原生对象初始化：list/dict.__init__()/.update()
    def _get_data(self) -> dict : return { key : self[key] for key in self }

    # 原生化 list, dict, str, Object._data, timedelta, date, time, datetime
    # NOT IN PLACE
    def get_raw(self) -> dict : return { key : self[key].get_raw() if hasattr(self[key], 'get_raw') else self[key] for key in self }

    json_serialize = _get_data

    @print_func
    def print_len(self) : return f'{self.len()}个键值', False

    @print_func
    def print_line(self) : return self.keys().mapped(lambda key, index : f'{index + 1} {Dict._wrap_str(key, format)}: {Dict._wrap_str(self[key], format)}').join('\n'), True

    # default object formatter
    def __format__(self, spec) : return "{{ {} }}".format(self.keys().map(lambda key : '{} : {}'.format(Dict._wrap_str(key, format), Dict._wrap_str(self[key], format))).join(', '), spec)

    @print_func
    def print_format(self) : return self.keys().mapped(lambda key : f'{Dict._wrap_str(key, format)}: {Dict._wrap_str(self[key], format)}').join('\n'), True

    # Return str(self).
    def __str__(self) : return 'Dict{{ {} }}'.format(self.keys().map(lambda key : '{} : {}'.format(Dict._wrap_str(key, str), Dict._wrap_str(self[key], str))).join(', '))

    @print_func
    def print_str(self) : return self.keys().mapped(lambda key : f'{Dict._wrap_str(key, str)}: {Dict._wrap_str(self[key], str)}').join('\n'), True

    # Return repr(self).
    def __repr__(self) : return 'Dict({{ {} }})'.format(self.keys().map(lambda key : '{} : {}'.format(Dict._wrap_str_or_type(key, repr), Dict._wrap_str_or_type(self[key], repr))).join(', '))

    @print_func
    def print_j(self) : return self.j(), True

    # 带有业务逻辑，与 j 不同
    # NOT IN PLACE
    def json(self) : return Dict((key, self[key].json()) if hasattr(self[key], 'json') else (key, self[key]) for key in self)

    @print_func
    def print_json(self) : return f'{self.json().j()}', False

    def inspect(self, **kwargs) : from ..app.Inspect import Inspect; return Inspect(self, **kwargs)

    # other: Union[dict, Dict]
    def diff(self, other) : from ..app.Inspect import Diff; return Diff(self, other)

    def is_list(self) : return False

    def is_dict(self) : return True

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

    def is_empty(self) : return self.len() == 0

    def is_not_empty(self) : return not self.is_empty()

    # D.__contains__(k) -> True if D has a key k, else False.
    def __contains__(self, key, /) : return dict.__contains__(self, key)

    def has(self, key_list, /) :
        if isinstance(key_list, self._raw_type_tuple)  : return dict.__contains__(self, key_list)
        elif isinstance(key_list, list)                :
            if len(key_list) == 0 : raise Exception(f'非法{key_list=}')
            now = self
            for key in key_list :
                if not dict.__contains__(now, key) : return False
                now = now[key]
            return True
        else                                           : raise CustomTypeError(key_list)

    def has_no(self, key_list, /) : return not self.has(key_list)

    def has_any_of(self, key_list_list, /) : return any(self.has(key_list) for key_list in key_list_list)

    def has_all_of(self, key_list_list, /) : return all(self.has(key_list) for key_list in key_list_list)

    def has_none_of(self, key_list_list, /) : return all(self.has_no(key_list) for key_list in key_list_list)

    # D.keys() -> a set-like object providing a view on D's keys
    def keys(self) : return self._List(list(dict.keys(self)))
    
    # D.values() -> an object providing a view on D's values
    def values(self) : return self._List(list(dict.values(self)))

    # D.items() -> a set-like object providing a view on D's items
    def items(self) : return self._List(list(dict.items(self)))

    # Implement iter(self).
    # iter(iterable) -> iterator
    # iter(callable, sentinel) -> iterator
    # Get an iterator from an object.  In the first form, the argument must supply its own iterator, or be a sequence.
    # In the second form, the callable is called until it returns the sentinel.
    def __iter__(self) : return self.keys().iter()

    def iter(self) : return self.__iter__()

    # Return getattr(self, name).
    # def __getattribute__(self, key) :
        # if key in ('List', 'Dict', 'Str', 'Object') : print(f'__getattribute__ {key=}')
        # return dict.__getattribute__(self, key)

    # D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None.
    def get(self, key_list, /, default = None) :
        if isinstance(key_list, self._raw_type_tuple)  :
            if default == self._no_value and not dict.__contains__(self, key_list) : raise Exception(f'键 {key_list} 不能为空\n{self.keys()=}')
            return dict.get(self, key_list, self._wrap_value(default))
        elif isinstance(key_list, list)                :
            if self.has_no(key_list) :
                if default == self._no_value : raise Exception(f'键 {key_list} 不能为空\n{self=}')
                return self._wrap_value(default)
            else                     :
                now = self
                for key in key_list : now = now[key]
                return now
        else                                           : raise CustomTypeError(key_list)

    # D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D
    def get_with_default_set(self, key, /, default = None) : return dict.setdefault(self, key, self._wrap_value(default))

    # x.__getitem__(y) <==> x[y]
    def __getitem__(self, key) : return self.get(key, self._no_value)

    # getattr(object, name[, default]) -> value
    # Get a named attribute from an object; getattr(x, 'y') is equivalent to x.y.
    # When a default argument is given, it is returned when the attribute doesn't exist; without it, an exception is raised in that case.
    def __getattr__(self, key) : return self.__getitem__(key)

    # operator.attrgetter(*attrs)
    # [ (key1,), (key2, None), key3 ]
    def get_multi(self, key_list: list, /, *, de_underscore: bool = False) :
        def de_underscoure(key: str) :
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
            else                      : raise CustomTypeError(key_list)
        return result

    # Set self[key] to value.
    # IN PLACE
    def __setitem__(self, key, value) : dict.__setitem__(self, key, self._wrap_value(value)); return value

    # Implement setattr(self, name, value).
    # Sets the named attribute on the given object to the specified value.
    # setattr(x, 'y', v) is equivalent to ``x.y = v
    # IN PLACE
    def __setattr__(self, key, value) : return self.__setitem__(key, value)

    # IN PLACE
    def set(self, key_list, value, /) :
        if isinstance(key_list, self._raw_type_tuple)  : self[key_list] = value
        elif isinstance(key_list, list)                :
            if len(key_list) == 0 : raise Exception(f'非法{key_list=}')
            now = self
            for index, key in enumerate(key_list) :
                if key in now : now = now[key]
                else          :
                    if index < len(key_list) - 1 : now[key] = Dict(); now = now[key]
                    else                         : now[key] = value
        else                                           : raise CustomTypeError(key_list)
        return self

    # NOT IN PLACE
    def setted(self, key_list, value, /) : return self.copy().set(key_list, value)

    # D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.
    # If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]
    # If E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v
    # In either case, this is followed by: for k in F:  D[k] = F[k]
    # IN PLACE
    def update(self, mapping: dict, /, **kwargs) :
        if isinstance(mapping, Dict)   : dict.update(self, mapping)
        elif isinstance(mapping, dict) : dict.update(self, Dict(mapping))
        else                           : raise CustomTypeError(mapping)
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
    def pop_key(self, key_list, /, default = _no_value) :
        if isinstance(key_list, self._raw_type_tuple)  :
            if default == self._no_value : return dict.pop(self, key_list)
            else                         : return dict.pop(self, key_list, self._wrap_value(default))
        elif isinstance(key_list, list)                :
            if self.has_no(key_list) :
                if default == self._no_value : raise KeyError(key_list)
                else                         : return self._wrap_value(default)
            else                    :
                now = self
                for key in key_list[ : -1] : now = now[key]
                if default == self._no_value : return dict.pop(now, key_list[-1])
                else                         : return dict.pop(now, key_list[-1], self._wrap_value(default))
        else                                           : raise CustomTypeError(key_list)

    # NOT IN PLACE
    def popped_key(self, key_list, /, default = _no_value) : return self.copy().pop_key(key_list, default)

    # IN PLACE
    def drop_key(self, key_list, /, default = _no_value) : self.pop_key(key_list, None); return self

    # NOT IN PLACE
    def dropped_key(self, key_list, /, default = _no_value) : self.copy().drop_key(key_list, default); return self

    # D.popitem() -> (k, v), remove and return some (key, value) pair as a 2-tuple; but raise KeyError if D is empty.
    # IN PLACE
    # def pop_item(self) : return dict.popitem(self)

    # NOT IN PLACE
    def for_each(self, func, /, *args, **kwargs) :
        for key, value in self.items() : func(key, value, *args, **kwargs)
        return self

    # D.clear() -> None.  Remove all items from D.
    # IN PLACE
    def clear(self) : dict.clear(self); return self

    def write_to_file(self, file, /, *, indent = True) : file.write_json(self, indent = indent); return self

if __name__ == '__main__':
    # print(hasattr(Dict({'a':'b',3:4}), 'get_multi'))
    # print(getattr(Dict({'a':'b',3:4}), 'get_multi'))
    # print(Dict({'a':'b',3:4}).get_multi)
    # # print(Dict({'a':'b',3:4}).__getattr__('get_multi'))
    # print(Dict({'a':'b',3:4}).__getattribute__('get_multi'))
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