# -*- coding: utf-8 -*-  
from util import List, Dict, Object, DateTime, time
from functools import wraps

class Timer(Object) :

    _global_total = 0
    _global_current = time()
    _global_delta_list = List()
    _timer_dict = Dict()

    def __init__(self, key) :
        Object.__init__(self)
        self._key = key
        self._total = 0
        self._delta_list = List()

    @property
    def key(self):
        return self._key

    def add(self, delta) :
        self._total += delta
        self._delta_list.append(delta)
        return self

    def len(self) :
        return self._delta_list.len()

    @property
    def total(self):
        return self._total

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
            Timer.printTiming('{}{} 结束'.format(func.__qualname__, msg), delta)
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
        else : raise Exception('timer of key{} not found.'.format(key))
        print(B, '类目({}) 总共({}次, {:.5f}s) 平均({:.5f}s) [ {} ]'.format(
            timer.key,
            timer.len(),
            timer.total,
            timer.average,
            msg
        ), E)
        return cls

    @classmethod
    def printTiming(cls, msg = '', delta = None, indent = 0) :
        from util import Y, E
        timing_delta = time() - cls._global_current
        cls._global_delta_list.append(timing_delta)
        cls._global_total += timing_delta
        if delta is None :
            # print(Y, '{}间隔({:.5f}s) 累计({:.2f}s) [{}] [当前({}) 堆栈({})]'.format(
            print(Y, '{}累计({:.5f}s) 间隔({:.5f}s) [ {} ]'.format(
                '\t' * indent,
                timing_delta,
                cls._global_total,
                msg
                # DateTime(),
                # cls._global_delta_list.len()
            ), E)
        else :
            # print(Y, '{}本轮({:.5f}s) 累计({:.2f}s) [{}] [当前({})]'.format(
            print(Y, '{}累计({:.5f}s) 本轮({:.5f}s) [ {} ]'.format(
                '\t' * indent,
                delta,
                cls._global_total,
                msg
                # DateTime()
            ), E)
        cls._global_current = time()
        return cls

if __name__ == '__main__':
    Timer.printTiming()