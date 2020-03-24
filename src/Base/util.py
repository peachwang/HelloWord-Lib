# -*- coding: utf-8 -*-  
import sys, os; sys.path.append(os.path.realpath(__file__ + '/../DataModel/'))

import json, re, requests
from sys        import exit
from Color      import R, Y, G, C, B, P, S, W, E
from functools  import wraps, cached_property, lru_cache
from shared     import ensureArgsType, UserTypeError, _print, enterLog, antiDuplicateNew, antiDuplicateInit
from typing     import Optional, Union
from Object     import Object
from List       import List
from Dict       import Dict
from Str        import Str
from DateTime   import TimeDelta, Date, Time, DateTime, DateRange, Year, Month, Week, timedelta_class, date_class, time_class, datetime_class
from Timer      import Timer
from File       import File
from Audio      import Audio
from Folder     import Folder
from Counter    import Counter
from LineStream import LineStream

from operator import attrgetter, itemgetter, methodcaller
# operator.attrgetter(*attrs)
# Return a callable object that fetches attr from its operand. If more than one attribute is requested, returns a tuple of attributes. The attribute names can also contain dots. For example:
# attrgetter('name.first', 'name.last')(a) = (a.name.first, a.name.last).

# operator.itemgetter(*items)
# Return a callable object that fetches item from its operand using the operand’s __getitem__() method. If multiple items are specified, returns a tuple of lookup values. For example:
# itemgetter('name')({'name' : 'tu', 'age' : 18}) = 'tu'
# itemgetter(1, 3, 5)('ABCDEFG') = ('B', 'D', 'F')
# itemgetter(slice(2, None))('ABCDEFG') = 'CDEFG'

# operator.methodcaller(name, /, *args, **kwargs)
# Return a callable object that calls the method name on its operand. If additional arguments and/or keyword arguments are given, they will be given to the method as well. For example:
# methodcaller('name', 'foo', bar = 1)(a) = a.name('foo', bar = 1).

# ==================== Data ====================

def json_serialize(data, /) :
    if isinstance(data, (List, Dict, Str, Object, TimeDelta, Date, Time, DateTime, File, Folder, Audio)) :
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
    elif isinstance(data, timedelta_class) :
        return f'timedelta({data})'
    elif isinstance(data, date_class) :
        return f'date({data})'
    elif isinstance(data, time_class) :
        return f'time({data})'
    elif isinstance(data, datetime_class) :
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
            Timer.printTiming('开始')
            result = func(*args, **kwargs)
            Timer.printTiming('结束')
            return result
        except :
            import traceback
            line_list = List(traceback.format_exception(*sys.exc_info())).reverse()
            flag = False
            for index, line in line_list.enum() :
                line_list[index] = line.strip('\n')
                if line.has('HelloWord-Lib') or line.has('Python.framework') :
                    flag = False
                elif not flag and (line.has(r'File "[A-Za-z_\-]+\.py"', re_mode = True) or line.hasNo('HelloWord-Lib') and line.hasNo('Python.framework')) :
                    line_list[index] = f'{B(line_list[index])}'
                    # if index >= 1 and line_list[index - 1].has('HelloWord-Lib') :
                    #     line_list[index - 1] = f'{Y(line_list[index - 1])}'
                    if index > 0 : flag = True
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
