# -*- coding: utf-8 -*-  

from DataModel.List import List
from DataModel.Dict import Dict

class Object() :
    
    def __init__(self) :
        object.__setattr__(self, 'data', Dict())

    def __getattr__(self, name) :
        if name == 'data' : return self.__getattribute__('data')
        return self.data[name]

    def __setattr__(self, name, value) :
        if type(value) is list : self.data[name] = List(value)
        elif type(value) is dict : self.data[name] = Dict(value)
        else : self.data[name] = value
        return value

    def _update(self, mapping) :
        self.data.update(mapping)
        return self

    def _getMulti(self, name_list) :
        return self.data.getMulti(name_list)


if __name__ == '__main__':
    pass