# -*- coding: utf-8 -*-  
import sys, requests
from sys        import exit
from .shared    import *
from .datatypes import *
from .app       import *

class SysArgv(SingularBaseClass) :

    _has_inited = False

    @classmethod
    def __initclass__(cls) :
        if cls._has_inited : return
        cls._args, cls._kwargs = List(), Dict()
        for index, arg in List(sys.argv).enum() :
            if index == 0    : continue
            if arg[0] == '-' :
                m                = arg.full_match(r'^-([^=]+)=(.*)$')
                key, value       = m.one_group(1), m.one_group(2)
                cls._kwargs[key] = value
            else             : cls._args.append(arg)
        cls._has_inited = True

    @cls_cached_prop
    def args(cls)   : cls.__initclass__(); return cls._args

    @cls_cached_prop
    def kwargs(cls) : cls.__initclass__(); return cls._kwargs

def main_func(kwarg_to_type_or_func) :
    if isinstance(kwarg_to_type_or_func, dict) : kwarg_to_type = kwarg_to_type_or_func
    else                                       : kwarg_to_type = Dict()
    def decorator(func) :
        @wraps(func)
        def wrapper() :
            try :
                kwarg_to_type['trace']   = bool
                kwarg_to_type['profile'] = bool
                kwargs                   = SysArgv.kwargs
                for name in kwargs :
                    if name in kwarg_to_type :
                        if isinstance(kwarg_to_type[name], tuple) : kwargs[name] = kwarg_to_type[name][0](kwargs[name], *(kwarg_to_type[name][1:]))
                        elif kwarg_to_type[name] is bool          : kwargs[name] = True if kwargs[name] == '1' else False
                        else                                      : kwargs[name] = kwarg_to_type[name](kwargs[name])
                Timer.print_timing('开始', color = Y)
                result = None
                if kwargs.get('trace', False) :
                    import trace
                    tracer = trace.Trace(
                        ignoredirs   = [sys.prefix, sys.exec_prefix, '/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/'],
                        ignoremods   = ['encodings', 'simplejson', 'logging', 'json', 'requests', '__init__', '_bootlocale', '_collections', '_collections_abc', '_internal_utils', '_policybase', '_strptime', 'abc', 'adapters', 'api', 'calendar', 'client', 'codecs', 'connection', 'connectionpool', 'contextlib', 'cookiejar', 'cookies', 'decoder', 'encoder', 'enum', 'feedparser', 'fnmatch', 'functools', 'genericpath', 'hooks', 'idna', 'inspect', 'locale', 'message', 'models', 'netrc', 'objectid', 'os', 'parse', 'parser', 'poolmanager', 'posixpath', 'py3compat', 'queue', 're', 'request', 'response', 'retry', 'sessions', 'shlex', 'six', 'socket', 'sre_compile', 'sre_parse', 'ssl', 'ssl_', 'structures', 'threading', 'timeout', 'types', 'url', 'wcwidth'],
                        trace        = 1,
                        count        = 1,
                        countfuncs   = 0,
                        countcallers = 0,
                        infile       = 'trace/count.txt',
                        outfile      = 'trace/count.txt',
                    )
                    Folder('trace/').mkdir()
                    temp = sys.stdout
                    sys.stdout = open('trace/trace.txt', 'w')

                    tracer.runctx('result = func(kwargs)', globals = {'result' : result}, locals = {'func' : func, 'kwargs' : kwargs})
                    
                    r = tracer.results()
                    r.write_results(show_missing = False, coverdir = "trace/")
                    sys.stdout = temp
                elif kwargs.get('profile', False) :
                    import cProfile, pstats
                    from pstats import SortKey
                    Folder('profile/').mkdir()
                    cProfile.runctx('result = func(kwargs)', filename = 'profile/profile.txt', globals = {'result' : result}, locals = {'func' : func, 'kwargs' : kwargs})
                    p = pstats.Stats('profile/profile.txt')
                    # p.strip_dirs()
                    # p.sort_stats(SortKey.NAME, SortKey.FILENAME).print_stats()
                    # p.sort_stats(SortKey.TIME, SortKey.CUMULATIVE).print_stats(.5, 'init')
                    p.sort_stats(SortKey.CUMULATIVE).print_stats(60)
                    # p.sort_stats(SortKey.CUMULATIVE).print_callers('Json.py', 60)
                    p.sort_stats(SortKey.CUMULATIVE).print_callees('python3.8/json', 60)
                    # p.add('restats')
                else :
                    result = func(kwargs)
                Timer.print_timing(f'结束 {result}', color = G)
                return result
            except :
                import traceback
                line_list = List(traceback.format_exception(*sys.exc_info())).reverse()
                flag = False
                for index, line in line_list.enum() :
                    line_list[index] = line.strip('\n')
                    if line.has('HelloWord-Lib') or line.has('Python.framework') : flag = False
                    elif line.has(r'File "[A-Za-z_\-]+\.py"', re_mode = True) or line.has_no('HelloWord-Lib') and line.has_no('Python.framework') :
                        if not flag :
                            line_list[index] = f'{B(line_list[index])}'
                            if index >= 1 and line_list[index - 1].has('HelloWord-Lib') : line_list[index - 1] = f'{Y(line_list[index - 1])}'
                            if index > 0 : flag = True
                        else :
                            line_list[index] = f'{Y(line_list[index])}'
                line_list.reverse().for_each(lambda line : print(line))
                Timer.print_timing('失败', color = R)
        return wrapper
    if isinstance(kwarg_to_type_or_func, dict)       : return decorator
    elif isinstance(kwarg_to_type_or_func, Callable) : return decorator(kwarg_to_type_or_func)
    else                                             : raise CustomTypeError(kwarg_to_type_or_func)


if __name__ == '__main__':
    a = ({
        'hello'           : DateTime(1500000000),
        (1,2,3)           : DateList([Date('2020-03-20'), Date('2020-04-20')]),
        4                 : DateRange(Date('2019-03-20'), Date('2019-04-20')),
        True              : Year(2013),
        None              : Month(2020, 12),
        5                 : Week(2019, 12, 29),
        ObjectId().binary : ObjectId(),
        range(1,3,2)      : File('.'),
        int               : Folder('.'),
        6                 : {5,6,7},
        7                 : (1,2,3),
        8                 : False,
        9                 : None,
        10                : ObjectId().binary,
        11                : range(1,3,2),
        12                : float,
        13                : 5,
        14                : 6.7,
        15                : 'word',
    })
    from ..app import Json
    import datetime
    print(Dict(a).j())
    print('1', a)
    print()
    a = Dict(a)
    print('2', a)
    print()
    c = Json.raw_dump_json_str(a)
    # print(c)
    b = Json.raw_load_json_str(c)
    print('3', f'{a}')
    print()
    # print(f'{b!a}')
    print('4', str(b))
    b = Dict(b)
    # print()
    print('5', f'{b}')

    # print(a)
    print()
    # print(b)

    # print()
    # print(f'{a!r}')
    # print()
    # print(f'{b!r}')
    
    # print(eval(repr(a)).j())
    # print(b.j())
    
    # print()
    print('6', b)
    # print(list(map(type, b.keys())))
    print()
    print('7', repr(b))
    print()
    print('8', eval(repr(b)))
    print()
    print(a == b)
    print(eval(repr(b)) == b)
    print(eval(repr(a)) == a)