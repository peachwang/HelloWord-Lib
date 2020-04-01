# -*- coding: utf-8 -*-  
import sys, requests
from sys        import exit
from shared     import R, Y, G, C, B, P, S, W, E, Timer
from shared     import json, isgenerator, wraps, cached_property, cached_func, total_ordering, Optional, Union
from shared     import UserTypeError, inspect_object, j, ensure_args_type, print_func, log_entering, anti_duplicate_new, anti_duplicate_init

from Str        import Str
from DateTime   import TimeDelta, Date, Time, DateTime, DateRange, Year, Month, Week, timedelta_class, date_class, time_class, datetime_class
from List       import List
from Dict       import Dict
from Inspect    import Inspect, Diff
from Object     import Object

from File       import File
from Folder     import Folder
from Counter    import Counter
from LineStream import LineStream
from Table      import Table
# from Audio      import Audio
# from Base import Base

class SysArgv :

    _has_inited = False

    @classmethod
    def __initclass__(cls) :
        if cls._has_inited : return
        cls._args, cls._kwargs = List(), Dict()
        for index, arg in List(sys.argv).enum() :
            if index == 0    : continue
            if arg[0] == '-' :
                m                = arg.fullMatch(r'^-([^=]+)=(.*)$')
                key, value       = m.oneGroup(1), m.oneGroup(2)
                cls._kwargs[key] = value
            else             : cls._args.append(arg)
        cls._has_inited = True

    @classmethod
    def getArgs(cls) : cls.__initclass__(); return cls._args

    @classmethod
    def getKwargs(cls) : cls.__initclass__(); return cls._kwargs

def main_func(kwarg_to_type = Dict(), /) :
    def decorator(func) :
        @wraps(func)
        def wrapper() :
            try :
                kwargs = SysArgv.getKwargs()
                for name in kwargs :
                    if name in kwarg_to_type :
                        if isinstance(kwarg_to_type[name], tuple) : kwargs[name] = kwarg_to_type[name][0](kwargs[name], *(kwarg_to_type[name][1:]))
                        elif kwarg_to_type[name] is bool          : kwargs[name] = True if kwargs[name] == '1' else False
                        else                                      : kwargs[name] = kwarg_to_type[name](kwargs[name])
                Timer.printTiming('开始', color = Y)
                result = func(kwargs)
                Timer.printTiming('结束', color = G)
                return result
            except :
                import traceback
                line_list = List(traceback.format_exception(*sys.exc_info())).reverse()
                flag = False
                for index, line in line_list.enum() :
                    line_list[index] = line.strip('\n')
                    if line.has('HelloWord-Lib') or line.has('Python.framework') : flag = False
                    elif not flag and (line.has(r'File "[A-Za-z_\-]+\.py"', re_mode = True) or line.hasNo('HelloWord-Lib') and line.hasNo('Python.framework')) :
                        line_list[index] = f'{B(line_list[index])}'
                        # if index >= 1 and line_list[index - 1].has('HelloWord-Lib') : line_list[index - 1] = f'{Y(line_list[index - 1])}'
                        if index > 0 : flag = True
                line_list.reverse().forEach(lambda line : print(line))
                Timer.printTiming('失败', color = R)
        return wrapper
    return decorator
