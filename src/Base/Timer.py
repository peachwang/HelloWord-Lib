# -*- coding: utf-8 -*-  
from util import *

class Timer(Object) :

    timing_total = 0
    timing_current = time()
    timing_delta_list = []

    @classmethod
    def printTiming(cls, msg = ''):
        timing_delta = time() - cls.timing_current
        cls.timing_delta_list.append(timing_delta)
        cls.timing_total += timing_delta
        print(Y, '当前时刻{}，用时{:.2f}秒，累计{:.2f}秒，[{}]'.format(DateTime(), timing_delta, cls.timing_total, msg), E)
        cls.timing_current = time()
        return timing_delta

    @classmethod
    def reset(cls) :
        cls.timing_total = 0
        cls.timing_current = time()
        cls.timing_delta_list = []

    @classmethod
    def printLastTiming(cls) :
        if len(cls.timing_delta_list) > 0 : print('用时{:.5f}秒'.format(cls.timing_delta_list[-1]), end = '')
        return

if __name__ == '__main__':
    Timer.printTiming()