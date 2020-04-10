# -*- coding: utf-8 -*-
import bson
from ..shared import *

# https://api.mongodb.com/python/current/api/bson/objectid.html
class ObjectId(bson.objectid.ObjectId) :

    # Checks if a oid string is valid or not.
    @classmethod
    def is_valid(cls, string) -> bool : super().is_valid(cls, string)

    def __init__(self, string = None) : super().__init__(string)

    @log_entering()
    def __format__(self, spec) : return f'{super().__str__():{spec}}' # 不用 super().__format__
    
    # Get a hex encoded version of ObjectId o.
    @log_entering()
    def __str__(self) : return f'ObjectId("{super().__str__()}")'
    
    @log_entering()
    def __repr__(self) : return f'ObjectId("{super().__str__()}")'

    def json_serialize(self) -> dict : return { '$id' : super().__str__() }

    # A datetime.datetime instance representing the time of generation for this ObjectId.
    # The datetime.datetime is timezone aware, and represents the generation time in UTC. It is precise to the second.
    @cached_prop
    def datetime(self) : from .DateTime import DateTime; return DateTime(super().generation_time)

    # 12-byte binary representation of this ObjectId.
    @cached_prop
    def binary(self) -> bytes : return super().binary

if __name__ == '__main__':
    print(type(eval(repr(ObjectId('5e452a91e154a7275a8b46a0')))))