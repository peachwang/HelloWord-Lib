# -*- coding: utf-8 -*-  
from functools import wraps, cached_property, lru_cache
import inspect
from pprint import pformat as pf, pprint as pp
from typing import Optional, Union

class UserTypeError(TypeError) :

    def __init__(self, value) :
        self._value = value

    def __str__(self) :
        return f'非法类型{type(self._value)}: {self._value!s}'

def inspectObject(obj, name = '', print_source = True) :
    import builtins
    from util import G, Y, R, B, I, P, E
    print(G(f'{name} = {obj = }'))
    print(f'{type(obj) = }')
    if ((type_str := (str(obj)[8:-2])) in dir(builtins)) and type_str != 'type' :
        print(B('obj is built-in.'))
        return
    if ((type_str := (str(obj.__class__)[8:-2])) in dir(builtins)) and type_str != 'type' :
        print(B('obj.__class__ is built-in.'))
        return
    if str(obj) == "<class 'type'>" :
        print(B('obj is type.'))
        return
    def printSource(obj) :
        import re
        from util import G, Y, R, B, I, P, E
        for line in inspect.getsourcelines(obj)[0] :
            if re.match(r' *def ', line) or re.match(r' *class ', line) :
                print(Y(f'{line}'), end = '')
            else :
                print(f'{line}', end = '')
    if print_source :
        if inspect.isclass(obj) or inspect.ismethod(obj) or inspect.isfunction(obj) or type_str == 'code' :
            printSource(obj)
        else :
            printSource(type(obj))
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
        if type(obj) is type :
            __ = obj.__getattribute__(obj(), key)
        else :
            __ = obj.__getattribute__(key)
        if inspect.isclass(__) or inspect.ismethod(__) or inspect.isfunction(__) :
            # print(f'\n{inspect.signature(__)}')
            # print(f'\n{inspect.getsource(__)}')
            print(Y(f'{__}'))
        elif '<method-wrapper' in str(__) or '<built-in method' in str(__):
            print(B(f'{__}'))
        else :
            if key in ('co_consts',) :
                print(P(f'{pf(__)}'))
            # elif isinstance(__, bytes) :
                # print(P(f'{__.decode()}'))
            else :
                print(P(f'{__}'))

def ensureArgsType(func) :
    @wraps(func)
    def wrapper(*args, **kwargs) :
        from typing import _GenericAlias, Union
        # from util import G, Y, R, E
        # inspectObject(func, 'func')
        # inspectObject(func.__code__, 'func.__code__')
        def ensureType(name, value, value_type) :
            # print(type(value), value, type(value_type), value_type)#, type(value_type.__origin__), value_type.__origin__, type(value_type.__args__), value_type.__args__)
            # any
            if value_type is inspect._empty : return
            elif type(value_type) is type :
                if isinstance(value, value_type) : return
            elif isinstance(value_type, _GenericAlias) and value_type.__origin__ is Union :
                if isinstance(value, value_type.__args__) : return
            raise Exception(f'预期 {value_type=}, 非法 {type(value)=} of {value=}')
        for index, param in enumerate(inspect.signature(func).parameters.values()) :
            if param.name == 'self' : continue
            # inspectObject(param.annotation, 'param.annotation', False)
            # print(param.name)
            # print(param.annotation)
            # print(param.kind)
            # print(args)
            if str(param.kind) in ('POSITIONAL_ONLY', 'POSITIONAL_OR_KEYWORD') :
                if index >= len(args) : continue
                value = args[index]
            elif str(param.kind) == 'KEYWORD_ONLY' :
                if param.name not in kwargs : continue
                value = kwargs[param.name]
            else :
                continue
            # print(param.kind.description)
            # print(value)
            # print()
            ensureType(param.name, value, param.annotation)
            # input()
        result = func(*args, **kwargs)
        if 'return' in func.__annotations__ :
            ensureType('return', result, func.__annotations__['return'])
        return result
    return wrapper

def _print(func) :
    @wraps(func)
    def wrapper(self, *args, pattern = '{}', color = None, **kwargs) :
        from util import E
        content, print_len = func(self, *args)
        content = pattern.format(content)
        print(f"{color}{content}{E() if color is not None else ''}", **kwargs)
        if print_len :
            self.printLen(color = color, **kwargs)
        return self
    return wrapper