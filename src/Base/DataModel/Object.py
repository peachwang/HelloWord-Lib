# -*- coding: utf-8 -*-  

from DataModel.List import List
from DataModel.Dict import Dict

class Object() :
    
    def __init__(self) :
        object.__setattr__(self, '_data', Dict())

    def __getattr__(self, name) :
        if name == '_data' : return self.__getattribute__('_data')
        return self._data[name]

    def __setattr__(self, name, value) :
        if type(value) is list : self._data[name] = List(value)
        elif type(value) is dict : self._data[name] = Dict(value)
        else : self._data[name] = value
        return value

    def _update(self, mapping) :
        self._data.update(mapping)
        return self

    def _get(self, name_list, default = None) :
        return self._data.get(name_list, default)

    def _getMulti(self, name_list) :
        return self._data.getMulti(name_list)

    def _has(self, name_list) :
        return self._data.has(name_list)


if __name__ == '__main__':
    pass