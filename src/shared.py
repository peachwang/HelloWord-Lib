# -*- coding: utf-8 -*-  
from Color import R, Y, G, C, B, P, S, W, E
from Timer import Timer
from inspect import isclass, isfunction, ismethod, isgenerator, signature
from functools import wraps, cached_property as cached_prop, lru_cache as cached_func, total_ordering; prop = property
from types import BuiltinFunctionType, BuiltinMethodType, FunctionType, MethodType, LambdaType, GeneratorType
from typing import Optional, Union
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


class CustomTypeError(TypeError) :

    def __init__(self, value, msg = '') :
        self._value = value
        self._msg   = msg

    def __format__(self, spec) : return f"{f'非法类型 {type(self._value)} {self._msg}: {self._value!s}':{spec}}"

    def __str__(self) : return self.__format__('')

def ensure_args_type(func) :
    @wraps(func)
    def wrapper(*args, **kwargs) :
        import inspect
        from typing import _GenericAlias
        # inspect_object(func, 'func')
        # inspect_object(func.__code__, 'func.__code__')
        def ensureType(name, value, value_type) :
            # print(type(value), value, type(value_type), value_type)#, type(value_type.__origin__), value_type.__origin__, type(value_type.__args__), value_type.__args__)
            if value_type is inspect._empty                 : return
            elif (type(value_type) is type
                and isinstance(value, value_type))          : return
            elif (isinstance(value_type, _GenericAlias)
                and value_type.__origin__ is Union
                and isinstance(value, value_type.__args__)) : return
            raise Exception(f'预期 {value_type=}, 非法 {type(value)=} of {value=}')
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
            ensureType(param.name, value, param.annotation)
            # input()
        result = func(*args, **kwargs)
        if 'return' in func.__annotations__ : ensureType('return', result, func.__annotations__['return'])
        return result
    return wrapper

def print_func(func) :
    @wraps(func)
    def wrapper(self, *args, pattern = '{}', color = None, print_timing = False, **kwargs) :
        content, print_len = func(self, *args)
        content = pattern.format(content)
        if color is not None : content = color(content)
        if print_timing      : Timer.printTiming(content)
        else                 : print(content, **kwargs)
        if print_len         : self.printLen(color = color, **kwargs)
        return self
    return wrapper

def log_entering(pattern: str = '') :
    def decorator(func) :
        @wraps(func)
        def wrapper(cls_or_self, *args, **kwargs) :
            # kwargs['self'] = cls_or_self
            msg = pattern.format(*args, self = cls_or_self, **kwargs)
            # kwargs.pop('self')
            if '.' in str(cls_or_self.__class__) : _ = f'{id(cls_or_self)}{str(cls_or_self.__class__).split(".")[1][ : -2]:>15}.{func.__qualname__:30}'
            else                                 : _ = f'{id(cls_or_self)}.{func.__qualname__:30}'
            Timer.printTiming(f'{_} {Y("开始")} {msg}')
            result = func(cls_or_self, *args, **kwargs)
            Timer.printTiming(f'{_} {G("结束")} {msg}')
            return result
        return wrapper
    return decorator

class base_class :

    @print_func
    def printFormat(self) : return self.__format__(''), False

    @print_func
    def printStr(self) : return self.__str__(), False

    def j(self, *, indent = True) : import Json; return Json.j(self.jsonSerialize(), indent = indent)

    @print_func
    def printJ(self) : return self.j(), False

def anti_duplicate_new(func) :
    @wraps(func)
    def wrapper(cls, *args, **kwargs) :
        key = func(cls, *args, **kwargs)
        if '_instance_dict' not in dir(cls)        : cls._instance_dict = {}
        if cls._instance_dict.get(key) is not None : return cls._instance_dict[key]
        else                                       : instance = cls.__bases__[0].__new__(cls); cls._instance_dict[key] = instance; return instance
    return wrapper

def anti_duplicate_init(func) :
    @wraps(func)
    def wrapper(self, *args, **kwargs) :
        if '_has_init' in dir(self) : return
        func(self, *args, **kwargs)
        object.__setattr__(self, '_has_init', True)
    return wrapper

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
    if ((type_str := (str(obj.__class__)[8:-2])) in dir(builtins)) and type_str != 'type' : print(B('obj.__class__ is built-in.')); return
    if str(obj) == "<class 'type'>" : print(B('obj is type.')); return
    def printSource(obj) :
        for line in inspect.getsourcelines(obj)[0] :
            if re.match(r' *def ', line) or re.match(r' *class ', line) : print(Y(f'{line}'), end = '')
            else                                                        : print(f'{line}', end = '')
    if print_source :
        if isclass(obj) or ismethod(obj) or isfunction(obj) or type_str == 'code' : printSource(obj)
        else                                                                      : printSource(type(obj))
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