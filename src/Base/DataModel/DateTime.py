# -*- coding: utf-8 -*-  

from datetime import datetime
from time import time, strftime, strptime

class DateTime() :

    def __init__(self, timestamp = None) :
        self.timestamp = time() if timestamp is None else timestamp
        self.datetime = datetime.fromtimestamp(self.timestamp)

    def fromStr(self, string, pattern = '%Y-%m-%d %H:%M:%S') :
        self.datetime = datetime.strptime(string, pattern)
        self.timestamp = self.datetime.timestamp()
        return self

    def str(self, pattern = '%Y-%m-%d %H:%M:%S') :
        return strftime(pattern, self.datetime.timetuple())

    def dateStr(self, pattern = '%Y-%m-%d') :
        return self.str(pattern)

    def timeStr(self, pattern = '%H:%M:%S') :
        return self.str(pattern)

if __name__ == '__main__':
    print(DateTime().dateStr('%y%m%d'))