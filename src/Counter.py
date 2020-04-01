# -*- coding: utf-8 -*-  
from shared import *
from DateTime import DateTime
from List import List

class Counter :

    def __init__(self, name, key_list = None) :
        self._name = name
        self._key_to_value_list = {}
        self._key_to_sum        = {}
        if key_list is not None :
            for key in key_list : self._init(key)

    def _init(self, key, /) :
        self._key_to_value_list[key] = []
        self._key_to_sum[key]        = 0
        return self

    def __getitem__(self, key, /) : return self._key_to_sum[key]

    def __getattr__(self, key, /) : return self.__getitem__(key)

    def __format__(self, code) : return f'Counter(name = {self._name}, key_to_sum = {self._key_to_sum})'

    def valueList(self, key, /) : return self._key_to_value_list[key]

    def keys(self) : return List(self._key_to_value_list.keys())
    
    def __iter__(self) : return self.keys().iter()
    
    def iter(self) : return self.__iter__()
    
    def items(self) : return List((key, self[key]) for key in self)

    def add(self, key, value, /) :
        if key not in self._key_to_value_list : self._init(key)
        self._key_to_value_list[key].append(value)
        if not isinstance(value, DateTime) : self._key_to_sum[key] = value + self._key_to_sum[key]
        return self

    def set(self, key, value, /) :
        self._key_to_value_list[key] = [value]
        if not isinstance(value, DateTime) : self._key_to_sum[key] = value
        return self

    def num(self, key, /) : return len(self._key_to_value_list[key])

    def len(self, key, /) : return self.num(key)
    
    def ave(self, key, /) : return List(self._key_to_value_list[key]).ave()

    def max(self, key, /) : return List(self._key_to_value_list[key]).max()
    
    def min(self, key, /) : return List(self._key_to_value_list[key]).min()