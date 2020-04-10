# -*- coding: utf-8 -*-
import json
from ..shared    import *
from ..datatypes import *

class CustomDecoder(json.JSONDecoder) :

    def object_hook(dct) :
        if len(dct) == 1 and '$id' in dct                   : return ObjectId(dct['$id'])
        if len(dct) == 2 and 'sec' in dct and 'usec' in dct : return DateTime(dct['sec'] + dct['usec'] / 1000000)
        if '__type__' in dct                                :
            if dct['__type__'] in ('tuple', 'set')                                   : return eval(dct['__type__'])(dct['__data__'])
            if dct['__type__'] == 'bytes'                                            : return dct['__data__'].encode('utf-8')
            if dct['__type__'].lower() == 'timedelta'                                : return TimeDelta(**dct['__data__'])
            if dct['__type__'].lower() == 'date'                                     : return Date(dct['__data__'])
            if dct['__type__'].lower() == 'time'                                     : return Time(dct['__data__'], '%H:%M:%S.%f')
            if dct['__type__'] == 'DateList'                                         : return DateList(dct['__data__'])
            if dct['__type__'] == 'DateRange'                                        : return DateRange(*dct['__data__'])
            if dct['__type__'] in ('Year', 'Month', 'Week')                          : return eval(dct['__type__'])(*dct['__data__'])
            # if dct['__type__'].lower() == 'datetime'                                 : return DateTime(*dct['__data__'])
            if dct['__type__'] == 'File'                                             : return File(dct['__data__'])
            if dct['__type__'] == 'Folder'                                           : return Folder(dct['__data__'])
            if dct['__type__'] == 'range'                                            : return range(*dct['__data__'])
            if dct['__type__'] == 'type'                                             : return eval(dct['__data__'])
            raise Exception(f'无法解析 {dct =}')
        return dct

    def decode(self, string) :
        try                              : return super().decode(string)
        except json.JSONDecodeError as e :
            if e.pos > 100               : start = e.pos - 100
            else                         : start = 0
            if e.pos + 100 <= len(e.doc) : end   = e.pos + 100
            else                         : end   = len(e.doc)
            msg = {
                # "Expecting ',' delimiter" : '逗号缺失或位置错误',
                # "Expecting ':' delimiter" : '冒号缺失或位置错误',
            }.get(e.msg, e.msg)
            print(f'无法解析 json 中第 {C(e.lineno)} 行，第 {C(e.colno)} 列，第 {C(e.pos)} 个字符的位置 {C(msg)} :\n{e.doc[start : e.pos]}{C(e.doc[e.pos])}{e.doc[e.pos + 1 : end]}')
            raise e

def raw_load_json_file(fp) -> object : return json.load(fp, cls = CustomDecoder, object_hook = CustomDecoder.object_hook)

def raw_load_json_str(string) -> object : return json.loads(string, cls = CustomDecoder, object_hook = CustomDecoder.object_hook)

def raw_load_json_stdin() -> object : import sys; return raw_load_json_file(sys.stdin)

class CustomEncoder(json.JSONEncoder) :

    def default(self, obj) -> object :
        type_to_str = lambda _type : str(_type).split('.')[1][ : -2] if '.' in str(_type) else str(_type)[8 : -2]
        wrap_dct    = lambda _obj, _data : { '__type__' : type_to_str(type(_obj)), '__data__' : _data }
        if isinstance(obj, Str)                                      : return str(obj)
        if isinstance(obj, (List, Dict))                             : return obj.jsonSerialize()
        if isinstance(obj, Object)                                   : return wrap_dct(obj, obj.jsonSerialize())
        if isinstance(obj, (type(None), str, int, float, bool))      : return obj
        if isinstance(obj, (ObjectId, DateTime))                     : return obj.jsonSerialize()
        if isinstance(obj, (tuple, set))                             : return wrap_dct(obj, list(obj))
        if isinstance(obj, bytes)                                    : return wrap_dct(obj, str(obj)[2 : -1])
        if isinstance(obj, datetime_class)                           : return DateTime(obj).jsonSerialize()
        if isinstance(obj, (TimeDelta, Date, Time, File, Folder))    : return wrap_dct(obj, obj.jsonSerialize())
        if isinstance(obj, timedelta_class)                          : return wrap_dct(obj, TimeDelta(obj).jsonSerialize())
        if isinstance(obj, date_class)                               : return wrap_dct(obj, Date(obj).jsonSerialize())
        if isinstance(obj, time_class)                               : return wrap_dct(obj, Time(obj).jsonSerialize())
        if isinstance(obj, (DateList, DateRange, Year, Month, Week)) : return wrap_dct(obj, obj.jsonSerialize())
        if 'jsonSerialize' in dir(obj)                               : return wrap_dct(obj, obj.jsonSerialize())
        if isinstance(obj, range)                                    : return wrap_dct(obj, [obj.start, obj.stop, obj.step])
        if isinstance(obj, type)                                     : return wrap_dct(obj, type_to_str(obj))
        if isinstance(obj, (zip, slice))                             : raise TypeError('无法序列化 zip, slice')
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

    # @log_entering('{0}')
    # def encode(self, obj) -> str :
        # if isinstance(obj, dict) : return super().encode({ str(key) : obj[key] for key in obj })
        # else                     : return super().encode(obj)

def raw_dump_json_file(obj, fp, /, *, indent = True) -> None :
    json.dump(obj, fp, indent = 4 if indent is True else (None if indent is False else indent), ensure_ascii = False, sort_keys = True, cls = CustomEncoder)

def raw_dump_json_str(obj, /, *, indent = True) -> str :
    return json.dumps(obj, indent = 4 if indent is True else (None if indent is False else indent), ensure_ascii = False, sort_keys = True, cls = CustomEncoder)

j = raw_dump_json_str

if __name__ == '__main__':
    string = '''
[
    [
        {
            "__data__": {
                "days": 10,
                "microseconds": 0,
                "seconds": 20
            },
            "__type__": "TimeDelta"
        },
        {
            "__data__": "2020-10-30",
            "__type__": "Date"
        },
        {
            "__data__": "20:30:00.000000",
            "__type__": "Time"
        },
        {
            "sec": 1604061000,
            "usec": 0
        }
    ],
    [
        {
            "__data__": {
                "days": 10,
                "microseconds": 0,
                "seconds": 20
            },
            "__type__": "TimeDelta"
        },
        {
            "__data__": "2020-10-30",
            "__type__": "Date"
        },
        {
            "__data__": "20:30:00.000000",
            "__type__": "Time"
        },
        {
            "sec": 1604061000,
            "usec": 0
        }
    ]
]
'''
    # List(raw_load_json_str(string)).printStr()
    # print(dir(ObjectId('5e452a91e154a7275a8b46a0')))
    o = ObjectId('5e452a91e154a7275a8b46a0')
    # print(o)
    # print(o, o._inc, o._inc_lock, o._machine_bytes, o._type_marker, o.binary, o.datetime)
    # List([o.binary]).printStr()
    
    # print(type(
    a = List(raw_load_json_str(j([
    # print(j([
        {1,2,3},
        o,
        o.binary,
        (
            timedelta_class(days=10, seconds=20),
            date_class(year=2020, month=10, day=30),
            time_class(hour=20, minute=30),
            datetime_class(year=2020, month=10, day=30, hour=20, minute=30,second=30,microsecond=123456),
        ),
        (
            TimeDelta(days=10, seconds=20),
            Date(year=2020, month=10, day=30),
            Time(hour=20, minute=30),
            DateTime(year=2020, month=10, day=30, hour=20, minute=30),
        )
    ])))[4][3]
    # ))
    # ]))
    print(eval(repr(a)) == a)