# -*- coding: utf-8 -*-  
from ..shared             import *
from ..datatypes.DateTime import DateTime
from ..datatypes.Dict     import Dict
from ..datatypes.List     import List
from ..datatypes.Iter     import Iter
# https://docs.python.org/3/library/collections.html#collections.Counter
# https://github.com/python/cpython/blob/3.8/Lib/collections/__init__.py#L489

@iterable
class Counter :

    def __init__(self, name, key_iterable = None) :
        self._name = name
        self._key_to_value_list = Dict()
        self._key_to_sum        = Dict()
        if key_iterable is not None :
            for key in key_iterable : self._init(key)

    # __missing__

    @cached_prop
    def name(self) -> str         : return self._name

    def _init(self, key, /)       :
        self._key_to_value_list[key] = List()
        self._key_to_sum[key]        = 0
        return self

    def __getitem__(self, key, /) : return self._key_to_sum[key]

    def __getattr__(self, key, /) : return self.__getitem__(key)

    def __format__(self, spec)    : return f'{f"{type(self).__name__}(name = {self._name}, key_to_sum = {self._key_to_sum})":{spec}}'

    def value_list(self, key, /)  : return self._key_to_value_list[key]

    def keys(self)                : return self._key_to_value_list.keys()
    
    def items(self)               : return self._key_to_sum.items()
    
    def __iter__(self) -> Iter    : return self.keys().iter
    
    def is_empty(self)            : return self._key_to_value_list.is_empty()

    # def __add__
    # def __iadd__
    # def __sub__
    # def __isub__
    # https://python3-cookbook.readthedocs.io/zh_CN/latest/c01/p12_determine_most_freqently_items_in_seq.html

    def add(self, key, value, /)  :
        if key not in self._key_to_value_list : self._init(key)
        self._key_to_value_list[key].append(value)
        if not isinstance(value, DateTime) : self._key_to_sum[key] = value + self._key_to_sum[key]
        return self

    def set(self, key, value, /)  :
        self._key_to_value_list[key] = List([value])
        if not isinstance(value, DateTime) : self._key_to_sum[key] = value
        return self

    def num(self, key, /)                    : return self._key_to_value_list[key].len

    def len(self, key, /)                    : return self.num(key)
    
    def ave(self, key, /, *, default = 0)    : return self._key_to_value_list[key].iter.ave(default = default)

    def max(self, key, /, *, default = None) : return self._key_to_value_list[key].iter.max(default = default)
    
    def min(self, key, /, *, default = None) : return self._key_to_value_list[key].iter.min(default = default)