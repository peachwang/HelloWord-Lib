# -*- coding: utf-8 -*-  
import sys, os; sys.path.append(os.path.realpath(__file__ + '/../'));
from types import GeneratorType
from shared import ensureArgsType

class List(list) :

    _has_imported_types = False

    def _importTypes(self) :
        if self._has_imported_types : return
        self.List = List
        from Dict import Dict; self.Dict = Dict
        from Str import Str; self.Str = Str
        from Object import Object; self.Object = Object
        from DateTime import DateTime, datetime; self.DateTime, self.datetime = DateTime, datetime
        from File import File; self.File = File
        from Folder import Folder; self.Folder = Folder
        from Audio import Audio; self.Audio = Audio
        # 如果不赋值到self中，本装饰器无效，原因：locals() 只读, globals() 可读可写。https://www.jianshu.com/p/4510a9d68f3f
        self._has_imported_types = True

    def _wrapItem(self, item) :
        self._importTypes()
        if isinstance(item, list)            : return self.List(item)
        elif isinstance(item, dict)          : return self.Dict(item)
        elif isinstance(item, str)           : return self.Str(item)
        elif isinstance(item, bytes)         : return self.Str(item.decode())
        elif isinstance(item, tuple)         : return tuple([ self._wrapItem(_) for _ in item ])
        elif isinstance(item, set)           : return set([ self._wrapItem(_) for _ in item ])
        elif isinstance(item, self.datetime) : return self.DateTime(item)
        else : return item

    def __init__(self, *args) :
        '''Initialize self.  See help(type(self)) for accurate signature.'''
        if len(args) == 0 :
            list.__init__(self, [])
        elif len(args) == 1 :
            if isinstance(args[0], list) :
                for item in args[0] :
                    list.append(self, self._wrapItem(item))
            elif isinstance(args[0], (range, GeneratorType)) :
                self.__init__(list(args[0]))
            elif isinstance(args[0], List) :
                list.__init__(self, args[0]._getData())
            else :
                self.__init__(list(args))
        else :
            self.__init__(list(args))

    def copy(self) :
        '''L.copy() -> list -- a shallow copy of L'''
        return List(self)

    def getId(self) :
        '''id(object) -> integer
        Return the identity of an object.  This is guaranteed to be unique among
        simultaneously existing objects.  (Hint: it's the object's memory address.)'''
        return hex(id(self))
    
    # 去除最外层封装，用于原生对象初始化：list/dict.__init__()/.update()
    def _getData(self) :
        return [ item for item in self ]

    # 原生化 list, dict, str, Object._data, datetime
    def getRaw(self) :
        '''NOT IN PLACE'''
        self._importTypes()
        return [ (item.getRaw()
                if isinstance(item, (self.List, self.Dict, self.Str, self.Object, self.DateTime, self.File, self.Folder, self.Audio))
                else item # 可能是int, float, bool, tuple, set, range, zip, object，不可能是list. dict, str, bytes, datetime
            ) for item in self
        ]

    def jsonSerialize(self) :
        '''NOT IN PLACE'''
        self._importTypes()
        from util import json_serialize
        _ = []
        for item in self :
            if isinstance(item, (self.List, self.Dict, self.Str, self.Object, self.DateTime, self.File, self.Folder, self.Audio)) :
                _.append(item.jsonSerialize())
            else :
                _.append(json_serialize(item)) # 可能是int, float, bool, tuple, set, range, zip, object，不可能是list. dict, str, bytes, datetime
        return _

    # 可读化
    def j(self) :
        from util import j
        return j(self.jsonSerialize())

    def print(self, color = '') :
        from util import E
        print(color, self.j(), E if color != '' else '')
        return self

    def __format__(self, code) :
        '''default object formatter'''
        return '[{}]'.format(
            self.mapped(lambda item : f'"{item}"' if isinstance(item, str) else f'{item}')
                .join(', ')
        )

    def __str__(self) :
        '''Return str(self).'''
        return 'List[{}]'.format(
            self.mapped(lambda item : f'"{item}"' if isinstance(item, str) else str(item))
                .join(', ')
        )

    def stat(self, msg = '') :
        print('{}{}个'.format('' if msg == '' else '{}: '.format(msg), self.len()))
        return self

    def inspect(self) :
        raise

    # DataStructure Module
    #   def inspect()
    #   def compatibleTo
    #   def validate
    #   def difference/delta


    # # move
    # def inspect(data, max_depth = 10, depth = 0) :
    # https://docs.python.org/3/library/reprlib.html
    #     # print(str(data)[:120])
    #     if depth > max_depth :
    #         if data is None : return None 
    #         elif isinstance(data, (str, int, float, bool, tuple, set)) : return data
    #         elif isinstance(data, list) : return '[ {} items folded ]'.format(len(data))
    #         elif isinstance(data, dict) : return '{{ {} keys folded }}'.format(len(data))
    #         else : raise UserTypeError('data', data, [str, list, tuple, set, dict, int, float, bool])
    #     if data is None : return None
    #     elif isinstance(data, (str, int, float, bool, tuple, set)) : return data
    #     elif isinstance(data, list) :
    #         if len(data) == 0 : return data
    #         elif len(data) == 1 : return List([ inspect(data[0], max_depth, depth + 1) ])
    #         elif len(data) == 2 : return List([ inspect(data[0], max_depth, depth + 1), inspect(data[1], max_depth, depth + 1) ])
            
    #         # len >= 3
    #         result_0 = inspect(data[0], max_depth, depth + 1)
    #         _ = '------------------------------'
    #         if isinstance(result_0, dict) :
    #             for index, datum_i in enumerate(data) :
    #                 if not isinstance(datum_i, dict) : raise Exception('列表中元素类型不一致({})'.format(datum_i))
    #                 for key, value in datum_i.items() :
    #                     if key not in result_0 :
    #                         result_0[key] = inspect(value, max_depth, depth + 1) # 【补充】第0个元素中不存在的字段
    #                         continue
    #                     if data[0].get(key) is not None and isinstance(data[0][key], list) : continue # 列表类【原生】字段不扩充POSSIBLE VALUES
    #                     if data[0].get(key) is not None and isinstance(data[0][key], dict) : continue # 字典类【原生】字段不扩充POSSIBLE VALUES
    #                     if data[0].get(key) is None and isinstance(result_0[key], list)
    #                         and not (isinstance(result_0[key][0], str) and 'POSSIBLE VALUES' in result_0[key][0]) : continue # 列表类【补充】字段不扩充POSSIBLE VALUES
    #                     if data[0].get(key) is None and isinstance(result_0[key], dict) : continue # 字典类【补充】字段不扩充POSSIBLE VALUES
    #                     # 此时待补充的是非列表字典类字段
    #                     if isinstance(value, list) or isinstance(value, dict) : raise Exception('列表中元素类型不一致({})'.format(value))
    #                     # 此时value一定为非列表字典类数据
    #                     if not isinstance(result_0[key], list) : # 暂未扩充过，现进行首次扩充POSSIBLE VALUES
    #                         result_0[key] = [
    #                             _ + 'POSSIBLE VALUES' + _, 
    #                             result_0[key]
    #                         ]
    #                         if inspect(value, max_depth, depth + 1) != result_0[key][1] :
    #                             result_0[key].append(inspect(value, max_depth, depth + 1))
    #                     else : # 非首次扩充POSSIBLE VALUES
    #                         if len(result_0[key]) < 5 :
    #                             if inspect(value, max_depth, depth + 1) not in result_0[key] :
    #                                 result_0[key].append(inspect(value, max_depth, depth + 1)) # 扩充
    #                         if index == len(data) - 1 :
    #                             result_0[key].append('{} TOTAL {} SIMILAR ITEMS {}'.format(_, len(data), _))
    #             return [ result_0, '{} TOTAL {} SIMILAR DICTS {}'.format(_, len(data), _) ]
    #         else : # 非字典类数据，含列表
    #             return [ inspect(data[0], max_depth, depth + 1), inspect(data[1], max_depth, depth + 1), '{} TOTAL {} SIMILAR LISTS {}'.formart(_, len(data), _) ]
    #     elif isinstance(data, dict) : return { key : inspect(value, max_depth, depth + 1) for key, value in data.items() }
    #     else : raise UserTypeError('data', data, [str, list, tuple, set, dict, int, float, bool])

    # def __len__(self) :
        '''
        Return len(self).
        '''

    def len(self) :
        return len(self)

    # def __contains__(self, item) :
        '''
        'x.__contains__(y) <==> y in x'
        '''

    def count(self, item) :
        '''L.count(value) -> integer -- return number of occurrences of value'''
        return list.count(self, item)

    def index(self, item, start = 0) :
        '''L.index(value, [start, [stop]]) -> integer -- return first index of value.
        Raises ValueError if the value is not present.'''
        return list.index(self, item, start)

    # def __getattribute__(self) :
        '''
        Return getattr(self, name).
        '''

    def __getattr__(self, key_or_func_name) :
        '''getattr(object, name[, default]) -> value
        Get a named attribute from an object; getattr(x, 'y') is equivalent to x.y.
        When a default argument is given, it is returned when the attribute doesn't
        exist; without it, an exception is raised in that case.'''
        '''NOT IN PLACE'''
        return self.valueList(key_or_func_name)

    def __getitem__(self, index) :
        '''x.__getitem__(y) <==> x[y]'''
        if isinstance(index, int) : return list.__getitem__(self, index)
        elif isinstance(index, slice) : return List(list.__getitem__(self, index))
        else : raise Exception('Unexpected type({}) of index: {}'.format(type(index), index))

    # def __setattr__(self) :
        '''
        Implement setattr(self, name, value).
        
        Sets the named attribute on the given object to the specified value.
        setattr(x, 'y', v) is equivalent to ``x.y = v''
        '''

    def __setitem__(self, index, item) :
        '''Set self[index] to value.'''
        '''IN PLACE'''
        list.__setitem__(self, index, self._wrapItem(item))
        return item

    def set(self, index, item) :
        '''IN PLACE'''
        self.__setitem__(index, item)
        return self

    def append(self, item) :
        '''L.append(object) -> None -- append object to end'''
        '''IN PLACE'''
        list.append(self, self._wrapItem(item))
        return self

    def insert(self, index, item) :
        '''L.insert(index, object) -> None -- insert object before index'''
        '''IN PLACE'''
        list.insert(self, index, self._wrapItem(item))
        return self

    def __add__(self, item_list) :
        '''Return self+value.'''
        '''NOT IN PLACE'''
        if isinstance(item_list, list) :
            return List(list.__add__(self, List(item_list)))
        else :
            raise Exception('Unexpected type({}) of item_list: {}'.format(type(item_list), item_list))

    def __iadd__(self, item_list) :
        '''Implement self+=value.'''
        '''IN PLACE'''
        if isinstance(item_list, list) :
            return list.__iadd__(self, List(item_list))
        else :
            raise Exception('Unexpected type({}) of item_list: {}'.format(type(item_list), item_list))
    
    def extend(self, item_list) :
        '''L.extend(iterable) -> None -- extend list by appending elements from the iterable'''
        '''IN PLACE'''
        if isinstance(item_list, list) :
            list.extend(self, List(item_list))
        elif item_list is None : return self
        else : raise Exception('Unexpected type({}) of item_list: {}'.format(type(item_list), item_list))
        return self

    def extended(self, item_list) :
        '''NOT IN PLACE'''
        return self.copy().extend(item_list)

    def pop(self, index = -1) :
        '''L.pop([index]) -> item -- remove and return item at index (default last).
        Raises IndexError if list is empty or index is out of range.'''
        '''IN PLACE'''
        return list.pop(self, index)

    def remove(self, item) :
        '''L.remove(value) -> None -- remove first occurrence of value.
        Raises ValueError if the value is not present.'''
        '''IN PLACE'''
        list.remove(self, item)
        return self
    
    # def __reversed__(self) :
        '''
        L.__reversed__() -- return a reverse iterator over the list
        '''

    def reverse(self) :
        '''L.reverse() -> None -- reverse *IN PLACE*'''
        '''IN PLACE'''
        list.reverse(self)
        return self

    def reversed(self) :
        '''NOT IN PLACE'''
        return self.copy().reverse()

    def sort(self, key_func = None, reverse = False) :
        '''L.sort(key=None, reverse=False) -> None -- stable sort *IN PLACE*'''
        '''IN PLACE'''
        list.sort(self, key = key_func, reverse = reverse)
        return self

    def sorted(self, key_func = None, reverse = False) :
        '''NOT IN PLACE'''
        return self.copy().sort(key_func, reverse)

    def enumerate(self) :
        return enumerate(self)

    # pos为index在func的参数表里的下标
    def _padIndexToArgs(self, func, args, index, pos) :
        import inspect
        func_args = inspect.getargspec(func).args
        if len(func_args) > pos and func_args[pos] == 'index' :
            return [ index ] + args
        else :
            return args

    def batch(self, func_name, *args, **kwargs) :
        '''IN PLACE'''
        if not isinstance(func_name, str) :
            raise Exception('Unexpected type({}) of func_name: {}'.format(type(func_name), func_name))
        for index, item in enumerate(self) :
            attribute = self[index].__getattribute__(func_name)
            if callable(attribute) :
                self[index] = attribute(*(self._padIndexToArgs(attribute, args, index, 0)), **kwargs)
            else : self[index] = attribute
        return self

    def batched(self, func_name, *args, **kwargs) :
        '''NOT IN PLACE'''
        return self.copy().batch(func_name, *args, **kwargs)

    def map(self, func, *args, **kwargs) :
        '''IN PLACE'''
        for index, item in enumerate(self) :
            self[index] = func(item, *(self._padIndexToArgs(func, args, index, 1)), **kwargs)
        return self

    def mapped(self, func, *args, **kwargs) :
        '''NOT IN PLACE'''
        return self.copy().map(func, *args, **kwargs)

    def valueList(self, key_list_or_func_name) :
        '''NOT IN PLACE'''
        self._importTypes()
        if self.len() == 0 : return self.copy()
        if isinstance(key_list_or_func_name, list) :
            if isinstance(self[0], self.Object) :
                return self.batched('_get', key_list_or_func_name)
            else :
                return self.batched('get', key_list_or_func_name)
        elif isinstance(key_list_or_func_name, str) :
            def getValue(item) :
                if isinstance(item, (self.Dict, self.Object)) :
                    attribute = item.__getattr__(key_list_or_func_name)
                else :
                    attribute = item.__getattribute__(key_list_or_func_name)
                if callable(attribute) : return attribute()
                else : return attribute
            return self.mapped(getValue)
        else : raise Exception('Unexpected type({}) of key_list_or_func_name: {}'.format(type(key_list_or_func_name), key_list_or_func_name))

    def json(self) :
        '''带有业务逻辑，与 j 不同'''
        '''NOT IN PLACE'''
        return self.valueList('json')

    def _stripItem(self, item, string) :
        self._importTypes()
        if item is None or isinstance(item, (int, float, bool, range, bytes, zip, self.datetime)):
            return item
        elif isinstance(item, (self.List, self.Dict, self.Str)) : # can't be list, dict, str
            return item.strip(string)
        elif isinstance(item, tuple) :
            return (self._stripItem(_, string) for _ in item)
        elif isinstance(item, set) :
            return set([self._stripItem(_, string) for _ in item])
        elif isinstance(item, object) :
            if 'strip' in dir(item) : item.strip(string)
            return item
        else :
            raise Exception('Unknown type{} of item{}'.format(type(item), item))

    def strip(self, string = ' \t\n') :
        '''IN PLACE'''
        return self.map(self._stripItem, string)

    def stripped(self, string = ' \t\n') :
        '''NOT IN PLACE'''
        return self.strip(string)

    def filter(self, func_or_func_name, *args, **kwargs) :
        '''IN PLACE'''
        index = 0
        if isinstance(func_or_func_name, str) :
            while index < self.len() :
                if self[index].__getattribute__(func_or_func_name)(*args, **kwargs) : index += 1
                else : self.pop(index)
        else :
            while index < self.len() :
                if func_or_func_name(self[index], *args, **kwargs) : index += 1
                else : self.pop(index)
        return self

    def filtered(self, func_or_func_name, *args, **kwargs) :
        '''NOT IN PLACE'''
        return self.copy().filter(func_or_func_name, *args, **kwargs)

    def filterByValue(self, key_list_or_func_name, value) :
        '''IN PLACE'''
        self._importTypes()
        if key_list_or_func_name is None :
            return self.filter(lambda item : item == value)
        elif isinstance(key_list_or_func_name, list) :
            if isinstance(self[0], self.Object) :
                return self.filter(lambda item : item._get(key_list_or_func_name) == value)
            else :
                return self.filter(lambda item : item.get(key_list_or_func_name) == value)
        elif isinstance(key_list_or_func_name, str) :
            def getValue(item) :
                if isinstance(item, self.Object) :
                    attribute = item.__getattr__(key_list_or_func_name)
                else :
                    attribute = item.__getattribute__(key_list_or_func_name)
                if callable(attribute) : return attribute()
                else : return attribute
            return self.filter(lambda item : getValue(item) == value)
        else : raise Exception('Unexpected type({}) of key_list_or_func_name: {}'.format(type(key_list_or_func_name), key_list_or_func_name))

    def filteredByValue(self, key_list_or_func_name, value) :
        '''NOT IN PLACE'''
        return self.copy().filterByValue(key_list_or_func_name, value)

    def reduce(self, func, initial_value, *args, **kwargs) :
        '''NOT IN PLACE'''
        result = initial_value
        for index, item in enumerate(self) :
            result = func(result, item, *(self._padIndexToArgs(func, args, index, 2)), **kwargs)
        return result

    # itertools.def accumulate(iterable, func=operator.add, *, initial=None):

    def merge(self) :
        '''Merge items of the items of self'''
        '''IN PLACE'''
        _ = self.reduce(lambda result, item : result.extend(item), List())
        return self.clear().extend(_)

    def merged(self) :
        '''NOT IN PLACE'''
        return self.copy().merge()

    def groupby(self) :
        raise
        # itertools.groupby(iterable, key=None)


    def _reduce(self, key_list_or_func_name, func, initial_value) :
        '''NOT IN PLACE'''
        if key_list_or_func_name is None :
            return self.reduce(func, initial_value)
        elif isinstance(key_list_or_func_name, (list, str)) :
            return self.valueList(key_list_or_func_name).reduce(func, initial_value)
        else : raise Exception('Unexpected type({}) of key_list_or_func_name: {}'.format(type(key_list_or_func_name), key_list_or_func_name))

    def sum(self, key_list_or_func_name = None) :
        '''NOT IN PLACE'''
        if self.len() == 0 : return 0
        return self._reduce(key_list_or_func_name, lambda result, item : result + item, 0)

    def mean(self, key_list_or_func_name = None, default = None) :
        '''NOT IN PLACE'''
        if self.len() == 0 : return default
        return 1.0 * self.sum(key_list_or_func_name) / self.len()

    def _initialValue(self, key_list_or_func_name) :
        '''NOT IN PLACE'''
        if key_list_or_func_name is None :
            return self[0]
        elif isinstance(key_list_or_func_name, list) :
            if isinstance(self[0], self.Object) :
                return self[0]._get(key_list_or_func_name)
            else :
                return self[0].get(key_list_or_func_name)
        elif isinstance(key_list_or_func_name, str) :
            attribute = self[0].__getattribute__(key_list_or_func_name)
            if callable(attribute) : return attribute()
            else : return attribute
        else : raise Exception('Unexpected type({}) of key_list_or_func_name: {}'.format(type(key_list_or_func_name), key_list_or_func_name))

    def max(self, key_list_or_func_name = None) :
        '''NOT IN PLACE'''
        if self.len() == 0 : return None
        return self._reduce(key_list_or_func_name,
            lambda result, item : item if item > result else result,
            self._initialValue(key_list_or_func_name)
        )

    def min(self, key_list_or_func_name = None) :
        '''NOT IN PLACE'''
        if self.len() == 0 : return None
        return self._reduce(key_list_or_func_name,
            lambda result, item : item if item < result else result,
            self._initialValue(key_list_or_func_name)
        )

    def join(self, sep) :
        '''NOT IN PLACE'''
        self._importTypes()
        if not isinstance(sep, str) :
            raise Exception('Unexpected type({}) of sep: {}'.format(type(sep), sep))
        return self.Str(sep).join(self)

    def unique(self) :
        '''IN PLACE'''
        '''O(??)'''
        _ = list(set(self))
        return self.clear().extend(_)

    def uniqued(self) :
        '''NOT IN PLACE'''
        return self.copy().unique()

    # 789
    @ensureArgsType
    # 456
    def intersect(self, item_list -> list) :
        # 123
        '''Update itself with the intersection of itself and another.'''
        '''IN PLACE'''
        '''O(N^2)???'''
        if not isinstance(item_list, list) :
            raise Exception('Unexpected type({}) of item_list: {}'.format(type(item_list), item_list))
        return self.filter(lambda item, item_list : item in item_list, List(item_list))

    def intersected(self, item_list) :
        '''NOT IN PLACE'''
        return self.copy().intersect(item_list)

    def __and__(self, item_list) :
        '''x.__and__(y) <==> x&y'''
        '''NOT IN PLACE'''
        return self.intersected(item_list)

    def difference(self, item_list) :
        '''Remove all elements of another list from this list.'''
        '''IN PLACE'''
        '''O(N^2)???'''
        if not isinstance(item_list, list) :
            raise Exception('Unexpected type({}) of item_list: {}'.format(type(item_list), item_list))
        return self.filter(lambda item, item_list : item not in item_list, List(item_list))

    def differenced(self, item_list) :
        '''NOT IN PLACE'''
        return self.copy().difference(item_list)

    def __sub__(self, item_list) :
        '''x.__sub__(y) <==> x-y'''
        '''NOT IN PLACE'''
        return self.differenced(item_list)

    def union(self, item_list) :
        '''Update a set with the union of itself and others.'''
        '''IN PLACE'''
        '''O(N^2)???'''
        if not isinstance(item_list, list) :
            raise Exception('Unexpected type({}) of item_list: {}'.format(type(item_list), item_list))
        return self.extend(List(item_list).difference(self))

    def unioned(self, item_list) :
        '''NOT IN PLACE'''
        return self.copy().union(item_list)

    def __or__(self, item_list) :
        '''x.__or__(y) <==> x|y'''
        '''NOT IN PLACE'''
        return self.unioned(item_list)

    def isDisjointFrom(self, item_list) :
        '''Return True if two lists have a null intersection.'''
        '''O(N^2)???'''
        return (self & item_list).len() == 0

    def isSubsetOf(self, item_list) :
        '''Report whether another set contains this set.'''
        '''O(N^2)???'''
        return (self - item_list).len() == 0

    def __le__(self, item_list) :
        '''Return self<=value.'''
        return self.isSubsetOf(item_list)

    def __lt__(self, item_list) :
        '''Return self<value.'''
        raise

    def isSupersetOf(self, item_list) :
        '''Report whether this set contains another set.'''
        '''O(N^2)???'''
        return (item_list - self).len() == 0

    def __ge__(self, item_list) :
        '''Return self>=value.'''
        return self.isSupersetOf(item_list)

    def __gt__(self, item_list) :
        '''Return self>value.'''
        raise

    def isSameSetOf(self, item_list) :
        return self <= item_list and self >= item_list

    def __eq__(self, item_list) :
        '''Return self==value.'''
        raise

    def __ne__(self, item_list) :
        '''Return self!=value.'''
        raise

    def flatten(self) :
        '''IN PLACE'''
        raise

    def bisect(self) :
        raise

    def clear(self) :
        '''L.clear() -> None -- remove all items from L'''
        '''IN PLACE'''
        list.clear(self)
        return self
    
    def writeToFile(self, file) :
        file.writeString(self.j())
        return self

    # list(map(lambda x : print('\n{}\n{}\n'.format(x, list.__getattribute__([], x).__doc__)), dir(list)))

    # python2
    # '__add__', '__class__', '__contains__', '__delattr__', '__delitem__', '__delslice__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getslice__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__setslice__', '__sizeof__', '__str__', '__subclasshook__', 'append', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort'


    # python3
    # '__add__', '__class__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort'

    # ===============================================================

    # def __class__(self) :
        '''
        list() -> new empty list
        list(iterable) -> new list initialized from iterable's items
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

    # def __imul__(self) :
        '''
        Implement self*=value.
        '''

    # def __init_subclass__(self) :
        '''
        This method is called when a class is subclassed.

        The default implementation does nothing. It may be
        overridden to extend subclasses.

        '''

    # def __iter__(self) :
        '''
        Implement iter(self).
        
        iter(iterable) -> iterator
        iter(callable, sentinel) -> iterator

        Get an iterator from an object.  In the first form, the argument must
        supply its own iterator, or be a sequence.
        In the second form, the callable is called until it returns the sentinel.
        '''

    # def __mul__(self, value) :
        '''
        Return self*value
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

    # def __rmul__(self, value) :
        '''
        Return value*self.
        '''

    # def __sizeof__(self) :
        '''
        L.__sizeof__() -- size of L in memory, in bytes
        '''

    # def __subclasshook__(self) :
        '''
        Abstract classes can override this to customize issubclass().

        This is invoked early on by abc.ABCMeta.__subclasscheck__().
        It should return True, False or NotImplemented.  If it returns
        NotImplemented, the normal algorithm is used.  Otherwise, it
        overrides the normal algorithm (and the outcome is cached).

        '''
