# -*- coding: utf-8 -*-  
import sys
from functools import wraps
# from Object import Object

class Timer() :

    _has_inited     = False
    _timeit_total_off = False

    @classmethod
    def timeitTotalOff(cls) :
        cls._timeit_total_off = True

    @classmethod
    def __initclass__(cls) :
        if cls._has_inited : return
        from DateTime import time
        cls._global_total      = 0
        cls._global_current    = time.time()
        cls._global_delta_list = []
        cls._timer_dict        = {}
        cls._has_inited        = True

    def __init__(self, key, /) :
        Timer.__initclass__()
        self._key = key
        self._total = 0
        self._last_total = 0
        self._delta_list = []
        self._last_len = 0

    def add(self, delta, /) :
        self._total += delta
        self._delta_list.append(delta)
        return self

    def len(self) :
        return len(self._delta_list)

    @property
    def len_delta(self) :
        result = self.len() - self._last_len
        self._last_len = self.len()
        return result

    @property
    def average(self):
        return self._total / self.len() if self.len() > 0 else 0

    @property
    def total_delta(self) :
        result = self._total - self._last_total
        self._last_total = self._total
        return result

    def timeitOnce(func, msg = '', /) :
        Timer.__initclass__()
        @wraps(func)
        def wrapper(self = None, *args, **kwargs) :
            Timer.printTiming(f'{func.__qualname__}{msg} 开始')
            from DateTime import time
            current = time.time()
            if self is None :
                result = func(*args, **kwargs)
            else :
                result = func(self, *args, **kwargs)
            delta = time.time() - current
            Timer.printTiming(f'{func.__qualname__}{msg} 结束', delta = delta)
            return result
        return wrapper

    def timeitTotal(key, *, group_args = False) :
        def decorator(func) :
            if Timer._timeit_total_off : return func
            @wraps(func)
            def wrapper(self = None, *args, **kwargs) :
                Timer.__initclass__()
                # key = func.__qualname__
                from DateTime import time
                if group_args :
                    key_args = f'{args}{kwargs if len(kwargs) > 0 else ""}'
                    if key not in Timer._timer_dict :
                        Timer._timer_dict[key] = {}
                    if key_args in Timer._timer_dict[key] :
                        timer = Timer._timer_dict[key][key_args]
                    else :
                        Timer._timer_dict[key][key_args] = timer = Timer(f'{key}{key_args}')
                else :
                    if key in Timer._timer_dict :
                        timer = Timer._timer_dict[key]
                    else :
                        Timer._timer_dict[key] = timer = Timer(key)
                current = time.time()
                if self is None :
                    result = func(*args, **kwargs)
                else :
                    result = func(self, *args, **kwargs)
                timer.add(time.time() - current)
                return result
            return wrapper
        return decorator

    @classmethod
    def printTotal(cls, key, /, msg = '') :
        cls.__initclass__()
        if Timer._timeit_total_off : return cls
        def printTimer(timer) :
            from util import P, E
            print(P(f'类目({timer._key:50}) 总共({timer.len():>10}次, +{timer.len_delta:>10}次, {timer._total:.6f}s, +{timer.total_delta:.6f}s) 平均{timer.average:.6f}s [ {msg} ]'))
        if key in cls._timer_dict :
            _ = cls._timer_dict[key]
            if isinstance(_, dict) :
                for key_args in _ :
                    printTimer(_[key_args])
            else :
                printTimer(_)
        else : raise Exception(f'Timer of {key=} 未找到')
        return cls

    @classmethod
    def printTiming(cls, msg = '', *, delta = None, indent = 0) :
        cls.__initclass__()
        from util import Y, E
        from DateTime import DateTime, time
        timing_delta = time.time() - cls._global_current
        cls._global_delta_list.append(timing_delta)
        cls._global_total += timing_delta
        if delta is None :
            print(Y(f'[{DateTime():%m-%d %H:%M:%S}] {cls._global_total:5.2f}s 间隔{timing_delta:9.6f}s'), f'[ {msg} ]')
        else :
            indent = '\t' * indent
            print(Y(f'{indent}[{DateTime():%m-%d %H:%M:%S}] {cls._global_total:5.2f}s 本轮{delta:9.6f}s'), f'[ {msg} ]')
        sys.stdout.flush()
        cls._global_current = time.time()
        return cls

if __name__ == '__main__':
    Timer.printTiming()