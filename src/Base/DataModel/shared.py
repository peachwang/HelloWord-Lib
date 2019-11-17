# -*- coding: utf-8 -*-  

from functools import wraps

def ensureArgsType(func) :
    @wraps(func)
    def wrapper(*args, **kwargs) :
        import inspect
        from pprint import pprint as p
        print(f'{func.__annotations__=}')
        # print(f'{inspect.getcomments(func)=}') # def前的注释
        # print(f'{inspect.getsourcelines(func)=}')
        print(f'{inspect.getargspec(func)=}')
        # if not isinstance(item_list, list) :
        #     raise Exception(f'Unexpected {type(item_list)=} of {item_list=}')
        # print(p(list(filter(lambda _ : _[0] != '__globals__', inspect.getmembers(func)))))
        print(p(inspect.getcomments(func)))
        input()
        result = func(*args, **kwargs)
        return result
    return wrapper
