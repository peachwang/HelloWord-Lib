# -*- coding: utf-8 -*-  
import sys, os; sys.path.append(os.path.realpath(__file__ + '/../DataModel/'));

import json, re, requests
from sys import exit
from Color import G, Y, R, B, P, W, E, GREEN as _G, YELLOW as _Y, RED as _R, BLUE as _B, PINK as _P, WHITE as _W, END as _E
from functools import wraps, cached_property, lru_cache
from shared import ensureArgsType, UserTypeError, _print
from typing import Optional, Union
from Object import Object
from List import List
from Dict import Dict
from Str import Str
from DateTime import DateTime, datetime, timedelta, time
from Timer import Timer
from File import File
from Audio import Audio
from Folder import Folder, makedirs as mkdir
from LineStream import LineStream

# ==================== Data ====================

# delete
def load_mapping(fin) :
    data = {}
    current = None
    for line in fin :
        line = line.strip('\n\r')
        if line.strip(' ') == '' : continue
        if '\t' not in line :
            current = line
            if current not in data : data[current] = []
            continue
        elif current is None : raise
        else :
            line = line.strip('\t')
            line = re.sub(r'\t+', '\t', line)
            data[current].append(line.split('\t'))
    data = strip(data)
    return data

# delete
def load_table(fin, fields = None, primary_key = None, cast = None, is_matrix = False, sep = '\t') :
    if not is_matrix :
        if fields == None :
            fields = fin.readline().strip('\n\r').split(sep)
        mapping_fields = dict([(_, fields[_]) for _ in range(len(fields))])
    if primary_key is None or is_matrix : data = []
    else : data = {}
    for line in fin :
        line = line.strip('\n\r')
        if line == '' : continue
        record = line.split(sep)
        if cast is not None and isinstance(cast, list) :
            record = [cast[_](record[_]) for _ in range(len(record))]
        if not is_matrix : datum = dict(zip(mapping_fields.values(), record))
        else : datum = record
        if cast is not None and isinstance(cast, dict) and not is_matrix :
            for field in cast.keys() :
                datum[field] = cast[field](datum[field])
        if primary_key is None or is_matrix: data.append(datum)
        else : data[datum[primary_key]] = datum
    return data

# delete
def load_json(fin, object_hook = None, encoding = 'utf-8') :
    return json.loads(''.join([line.strip('\n') for line in fin.readlines()]), object_hook = object_hook, encoding = encoding)

def json_serialize(data, /) :
    if isinstance(data, (List, Dict, Str, Object, DateTime, File, Folder, Audio)) :
        return data.jsonSerialize()
    elif isinstance(data, (type(None), str, int, float, bool)) :
        return data
    elif isinstance(data, list) :
        return [ json_serialize(item) for item in data ]
    elif isinstance(data, dict) :
        return { json_serialize(key) : json_serialize(data[key]) for key in data }
    elif isinstance(data, tuple) :
        return '({})'.format(', '.join(str(json_serialize(item)) for item in data))
    elif isinstance(data, set) :
        return '{{{}}}'.format(', '.join(str(json_serialize(item)) for item in data))
    elif isinstance(data, (range, bytes, object)) :
        return f'{data}'
    elif isinstance(data, zip) :
        return f'zip{json_serialize(list(data))}'
    elif isinstance(data, datetime) :
        return f'datetime({data})'
    else : raise UserTypeError(data)

def j(data, /, *, indent = 4, ensure_ascii = False, sort_keys = True, encoding = 'utf-8') :
    # return json.dumps(data, indent = indent, ensure_ascii = ensure_ascii, sort_keys = sort_keys, encoding = encoding)
    return json.dumps(data, indent = indent, ensure_ascii = ensure_ascii, sort_keys = sort_keys)

# ==================== Runtime ====================

def highlightTraceback(func) :
    @wraps(func)
    def wrapper(*args, **kwargs) :
        try :
            return func(*args, **kwargs)
        except :
            import traceback
            line_list = List(traceback.format_exception(*sys.exc_info())).reverse()
            flag = False
            for index, line in line_list.enum() :
                line_list[index] = line.strip('\n')
                if line.has('HelloWord-Lib') :
                    flag = False
                elif not flag and line.has('HelloWord') :
                    line_list[index] = f'{P(line_list[index])}'
                    if index >= 1 and line_list[index - 1].has('HelloWord-Lib') :
                        line_list[index - 1] = f'{Y(line_list[index - 1])}'
                    flag = True
            line_list.reverse().forEach(lambda line : print(line))
            Timer.printTiming('失败')
    return wrapper

# ==================== System ====================

def parse_argv(args) :
    sequence, kwargs = List(), Dict()
    for index, arg in List(args).enum() :
        if index == 0 : continue
        if arg[0] == '-' :
            key, value = arg.findall(r'^-([^=]+)=(.*)$')[0]
            kwargs[key] = value
        else :
            sequence.append(arg)
    return kwargs, sequence

def shell(command) :
    import subprocess
    p = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    # for index, line in enumerate(p.stdout.readlines()):
        # print index, line.strip()
    retval = p.wait()
    return (p.stdout, retval)

from Base import Base
