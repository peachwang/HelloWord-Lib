# -*- coding: utf-8 -*-  
from util import List, Dict, Object, DateTime, time, sys
from functools import wraps

class Timer(Object) :

    _global_total = 0
    _global_current = time()
    _global_delta_list = List()
    _timer_dict = Dict()

    def __init__(self, key) :
        Object.__init__(self)
        self._registerProperty(['key', 'total'])
        self._key = key
        self._total = 0
        self._delta_list = List()

    def add(self, delta) :
        self._total += delta
        self._delta_list.append(delta)
        return self

    def len(self) :
        return self._delta_list.len()

    @property
    def average(self):
        return self._total / self.len() if self.len() > 0 else 0

    def timeitOnce(func, msg = '') :
        @wraps(func)
        def wrapper(self, *args, **kwargs) :
            # Timer.printTiming('{}{} starts'.format(func.__qualname__, msg))
            current = time()
            result = func(self, *args, **kwargs)
            delta = time() - current
            Timer.printTiming(f'{func.__qualname__}{msg} 结束', delta)
            return result
        return wrapper

    def timeitTotal(key) :
        def decorator(func) :
            @wraps(func)
            def wrapper(self, *args, **kwargs) :
                # key = func.__qualname__
                if Timer._timer_dict.has(key) :
                    timer = Timer._timer_dict[key]
                else :
                    Timer._timer_dict[key] = timer = Timer(key)
                current = time()
                result = func(self, *args, **kwargs)
                timer.add(time() - current)
                return result
            return wrapper
        return decorator

    @classmethod
    def printTotal(cls, key, msg = '') :
        from util import B, E
        if cls._timer_dict.has(key) :
            timer = cls._timer_dict[key]
        else : raise Exception(f'timer of {key=} not found.')
        print(B, f'类目({timer.key}) 总共({timer.len()}次, {timer.total:.5f}s) 平均({timer.average:.5f}s) [ {msg} ]', E)
        return cls

    @classmethod
    def printTiming(cls, msg = '', delta = None, indent = 0) :
        from util import Y, E
        timing_delta = time() - cls._global_current
        cls._global_delta_list.append(timing_delta)
        cls._global_total += timing_delta
        if delta is None :
            # print(Y, '{}间隔({:.5f}s) 累计({:.2f}s) [{}] [当前({}) 堆栈({})]'.format(
                # DateTime(),
                # cls._global_delta_list.len()
            print(Y, '\t' * indent, f'累计({cls._global_total:.5f}s) 间隔({timing_delta:.5f}s) [ {msg} ]', E)
        else :
            # print(Y, '{}本轮({:.5f}s) 累计({:.2f}s) [{}] [当前({})]'.format(
            print(Y, '\t' * indent, f'累计({cls._global_total:.5f}s) 本轮({delta:.5f}s) [ {msg} ]', E)
        sys.stdout.flush()
        cls._global_current = time()
        return cls

if __name__ == '__main__':
    Timer.printTiming()