# -*- coding: utf-8 -*-  
from Object import Object
from datetime import datetime, timedelta
from time import time, strftime
from shared import ensureArgsType, Optional, Union, UserTypeError, _print, cached_property, lru_cache

class DateTime(Object) :

    # @ensureArgsType
    def __init__(self, timestamp_or_datetime_or_string: Optional[Union[datetime, int, float, str]] = None, pattern = '%Y-%m-%d %H:%M:%S', /) :
        Object.__init__(self)
        self._registerProperty(['timestamp'])
        if timestamp_or_datetime_or_string is None :
            self._timestamp = time()
        elif isinstance(timestamp_or_datetime_or_string, datetime) :
            self._timestamp = timestamp_or_datetime_or_string.timestamp()
        elif isinstance(timestamp_or_datetime_or_string, (int, float)) :
            self._timestamp = timestamp_or_datetime_or_string
        elif isinstance(timestamp_or_datetime_or_string, str) :
            self._timestamp = datetime.strptime(timestamp_or_datetime_or_string, pattern).timestamp()
        else : raise UserTypeError(timestamp_or_datetime_or_string)

    @cached_property
    def getRaw(self) :
        return self.datetime

    @cached_property
    def datetime(self) :
        return datetime.fromtimestamp(self._timestamp)

    def __lt__(self, other, /) : return self.timestamp < other.timestamp
    def __le__(self, other, /) : return self.timestamp <= other.timestamp
    def __gt__(self, other, /) : return self.timestamp > other.timestamp
    def __ge__(self, other, /) : return self.timestamp >= other.timestamp
    def __eq__(self, other, /) : return self.timestamp == other.timestamp
    def __ne__(self, other, /) : return self.timestamp != other.timestamp

    @cached_property
    def date_str(self) :
        return self.__format__('%Y-%m-%d')

    def dateStr(self, pattern, /) :
        return self.__format__(pattern)

    @cached_property
    def time_str(self) :
        return self.__format__('%H:%M:%S')

    def timeStr(self, pattern, /) :
        return self.__format__(pattern)

    def __format__(self, pattern) :
        if pattern == '' : pattern = '%Y-%m-%d %H:%M:%S'
        return strftime(pattern, self.datetime.timetuple())

    @_print
    def printFormat(self) :
        return f'{self}', False

    def __str__(self) :
        return f'DateTime({self.__format__("%Y-%m-%d %H:%M:%S")})'

    @_print
    def printStr(self) :
        return f'{str(self)}', False

    def jsonSerialize(self) :
        return str(self.datetime)

    # 可读化
    def j(self) :
        from util import j
        return j(self.jsonSerialize())

    @_print
    def printJ(self) :
        return f'{self.j()}', False
