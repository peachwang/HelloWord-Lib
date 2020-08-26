# -*- coding: utf-8 -*-  
from ..shared             import *
from ..datatypes.Str      import Str
from ..datatypes.DateTime import TimeDelta
from ..datatypes.List     import List
from ..datatypes.Dict     import Dict

class Counter :

    def __init__(self, name, key_list = None) :
        self._name = name
        self._key_to_value_list = Dict()
        self._key_to_sum        = Dict()
        if key_list is not None :
            for key in key_list : self._init(key)

    @cached_prop
    def name(self) -> Str : return Str(self._name)

    def _init(self, key, /) :
        if isinstance(key, tuple) :
            self._key_to_value_list[key[0]] = List()
            self._key_to_sum[key[0]]        = key[1]
        else :
            self._key_to_value_list[key] = List()
            self._key_to_sum[key]        = 0
        return self

    def __getitem__(self, key, /) : return self._key_to_sum[key]

    def __getattr__(self, key, /) : return self.__getitem__(key)

    def __format__(self, spec) : return f"{f'Counter(name = {self._name}, key_to_sum = {self._key_to_sum})':{spec}}"

    def value_list(self, key, /) : return self._key_to_value_list[key]

    def keys(self) : return self._key_to_value_list.keys()
    
    def __iter__(self) : return self.keys().iter()
    
    def iter(self) : return self.__iter__()
    
    def items(self) : return self._key_to_sum.items()

    # def __add__
    # def __iadd__
    # def __sub__
    # def __isub__
    # https://python3-cookbook.readthedocs.io/zh_CN/latest/c01/p12_determine_most_freqently_items_in_seq.html

    def add(self, key, value, /) :
        if key not in self._key_to_value_list : self._init(key)
        self._key_to_value_list[key].append(value)
        if isinstance(value, (int, float, TimeDelta)) : self._key_to_sum[key] = value + self._key_to_sum[key]
        return self

    def set(self, key, value, /) :
        self._key_to_value_list[key] = List([value])
        if isinstance(value, (int, float, TimeDelta)) : self._key_to_sum[key] = value
        return self

    def num(self, key, /) : return len(self._key_to_value_list[key])

    def len(self, key, /) : return self.num(key)
    
    def ave(self, key, /, *, default = 0) : return self._key_to_value_list[key].ave(default = default)

    def max(self, key, /, *, default = None) : return self._key_to_value_list[key].max(default = default)
    
    def min(self, key, /, *, default = None) : return self._key_to_value_list[key].min(default = default)