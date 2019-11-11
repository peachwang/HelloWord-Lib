# -*- coding: utf-8 -*-  
from Object import Object
from datetime import datetime, timedelta
from time import time, strftime

class DateTime(Object) :

    def __init__(self, timestamp_or_datetime = None) :
        Object.__init__(self)
        if timestamp_or_datetime is None :
            self._timestamp = time()
        elif isinstance(timestamp_or_datetime, datetime) :
            self._timestamp = timestamp_or_datetime.timestamp()
        elif isinstance(timestamp, (int, float)) :
            self._timestamp = timestamp

    def fromStr(self, string, pattern = '%Y-%m-%d %H:%M:%S') :
        self._timestamp = datetime.strptime(string, pattern).timestamp()
        return self

    def getRaw(self) :
        return self.datetime

    def j(self) :
        return str(self.datetime)

    def __format__(self, pattern) :
        if pattern == '' : pattern = '%Y-%m-%d %H:%M:%S'
        return strftime(pattern, self.datetime.timetuple())

    def __str__(self) :
        return 'DateTime({})'.format(self.__format__('%Y-%m-%d %H:%M:%S'))

    @property
    def datetime(self):
        return datetime.fromtimestamp(self._timestamp)

    @property
    def date_str(self) :
        return self.__format__('%Y-%m-%d')

    def dateStr(self, pattern) :
        return self.__format__(pattern)

    @property
    def time_str(self) :
        return self.__format__('%H:%M:%S')

    def timeStr(self, pattern) :
        return self.__format__(pattern)
