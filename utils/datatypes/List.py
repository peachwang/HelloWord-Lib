# -*- coding: utf-8 -*-  
from ..shared import *
from .Iter    import Iter

# ListDiff: 以 item 作为最小比较单元。降维后可用于StrDiff

@add_print_func
class List(list) :

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
        cls._List                                             = List
        from .Dict     import Dict;            cls._Dict      = Dict
        from .Object   import Object;          cls._Object    = Object
        from .File     import File;            cls._File      = File
        from .Folder   import Folder;          cls._Folder    = Folder
        cls._raw_type_tuple = (type(None), str, bytes, int, float, bool, tuple, range, zip, cls._timedelta, cls._date, cls._time, cls._datetime, type)
        cls._type_tuple     = (cls._ObjectId, cls._Str, cls._TimeDelta, cls._Date, cls._Time, cls._DateTime, cls._DateList, cls._DateRange, cls._Year, cls._Month, cls._Week, cls._List, cls._Dict, cls._Object, cls._File, cls._Folder)
        # 如果不赋值到self中，本装饰器无效，原因：locals() 只读, globals() 可读可写。https://www.jianshu.com/p/4510a9d68f3f
        cls._has_imported_types = True

    # @Timer.timeit_total('wrap_item')
    @classmethod
    def wrap_item(cls, item, /) :
        cls._import_types()
        if isinstance(item, (cls._ObjectId, cls._Str, cls._List, cls._Dict)) : return item
        elif isinstance(item, str)                                           : return cls._Str(item)
        elif isinstance(item, dict)                                          : return cls._Dict(item)
        elif isinstance(item, list)                                          : return cls._List(item)
        elif isinstance(item, tuple)                                         : return tuple(cls.wrap_item(_) for _ in item)
        elif isinstance(item, cls._timedelta)                                : return cls._TimeDelta(item)
        elif isinstance(item, cls._date)                                     : return cls._Date(item)
        elif isinstance(item, cls._time)                                     : return cls._Time(item)
        elif isinstance(item, cls._datetime)                                 : return cls._DateTime(item)
        elif isinstance(item, set)                                           : return set(cls.wrap_item(_) for _ in item)
        else                                                                 : return item

    @staticmethod
    def wrap_str(_, func) : return '"{}"'.format(_) if isinstance(_, str) else func(_)
    
    @staticmethod
    def wrap_str_or_type(_, func) : return '"{}"'.format(_) if isinstance(_, str) else (str(_).split("'")[1] if isinstance(_, type) else func(_))

    # Create and return a new object.  See help(type) for accurate signature.
    # def __new__(self) :

    # Initialize self.  See help(type(self)) for accurate signature.
    # list() -> new empty list
    # list(iterable) -> new list initialized from iterable's items
    def __init__(self, *args) :
        self._import_types()
        if len(args) == 0   : list.__init__(self, [])
        elif len(args) == 1 :
            if isinstance(args[0], List)       : list.__init__(self, args[0]._get_data())
            elif isinstance(args[0], list)     :
                for item in args[0] : list.append(self, self.wrap_item(item))
            elif isinstance(args[0], Iterable) : self.__init__(list(args[0]))
            else                               : self.__init__(list(args))
        else                : self.__init__(list(args))

    # L.copy() -> list -- a shallow copy of L
    def copy(self) : return List(self)

    # id(object) -> integer
    # Return the identity of an object.
    # This is guaranteed to be unique among simultaneously existing objects.
    # (Hint: it's the object's memory address.)
    def get_id(self) -> int : return hex(id(self))

    # iter(iterable) -> iterator
    # iter(callable, sentinel) -> iterator
    # Get an iterator from an object.
    # In the first form, the argument must supply its own iterator, or be a sequence.
    # In the second form, the callable is called until it returns the sentinel.
        # __iter__(self, /)
            # Implement iter(self).
    def __iter__(self) -> Iter : return Iter(list.__iter__(self))
    
    @prop
    def iter(self) -> Iter : return self.__iter__()
    
    # 去除最外层封装，用于原生对象初始化：list/dict.__init__()/.update()
    def _get_data(self) -> list : return [ item for item in self ]

    # 原生化 list, dict, str, Object._data, timedelta, date, time, datetime
    # NOT IN PLACE
    def get_raw(self) -> list : return [ item.get_raw() if hasattr(item, 'get_raw') else item for item in self ]

    json_serialize = _get_data

    @print_func
    def print_len(self, msg = None) : return f'{"" if msg is None else f"{msg}: "}{self.len()}个元素', False

    @print_func
    def print_line(self, pattern = None, /) :
        if pattern is None : return self.mapped(lambda item, index : f'{index + 1:>3} {List.wrap_str(item, format)}').join('\n'), True
        else               : return self.mapped(lambda item, index : pattern.format(List.wrap_str(item, format), index)).join('\n'), True

    # default object formatter
    # @log_entering
    def __format__(self, spec) : return '[ {} ]'.format(self.mapped(lambda item : List.wrap_str(item, format)).join(', '), spec)

    @print_func
    def print_format(self, pattern = None, /) :
        if pattern is None : return self.mapped(lambda item : List.wrap_str(item, format)).join('\n'), True
        else               : return self.mapped(lambda item, index : pattern.format(List.wrap_str(item, format), index)).join('\n'), True

    # Return str(self).
    # @log_entering
    def __str__(self) : return f'{type(self).__name__}[ {{}} ]'.format(self.mapped(lambda item : List.wrap_str(item, str)).join(', '))

    @print_func
    def print_str(self) : return self.mapped(lambda item : List.wrap_str(item, str)).join('\n'), True

    # Return repr(self).
    # @log_entering
    def __repr__(self) : return f'{type(self).__name__}( {{}} )'.format(self.mapped(lambda item : List.wrap_str_or_type(item, repr)).join(', '))

    @print_func
    def print_j(self) : return self.j(), True

    # 带有业务逻辑，与 j 不同
    # NOT IN PLACE
    def json(self) : return List(item.json() if hasattr(item, 'json') else item for item in self)

    @print_func
    def print_json(self) : return f'{self.json().j()}', False

    def inspect(self, **kwargs) : from ..app.Inspect import Inspect; return Inspect(self, **kwargs)

    # other: Union[list, List]
    def diff(self, other) : from ..app.Inspect import Diff; return Diff(self, other)

    def is_list(self) : return True

    def is_dict(self) : return False

    # Return self==value.
    def __eq__(self, other) :
        if not isinstance(other, list) or self.len() != len(other) : return False
        return self.j() == other.j() if isinstance(other, List) else j(other)

    # Return self!=value.
    def __ne__(self, other) : return not self.__eq__(other)

    # Return len(self).
    def __len__(self) : return list.__len__(self)

    def len(self) : return list.__len__(self)

    def is_empty(self) : return self.len() == 0

    # x.__contains__(y) <==> y in x
    def __contains__(self, item, /) : return list.__contains__(self, item)

    def has(self, item, /) : return list.__contains__(self, item)

    def has_no(self, item, /) : return not self.has(item)

    def has_any_of(self, *item_iterable) : return any(self.has(item) for item in item_iterable)

    def has_all_of(self, *item_iterable) : return all(self.has(item) for item in item_iterable)

    def has_none_of(self, *item_iterable) : return all(self.has_no(item) for item in item_iterable)

    # L.count(value) -> integer -- return number of occurrences of value
    def count(self, item, /) -> int : return list.count(self, item)

    # L.index(value, [start, [stop]]) -> integer -- return first index of value.
    # Raises ValueError if the value is not present.
    def left_index(self, item, /, *, start = 0) -> Optional[int] :
        try               : index = list.index(self, item, start)
        except ValueError : return None
        else              : return index

    # L.index(value, [start, [stop]]) -> integer -- return first index of value.
    # Raises ValueError if the value is not present.
    def right_index(self, item, /) -> Optional[int] :
        try               : index = self.reversed().left_index(item)
        except ValueError : return None
        else              : return self.len() - index - 1

    def unique_index(self, item, /) -> int :
        if self.count(item) == 0  : raise ValueError(f'{self=}\n中值：\n{item=}\n不存在')
        elif self.count(item) > 1 : raise ValueError(f'{self=}\n中值：\n{item=}\n不唯一')
        return list.index(self, item)

    # Return getattr(self, name).
    # def __getattribute__(self) :

    # getattr(object, name[, default]) -> value
    # Get a named attribute from an object; getattr(x, 'y') is equivalent to x.y.
    # When a default argument is given, it is returned when the attribute doesn't exist; without it, an exception is raised in that case.
    '''NOT IN PLACE'''
    def __getattr__(self, key_or_func_name) : return self.value_list(key_or_func_name)
        # if self.is_empty() :
        #     raise TypeError('不能对空列表进行 __getattr__ 操作，请检查是否是希望对Dict进行操作！')

    def __call__(self) : raise RuntimeError('请检查是否在批量调用List元素的方法获取结果List后，对结果List多加了()调用！')

    def get(self, index: int, default = None, /) :
        if not isinstance(index, int) : raise CustomTypeError(index)
        if abs(index) >= self.len()   : return default
        else                          : return self.__getitem__(index)

    # x.__getitem__(y) <==> x[y]
    # https://docs.python.org/3/library/collections.abc.html?highlight=__contains__#collections.abc.ByteString
    # Implementation note: Some of the mixin methods, such as __iter__(), __reversed__() and index(), make repeated calls to the underlying __getitem__() method.
    # Consequently, if __getitem__() is implemented with constant access speed, the mixin methods will have linear performance;
    # however, if the underlying method is linear (as it would be with a linked list), the mixins will have quadratic performance and will likely need to be overridden.
    def __getitem__(self, index: Union[int, slice], /) :
        if isinstance(index, int)     : return list.__getitem__(self, index)
        elif isinstance(index, slice) :
            if (index.start is None or isinstance(index.start, int)) and (index.stop is None or isinstance(index.stop, int)) :
                return List(list.__getitem__(self, index))
            else :
                start, end = None, None
                for idx, item in self.enum() :
                    if index.start is not None and start is None and index.start == item : start = idx
                    elif start is not None and index.start == item                       : raise RuntimeError(f'\n{self=}\n中有重复的 [{index.start=}]: [{item}]')
                    if index.stop is not None and end is None and index.stop == item     : end = idx
                    elif end is not None and index.stop == item                          : raise RuntimeError(f'\n{self=}\n中有重复的 [{index.stop=}]: [{item}]')
                if index.start is not None and start is None : raise RuntimeError(f'\n{self=}\n中不存在 [{index.start=}]')
                if index.stop is not None and end is None    : raise RuntimeError(f'\n{self=}\n中不存在 [{index.stop=}]')
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
    def __setitem__(self, index, item) : list.__setitem__(self, index, self.wrap_item(item)); return item

    # IN PLACE
    def set(self, index, item, /) : self.__setitem__(index, item); return self

    # NOT IN PLACE
    def setted(self, index, item, /) : return self.copy().set(index, item)

    # L.append(object) -> None -- append object to end
    # IN PLACE
    def append(self, item, /) : list.append(self, self.wrap_item(item)); return self

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
    def insert(self, index, item, /) : list.insert(self, index, self.wrap_item(item)); return self

    # NOT IN PLACE
    def inserted(self, index, item, /) : return self.copy().insert(index, item)

    # Return self+value.
    # NOT IN PLACE
    # item_list: Union[list, List]
    def __add__(self, item_list) : return List(list.__add__(self, List(item_list)))

    # Implement self+=value.
    # IN PLACE
    # item_list: Union[list, List]
    def __iadd__(self, item_list) : return list.__iadd__(self, List(item_list))
    
    # L.extend(iterable) -> None -- extend list by appending elements from the iterable
    # IN PLACE
    def extend(self, iterable: Optional[list], /) :
        if isinstance(iterable, Iterable) : list.extend(self, iterable); return self
        elif iterable is None             : return self
        else                              : raise CustomTypeError(iterable)

    # NOT IN PLACE
    def extended(self, item_list, /) : return self.copy().extend(item_list)

    # Return self*value
    # NOT IN PLACE
    def __mul__(self, value: int) : return List(list.__mul__(self, value))
    
    # Return value*self.
    # NOT IN PLACE
    def __rmul__(self, value: int) : return List(list.__rmul__(self, value))

    # Implement self*=value.
    # IN PLACE
    def __imul__(self, value: int) : return list.__imul__(self, value)

    # Implement delattr(self, name).
    # Deletes the named attribute from the given object.
    # delattr(x, 'y') is equivalent to ``del x.y''
    # def __delattr__(self) :

    # Delete self[key].
    def __delitem__(self, key: Union[int, slice]) : return list.__delitem__(self, key)

    # L.pop([index]) -> item -- remove and return item at index (default last).
    # Raises IndexError if list is empty or index is out of range.
    # IN PLACE
    def pop_index(self, index, /) : return list.pop(self, index)

    # NOT IN PLACE
    def popped_index(self, index, /) : return self.copy().pop_index(index)

    # L.remove(value) -> None -- remove first occurrence of value.
    # Raises ValueError if the value is not present.
    # IN PLACE
    def drop_item(self, item, /) : list.remove(self, item); return self

    # NOT IN PLACE
    def dropped_item(self, item, /) : return self.copy().drop_item()
    
    # L.__reversed__() -- return a reverse iterator over the list
    def __reversed__(self) : return Iter(list.__reversed__(self))

    # L.reverse() -> None -- reverse *IN PLACE*
    # IN PLACE
    def reverse(self) : list.reverse(self); return self

    # NOT IN PLACE
    def reversed(self) : return self.copy().reverse()

    # ================ 20200514 已优化 ================
    @classmethod
    def get_value(cls, item, attr_or_func_name: Optional[str], default = _no_value, /, *args, **kwargs) :
        if attr_or_func_name is None : return item
        # 可以允许字段不存在
        attr = getattr(item, attr_or_func_name) if default == self._no_value else getattr(item, attr_or_func_name, cls.wrap_item(default))
        if isinstance(attr, Callable)                                        : return attr(*args, **kwargs) # attr 存在
        # 此时，要么 attr 存在，且非函数；要么 attr 不存在
        elif isinstance(item, List) and not hasattr(item, attr_or_func_name) :
            raise AttributeError(
                f'{P()}{type(item) = }{E()} 不含属性 {P(attr_or_func_name)}; '
                f'请检查是否采用了错误的调用方式：x_list.y_list.z; {item = }'
            )
        else                                                                 : return attr

    # L.sort(key=None, reverse=False) -> None -- stable sort *IN PLACE*
    # Sort the list in ascending order and return None.
    # The sort is in-place (i.e. the list itself is modified) and stable (i.e. the order of two equal elements is maintained).
    # If a key function is given, apply it once to each list item and sort them, ascending or descending, according to their function values.
    # The reverse flag can be set to sort in descending order.
    # IN PLACE
    def sort(self, key_func_or_attr_or_func_name = None, /, *, reverse = False) :
        if isinstance(key_func_or_attr_or_func_name, Callable) :
            list.sort(self, key = key_func_or_attr_or_func_name, reverse = reverse)
        else                                                   :
            list.sort(self, key = lambda item : self.get_value(item, key_func_or_attr_or_func_name), reverse = reverse)
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



    # IN PLACE
    def map(self, func, /, *args, **kwargs) :
        return self.clear().extend(
            func(item, *(self._left_pad_index_to_args(func, args, index, 1)), **kwargs)
            for index, item in self.enum()
        )

    # NOT IN PLACE
    def mapped(self, func, /, *args, **kwargs) : return self.copy().map(func, *args, **kwargs)

    # NOT IN PLACE
    def for_each(self, func, /, *args, **kwargs) : self.mapped(func, *args, **kwargs); return self

    # func 可以有参数
    # 或许可以和 map 合并
    # IN PLACE
    def batch(self, attr_or_func_name: str, /, *args, **kwargs) :
        return self.clear().extend(
            self.get_value(
                item,
                attr_or_func_name,
                self._no_value,
                *(self._left_pad_index_to_args(getattr(item, attr_or_func_name), args, index, 0)),
                **kwargs
            )
            for index, item in self.enum()
        )

    # 等价于 value_list，但不支持 default，可以有参数
    # NOT IN PLACE
    def batched(self, attr_or_func_name: str, /, *args, **kwargs) : return self.copy().batch(attr_or_func_name, *args, **kwargs)

    # func 无参数
    # 参考 Iter.__getattr__
    # NOT IN PLACE
    def value_list(self, attr_or_func_name: Optional[str], /, *, default = _no_value) :
        return self.mapped(lambda item : self.get_value(item, attr_or_func_name, default)) # 对于 attr_or_func_name = None 或 空列表的情况，均返回自身

    # NOT IN PLACE
    def format(self, pattern, /) : return self.mapped(lambda _ : pattern.format(_))

    # IN PLACE
    def filter(self, func_or_func_name, /, *args, **kwargs) :
        return self.clear().extend(
            item
            for item in self
            if (func_or_func_name(item, *args, **kwargs)
                if isinstance(func_or_func_name, Callable)
                else getattr(item, func_or_func_name)(*args, **kwargs)
            )
        )

    # NOT IN PLACE
    def filtered(self, func_or_func_name, /, *args, **kwargs) : return self.copy().filter(func_or_func_name, *args, **kwargs)

    def filter_the_only_one(self, func_or_func_name, /, *args, **kwargs) :
        result = self.filtered(func_or_func_name, *args, **kwargs)
        if result.len() != 1 : raise RuntimeError(f'结果不唯一：{result}')
        else                 : return result[0]

    # IN PLACE
    def filter_by_value(self, attr_or_func_name: Optional[str], value_or_list, /, *, default = None) :
        if not isinstance(value_or_list, list) : value_or_list = [ value_or_list ]
        return self.filter(lambda item : self.get_value(item, attr_or_func_name, default) in value_or_list)

    # NOT IN PLACE
    def filtered_by_value(self, attr_or_func_name, value_or_list, /, *, default = None) :
        return self.copy().filter_by_value(attr_or_func_name, value_or_list, default = default)

    # NOT IN PLACE
    def reduce(self, func, initial_value, /, *args, **kwargs) :
        result = initial_value
        for index, item in self.enum() :
            result = func(result, item, *(self._left_pad_index_to_args(func, args, index, 2)), **kwargs)
        return result

    # Merge items of the items of self
    # IN PLACE
    def merge(self) : return self.clear().extend(self.reduce(lambda result, item : result.extend(item), List()))

    # NOT IN PLACE
    def merged(self) : return self.copy().merge()

    def group_by(self, key_func = None, /, *, value_func = None) :
        from itertools import groupby
        result = self._Dict()
        for k, g in groupby(self.sorted(key_func or (lambda _ : f'{_}' if _ is not None else hash(object()))), key = key_func) :
            result[k] = List((value_func or lambda _ : _)(item) for item in g)
        return result
    
    def count_by(self, key_func = None, /) : return self._Dict((k, g.len()) for k, g in self.group_by(key_func).items())

    # NOT IN PLACE
    def _reduce(self, attr_or_func_name: Optional[str], func, initial_value, /, *, default = _no_value) :
        return self.value_list(attr_or_func_name, default = default).reduce(func, initial_value)

    # NOT IN PLACE
    def sum(self, attr_or_func_name: Optional[str] = None, /, *, initial_or_empty_value = 0, default = _no_value) :
        return self._reduce(attr_or_func_name, lambda result, item : item + result, initial_or_empty_value, default = default)

    # NOT IN PLACE
    def ave(self, attr_or_func_name: Optional[str] = None, /, *, initial_or_empty_value = 0, default = _no_value) :
        result = 1.0 * self.sum(attr_or_func_name, initial_or_empty_value = initial_or_empty_value, default = default)
        return result if self.is_empty() else result / self.len()

    # NOT IN PLACE
    def max(self, attr_or_func_name: Optional[str] = None, /, *, initial_or_empty_value = 0, default = _no_value) :
        return initial_or_empty_value if self.is_empty() else self._reduce(
            attr_or_func_name,
            lambda result, item : item if item > result else result,
            self.get_value(self[0], attr_or_func_name, default),
            default = default
        )

    # NOT IN PLACE
    def min(self, attr_or_func_name: Optional[str] = None, /, *, initial_or_empty_value = 0, default = _no_value) :
        return initial_or_empty_value if self.is_empty() else self._reduce(
            attr_or_func_name,
            lambda result, item : item if item < result else result,
            self.get_value(self[0], attr_or_func_name, default),
            default = default
        )

    # ================== 20200514 已优化 ============

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
    def clear(self) : list.clear(self); return self
    
    def write_to_file(self, file, /, *, indent = True) : file.write_json(self, indent = indent); return self

    def write_line_list_to_file(self, file, /) : file.write_line_list(self); return self

    # list(map(lambda x : print(f'\n{x}\n{list.__getattribute__([], x).__doc__}\n'), dir(list)))

    # ===================== 3.3.7.     Emulating container types =====================
    # The following methods can be defined to implement container objects.
    # Containers usually are sequences (such as lists or tuples) or mappings (like dictionaries), but can represent other containers as well.

    # The first set of methods is used either to emulate a sequence or to emulate a mapping;
    # the difference is that for a sequence, the allowable keys should be the integers k for which 0 <= k < N where N is the length of the sequence,
    # or slice objects, which define a range of items.

    # It is also recommended that mappings provide the methods keys(), values(), items(), get(), clear(), setdefault(), pop(), popitem(), copy(), and update()
    # behaving similar to those for Python’s standard dictionary objects.
    # The collections.abc module provides a MutableMapping abstract base class to help create those methods
    # from a base set of __getitem__(), __setitem__(), __delitem__(), and keys().

    # Mutable sequences should provide methods append(), count(), index(), extend(), insert(), pop(), remove(), reverse() and sort(), like Python standard list objects.
    # Finally, sequence types should implement addition (meaning concatenation) and multiplication (meaning repetition) by defining the methods
    # __add__(), __radd__(), __iadd__(), __mul__(), __rmul__() and __imul__() described below; they should not define other numerical operators.

    # It is recommended that both mappings and sequences implement the __contains__() method to allow efficient use of the in operator;
    # for mappings, in should search the mapping’s keys; for sequences, it should search through the values.

    # It is further recommended that both mappings and sequences implement the __iter__() method to allow efficient iteration through the container;
    # for mappings, __iter__() should iterate through the object’s keys; for sequences, it should iterate through the values.

    # len(s)
        # Return the length (the number of items) of an object.
        # The argument may be a sequence (such as a string, bytes, tuple, list, or range) or a collection (such as a dictionary, set, or frozen set).
        # len(obj, /)
            # Return the number of items in a container.

    # object.__len__(self)
        # Called to implement the built-in function len().
        # Should return the length of the object, an integer >= 0.
        # Also, an object that doesn’t define a __bool__() method and whose __len__() method returns zero is considered to be false in a Boolean context.
        # CPython implementation detail: In CPython, the length is required to be at most sys.maxsize.
        # If the length is larger than sys.maxsize some features (such as len()) may raise OverflowError.
        # To prevent raising OverflowError by truth value testing, an object must define a __bool__() method.

    # object.__length_hint__(self)
        # Called to implement operator.length_hint().
        # Should return an estimated length for the object (which may be greater or less than the actual length).
        # The length must be an integer >= 0.
        # The return value may also be NotImplemented, which is treated the same as if the __length_hint__ method didn’t exist at all.
        # This method is purely an optimization and is never required for correctness.

    # Note: Slicing is done exclusively with the following three methods.
    # A call like a[1:2] = b is translated to a[slice(1, 2, None)] = b and so forth.
    # Missing slice items are always filled in with None.

    # object.__getitem__(self, key)
        # Called to implement evaluation of self[key].
        # For sequence types, the accepted keys should be integers and slice objects.
        # Note that the special interpretation of negative indexes (if the class wishes to emulate a sequence type) is up to the __getitem__() method.
        # If key is of an inappropriate type, TypeError may be raised;
        # if of a value outside the set of indexes for the sequence (after any special interpretation of negative values), IndexError should be raised.
        # For mapping types, if key is missing (not in the container), KeyError should be raised.
        # Note: for loops expect that an IndexError will be raised for illegal indexes to allow proper detection of the end of the sequence.

    # object.__setitem__(self, key, value)
        # Called to implement assignment to self[key].
        # Same note as for __getitem__().
        # This should only be implemented for mappings if the objects support changes to the values for keys, or if new keys can be added,
        # or for sequences if elements can be replaced.
        # The same exceptions should be raised for improper key values as for the __getitem__() method.

    # object.__delitem__(self, key)
        # Called to implement deletion of self[key].
        # Same note as for __getitem__().
        # This should only be implemented for mappings if the objects support removal of keys,
        # or for sequences if elements can be removed from the sequence.
        # The same exceptions should be raised for improper key values as for the __getitem__() method.

    # object.__missing__(self, key)
        # Called by dict.__getitem__() to implement self[key] for dict subclasses when key is not in the dictionary.

    # iter(object[, sentinel])
        # Return an iterator object.
        # The first argument is interpreted very differently depending on the presence of the second argument.
        # Without a second argument, object must be a collection object which supports the iteration protocol (the __iter__() method),
        # or it must support the sequence protocol (the __getitem__() method with integer arguments starting at 0).
        # If it does not support either of those protocols, TypeError is raised.

        # If the second argument, sentinel, is given, then object must be a callable object.
        # The iterator created in this case will call object with no arguments for each call to its __next__() method;
        # if the value returned is equal to sentinel, StopIteration will be raised, otherwise the value will be returned.

        # See also Iterator Types.

        # One useful application of the second form of iter() is to build a block-reader.
        # For example, reading fixed-width blocks from a binary database file until the end of file is reached:
        # from functools import partial
        # with open('mydata.db', 'rb') as f:
            # for block in iter(partial(f.read, 64), b''):
                # process_block(block)

        # iter(...)
            # iter(iterable) -> iterator
            # iter(callable, sentinel) -> iterator
            # Get an iterator from an object.
            # In the first form, the argument must supply its own iterator, or be a sequence.
            # In the second form, the callable is called until it returns the sentinel.

    # object.__iter__(self)
        # This method is called when an iterator is required for a container.
        # This method should return a new iterator object that can iterate over all the objects in the container.
        # For mappings, it should iterate over the keys of the container.
        # Iterator objects also need to implement this method; they are required to return themselves.
        # For more information on iterator objects, see Iterator Types.

    # reversed(seq)
        # Return a reverse iterator.
        # seq must be an object which has a __reversed__() method or supports the sequence protocol
        # (the __len__() method and the __getitem__() method with integer arguments starting at 0).
        # class reversed(object)
            # reversed(sequence, /)
            # Return a reverse iterator over the values of the given sequence.

    # object.__reversed__(self)
        # Called (if present) by the reversed() built-in to implement reverse iteration.
        # It should return a new iterator object that iterates over all the objects in the container in reverse order.
        # If the __reversed__() method is not provided, the reversed() built-in will fall back to using the sequence protocol (__len__() and __getitem__()).
        # Objects that support the sequence protocol should only provide __reversed__()
        # if they can provide an implementation that is more efficient than the one provided by reversed().

    # The membership test operators (in and not in) are normally implemented as an iteration through a container.
    # However, container objects can supply the following special method with a more efficient implementation, which also does not require the object be iterable.

    # object.__contains__(self, item)
        # Called to implement membership test operators.
        # Should return true if item is in self, false otherwise.
        # For mapping objects, this should consider the keys of the mapping rather than the values or the key-item pairs.
        # For objects that don’t define __contains__(), the membership test first tries iteration via __iter__(),
        # then the old sequence iteration protocol via __getitem__(), see this section in the language reference.
        # For container types such as list, tuple, set, frozenset, dict, or collections.deque,
        # the expression x in y is equivalent to any(x is e or x == e for e in y).


if __name__ == '__main__':
    a = List([1,2,3])
    a = 3 * a
    print(a)