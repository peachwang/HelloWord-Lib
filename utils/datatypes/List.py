# -*- coding: utf-8 -*-  
from ..shared import *

# ListDiff: 以 item 作为最小比较单元。降维后可用于StrDiff

class List(list, base_class) :

    _has_imported_types = False

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
        cls._List                                            = List
        from .Dict     import Dict;            cls._Dict      = Dict
        from .Object   import Object;          cls._Object    = Object
        from .File     import File;            cls._File      = File
        from .Folder   import Folder;          cls._Folder    = Folder
        cls._raw_type_tuple = (type(None), str, bytes, int, float, bool, tuple, range, zip, cls._timedelta, cls._date, cls._time, cls._datetime, type)
        cls._type_tuple     = (cls._ObjectId, cls._Str, cls._TimeDelta, cls._Date, cls._Time, cls._DateTime, cls._DateList, cls._DateRange, cls._Year, cls._Month, cls._Week, cls._List, cls._Dict, cls._Object, cls._File, cls._Folder)
        # 如果不赋值到self中，本装饰器无效，原因：locals() 只读, globals() 可读可写。https://www.jianshu.com/p/4510a9d68f3f
        cls._has_imported_types = True

    # @Timer.timeit_total('_wrap_item')
    def _wrap_item(self, item, /) :
        if isinstance(item, (self._ObjectId, self._Str, self._List, self._Dict)) : return item
        elif isinstance(item, str)                                               : return self._Str(item)
        elif isinstance(item, dict)                                              : return self._Dict(item)
        elif isinstance(item, list)                                              : return self._List(item)
        elif isinstance(item, tuple)                                             : return tuple([ self._wrap_item(_) for _ in item ])
        elif isinstance(item, self._timedelta)                                   : return self._TimeDelta(item)
        elif isinstance(item, self._date)                                        : return self._Date(item)
        elif isinstance(item, self._time)                                        : return self._Time(item)
        elif isinstance(item, self._datetime)                                    : return self._DateTime(item)
        elif isinstance(item, set)                                               : return set([ self._wrap_item(_) for _ in item ])
        else                                                                     : return item

    def _wrap_str(self, _, func) : return '"{}"'.format(_) if isinstance(_, str) else func(_)
    
    def _wrap_str_or_type(self, _, func) : return '"{}"'.format(_) if isinstance(_, str) else (str(_).split("'")[1] if isinstance(_, type) else func(_))

    # Initialize self.  See help(type(self)) for accurate signature.
    # list() -> new empty list
    # list(iterable) -> new list initialized from iterable's items
    # def __class__(self) :
    def __init__(self, *args) :
        self._import_types()
        if len(args) == 0   : super().__init__([])
        elif len(args) == 1 :
            if isinstance(args[0], List)       : super().__init__(args[0]._get_data())
            elif isinstance(args[0], list)     :
                for item in args[0] : super().append(self._wrap_item(item))
            elif (isinstance(args[0], (range, GeneratorType))
                or isgenerator(args[0])
                or '__next__' in dir(args[0])) : self.__init__(list(args[0]))
            else                               : self.__init__(list(args))
        else                : self.__init__(list(args))

    # L.copy() -> list -- a shallow copy of L
    def copy(self) : return List(self)

    # id(object) -> integer
    # Return the identity of an object.  This is guaranteed to be unique among
    # simultaneously existing objects.  (Hint: it's the object's memory address.)
    def get_id(self) -> int : return hex(id(self))

    # Implement iter(self).
    # iter(iterable) -> iterator
    # iter(callable, sentinel) -> iterator
    # Get an iterator from an object.  In the first form, the argument must
    # supply its own iterator, or be a sequence.
    # In the second form, the callable is called until it returns the sentinel.
    def iter(self) : return super().__iter__()
    
    # 去除最外层封装，用于原生对象初始化：list/dict.__init__()/.update()
    def _get_data(self) -> list : return [ item for item in self ]

    # 原生化 list, dict, str, Object._data, timedelta, date, time, datetime
    # NOT IN PLACE
    def get_raw(self) -> list : return [ item.get_raw() if 'get_raw' in dir(item) else item for item in self ]

    json_serialize = _get_data

    @print_func
    def print_len(self, msg = None) : return f"{'' if msg is None else f'{msg}: '}{self.len()}个元素", False

    @print_func
    def print_line(self, pattern = None, /) :
        if pattern is None : return self.mapped(lambda item, index : f'{index + 1} {self._wrap_str(item, format)}').join('\n'), True
        else               : return self.mapped(lambda item, index : pattern.format(self._wrap_str(item, format), index)).join('\n'), True

    # default object formatter
    # @log_entering()
    def __format__(self, spec) : return '[ {} ]'.format(self.mapped(lambda item : self._wrap_str(item, format)).join(', '), spec)

    @print_func
    def print_format(self, pattern = None, /) :
        if pattern is None : return self.mapped(lambda item : self._wrap_str(item, format)).join('\n'), True
        else               : return self.mapped(lambda item, index : pattern.format(self._wrap_str(item, format), index)).join('\n'), True

    # Return str(self).
    # @log_entering()
    def __str__(self) : return 'List[ {} ]'.format(self.mapped(lambda item : self._wrap_str(item, str)).join(', '))

    @print_func
    def print_str(self) : return self.mapped(lambda item : self._wrap_str(item, str)).join('\n'), True

    # Return repr(self).
    # @log_entering()
    def __repr__(self) : return 'List( {} )'.format(self.mapped(lambda item : self._wrap_str_or_type(item, repr)).join(', '))

    @print_func
    def print_j(self) : return self.j(), True

    # 带有业务逻辑，与 j 不同
    # NOT IN PLACE
    def json(self) : return List(item.json() if 'json' in dir(item) else item for item in self)

    @print_func
    def print_json(self) : return f'{self.json().j()}', False

    def inspect(self, **kwargs) : from ..app.Inspect import Inspect; return Inspect(self, **kwargs)

    # other: Union[list, List]
    def diff(self, other) : from ..app.Inspect import Diff; return Diff(self, other)

    def is_list(self) : return True

    def is_dict(self) : return False

    # Return self==value.
    def __eq__(self, other) :
        if not isinstance(other, List) or self.len() != other.len() : return False
        return self.j() == other.j()

    # Return self!=value.
    def __ne__(self, other) : return not self.__eq__(other)

    # Return len(self).
    def __len__(self) : return super().__len__()

    def len(self) : return super().__len__()

    def is_empty(self) : return self.len() == 0

    def is_not_empty(self) : return not self.is_empty()

    # x.__contains__(y) <==> y in x
    def __contains__(self, item, /) : return super().__contains__(item)

    def has(self, item, /) : return super().__contains__(item)

    def has_no(self, item, /) : return not self.has(item)

    def has_any_of(self, item_list, /) : return any(self.has(item) for item in item_list)

    def has_all_of(self, item_list, /) : return all(self.has(item) for item in item_list)

    def has_none_of(self, item_list, /) : return all(self.has_no(item) for item in item_list)

    # L.count(value) -> integer -- return number of occurrences of value
    def count(self, item, /) -> int : return super().count(item)

    # L.index(value, [start, [stop]]) -> integer -- return first index of value.
    # Raises ValueError if the value is not present.
    def left_index(self, item, /, *, start = 0) -> Optional[int] :
        try               : index = super().index(item, start)
        except ValueError : return None
        else              : return index

    # L.index(value, [start, [stop]]) -> integer -- return first index of value.
    # Raises ValueError if the value is not present.
    def right_index(self, item, /) -> Optional[int] :
        try               : index = self.reversed().left_index(item)
        except ValueError : return None
        else              : return self.len() - index - 1

    def unique_index(self, item, /) -> int :
        if self.count(item) == 0  : raise Exception(f'{self=}\n中值：\n{item=}\n不存在')
        elif self.count(item) > 1 : raise Exception(f'{self=}\n中值：\n{item=}\n不唯一')
        return super().index(item)

    # Return getattr(self, name).
    # def __getattribute__(self) :

    # getattr(object, name[, default]) -> value
    # Get a named attribute from an object; getattr(x, 'y') is equivalent to x.y.
    # When a default argument is given, it is returned when the attribute doesn't
    # exist; without it, an exception is raised in that case.
    '''NOT IN PLACE'''
    def __getattr__(self, key_or_func_name) : return self.value_list(key_or_func_name)
        # if self.len() == 0 :
        #     raise Exception('不能对空列表进行 __getattr__ 操作，请检查是否是希望对Dict进行操作！')

    def __call__(self) : raise Exception('请检查是否在批量调用List元素的方法获取结果List后，对结果List多加了()调用！')

    def get(self, index: int, /, default = None) :
        if not isinstance(index, int) : raise CustomTypeError(index)
        if abs(index) >= self.len()   : return default
        else                          : return self.__getitem__(index)

    # x.__getitem__(y) <==> x[y]
    # https://docs.python.org/3/library/collections.abc.html?highlight=__contains__#collections.abc.ByteString
    # Implementation note: Some of the mixin methods, such as __iter__(), __reversed__() and index(), make repeated calls to the underlying __getitem__() method. Consequently, if __getitem__() is implemented with constant access speed, the mixin methods will have linear performance; however, if the underlying method is linear (as it would be with a linked list), the mixins will have quadratic performance and will likely need to be overridden.
    def __getitem__(self, index: Union[int, slice], /) :
        if isinstance(index, int)     : return super().__getitem__(index)
        elif isinstance(index, slice) :
            if (index.start is None or isinstance(index.start, int)) and (index.stop is None or isinstance(index.stop, int)) :
                return List(super().__getitem__(index))
            else :
                start, end = None, None
                for idx, item in self.enum() :
                    if index.start is not None and start is None and index.start == item : start = idx
                    elif start is not None and index.start == item                       : raise Exception(f'\n{self=}\n中有重复的 [{index.start=}]: [{item}]')
                    if index.stop is not None and end is None and index.stop == item     : end = idx
                    elif end is not None and index.stop == item                          : raise Exception(f'\n{self=}\n中有重复的 [{index.stop=}]: [{item}]')
                if index.start is not None and start is None : raise Exception(f'\n{self=}\n中不存在 [{index.start=}]')
                if index.stop is not None and end is None    : raise Exception(f'\n{self=}\n中不存在 [{index.stop=}]')
                return self[start : end]
        # Str.to_range_tuple() -> ((None, e1), idx2, (s3, e3), (s4, None))
        elif isinstance(index, tuple) : raise NotImplementedError
        else                          : raise CustomTypeError(index)

    def get_unique_item(self, item, /) : return self[self.unique_index(item)] # 通常针对重载了 __eq__ 的情况

    # Implement setattr(self, name, value).
    # Sets the named attribute on the given object to the specified value.
    # setattr(x, 'y', v) is equivalent to ``x.y = v''
    # def __setattr__(self) :

    # Set self[index] to value.
    # IN PLACE
    def __setitem__(self, index, item) : super().__setitem__(index, self._wrap_item(item)); return item

    # IN PLACE
    def set(self, index, item, /) : self.__setitem__(index, item); return self

    # NOT IN PLACE
    def setted(self, index, item, /) : return self.copy().set(index, item)

    # L.append(object) -> None -- append object to end
    # IN PLACE
    def append(self, item, /) : super().append(self._wrap_item(item)); return self

    # NOT IN PLACE
    def appended(self, item, /) : return self.copy().append(item)

    # IN PLACE
    def unique_append(self, item, /) : return self if self.has(item) else self.append(item)

    # NOT IN PLACE
    def unique_appended(self, item, /) : return self.copy().unique_append(item)

    # L.prepend(object) -> None -- append object to start
    # IN PLACE
    def prepend(self, item, /) : return self.insert(0, item)

    # NOT IN PLACE
    def prepended(self, item, /) : return self.copy().prepend(item)

    # IN PLACE
    def unique_prepend(self, item, /) : return self if self.has(item) else self.prepend(item)

    # NOT IN PLACE
    def unique_prepended(self, item, /) : return self.copy().unique_prepend()

    # L.insert(index, object) -> None -- insert object before index
    # IN PLACE
    def insert(self, index, item, /) : super().insert(index, self._wrap_item(item)); return self

    # NOT IN PLACE
    def inserted(self, index, item, /) : return self.copy().insert(index, item)

    # Return self+value.
    # NOT IN PLACE
    # item_list: Union[list, List]
    def __add__(self, item_list) : return List(super().__add__(List(item_list)))

    # Implement self+=value.
    # IN PLACE
    # item_list: Union[list, List]
    def __iadd__(self, item_list) : return super().__iadd__(List(item_list))
    
    # L.extend(iterable) -> None -- extend list by appending elements from the iterable
    # IN PLACE
    def extend(self, item_list: Optional[list], /) :
        if (isinstance(item_list, (list, GeneratorType))
            or isgenerator(item_list)
            or '__next__' in dir(item_list)) : super().extend(List(item_list)); return self
        elif item_list is None               : return self
        else                                 : raise CustomTypeError(item_list)

    # NOT IN PLACE
    def extended(self, item_list, /) : return self.copy().extend(item_list)

    # Return self*value
    # NOT IN PLACE
    def __mul__(self, value: int) : return List(super().__mul__(value))
    
    # Return value*self.
    # NOT IN PLACE
    def __rmul__(self, value: int) : return List(super().__rmul__(value))

    # Implement self*=value.
    # IN PLACE
    def __imul__(self, value: int) : return super().__imul__(value)

    # Implement delattr(self, name).
    # Deletes the named attribute from the given object.
    # delattr(x, 'y') is equivalent to ``del x.y''
    # def __delattr__(self) :

    # Delete self[key].
    def __delitem__(self, key: Union[int, slice]) : return super().__delitem__(key)

    # L.pop([index]) -> item -- remove and return item at index (default last).
    # Raises IndexError if list is empty or index is out of range.
    # IN PLACE
    def pop_index(self, index, /) : return super().pop(index)

    # NOT IN PLACE
    def popped_index(self, index, /) : return self.copy().pop_index(index)

    # L.remove(value) -> None -- remove first occurrence of value.
    # Raises ValueError if the value is not present.
    # IN PLACE
    def drop_item(self, item, /) : super().remove(item); return self

    # NOT IN PLACE
    def dropped_item(self, item, /) : return self.copy().drop_item()
    
    # L.__reversed__() -- return a reverse iterator over the list
    def __reversed__(self) : return super().__reversed__()

    # L.reverse() -> None -- reverse *IN PLACE*
    # IN PLACE
    def reverse(self) : super().reverse(); return self

    # NOT IN PLACE
    def reversed(self) : return self.copy().reverse()

    # L.sort(key=None, reverse=False) -> None -- stable sort *IN PLACE*
    # IN PLACE
    def sort(self, key_func_or_attr_name = None, /, *, reverse = False) :
        if (callable(key_func_or_attr_name)
            or key_func_or_attr_name is None)       : super().sort(key = key_func_or_attr_name, reverse = reverse)
        elif isinstance(key_func_or_attr_name, str) : super().sort(key = lambda _ : _.__getattr__(key_func_or_attr_name), reverse = reverse)
        else                                        : raise CustomTypeError(key_func_or_attr_name)
        return self

    # NOT IN PLACE
    def sorted(self, key_func_or_attr_name = None, /, *, reverse = False) :
        return self.copy().sort(key_func_or_attr_name, reverse = reverse)

    # IN PLACE
    def shuffle(self) : import random; random.shuffle(self); return self

    # NOT IN PLACE
    def shuffled(self) : return self.copy().shuffle()

    def enumerate(self) : return enumerate(self)

    def enum(self) : return enumerate(self)

    # pos为index在func的参数表里的下标，即本函数在func的参数表的下标
    def _left_pad_index_to_args(self, func, args, index, pos, /) :
        if isclass(func)                                           : func = func.__init__; pos += 1
        func_args = list(signature(func).parameters.values())
        if len(func_args) > pos and func_args[pos].name == 'index' : return [ index ] + list(args)
        else                                                       : return args

    # NOT IN PLACE
    def for_each(self, func, /, *args, **kwargs) :
        for index, item in self.enum() :
            func(item, *(self._left_pad_index_to_args(func, args, index, 1)), **kwargs)
        return self

    # IN PLACE
    def batch(self, func_name_or_attr_name: str, /, *args, **kwargs) :
        for index, item in self.enum() :
            attribute = self[index].__getattribute__(func_name_or_attr_name)
            if callable(attribute) : self[index] = attribute(*(self._left_pad_index_to_args(attribute, args, index, 0)), **kwargs)
            else                   : self[index] = attribute
        return self

    # NOT IN PLACE
    def batched(self, func_name_or_attr_name, /, *args, **kwargs) : return self.copy().batch(func_name_or_attr_name, *args, **kwargs)

    # IN PLACE
    def map(self, func, /, *args, **kwargs) :
        for index, item in self.enum() :
            self[index] = func(item, *(self._left_pad_index_to_args(func, args, index, 1)), **kwargs)
        return self

    # NOT IN PLACE
    def mapped(self, func, /, *args, **kwargs) : return self.copy().map(func, *args, **kwargs)

    # @Timer.timeit_total('value_list')
    # NOT IN PLACE
    # 可以允许字段不存在
    def value_list(self, key_list_or_func_name: Union[list, str], /, *, default = None) :
        if self.len() == 0                          : return self.copy()
        if isinstance(key_list_or_func_name, list)  :
            if isinstance(self[0], self._Object) : return self.batched('_get', key_list_or_func_name)
            else                                 : return self.batched('get', key_list_or_func_name)
        elif isinstance(key_list_or_func_name, str) :
            def get_value(item) :
                try                        :
                    if key_list_or_func_name in dir(item) and callable(attribute := item.__getattribute__(key_list_or_func_name)) :
                        return attribute()
                except AttributeError as e : raise e
                except Exception as e      : raise e
                if isinstance(item, self._Dict)     : attribute = item.__getattr__(key_list_or_func_name) # 可以允许字段不存在
                elif isinstance(item, self._Object) :
                    try : attribute = item.__getattr__(key_list_or_func_name)
                    except Exception as e : attribute = self._wrap_item(default) # 可以允许字段不存在
                else                                :
                    try                   : attribute = item.__getattribute__(key_list_or_func_name)
                    except AttributeError :
                        raise Exception(f'{P()}{type(item)=}{E()} has no attribute {P(key_list_or_func_name)}; 请检查是否采用了错误的调用方式：xList.yList.z; {self=}; {item=}')
                    except Exception as e :
                        raise e
                return attribute
            return self.mapped(get_value)
        else                                        : raise CustomTypeError(key_list_or_func_name)

    # NOT IN PLACE
    def format(self, pattern, /) : return self.mapped(lambda _ : pattern.format(_))

    # IN PLACE
    def filter(self, func_or_func_name, /, *args, **kwargs) :
        index = 0
        while index < self.len() :
            if isinstance(func_or_func_name, str) :
                if self[index].__getattribute__(func_or_func_name)(*args, **kwargs) : index += 1
                else                                                                : self.pop_index(index)
            elif callable(func_or_func_name)      :
                if func_or_func_name(self[index], *args, **kwargs) : index += 1
                else                                               : self.pop_index(index)
            else                                  : raise CustomTypeError(func_or_func_name)
        return self

    # NOT IN PLACE
    def filtered(self, func_or_func_name, /, *args, **kwargs) : return self.copy().filter(func_or_func_name, *args, **kwargs)

    def filter_one(self, func_or_func_name, /, *args, **kwargs) :
        result = self.filtered(func_or_func_name, *args, **kwargs)
        if result.len() != 1 : raise CustomTypeError(result)
        else                 : return result[0]

    # IN PLACE
    def filter_by_value(self, key_list_or_func_name: Optional[Union[list, str]], value_or_list, /) :
        if not isinstance(value_or_list, list)       : value_or_list = [ value_or_list ]
        if key_list_or_func_name is None             : return self.filter(lambda item : item in value_or_list)
        elif isinstance(key_list_or_func_name, list) :
            if isinstance(self[0], self._Object) : return self.filter(lambda item : item._data.get(key_list_or_func_name) in value_or_list)
            else                                 : return self.filter(lambda item : item.get(key_list_or_func_name) in value_or_list)
        elif isinstance(key_list_or_func_name, str)  :
            def get_value(item) :
                if isinstance(item, self._Object) : attribute = item.__getattr__(key_list_or_func_name)
                else                              : attribute = item.__getattribute__(key_list_or_func_name)
                if callable(attribute)            : return attribute()
                else                              : return attribute
            return self.filter(lambda item : get_value(item) in value_or_list)
        else                                         : raise CustomTypeError(key_list_or_func_name)

    # NOT IN PLACE
    def filtered_by_value(self, key_list_or_func_name, value_or_list, /) : return self.copy().filter_by_value(key_list_or_func_name, value_or_list)

    # NOT IN PLACE
    def reduce(self, func, initial_value, /, *args, **kwargs) :
        result = initial_value
        for index, item in self.enum() :
            result = func(result, item, *(self._left_pad_index_to_args(func, args, index, 2)), **kwargs)
        return result

    # itertools.def accumulate(iterable, func=operator.add, *, initial=None):

    # Merge items of the items of self
    # IN PLACE
    def merge(self) : return self.clear().extend(self.reduce(lambda result, item : result.extend(item), List()))

    # NOT IN PLACE
    def merged(self) : return self.copy().merge()

    def group_by(self, key_func = None, /, *, value_func = None) :
        from itertools import groupby
        result = self._Dict()
        for k, g in groupby(self.sorted((lambda _ : f'{_}' if _ is not None else '') if key_func is None else key_func), key = key_func) :
            if value_func is None : result[k] = List(g)
            else                  : result[k] = List(value_func(item) for item in g)
        return result
    
    def count_by(self, key_func = None, /) : return self._Dict((k, g.len()) for k, g in self.group_by(key_func).items())

    # NOT IN PLACE
    def _reduce(self, key_list_or_func_name: Optional[Union[list, str]], func, initial_value, /) :
        if key_list_or_func_name is None                    : return self.reduce(func, initial_value)
        elif isinstance(key_list_or_func_name, (list, str)) : return self.value_list(key_list_or_func_name).reduce(func, initial_value)
        else                                                : raise CustomTypeError(key_list_or_func_name)

    # NOT IN PLACE
    def sum(self, key_list_or_func_name = None, /, *, default = 0) :
        if self.len() == 0 : return default
        return self._reduce(key_list_or_func_name, lambda result, item : item + result, 0)

    # NOT IN PLACE
    def ave(self, key_list_or_func_name = None, /, *, default = 0) :
        if self.len() == 0 : return default
        return 1.0 * self.sum(key_list_or_func_name) / self.len()

    # NOT IN PLACE
    def _initial_value(self, key_list_or_func_name: Optional[Union[list, str]], /) :
        if key_list_or_func_name is None             : return self[0]
        elif isinstance(key_list_or_func_name, list) :
            if isinstance(self[0], self._Object) : return self[0]._data.get(key_list_or_func_name)
            else                                 : return self[0].get(key_list_or_func_name)
        elif isinstance(key_list_or_func_name, str)  :
            if isinstance(self[0], self._Object) : attribute = self[0].__getattr__(key_list_or_func_name)
            else                                 : attribute = self[0].__getattribute__(key_list_or_func_name)
            if callable(attribute)               : return attribute()
            else                                 : return attribute
        else                                         : raise CustomTypeError(key_list_or_func_name)

    # NOT IN PLACE
    def max(self, key_list_or_func_name = None, /, *, default = 0) :
        if self.len() == 0 : return default
        return self._reduce(
            key_list_or_func_name,
            lambda result, item : item if item > result else result,
            self._initial_value(key_list_or_func_name)
        )

    # NOT IN PLACE
    def min(self, key_list_or_func_name = None, /, *, default = 0) :
        if self.len() == 0 : return default
        return self._reduce(
            key_list_or_func_name,
            lambda result, item : item if item < result else result,
            self._initial_value(key_list_or_func_name)
        )

    # NOT IN PLACE
    def join(self, sep: str = '', /) : return self._Str(sep).join(self)

    # IN PLACE
    # O(??)
    def unique(self) : return self.clear().extend(list(set(self)))

    # NOT IN PLACE
    def uniqued(self) : return self.copy().unique()

    @prop
    def duplicate_item_list(self) : return (self - self.uniqued()).unique()

    # Update itself with the intersection of itself and another.
    # IN PLACE
    # O(N^2)???
    def intersect(self, item_list: list, /) :
        if not isinstance(item_list, list) : raise CustomTypeError(item_list)
        return self.filter(lambda item, item_list : item in item_list, List(item_list))

    # NOT IN PLACE
    def intersected(self, item_list, /) : return self.copy().intersect(item_list)

    # x.__and__(y) <==> x&y
    # NOT IN PLACE
    def __and__(self, item_list) : return self.intersected(item_list)

    # Remove all elements of another list from this list.
    # IN PLACE
    # O(N^2)???
    def difference(self, item_list: list, /) :
        if not isinstance(item_list, list) : raise CustomTypeError(item_list)
        return self.filter(lambda item, item_list : item not in item_list, List(item_list))

    # NOT IN PLACE
    def differenced(self, item_list, /) : return self.copy().difference(item_list)

    # x.__sub__(y) <==> x-y
    # NOT IN PLACE
    def __sub__(self, item_list) : return self.differenced(item_list)

    # Update a set with the union of itself and others.
    # IN PLACE
    # O(N^2)???
    def union(self, item_list: list, /) :
        if not isinstance(item_list, list) : raise CustomTypeError(item_list)
        return self.extend(List(item_list).difference(self))

    # NOT IN PLACE
    def unioned(self, item_list, /) : return self.copy().union(item_list)

    # x.__or__(y) <==> x|y
    # NOT IN PLACE
    def __or__(self, item_list) : return self.unioned(item_list)

    # Return True if two lists have a null intersection.
    # O(N^2)???
    def is_disjoint_from(self, item_list, /) : return (self & item_list).len() == 0

    # Report whether another set contains this set.
    # O(N^2)???
    def is_subset_of(self, item_list, /) : return (self - item_list).len() == 0

    # Return self<=value.
    def __le__(self, other) : return self.is_subset_of(other)

    # Return self<value.
    def __lt__(self, other) : return self.len() < other.len() and self.__le__(other)

    # Report whether this set contains another set.
    # O(N^2)???
    def is_superset_of(self, item_list, /) : return (List(item_list) - self).len() == 0

    # Return self>=value.
    def __ge__(self, other) : return self.is_superset_of(other)

    # Return self>value.
    def __gt__(self, other) : return self.len() > other.len() and self.__ge__(other)

    def is_same_set_of(self, item_list, /) : return self <= item_list and self >= item_list

    # L.clear() -> None -- remove all items from L
    # IN PLACE
    def clear(self) : super().clear(); return self
    
    def write_to_file(self, file, /, *, indent = True) : file.write_data(self, indent = indent); return self

    def write_line_list_to_file(self, file, /) : file.write_line_list(self); return self

    # list(map(lambda x : print(f'\n{x}\n{list.__getattribute__([], x).__doc__}\n'), dir(list)))

    # python2
    # '__add__', '__class__', '__contains__', '__delattr__', '__delitem__', '__delslice__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getslice__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__setslice__', '__sizeof__', '__str__', '__subclasshook__', 'append', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort'


    # python3
    # '__add__', '__class__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort'

    # ===============================================================

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

    # L.__sizeof__() -- size of L in memory, in bytes
    # def __sizeof__(self) :

    # Abstract classes can override this to customize issubclass().
    # This is invoked early on by abc.ABCMeta.__subclasscheck__().
    # It should return True, False or NotImplemented.  If it returns
    # NotImplemented, the normal algorithm is used.  Otherwise, it
    # overrides the normal algorithm (and the outcome is cached).
    # def __subclasshook__(self) :

if __name__ == '__main__':
    a = List([1,2,3])
    a = 3 * a
    print(a)