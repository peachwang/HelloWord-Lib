# -*- coding: utf-8 -*-
from bson.objectid import ObjectId as objectid
from ..shared import *

# https://api.mongodb.com/python/current/api/bson/objectid.html
@add_print_func
class ObjectId(objectid) :

    # Checks if a oid string is valid or not.
    @classmethod
    def is_valid(cls, string) -> bool : objectid.is_valid(cls, string)

    def __init__(self, string = None) : objectid.__init__(self, string)

    @log_entering()
    def __format__(self, spec) : return f'{objectid.__str__(self):{spec}}' # 不用 objectid.__format__
    
    # Get a hex encoded version of ObjectId o.
    @log_entering()
    def __str__(self) : return f'ObjectId("{objectid.__str__(self)}")'
    
    @log_entering()
    def __repr__(self) : return f'ObjectId("{objectid.__str__(self)}")'

    def json_serialize(self) -> dict : return { '$id' : objectid.__str__(self) }

    # A datetime.datetime instance representing the time of generation for this ObjectId.
    # The datetime.datetime is timezone aware, and represents the generation time in UTC. It is precise to the second.
    @cached_prop
    def datetime(self) : from .DateTime import DateTime; return DateTime(self.generation_time)

    # 12-byte binary representation of this ObjectId.
    @cached_prop
    def binary(self) -> bytes : return self.binary

if __name__ == '__main__':
    print(type(eval(repr(ObjectId('5e452a91e154a7275a8b46a0')))))