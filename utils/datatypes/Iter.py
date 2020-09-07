# -*- coding: utf-8 -*-  
from ..shared import *

class Iter :

    def __init__(self, iterable, /) :
        self.iterator = iter(iterable)

    def __iter__(self) : return self

    def __next__(self) : return next(self.iterator)

    def map(self, func) : return Iter(map(func, self))
    # def filter(self)
