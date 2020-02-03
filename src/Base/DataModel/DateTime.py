# -*- coding: utf-8 -*-  
from Object import Object
from datetime import datetime, timedelta
from time import time, strftime
from shared import ensureArgsType, Optional, Union, UserTypeError

class DateTime(Object) :

    # @ensureArgsType
    def __init__(self, timestamp_or_datetime: Optional[Union[datetime, int, float]] = None, /) :
        Object.__init__(self)
        self._registerProperty(['timestamp'])
        if timestamp_or_datetime is None :
            self._timestamp = time()
        elif isinstance(timestamp_or_datetime, datetime) :
            self._timestamp = timestamp_or_datetime.timestamp()
        elif isinstance(timestamp_or_datetime, (int, float)) :
            self._timestamp = timestamp_or_datetime
        else : raise UserTypeError(timestamp_or_datetime)

    def fromStr(self, string, pattern = '%Y-%m-%d %H:%M:%S', /) :
        self._timestamp = datetime.strptime(string, pattern).timestamp()
        return self

    def getRaw(self) :
        return self.datetime

    def jsonSerialize(self) :
        return str(self.datetime)

    # 可读化
    def j(self) :
        from util import j
        return j(self.jsonSerialize())

    def print(self, *, color = '') :
        from util import E
        print(color, self.j(), E() if color != '' else '')
        return self

    def __format__(self, pattern) :
        if pattern == '' : pattern = '%Y-%m-%d %H:%M:%S'
        return strftime(pattern, self.datetime.timetuple())

    def __str__(self) :
        return f'DateTime({self.__format__("%Y-%m-%d %H:%M:%S")})'

    @property
    def datetime(self):
        return datetime.fromtimestamp(self._timestamp)

    @property
    def date_str(self) :
        return self.__format__('%Y-%m-%d')

    def dateStr(self, pattern, /) :
        return self.__format__(pattern)

    @property
    def time_str(self) :
        return self.__format__('%H:%M:%S')

    def timeStr(self, pattern, /) :
        return self.__format__(pattern)
