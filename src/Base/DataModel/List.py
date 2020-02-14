# -*- coding: utf-8 -*-  
import sys, os; sys.path.append(os.path.realpath(__file__ + '/../'));
from types import BuiltinFunctionType, FunctionType, BuiltinMethodType, MethodType, LambdaType, GeneratorType
from inspect import isgenerator
from functools import wraps
from shared import ensureArgsType, Optional, Union, UserTypeError, _print
# from Timer import Timer

class List(list) :

    _has_imported_types = False

    def _importTypes(self) :
        if self._has_imported_types : return
        self._List = List
        from Dict import Dict; self._Dict = Dict
        from Str import Str; self._Str = Str
        from Object import Object; self._Object = Object
        from DateTime import DateTime, datetime; self._DateTime, self._datetime = DateTime, datetime
        from File import File; self._File = File
        from Folder import Folder; self._Folder = Folder
        from Audio import Audio; self._Audio = Audio
        # 如果不赋值到self中，本装饰器无效，原因：locals() 只读, globals() 可读可写。https://www.jianshu.com/p/4510a9d68f3f
        self._has_imported_types = True

    def _wrapItem(self, item, /) :
        self._importTypes()
        if isinstance(item, list)            : return self._List(item)
        elif isinstance(item, dict)          : return self._Dict(item)
        elif isinstance(item, str)           : return self._Str(item)
        elif isinstance(item, bytes)         : return self._Str(item.decode())
        elif isinstance(item, tuple)         : return tuple([ self._wrapItem(_) for _ in item ])
        elif isinstance(item, set)           : return set([ self._wrapItem(_) for _ in item ])
        elif isinstance(item, self._datetime) : return self._DateTime(item)
        else : return item

    def __init__(self, *args) :
        '''Initialize self.  See help(type(self)) for accurate signature.'''
        if len(args) == 0 :
            list.__init__(self, [])
        elif len(args) == 1 :
            if isinstance(args[0], list) :
                for item in args[0] :
                    list.append(self, self._wrapItem(item))
            elif isinstance(args[0], (range, GeneratorType)) or isgenerator(args[0]) or '__next__' in dir(args[0]) :
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

    def iter(self) :
        '''
        Implement iter(self).
        iter(iterable) -> iterator
        iter(callable, sentinel) -> iterator
        Get an iterator from an object.  In the first form, the argument must
        supply its own iterator, or be a sequence.
        In the second form, the callable is called until it returns the sentinel.
        '''
        return list.__iter__(self)
    
    # 去除最外层封装，用于原生对象初始化：list/dict.__init__()/.update()
    def _getData(self) :
        return [ item for item in self ]

    # 原生化 list, dict, str, Object._data, datetime
    def getRaw(self) :
        '''NOT IN PLACE'''
        self._importTypes()
        return [ (item.getRaw()
                if isinstance(item, (self._List, self._Dict, self._Str, self._Object, self._DateTime, self._File, self._Folder, self._Audio))
                else item # 可能是int, float, bool, tuple, set, range, zip, object，不可能是list. dict, str, bytes, datetime
            ) for item in self
        ]

    def toMongoDoc(self) :
        from bson import ObjectId
        self._importTypes()
        for index, item in self.enum() :
            if isinstance(item, self._Dict) :
                if item.has('$id') :
                    self[index] = ObjectId(item['$id'])
                elif item.has('sec') and item.has('usec') :
                    self[index] = self._DateTime(item.sec + item.usec / 1000000).getRaw()
                else :
                    self[index].toMongoDoc()
            elif isinstance(item, self._List) :
                self[index].toMongoDoc()
        return self

    @_print
    def printLen(self) :
        return f'{self.len()}个元素', False

    @_print
    def printLine(self, pattern = None, /) :
        if pattern is None :
            return self.mapped(lambda item : f'{item}').join('\n'), True
        else :
            return self.mapped(lambda item, index : pattern.format(item, index)).join('\n'), True

    def __format__(self, code) :
        '''default object formatter'''
        return '[{}]'.format(
            self.mapped(lambda item : f'"{item}"' if isinstance(item, str) else f'{item}')
                .join(', ')
        )

    @_print
    def printFormat(self, pattern = None, /) :
        if pattern is None :
            return self.mapped(lambda item : f'{item}').join('\n'), True
        else :
            return self.mapped(lambda item, index : pattern.format(item, index)).join('\n'), True

    def __str__(self) :
        '''Return str(self).'''
        return 'List[{}]'.format(
            self.mapped(lambda item : f'"{item}"' if isinstance(item, str) else str(item))
                .join(', ')
        )

    @_print
    def printStr(self) :
        return self.mapped(lambda item : str(item)).join('\n'), True

    def jsonSerialize(self) :
        '''NOT IN PLACE'''
        self._importTypes()
        from util import json_serialize
        _ = []
        for item in self :
            if isinstance(item, (self._List, self._Dict, self._Str, self._Object, self._DateTime, self._File, self._Folder, self._Audio)) :
                _.append(item.jsonSerialize())
            else :
                _.append(json_serialize(item)) # 可能是int, float, bool, tuple, set, range, zip, object，不可能是list. dict, str, bytes, datetime
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
        return List(item.json() if 'json' in dir(item) else item for item in self)

    @_print
    def printJson(self) :
       return f'{self.json().j()}', False

    def inspect(self) :
        from Inspect import Inspect
        return Inspect(self)

    def isList(self) :
        return True

    def isDict(self) :
        return False

    def __len__(self) :
        '''
        Return len(self).
        '''
        return list.__len__(self)

    def len(self) :
        return list.__len__(self)

    def isEmpty(self) :
        return self.len() == 0

    def isNotEmpty(self) :
        return not self.isEmpty()

    def __contains__(self, item, /) :
        '''
        x.__contains__(y) <==> y in x
        '''
        return list.__contains__(self, item)

    def has(self, item, /) :
        return list.__contains__(self, item)

    def hasNot(self, item, /) :
        return not self.has(item)

    def hasAnyOf(self, item_list, /) :
        return any(self.has(item) for item in item_list)

    def hasAllOf(self, item_list, /) :
        return all(self.has(item) for item in item_list)

    def hasNoneOf(self, item_list, /) :
        return all(self.hasNot(item) for item in item_list)

    def count(self, item, /) :
        '''
        L.count(value) -> integer -- return number of occurrences of value
        '''
        return list.count(self, item)

    def leftIndex(self, item, /, *, start = 0) :
        '''
        L.index(value, [start, [stop]]) -> integer -- return first index of value.
        Raises ValueError if the value is not present.
        '''
        try :
            index = list.index(self, item, start)
        except ValueError :
            return None
        else :
            return index

    def rightIndex(self, item, /) :
        '''
        L.index(value, [start, [stop]]) -> integer -- return first index of value.
        Raises ValueError if the value is not present.
        '''
        try :
            index = list.index(self.reversed(), item)
        except ValueError :
            return None
        else :
            return self.len() - index - 1

    def uniqueIndex(self, item, /) :
        if self.count(item) == 0 :
            raise Exception(f'{self=}\n中值：\n{item=}\n不存在')
        elif self.count(item) > 1 :
            raise Exception(f'{self=}\n中值：\n{item=}\n不唯一')
        return list.index(self, item)

    # def __getattribute__(self) :
        '''
        Return getattr(self, name).
        '''

    def __getattr__(self, key_or_func_name) :
        '''
        getattr(object, name[, default]) -> value
        Get a named attribute from an object; getattr(x, 'y') is equivalent to x.y.
        When a default argument is given, it is returned when the attribute doesn't
        exist; without it, an exception is raised in that case.
        '''
        '''NOT IN PLACE'''
        # if self.len() == 0 :
        #     raise Exception('不能对空列表进行 __getattr__ 操作，请检查是否是希望对Dict进行操作！')
        return self.valueList(key_or_func_name)

    def __call__(self) :
        raise Exception('请检查是否在批量调用List元素的方法获取结果List后，对结果List多加了()调用！')

    def get(self, index: int, /, *, default = None) :
        if not isinstance(index, int) :raise UserTypeError(index)
        if index >= self.len() : return default
        else : return self.__getitem__(index)

    # @ensureArgsType
    def __getitem__(self, index: Union[int, slice], /) :
        '''
        x.__getitem__(y) <==> x[y]
        https://docs.python.org/3/library/collections.abc.html?highlight=__contains__#collections.abc.ByteString
        Implementation note: Some of the mixin methods, such as __iter__(), __reversed__() and index(), make repeated calls to the underlying __getitem__() method. Consequently, if __getitem__() is implemented with constant access speed, the mixin methods will have linear performance; however, if the underlying method is linear (as it would be with a linked list), the mixins will have quadratic performance and will likely need to be overridden.
        '''
        if isinstance(index, int) : return list.__getitem__(self, index)
        elif isinstance(index, slice) : 
            if (index.start is None or isinstance(index.start, int))\
            and (index.stop is None or isinstance(index.stop, int)) :
                return List(list.__getitem__(self, index))
            else :
                start, end = None, None
                for idx, item in self.enum() :
                    if index.start is not None and start is None and index.start == item :
                        start = idx
                    elif start is not None and index.start == item :
                        raise Exception(f'\n{self=}\n中有重复的 [{index.start=}]: [{item}]')
                    if index.stop is not None and end is None and index.stop == item :
                        end = idx
                    elif end is not None and index.stop == item :
                        raise Exception(f'\n{self=}\n中有重复的 [{index.stop=}]: [{item}]')
                if index.start is not None and start is None :
                    raise Exception(f'\n{self=}\n中不存在 [{index.start=}]')
                if index.stop is not None and end is None :
                    raise Exception(f'\n{self=}\n中不存在 [{index.stop=}]')
                return self[start : end]
        elif isinstance(index, tuple) : # Str.toRangeTuple() -> ((None, e1), idx2, (s3, e3), (s4, None))
            raise NotImplementedError
        else : raise UserTypeError(index)

    def getUniqueItem(self, item, /) :
        return self[self.uniqueIndex(item)]

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

    def set(self, index, item, /) :
        '''IN PLACE'''
        self.__setitem__(index, item)
        return self

    def setted(self, index, item, /) :
        '''NOT IN PLACE'''
        return self.copy().set(index, item)

    def append(self, item, /) :
        '''L.append(object) -> None -- append object to end'''
        '''IN PLACE'''
        list.append(self, self._wrapItem(item))
        return self

    def appended(self, item, /) :
        '''NOT IN PLACE'''
        return self.copy().append(item)

    def uniqueAppend(self, item, /) :
        '''IN PLACE'''
        if self.has(item) : return self
        else : return self.append(item)

    def uniqueAppended(self, item, /) :
        '''NOT IN PLACE'''
        return self.copy().uniqueAppend(item)

    def prepend(self, item, /) :
        '''L.prepend(object) -> None -- append object to start'''
        '''IN PLACE'''
        return self.insert(0, item)

    def prepended(self, item, /) :
        '''NOT IN PLACE'''
        return self.copy().prepend(item)

    def uniquePrepend(self, item, /) :
        '''IN PLACE'''
        if self.has(item) : return self
        else : return self.prepend(item)

    def uniquePrepended(self, item, /) :
        '''NOT IN PLACE'''
        return self.copy().uniquePrepend()

    def insert(self, index, item, /) :
        '''L.insert(index, object) -> None -- insert object before index'''
        '''IN PLACE'''
        list.insert(self, index, self._wrapItem(item))
        return self

    def inserted(self, index, item, /) :
        '''NOT IN PLACE'''
        return self.copy().insert(index, item)

    # @ensureArgsType
    def __add__(self, item_list: list) :
        '''Return self+value.'''
        '''NOT IN PLACE'''
        return List(list.__add__(self, List(item_list)))

    # @ensureArgsType
    def __iadd__(self, item_list: list) :
        '''Implement self+=value.'''
        '''IN PLACE'''
        return list.__iadd__(self, List(item_list))
    
    # @ensureArgsType
    def extend(self, item_list: Optional[list], /) :
        '''L.extend(iterable) -> None -- extend list by appending elements from the iterable'''
        '''IN PLACE'''
        if isinstance(item_list, (list, GeneratorType)) or isgenerator(item_list) or '__next__' in dir(item_list) :
            list.extend(self, List(item_list))
            return self
        elif item_list is None :
            return self
        else :
            raise UserTypeError(item_list)

    def extended(self, item_list, /) :
        '''NOT IN PLACE'''
        return self.copy().extend(item_list)

    def popIndex(self, index = -1, /) :
        '''L.pop([index]) -> item -- remove and return item at index (default last).
        Raises IndexError if list is empty or index is out of range.'''
        '''IN PLACE'''
        return list.pop(self, index)

    def poppedIndex(self, index = -1, /) :
        '''NOT IN PLACE'''
        return self.copy().popIndex(index)

    def dropItem(self, item, /) :
        '''L.remove(value) -> None -- remove first occurrence of value.
        Raises ValueError if the value is not present.'''
        '''IN PLACE'''
        list.remove(self, item)
        return self

    def droppedItem(self, item, /) :
        '''NOT IN PLACE'''
        return self.copy().dropItem()
    
    def __reversed__(self) :
        '''
        L.__reversed__() -- return a reverse iterator over the list
        '''
        return list.__reversed__(self)

    def reverse(self) :
        '''L.reverse() -> None -- reverse *IN PLACE*'''
        '''IN PLACE'''
        list.reverse(self)
        return self

    def reversed(self) :
        '''NOT IN PLACE'''
        return self.copy().reverse()

    def sort(self, key_func_or_attr_name = None, /, *, reverse = False) :
        '''L.sort(key=None, reverse=False) -> None -- stable sort *IN PLACE*'''
        '''IN PLACE'''
        if callable(key_func_or_attr_name) or key_func_or_attr_name is None :
            list.sort(self, key = key_func_or_attr_name, reverse = reverse)
        elif isinstance(key_func_or_attr_name, str) :
            key_func = lambda _ : _.__getattr__(key_func_or_attr_name)
            list.sort(self, key = key_func, reverse = reverse)
        else : raise UserTypeError(key_func_or_attr_name)
        return self

    def sorted(self, key_func_or_attr_name = None, /, *, reverse = False) :
        '''NOT IN PLACE'''
        return self.copy().sort(key_func_or_attr_name, reverse = reverse)

    def shuffle(self) :
        '''IN PLACE'''
        import random
        random.shuffle(self)
        return self

    def shuffled(self) :
        '''NOT IN PLACE'''
        return self.copy().shuffle()

    def enumerate(self) :
        return enumerate(self)

    def enum(self) :
        return enumerate(self)

    # pos为index在func的参数表里的下标，即本函数在func的参数表的下标
    def _leftPadIndexToArgs(self, func, args, index, pos, /) :
        import inspect
        if inspect.isclass(func) :
            func = func.__init__
            pos += 1
        func_args = list(inspect.signature(func).parameters.values())
        if len(func_args) > pos and func_args[pos].name == 'index' :
            return [ index ] + list(args)
        else :
            return args

    def forEach(self, func, /, *args, **kwargs) :
        '''NOT IN PLACE'''
        for index, item in self.enum() :
            func(item, *(self._leftPadIndexToArgs(func, args, index, 1)), **kwargs)
        return self

    # @ensureArgsType
    def batch(self, func_name: str, /, *args, **kwargs) :
        '''IN PLACE'''
        for index, item in self.enum() :
            attribute = self[index].__getattribute__(func_name)
            if callable(attribute) :
                self[index] = attribute(*(self._leftPadIndexToArgs(attribute, args, index, 0)), **kwargs)
            else : self[index] = attribute
        return self

    def batched(self, func_name, /, *args, **kwargs) :
        '''NOT IN PLACE'''
        return self.copy().batch(func_name, *args, **kwargs)

    def map(self, func, /, *args, **kwargs) :
        '''IN PLACE'''
        for index, item in self.enum() :
            self[index] = func(item, *(self._leftPadIndexToArgs(func, args, index, 1)), **kwargs)
        return self

    def mapped(self, func, /, *args, **kwargs) :
        '''NOT IN PLACE'''
        return self.copy().map(func, *args, **kwargs)

    # @ensureArgsType
    # @Timer.timeitTotal('valueList')
    def valueList(self, key_list_or_func_name: Union[list, str], /, *, default = None) :
        '''NOT IN PLACE'''
        '''可以允许字段不存在'''
        self._importTypes()
        if self.len() == 0 : return self.copy()
        if isinstance(key_list_or_func_name, list) :
            if isinstance(self[0], self._Object) :
                return self.batched('_get', key_list_or_func_name)
            else :
                return self.batched('get', key_list_or_func_name)
        elif isinstance(key_list_or_func_name, str) :
            def getValue(item) :
                try :
                    if key_list_or_func_name in dir(item) and callable(attribute := item.__getattribute__(key_list_or_func_name)) :
                        return attribute()
                except AttributeError as e :
                    raise e
                except Exception as e :
                    raise e
                if isinstance(item, self._Dict) :
                    attribute = item.__getattr__(key_list_or_func_name) # 可以允许字段不存在
                elif isinstance(item, self._Object) :
                    try :
                        attribute = item.__getattr__(key_list_or_func_name)
                    except Exception as e :
                        attribute = self._wrapItem(default) # 可以允许字段不存在
                else :
                    try :
                        attribute = item.__getattribute__(key_list_or_func_name)
                    except AttributeError :
                        from util import P, E
                        raise Exception(f'{P()}{type(item)=}{E()} has no attribute {P(key_list_or_func_name)}; 请检查是否采用了错误的调用方式：xList.yList.z; {self=}; {item=}')
                    except Exception as e :
                        raise e
                return attribute
            return self.mapped(getValue)
        else : raise UserTypeError(key_list_or_func_name)

    def format(self, pattern, /) :
        '''NOT IN PLACE'''
        return self.mapped(lambda _ : pattern.format(_))

    def _stripItem(self, item, string, /) :
        self._importTypes()
        if item is None or isinstance(item, (int, float, bool, range, bytes, zip, self._datetime)):
            return item
        elif isinstance(item, (self._List, self._Dict, self._Str)) : # can't be list, dict, str
            return item.strip(string)
        elif isinstance(item, tuple) :
            return (self._stripItem(_, string) for _ in item)
        elif isinstance(item, set) :
            return set([self._stripItem(_, string) for _ in item])
        elif isinstance(item, object) :
            if 'strip' in dir(item) : item.strip(string)
            return item
        else :
            raise UserTypeError(item)

    def strip(self, string = ' \t\n', /) :
        '''IN PLACE'''
        return self.map(self._stripItem, string)

    def stripped(self, string = ' \t\n', /) :
        '''NOT IN PLACE'''
        return self.copy().strip(string)

    def replaceStrList(self, sub_or_pattern, repl_str_func, /, *, re_mode: bool, count = None, flags = 0) :
        '''IN PLACE'''
        from Str import Str
        return self.map(Str.replace, sub_or_pattern, repl_str_func, re_mode = re_mode, count = count, flags = flags)

    def replacedStrList(self, sub_or_pattern, repl_str_func, /, *, re_mode: bool, count = None, flags = 0) :
        '''NOT IN PLACE'''
        return self.copy().replaceStrList()

    def filter(self, func_or_func_name, /, *args, **kwargs) :
        '''IN PLACE'''
        index = 0
        if isinstance(func_or_func_name, str) :
            while index < self.len() :
                if self[index].__getattribute__(func_or_func_name)(*args, **kwargs) : index += 1
                else : self.popIndex(index)
        else :
            while index < self.len() :
                if func_or_func_name(self[index], *args, **kwargs) : index += 1
                else : self.popIndex(index)
        return self

    def filtered(self, func_or_func_name, /, *args, **kwargs) :
        '''NOT IN PLACE'''
        return self.copy().filter(func_or_func_name, *args, **kwargs)

    # @ensureArgsType
    def filterByValue(self, key_list_or_func_name: Optional[Union[list, str]], value_or_list, /) :
        '''IN PLACE'''
        self._importTypes()
        if not isinstance(value_or_list, list) :
            value_or_list = [ value_or_list ]
        if key_list_or_func_name is None :
            return self.filter(lambda item : item in value_or_list)
        elif isinstance(key_list_or_func_name, list) :
            if isinstance(self[0], self._Object) :
                return self.filter(lambda item : item._data.get(key_list_or_func_name) in value_or_list)
            else :
                return self.filter(lambda item : item.get(key_list_or_func_name) in value_or_list)
        elif isinstance(key_list_or_func_name, str) :
            def getValue(item) :
                if isinstance(item, self._Object) :
                    attribute = item.__getattr__(key_list_or_func_name)
                else :
                    attribute = item.__getattribute__(key_list_or_func_name)
                if callable(attribute) : return attribute()
                else : return attribute
            return self.filter(lambda item : getValue(item) in value_or_list)
        else : raise UserTypeError(key_list_or_func_name)

    def filteredByValue(self, key_list_or_func_name, value_or_list, /) :
        '''NOT IN PLACE'''
        return self.copy().filterByValue(key_list_or_func_name, value_or_list)

    def reduce(self, func, initial_value, /, *args, **kwargs) :
        '''NOT IN PLACE'''
        result = initial_value
        for index, item in self.enum() :
            result = func(result, item, *(self._leftPadIndexToArgs(func, args, index, 2)), **kwargs)
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

    def groupBy(self, key_func = None, /, *, value_func = None) :
        from itertools import groupby
        from Dict import Dict
        result = Dict()
        for k, g in groupby(self.sorted((lambda _ : f'{_}' if _ is not None else '') if key_func is None else key_func), key = key_func) :
            if value_func is None :
                result[k] = List(g)
            else :
                result[k] = List(value_func(item) for item in g)
        return result
    
    def countBy(self, key_func = None, /) :
        from Dict import Dict
        return Dict((k, g.len()) for k, g in self.groupBy(key_func).items())

    # @ensureArgsType
    def _reduce(self, key_list_or_func_name: Optional[Union[list, str]], func, initial_value, /) :
        '''NOT IN PLACE'''
        if key_list_or_func_name is None :
            return self.reduce(func, initial_value)
        elif isinstance(key_list_or_func_name, (list, str)) :
            return self.valueList(key_list_or_func_name).reduce(func, initial_value)
        else : raise UserTypeError(key_list_or_func_name)

    def sum(self, key_list_or_func_name = None, /) :
        '''NOT IN PLACE'''
        if self.len() == 0 : return 0
        return self._reduce(key_list_or_func_name, lambda result, item : result + item, 0)

    def mean(self, key_list_or_func_name = None, /, *, default = None) :
        '''NOT IN PLACE'''
        if self.len() == 0 : return default
        return 1.0 * self.sum(key_list_or_func_name) / self.len()

    # @ensureArgsType
    def _initialValue(self, key_list_or_func_name: Optional[Union[list, str]], /) :
        '''NOT IN PLACE'''
        if key_list_or_func_name is None :
            return self[0]
        elif isinstance(key_list_or_func_name, list) :
            if isinstance(self[0], self._Object) :
                return self[0]._data.get(key_list_or_func_name)
            else :
                return self[0].get(key_list_or_func_name)
        elif isinstance(key_list_or_func_name, str) :
            if isinstance(self[0], self._Object) :
                attribute = self[0].__getattr__(key_list_or_func_name)
            else :
                attribute = self[0].__getattribute__(key_list_or_func_name)
            if callable(attribute) : return attribute()
            else : return attribute
        else : raise UserTypeError(key_list_or_func_name)

    def max(self, key_list_or_func_name = None, /) :
        '''NOT IN PLACE'''
        if self.len() == 0 : return None
        return self._reduce(key_list_or_func_name,
            lambda result, item : item if item > result else result,
            self._initialValue(key_list_or_func_name)
        )

    def min(self, key_list_or_func_name = None, /) :
        '''NOT IN PLACE'''
        if self.len() == 0 : return None
        return self._reduce(key_list_or_func_name,
            lambda result, item : item if item < result else result,
            self._initialValue(key_list_or_func_name)
        )

    # @ensureArgsType
    def join(self, sep: str = '', /) :
        '''NOT IN PLACE'''
        self._importTypes()
        return self._Str(sep).join(self)

    def unique(self) :
        '''IN PLACE'''
        '''O(??)'''
        _ = list(set(self))
        return self.clear().extend(_)

    def uniqued(self) :
        '''NOT IN PLACE'''
        return self.copy().unique()

    # @ensureArgsType
    def intersect(self, item_list: list, /) :
        '''Update itself with the intersection of itself and another.'''
        '''IN PLACE'''
        '''O(N^2)???'''
        return self.filter(lambda item, item_list : item in item_list, List(item_list))

    def intersected(self, item_list, /) :
        '''NOT IN PLACE'''
        return self.copy().intersect(item_list)

    def __and__(self, item_list) :
        '''x.__and__(y) <==> x&y'''
        '''NOT IN PLACE'''
        return self.intersected(item_list)

    # @ensureArgsType
    def difference(self, item_list: list, /) :
        '''Remove all elements of another list from this list.'''
        '''IN PLACE'''
        '''O(N^2)???'''
        return self.filter(lambda item, item_list : item not in item_list, List(item_list))

    def differenced(self, item_list, /) :
        '''NOT IN PLACE'''
        return self.copy().difference(item_list)

    def __sub__(self, item_list) :
        '''x.__sub__(y) <==> x-y'''
        '''NOT IN PLACE'''
        return self.differenced(item_list)

    # @ensureArgsType
    def union(self, item_list: list, /) :
        '''Update a set with the union of itself and others.'''
        '''IN PLACE'''
        '''O(N^2)???'''
        return self.extend(List(item_list).difference(self))

    def unioned(self, item_list, /) :
        '''NOT IN PLACE'''
        return self.copy().union(item_list)

    def __or__(self, item_list) :
        '''x.__or__(y) <==> x|y'''
        '''NOT IN PLACE'''
        return self.unioned(item_list)

    def isDisjointFrom(self, item_list, /) :
        '''Return True if two lists have a null intersection.'''
        '''O(N^2)???'''
        return (self & item_list).len() == 0

    def isSubsetOf(self, item_list, /) :
        '''Report whether another set contains this set.'''
        '''O(N^2)???'''
        return (self - item_list).len() == 0

    def __le__(self, item_list) :
        '''Return self<=value.'''
        return self.isSubsetOf(item_list)

    def __lt__(self, item_list) :
        '''Return self<value.'''
        raise NotImplementedError

    def isSupersetOf(self, item_list, /) :
        '''Report whether this set contains another set.'''
        '''O(N^2)???'''
        return (List(item_list) - self).len() == 0

    def __ge__(self, item_list) :
        '''Return self>=value.'''
        return self.isSupersetOf(item_list)

    def __gt__(self, item_list) :
        '''Return self>value.'''
        raise NotImplementedError

    def isSameSetOf(self, item_list, /) :
        return self <= item_list and self >= item_list

    def __eq__(self, item_list) :
        '''Return self==value.'''
        raise NotImplementedError

    def __ne__(self, item_list) :
        '''Return self!=value.'''
        raise NotImplementedError

    def clear(self) :
        '''L.clear() -> None -- remove all items from L'''
        '''IN PLACE'''
        list.clear(self)
        return self
    
    def writeToFile(self, file, /, *, indent = True) :
        file.writeString(self.j(indent = indent))
        return self

    def writeLineListToFile(self, file, /) :
        file.writeLineList(self)
        return self

    # list(map(lambda x : print(f'\n{x}\n{list.__getattribute__([], x).__doc__}\n'), dir(list)))

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
