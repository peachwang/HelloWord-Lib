# -*- coding: utf-8 -*-  
from .Color          import R, Y, G, C, B, P, S, W, E
from .Timer          import Timer
from .ClassTools     import (
    log_entering,
    container, iterable, sized,
    print_func, printable,
    anti_duplicate_new, anti_duplicate_init,
    total_ordering,
    cls_prop, cls_cached_prop,
    prop, iter_func, iter_prop, cached_prop,
    MetaClass, BaseClass, SingularMetaClass, SingularBaseClass,
    ABCMeta, ABC, abstractmethod)
from functools       import wraps, lru_cache as cached_func
from weakref         import ref, WeakValueDictionary
from inspect         import isclass, isfunction, ismethod, signature
from collections.abc import Iterable, Iterator, Generator, Callable
from typing          import Optional, Union
from operator        import attrgetter, itemgetter, methodcaller
identical = lambda _ : _
# operator.attrgetter(*attrs)
# Return a callable object that fetches attr from its operand.
# If more than one attribute is requested, returns a tuple of attributes.
# The attribute names can also contain dots.
# For example:
# attrgetter('name.first', 'name.last')(a) = (a.name.first, a.name.last).

# operator.itemgetter(*items)
# Return a callable object that fetches item from its operand using the operand’s __getitem__() method.
# If multiple items are specified, returns a tuple of lookup values.
# For example:
# itemgetter('name')({'name' : 'tu', 'age' : 18}) = 'tu'
# itemgetter(1, 3, 5)('ABCDEFG') = ('B', 'D', 'F')
# itemgetter(slice(2, None))('ABCDEFG') = 'CDEFG'

# operator.methodcaller(name, /, *args, **kwargs)
# Return a callable object that calls the method name on its operand.
# If additional arguments and/or keyword arguments are given, they will be given to the method as well.
# For example:
# methodcaller('name', 'foo', bar = 1)(a) = a.name('foo', bar = 1).

# https://docs.python.org/3/library/types.html

class CustomTypeError(TypeError) :

    def __init__(self, value, msg = '') :
        self._value = value
        self._msg   = msg

    def __format__(self, spec) : return f'{f"非法类型 {type(self._value)} {self._msg}: {self._value!s}":{spec}}'

    def __str__(self) : return self.__format__('')

def ensure_args_type(func) :
    @wraps(func)
    def wrapper(*args, **kwargs) :
        import inspect
        from typing import _GenericAlias
        # inspect_object(func, 'func')
        # inspect_object(func.__code__, 'func.__code__')
        def ensure_type(name, value, value_type) :
            # print(type(value), value, type(value_type), value_type)#, type(value_type.__origin__), value_type.__origin__, type(value_type.__args__), value_type.__args__)
            if value_type is inspect._empty                 : return
            elif (type(value_type) is type
                and isinstance(value, value_type))          : return
            elif (isinstance(value_type, _GenericAlias)
                and value_type.__origin__ is Union
                and isinstance(value, value_type.__args__)) : return
            raise CustomTypeError(value, f'字段 {name} 预期 {value_type}')
        for index, param in enumerate(signature(func).parameters.values()) :
            if param.name == 'self' : continue
            # inspect_object(param.annotation, 'param.annotation', False)
            # print(param.name)
            # print(param.annotation)
            # print(param.kind)
            # print(args)
            if str(param.kind) in ('POSITIONAL_ONLY', 'POSITIONAL_OR_KEYWORD') :
                if index >= len(args) : continue
                value = args[index]
            elif str(param.kind) == 'KEYWORD_ONLY'                             :
                if param.name not in kwargs : continue
                value = kwargs[param.name]
            else                                                               : continue
            # print(param.kind.description)
            # print(value)
            # print()
            ensure_type(param.name, value, param.annotation)
            # input()
        result = func(*args, **kwargs)
        if 'return' in func.__annotations__ : ensure_type('return', result, func.__annotations__['return'])
        return result
    return wrapper

def bar(num, mod, /, *, char = '-') : return char * (num // mod)

def shell(command) :
    import subprocess
    p = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    # for index, line in enumerate(p.stdout.readlines()):
        # print index, line.strip()
    retval = p.wait()
    return (p.stdout, retval)

def inspect_object(obj, name = '', print_source = True) :
    import builtins, inspect, re
    from pprint import pformat as pf, pprint as pp
    print(G(f'{name} = {obj = }'))
    print(f'{type(obj) = }')
    if ((type_str := (str(obj)[8:-2])) in dir(builtins)) and type_str != 'type' : print(B('obj is built-in.')); return
    if ((type_str := (str(type(obj))[8:-2])) in dir(builtins)) and type_str != 'type' : print(B('type(obj) is built-in.')); return
    if str(obj) == "<class 'type'>" : print(B('obj is type.')); return
    def print_source(obj) :
        for line in inspect.getsourcelines(obj)[0] :
            if re.match(r' *def ', line) or re.match(r' *class ', line) : print(Y(f'{line}'), end = '')
            else                                                        : print(f'{line}', end = '')
    if print_source :
        if isclass(obj) or ismethod(obj) or isfunction(obj) or type_str == 'code' : print_source(obj)
        else                                                                      : print_source(type(obj))
    # print(f'{dir(obj) = }')
    print(Y(f'{name} = {obj = }'))
    # print(f'{inspect.getcomments(obj)=}') # def前的注释
    # print(f'{inspect.getargspec(obj)=}')
    # print(f'{inspect.getfullargspec(obj)=}')
    # print(f'{inspect.getargvalues(obj)=}')
    # currentframe = inspect.currentframe()
    # print(Y(f'{inspect.getframeinfo(currentframe)=}'))
    # print(P(), f'inspect.getouterframes(currentframe)')
    # pp(frames := inspect.getouterframes(currentframe), indent = 4)
    # print(E())
    # print(currentframe)
    # print(f'{pp(inspect.getargvalues(currentframe).locals)}')
    # print(G())
    # print(currentframe.f_back)
    # print(f'{pp(inspect.getargvalues(currentframe.f_back).locals)}', E())
    # print(inspect.signature(obj).parameters)
    # print(currentframe.f_back.f_back)
    # print(f'{pp(inspect.getargvalues(currentframe.f_back.f_back).locals)}')
    # print(f'{inspect.getinnerframes(currentframe)=}', E())
    # print(P(), f'inspect.stack()=')
    # pp(stack := inspect.stack(), indent = 4)
    # print(E())
    # print(f'{inspect.getargvalues(frames[1])=}', E())
    # print(G(f'{inspect.getargvalues(frames[2])=}'))
    # print(f'{inspect.trace()=}', E())
    for key in dir(obj) :
        if key == '__globals__' : continue
        print(f'{key:20s} = ', end = '')
        if type(obj) is type                                               : __ = obj.__getattribute__(obj(), key)
        else                                                               : __ = obj.__getattribute__(key)
        if isclass(__) or ismethod(__) or isfunction(__)                   : print(Y(f'{__}'))
            # print(f'\n{inspect.signature(__)}')
            # print(f'\n{inspect.getsource(__)}')
        elif '<method-wrapper' in str(__) or '<built-in method' in str(__) : print(B(f'{__}'))
        else                                                               :
            if key in ('co_consts',)   : print(P(f'{pf(__)}'))
            # elif isinstance(__, bytes) : print(P(f'{__.decode()}'))
            else                       : print(P(f'{__}'))