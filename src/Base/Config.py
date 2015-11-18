# -*- coding: utf-8 -*-  
import sys, os; sys.path.extend([os.path.abspath(_[0]) for _ in os.walk(os.path.join(os.getcwd(), '../'))]);
from util import *

class Config :

    def __init__(self, original_path) :
        self.config = {}
        self.original_path = original_path
        self.__recursive_merge(self.original_path)

    def __recursive_merge(self, path) :
        config = load_json(open(config_path))
        if config.get('_Path_Parent') is not None :
            path_parent = config['_Path_Parent']
            if type(path_parent) == str :
                path_parent = [path_parent]
            for path in path_parent :
                self.__recursive_merge(path)
        self.config.update(config)
        return self

    def clear(self) :
        self.config = {}
        self.original_path = None
        return self

    def has(self, key) :
        return self.config.has_key(key)

    def __get__(self, key) :
        return self.get(key)

    def get(self, key, default = None) :
        if self.config.get(key) is None :
            return default
        else :
            return self.config[key]

    def __set__(self, key, value) :
        self.set(key, value)
    
    def set(self, key, value) :
        self.config[key] = value
        return self

    def unset(self, key) :
        if self.config.has_key(key) :
            self.config.pop(key)
        return self

