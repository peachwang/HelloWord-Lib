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
        print(PASS, '当前时刻%s，用时%.2f秒，累计%.2f秒，[%s]' % (DateTime().str(), timing_delta, cls.timing_total, msg), END)
        cls.timing_current = time()
        return timing_delta