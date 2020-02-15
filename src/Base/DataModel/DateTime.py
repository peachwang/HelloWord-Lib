# -*- coding: utf-8 -*-  
from Object import Object
from datetime import datetime, timedelta
from time import time, strftime
from shared import ensureArgsType, Optional, Union, UserTypeError, _print, cached_property, lru_cache

class DateTime(Object) :

    # @ensureArgsType
    def __init__(self, timestamp_or_datetime_or_string: Optional[Union[datetime, int, float, str]] = None, pattern = '%Y-%m-%d %H:%M:%S', /) :
        super().__init__()
        self._registerProperty(['timestamp', 'datetime'])
        if timestamp_or_datetime_or_string is None :
            self._timestamp = time()
        elif isinstance(timestamp_or_datetime_or_string, datetime) :
            self._timestamp = timestamp_or_datetime_or_string.timestamp()
        elif isinstance(timestamp_or_datetime_or_string, (int, float)) :
            self._timestamp = timestamp_or_datetime_or_string
        elif isinstance(timestamp_or_datetime_or_string, str) :
            self._timestamp = datetime.strptime(timestamp_or_datetime_or_string, pattern).timestamp()
        else : raise UserTypeError(timestamp_or_datetime_or_string)
        self._datetime = datetime.fromtimestamp(self._timestamp)

    @cached_property
    def getRaw(self) :
        return self._datetime

    def __lt__(self, other, /) : return self._timestamp < other.timestamp
    def __le__(self, other, /) : return self._timestamp <= other.timestamp
    def __gt__(self, other, /) : return self._timestamp > other.timestamp
    def __ge__(self, other, /) : return self._timestamp >= other.timestamp
    def __eq__(self, other, /) : return self._timestamp == other.timestamp
    def __ne__(self, other, /) : return self._timestamp != other.timestamp

    @cached_property
    def date_str(self) :
        return self.__format__('%Y-%m-%d')

    @cached_property
    def year(self) :
        return self._datetime.year

    @cached_property
    def month(self) :
        return self._datetime.month

    @cached_property
    def day(self) :
        return self._datetime.day

    def dateStr(self, pattern, /) :
        return self.__format__(pattern)

    @cached_property
    def time_str(self) :
        return self.__format__('%H:%M:%S')

    @cached_property
    def hour(self) :
        return self._datetime.hour

    @cached_property
    def minute(self) :
        return self._datetime.minute

    @cached_property
    def second(self) :
        return self._datetime.second

    @cached_property
    def microsecond(self) :
        return self._datetime.microsecond

    def timeStr(self, pattern, /) :
        return self.__format__(pattern)

    def __format__(self, pattern) :
        if pattern == '' : pattern = '%Y-%m-%d %H:%M:%S' # Microsecond %f
        return strftime(pattern, self._datetime.timetuple())

    @_print
    def printFormat(self) :
        return f'{self}', False

    def __str__(self) :
        return f'DateTime({self.__format__("")})'

    @_print
    def printStr(self) :
        return f'{str(self)}', False

    def jsonSerialize(self) :
        return str(self._datetime)

    # 可读化
    def j(self) :
        from util import j
        return j(self.jsonSerialize())

    @_print
    def printJ(self) :
        return f'{self.j()}', False
