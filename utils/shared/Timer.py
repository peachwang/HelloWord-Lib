# -*- coding: utf-8 -*-  
import sys, time
from functools import wraps
from typing    import Optional
from .Color    import Y, P, E
prop = property

class Timer :

    _has_inited          = False

    @classmethod
    def __initclass__(cls) :
        if cls._has_inited : return
        cls._global_total      = 0
        cls._global_current    = time.time()
        cls._global_delta_list = []
        cls._timer_dict        = {}
        cls._has_inited        = True

    @classmethod
    def get_timer_dict(cls) : return cls._timer_dict

    def __init__(self, key: str, /) :
        self.__initclass__()
        self._key        = key
        self._total      = 0
        self._last_total = 0
        self._delta_list = []
        self._last_len   = 0

    @prop
    def key(self) : return self._key
    
    @prop
    def total(self) : return self._total

    def add(self, delta: float, /) : self._total += delta; self._delta_list.append(delta); return self

    def len(self) -> int : return len(self._delta_list)

    @prop
    def len_delta(self) -> int : result = self.len() - self._last_len; self._last_len = self.len(); return result

    @prop
    def ave(self) -> float : return self._total / self.len() if self.len() > 0 else 0

    @prop
    def total_delta(self) -> float : result = self._total - self._last_total; self._last_total = self._total; return result

    def timeit_once(msg = '', /) :
        def decorator(func) :
            Timer.__initclass__()
            @wraps(func)
            def wrapper(*args, **kwargs) :
                Timer.print_timing(f'{func.__qualname__}{msg} 开始')
                current = time.time()
                result = func(*args, **kwargs)
                delta   = time.time() - current
                Timer.print_timing(f'{func.__qualname__}{msg} 结束', delta = delta)
                return result
            return wrapper
        return decorator

    def timeit_total(key, *, group_args = False) :
        def decorator(func) :
            Timer.__initclass__()
            @wraps(func)
            def wrapper(*args, **kwargs) :
                # key = func.__qualname__
                if group_args :
                    key_args = f'{args}{kwargs if len(kwargs) > 0 else ""}'
                    if key not in Timer.get_timer_dict()       : Timer.get_timer_dict()[key] = {}
                    if key_args in Timer.get_timer_dict()[key] : timer = Timer.get_timer_dict()[key][key_args]
                    else                                     : Timer.get_timer_dict()[key][key_args] = timer = Timer(f'{key}{key_args}')
                else          :
                    if key in Timer.get_timer_dict() : timer = Timer.get_timer_dict()[key]
                    else                           : Timer.get_timer_dict()[key] = timer = Timer(key)
                current = time.time()
                result = func(*args, **kwargs)
                timer.add(time.time() - current)
                return result
            return wrapper
        return decorator

    @classmethod
    def print_total(cls, key: str, /, msg = '') :
        cls.__initclass__()
        def print_timer(timer) :
            print(P(f'类目({timer.key:50}) 总共({timer.len():>10}次, +{timer.len_delta:>10}次, {timer.total:.6f}s, +{timer.total_delta:.6f}s) 平均{timer.ave:.6f}s [ {msg} ]'))
        if key in cls._timer_dict :
            _ = cls._timer_dict[key]
            if isinstance(_, dict) :
                for key_args in _ : print_timer(_[key_args])
            else                   : print_timer(_)
        else                      : raise Exception(f'Timer of {key=} 未找到')
        return cls

    @classmethod
    def print_timing(cls, msg = '', *, delta: Optional[float] = None, indent: int = 0, color = None) :
        cls.__initclass__()
        from ..datatypes.DateTime import DateTime
        timing_delta = time.time() - cls._global_current
        cls._global_delta_list.append(timing_delta)
        cls._global_total += timing_delta
        if color is not None : msg = color(msg)
        if delta is None     : print(Y(f'[{DateTime():%m-%d %H:%M:%S}] {cls._global_total:5.2f}s 间隔{timing_delta:9,.6f}s'), f'[ {msg} ]')
        else                 : indent = '\t' * indent; print(Y(f'{indent}[{DateTime():%m-%d %H:%M:%S}] {cls._global_total:5.2f}s 本轮{delta:9,.6f}s'), f'[ {msg} ]')
        sys.stdout.flush()
        cls._global_current = time.time()
        return cls

if __name__ == '__main__':
    Timer.print_timing()