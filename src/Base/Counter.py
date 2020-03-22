# -*- coding: utf-8 -*-  
from util import List, Dict, Str, Object, json, Optional, Union, ensureArgsType, UserTypeError, _print, R

class Counter(Object) :

    def __init__(self, name, key_list = None) :
        super().__init__()
        self._registerProperty(['name'])
        self._name = name
        self._key_to_value_list = Dict()
        self._key_to_sum        = Dict()
        if key_list is not None :
            for key in key_list :
                self._key_to_value_list[key] = List()
                self._key_to_sum[key]        = 0

    def __getitem__(self, key, /) :
        return self._key_to_sum[key]

    def __getattr__(self, key, /) :
        
        if Object.__getattr__(self, '_key_to_value_list').has(key) :
            return self.__getitem__(key)
        else :
            return Object.__getattr__(self, key)

    def valueList(self, key, /) :
        return self._key_to_value_list[key]

    def __iter__(self) :
        return self._key_to_value_list.keys().iter()

    def iter(self) :
        return self.__iter__()

    def keys(self) :
        return self._key_to_value_list.keys()

    def items(self) :
        return List((key, self[key]) for key in self)

    def add(self, key, value, /) :
        if self._key_to_value_list.hasNo(key) :
            self._key_to_value_list[key] = List()
            self._key_to_sum[key]        = 0
        self._key_to_value_list[key].append(value)
        self._key_to_sum[key] += value
        return self

    def set(self, key, value, /) :
        self._key_to_value_list[key] = List(value)
        self._key_to_sum[key]        = value
        return self

    def num(self, key, /) : return self._key_to_value_list[key].len()

    def len(self, key, /) : return self.num(key)
    
    def ave(self, key, /) : return self._key_to_value_list[key].ave()

    def max(self, key, /) : return self._key_to_value_list[key].max()
    
    def min(self, key, /) : return self._key_to_value_list[key].min()