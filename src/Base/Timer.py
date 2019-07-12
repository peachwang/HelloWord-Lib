# -*- coding: utf-8 -*-  

from util import *
from time import time

class Timer :

    timing_total = 0
    timing_current = time()
    timing_delta_list = []

    @classmethod
    def printTiming(cls, msg = ''):
        timing_delta = time() - cls.timing_current
        cls.timing_delta_list.append(timing_delta)
        cls.timing_total += timing_delta
        # print(PASS, '当前时刻%s，用时%.2f秒，累计%.2f秒，[%s]' % (DateTime().str(), timing_delta, cls.timing_total, msg), END)
        print('当前时刻%s，用时%.2f秒，累计%.2f秒，[%s]' % (DateTime().str(), timing_delta, cls.timing_total, msg))
        cls.timing_current = time()
        return timing_delta

    @classmethod
    def printLastTiming(cls) :
        if len(cls.timing_delta_list) > 0 : print('用时%.2f秒' % cls.timing_delta_list[-1], end = '')
        return