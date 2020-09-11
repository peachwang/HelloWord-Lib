# -*- coding: utf-8 -*-  
from ..shared import *
from itertools import chain, filterfalse
from more_itertools import consume
# https://more-itertools.readthedocs.io/en/stable/api.html

class Iter :

    _no_value = object()

    def __init__(self, item_iterable, /) : self._iterator = iter(item_iterable)

    def __iter__(self)                   : return self

    def __next__(self)                   : return next(self._iterator)

    def enum(self)                       : return Iter(enumerate(self))

    def map(self, func)                  : return Iter(map(func, self))
    def foreach
    def filter
    def filter_one
    def print_line

    def is_empty
    def merge
    def unique
    def prepend
    def head
    def join
    def sort() : return Iter(sorted(self))

    # def filter(self)
    
    # pos为index在func的参数表里的下标，即本函数在func的参数表的下标
    def _left_pad_index_to_args(self, func, args, index, pos, /) :
        if isclass(func)                                           : func = func.__init__; pos += 1
        func_args = list(signature(func).parameters.values())
        if len(func_args) > pos and func_args[pos].name == 'index' : return [ index ] + list(args)
        else                                                       : return args

    def reduce(self, func, initial_value, /, *args, **kwargs) :
        result = initial_value
        for index, item in enumerate(self) :
            result = func(result, item, *(self._left_pad_index_to_args(func, args, index, 2)), **kwargs)
        return result

    # 可以允许字段不存在
    @iter_func
    def value_iter(self, attr_or_func_name: str, /, *, default = None) :
        from .List   import List
        if isinstance(attr_or_func_name, str) :
            for item in self :
                yield List.get_value(item, attr_or_func_name, default)
        else                                  : raise TypeError(attr_or_func_name)

    def _reduce(self, attr_or_func_name: Optional[str], func, initial_value, /, *, default = _no_value) :
        return self.value_iter(attr_or_func_name, default = default).reduce(func, initial_value)

    def sum(self, attr_or_func_name: Optional[str] = None, /, *, initial_or_empty_value = 0, default = _no_value) :
        return self._reduce(attr_or_func_name, lambda result, item : item + result, initial_or_empty_value, default = default)
