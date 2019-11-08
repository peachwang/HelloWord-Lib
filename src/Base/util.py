# -*- coding: utf-8 -*-  
import sys, os; sys.path.append(os.path.realpath(__file__ + '/../DataModel/'));

import json, re, requests
from sys import exit
from bcolors import OKMSG as OK, PASS, WARN, ERRMSG as ERROR, FAIL, WAITMSG as WAIT, BLUE, BOLD, UNDERLINE, HEADER, ENDC
G, Y, R, B, E = GREEN, YELLOW, RED, BLUE, END = PASS, WARN, FAIL, BLUE, ENDC
# print(sys.path)

from Object import Object
from List import List
from Dict import Dict
from Str import Str
from DateTime import DateTime, datetime, timedelta, time
from Timer import Timer
from File import File
from Audio import Audio
from Folder import Folder, makedirs as mkdir

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
        if self.containsSameItems(list(map(type, self.expectedTypes)), True, type) is False :
            raise Exception('Expected_types does not contain just types.\nexpected_types:\n{}'.format(j(list(map(str, self.expectedTypes)))))
        self.value = self.__str__()

    def __str__(self) :
        expected_types = ' or '.join([self.getTypeStr(expected_type) for expected_type in self.expectedTypes])
        return 'Unexpected type({}) of {} is given, but type({}) is expected.'.format(
            self.getTypeStr(self.fieldValue), self.fieldName, str(self.expectedTypes)
        )

    def getTypeStr(self, var_type) :
        return re.findall(r'\'([^\']+)\'', str(type(var_type)))[0]

    def containsSameItems(self, data, check_specific_value = False, specific_value = None) :
        if not isinstance(data, (list, dict)) :
            raise UserTypeError('data', data, [list, dict])
        if isinstance(data, dict) : data = data.values()
        if len(data) == 0 : return True
        if check_specific_value is True :
            return data.count(specific_value) == len(data)
        else :
            return data.count(data[0]) == len(data)

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

def json_serialize(data) :
    if isinstance(data, (List, Dict, Str, Object, DateTime, File, Folder, Audio)) :
        raise Exception('Unexpected type{} of data{}'.format(type(data), data))
    elif isinstance(data, (str, int, float, bool)) :
        return data
    elif isinstance(data, list) :
        return [ json_serialize(item) for item in data ]
    elif isinstance(data, dict) :
        return { json_serialize(key) : json_serialize(data[key]) for key in data }
    elif isinstance(data, tuple) :
        return 'tuple({})'.format(', '.join(str(json_serialize(item)) for item in data))
    elif isinstance(data, set) :
        return 'set{{{}}}'.format(', '.join(str(json_serialize(item)) for item in data))
    elif isinstance(data, (range, bytes, object)) :
        return '{}'.format(data)
    elif isinstance(data, zip) :
        return 'zip{}'.format(json_serialize(list(data)))
    elif isinstance(data, datetime) :
        return 'datetime({})'.format(data)

def j(data, indent = 4, ensure_ascii = False, sort_keys = True, encoding = 'utf-8') :
    # return json.dumps(data, indent = indent, ensure_ascii = ensure_ascii, sort_keys = sort_keys, encoding = encoding)
    return json.dumps(data, indent = indent, ensure_ascii = ensure_ascii, sort_keys = sort_keys)

# ==================== System ====================

def parse_argv(args) :
    sequence, kwargs = List(), Dict()
    for index, arg in enumerate(List(args)) :
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
