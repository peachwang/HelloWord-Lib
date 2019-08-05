# -*- coding: utf-8 -*-  
import re, json, sys, os, requests
from time import sleep, time, gmtime, mktime, ctime, localtime, strftime, strptime
from datetime import datetime, date, timedelta
from os.path import exists, getsize, join, isfile, realpath
from os import rename, listdir, remove, mkdir, makedirs
from sys import exit
from math import *
from copy import *

from bcolors import OKMSG as OK, PASS, WARN, ERRMSG as ERROR, FAIL, WAITMSG as WAIT, BLUE, BOLD, UNDERLINE, HEADER, ENDC
G, Y, R, B, E = GREEN, YELLOW, RED, BLUE, END = PASS, WARN, FAIL, BLUE, ENDC

sys.path.append(os.path.realpath(__file__ + '/../DataModel/'));

from DateTime import DateTime
from Dict import Dict
from List import List
from Object import Object
from Str import Str
from Audio import Audio
from File import File
from Folder import Folder
from Timer import Timer


# @todo: add comments for the following functions
# ================= Exception =================

class UserTypeError(TypeError):

    def __init__(self, field_name, field_value, expected_types) :
        self.fieldName  = field_name
        self.fieldValue = field_value
        self.expectedTypes = expected_types
        if isinstance(self.expectedTypes, type) :
            self.expectedTypes = [self.expectedTypes]
        if not isinstance(self.expectedTypes, list) :
            raise UserTypeError('expected_types', expected_types, [type, list])
        if contains_same_items(list(map(type, self.expectedTypes)), True, type) is False :
            raise Exception('Expected_types does not contain just types.\nexpected_types:\n{}'.format(j(list(map(str, self.expectedTypes)))))
        self.value = self.__str__()

    def __str__(self) :
        expected_types = ' or '.join([self.getTypeStr(expected_type) for expected_type in self.expectedTypes])
        return 'Unexpected type({}) of {} is given, but type({}) is expected.'.format(
            self.getTypeStr(self.fieldValue), self.fieldName, str(self.expectedTypes)
        )

    def getTypeStr(self, var_type) :
        return re.findall(r'\'([^\']+)\'', str(type(var_type)))[0]

class UserException(BaseException) :

    def __init__(self, message = '', code = 0) :
        self.message = message
        self.code    = code

    def __str__(self) :
        return 'UserException ({}) : {}.'.format(self.code, self.message)

# ==================== List ====================

# delete
def extend(*lists) :
    _ = []
    for __ in lists : _.extend(__)
    return _

# delete
def unique(data) : 
    _ = sorted(data)
    __ = []
    for index, item in enumerate(_) :
        if index == 0 or type(item) != type(_[index - 1]) or item != _[index - 1] :
            __.append(item)
    return __

# delete
def intersection(*lists) :
    _ = list(lists[0])
    for __ in lists[1:] :
        ___ = []
        for index, item in enumerate(_) :
            if item in list(__) : ___.append(item)
        _ = ___
    return _

# ==================== Dict ====================

# delete
def map_to(field_names, field_values) :
    if not isinstance(field_names, list) :
        raise UserTypeError('field_names', field_names, list)
    if isinstance(field_values, (int, float, bool, str)) :
    # if isinstance(field_values, (int, float, bool, str, unicode)) :
        return dict(zip(field_names, [field_values] * len(field_names)))
    elif isinstance(field_values, list) :
        if len(field_values) == len(field_names) :
            return dict(zip(field_names, field_values))
        else :
            raise Exception('Lengths of field_names and field_values do not equal.\nfield_names:\n{}\nfield_values:\n{}'.format(
                j(field_names), j(field_values)
            ))
    else :
        raise UserTypeError('field_values', field_values, [int, float, bool, str, unicode, list])

# ==================== String ====================

# delete
def strip(data, chars = ' \n\t', encoding = 'utf-8') :
    if data is None :
        return None
    elif type(data) is str :
        return data.strip(chars)
    # elif type(data) == unicode :
        # return data.encode(encoding).strip(chars).decode(encoding)
    elif type(data) is list :
        return [strip(datum, chars, encoding) for datum in data]
    elif type(data) is tuple :
        return (strip(datum, chars, encoding) for datum in data)
    elif type(data) is set :
        return set([strip(datum, chars, encoding) for datum in data])
    elif type(data) is dict :
        return dict([(key, strip(data[key], chars, encoding)) for key in data.keys()])
    elif isinstance(data, (int, float, bool)) :
        return data
    else :
        raise UserTypeError('data', data, [str, list, tuple, set, dict, int, float, bool])

# delete
def safe(data, encoding = 'utf-8') :
    try :
        if data is None :
            return None
        elif type(data) is str :
            return data
        # elif type(data) is unicode :
            # return data.encode(encoding)
        elif type(data) is list :
            return [safe(datum, encoding) for datum in data]
        elif type(data) is tuple :
            return tuple([safe(datum, encoding) for datum in data])
        elif type(data) is set :
            return set([safe(datum, encoding) for datum in data])
        elif type(data) is dict :
            return dict([(safe(key, encoding), safe(data[key], encoding)) for key in data.keys()])
        elif isinstance(data, (int, float, bool)) :
            return data
        elif data is None :
            return data
        else :
            raise UserTypeError('data', data, [str, unicode, list, tuple, set, dict, int, float, bool])
    except Exception :
        print(type(data))
        print([data])
        raise e
        exit()

# delete
def contains_empty_string(data) :
    if type(data) in [str, unicode] :
        if strip(data) == '' :
            return True
        else :
            return False
    elif type(data) in [list, tuple, set] :
        for datum in data :
            if contains_empty_string(datum) :
                return True
        return False
    elif type(data) is dict :
        for key, value in data.items() :
            if contains_empty_string(value) :
                return True
        return False
    elif isinstance(data, (int, float, bool)) :
        return False
    else :
        raise UserTypeError('data', data, [str, unicode, list, tuple, set, dict, int, float, bool])

# delete
# 为了防止json无法解析对象类数据
def str_object(data) :
    if isinstance(data, (str, int, float, bool)) :
    # if isinstance(data, (str, unicode, int, float, bool)) :
        return data
        # return str(data)
    elif type(data) is list :
        return [str_object(datum) for datum in data]
    elif type(data) is tuple :
        return '(' + ', '.join(str(datum) for datum in data) + ')'
        # return (str_object(datum) for datum in data)
    elif type(data) is set :
        return set([str_object(datum) for datum in data])
    elif type(data) is dict :
        return dict([(str_object(key), str_object(data[key])) for key in data.keys()])
    else :
        return str(data)

# ==================== Data ====================

def j(data, indent = 4, ensure_ascii = False, sort_keys = True, encoding = 'utf-8') :
    return json.dumps(data, indent = indent, ensure_ascii = ensure_ascii, sort_keys = sort_keys)
    # return json.dumps(data, indent = indent, ensure_ascii = ensure_ascii, sort_keys = sort_keys, encoding = encoding)

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

# DataStructure Module
#   def inspect()
#   def compatibleTo
#   def validate
#   def difference/delta
#   

# move
def inspect(data, max_depth = 10, depth = 0) :
    # print(str(data)[:120])
    if depth > max_depth :
        if data is None : return None 
        elif isinstance(data, (str, int, float, bool, tuple, set)) : return data
        elif isinstance(data, list) : return '[ {} items folded ]'.format(len(data))
        elif isinstance(data, dict) : return '{{ {} keys folded }}'.format(len(data))
        else : raise UserTypeError('data', data, [str, list, tuple, set, dict, int, float, bool])
    if data is None : return None
    elif isinstance(data, (str, int, float, bool, tuple, set)) : return data
    elif isinstance(data, list) :
        if len(data) == 0 : return data
        elif len(data) == 1 : return List([ inspect(data[0], max_depth, depth + 1) ])
        elif len(data) == 2 : return List([ inspect(data[0], max_depth, depth + 1), inspect(data[1], max_depth, depth + 1) ])
        
        # len >= 3
        result_0 = inspect(data[0], max_depth, depth + 1)
        _ = '------------------------------'
        if isinstance(result_0, dict) :
            for index, datum_i in enumerate(data) :
                if not isinstance(datum_i, dict) : raise Exception('列表中元素类型不一致({})'.format(datum_i))
                for key, value in datum_i.items() :
                    if key not in result_0 :
                        result_0[key] = inspect(value, max_depth, depth + 1) # 【补充】第0个元素中不存在的字段
                        continue
                    if data[0].get(key) is not None and isinstance(data[0][key], list) : continue # 列表类【原生】字段不扩充POSSIBLE VALUES
                    if data[0].get(key) is not None and isinstance(data[0][key], dict) : continue # 字典类【原生】字段不扩充POSSIBLE VALUES
                    if data[0].get(key) is None and isinstance(result_0[key], list) \
                        and not (isinstance(result_0[key][0], str) and 'POSSIBLE VALUES' in result_0[key][0]) : continue # 列表类【补充】字段不扩充POSSIBLE VALUES
                    if data[0].get(key) is None and isinstance(result_0[key], dict) : continue # 字典类【补充】字段不扩充POSSIBLE VALUES
                    # 此时待补充的是非列表字典类字段
                    if isinstance(value, list) or isinstance(value, dict) : raise Exception('列表中元素类型不一致({})'.format(value))
                    # 此时value一定为非列表字典类数据
                    if not isinstance(result_0[key], list) : # 暂未扩充过，现进行首次扩充POSSIBLE VALUES
                        result_0[key] = [
                            _ + 'POSSIBLE VALUES' + _, 
                            result_0[key]
                        ]
                        if inspect(value, max_depth, depth + 1) != result_0[key][1] :
                            result_0[key].append(inspect(value, max_depth, depth + 1))
                    else : # 非首次扩充POSSIBLE VALUES
                        if len(result_0[key]) < 5 :
                            if inspect(value, max_depth, depth + 1) not in result_0[key] :
                                result_0[key].append(inspect(value, max_depth, depth + 1)) # 扩充
                        if index == len(data) - 1 :
                            result_0[key].append('{} TOTAL {} SIMILAR ITEMS {}'.format(_, len(data), _))
            return [ result_0, '{} TOTAL {} SIMILAR DICTS {}'.format(_, len(data), _) ]
        else : # 非字典类数据，含列表
            return [ inspect(data[0], max_depth, depth + 1), inspect(data[1], max_depth, depth + 1), '{} TOTAL {} SIMILAR LISTS {}'.formart(_, len(data), _) ]
    elif isinstance(data, dict) : return { key : inspect(value, max_depth, depth + 1) for key, value in data.items() }
    else : raise UserTypeError('data', data, [str, list, tuple, set, dict, int, float, bool])

# ==================== System ====================

def parse_argv(argv) :
    mapping  = {}
    sequence = []
    for index, arg in enumerate(argv) :
        if index == 0 :
            continue
        if arg[0] == '-' :
            key, value = re.findall(r'-([^=]+)=(.*)', arg)[0]
            mapping[key] = value
        else :
            sequence.append(arg)
    return mapping, sequence

def shell(command) :
    import subprocess
    p = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    # for index, line in enumerate(p.stdout.readlines()):
        # print index, line.strip()
    retval = p.wait()
    return (p.stdout, retval)

from Base import Base


if __name__ == '__main__' :
    pass
