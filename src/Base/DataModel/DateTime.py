# -*- coding: utf-8 -*-  
from Object import Object
from datetime import datetime, timedelta
from time import time, strftime
from shared import ensureArgsType, Optional, Union, UserTypeError, _print, cached_property, lru_cache

class TimeDelta(timedelta) :

    def __init__(self, *, days = 0, seconds = 0, microseconds = 0, milliseconds = 0, minutes = 0, hours = 0, weeks = 0) :
        timedelta.__init__(self, days, seconds, microseconds, milliseconds, minutes, hours, weeks)
    
    # READ-ONLY PROPERTIES
    @cached_property
    def min(self) : return timedelta.min

    @cached_property
    def max(self) : return timedelta.max

    def __getattr__(self, name) :
        if name in ['hours', 'minutes', 'seconds', 'milliseconds'] :
            return getattr(self, f'_{name}')
        else :
            return getattr(self, name)

    # @property days -999999999 至 999999999
    # @property seconds       0 至 86399
    # @property microseconds  0 至 999999
    
    @cached_property
    def _weeks(self) : return getattr(self, 'days') // 7
    
    @cached_property
    def _hours(self) : return getattr(self, 'seconds') // (60 * 60)
    
    @cached_property
    def _minutes(self) : return (getattr(self, 'seconds') - self._hours * (60 * 60)) // 60

    @cached_property
    def _seconds(self) : return getattr(self, 'seconds') - self._hours * (60 * 60) - self._minutes * 60

    @cached_property
    def _milliseconds(self) : return getattr(self, 'microseconds') // 1000

    @cached_property
    def total_seconds(self) :
        '''返回时间间隔包含了多少秒。等价于 td / timedelta(seconds=1)。对于其它单位可以直接使用除法的形式 (例如 td / timedelta(microseconds=1))。'''
        return timedelta.total_seconds(self)


    
    # OPERATIONS
    # t1 = t2 + t3                 t2 和 t3 的和。 运算后 t1-t2 == t3 and t1-t3 == t2 必为真值。 结果正确，但可能会溢出。
    # t1 = t2 - t3                 t2 减 t3 的差。 运算后 t1 == t2 - t3 and t2 == t1 + t3 必为真值。
    # t1 = t2 * i or t1 = i * t2   乘以一个整数。运算后假如 i != 0 则 t1 // i == t2 必为真值。 In general, t1 * i == t1 * (i-1) + t1 is true.
    # t1 = t2 * f or t1 = f * t2   乘以一个浮点数，结果会被舍入到 timedelta 最接近的整数倍。 精度使用四舍五偶入奇不入规则。
    # f = t2 / t3                  总时间 t2 除以间隔单位 t3 (3)。 返回一个 float 对象。
    # t1 = t2 / f or t1 = t2 / i   除以一个浮点数或整数。 结果会被舍入到 timedelta 最接近的整数倍。 精度使用四舍五偶入奇不入规则。
    # t1 = t2 // i or i = t2 // t3 计算底数，其余部分（如果有）将被丢弃。在第二种情况下，将返回整数。 
    # t1 = t2 % t3                 余数为一个 timedelta 对象。
    # q, r = divmod(t1, t2)        通过 : q = t1 // t2 (3) and r = t1 % t2 计算出商和余数。q是一个整数，r是一个 timedelta 对象。
    # +t1                          返回一个相同数值的 timedelta 对象。
    # -t1                          等价于 timedelta(-t1.days, -t1.seconds, -t1.microseconds), 和 t1* -1. -timedelta.max 不是一个 timedelta 类对象。
    # abs(t)                       当 t.days >= 0 时等于 +t, 当 t.days < 0 时 -t 。
    # str(t)                       返回一个形如 [D day[s], ][H]H:MM:SS[.UUUUUU] 的字符串，当 t 为负数的时候， D 也为负数。 timedelta 对象的字符串表示形式类似于其内部表示形式被规范化。对于负时间增量，这会导致一些不寻常的结果。例如:
    # repr(t)                      返回一个 timedelta 对象的字符串表示形式，作为附带正规属性值的构造器调用。
    
    def __eq__(self, other, /) :
        if not isinstance(other, timedelta) : raise UserTypeError(other)
        else : return timedelta.__eq__(self, other)

    def __ne__(self, other, /) :
        if not isinstance(other, timedelta) : raise UserTypeError(other)
        else : return timedelta.__ne__(self, other)

class DateTime(Object) :

    # @ensureArgsType
    def __init__(self, timestamp_or_datetime_or_string: Optional[Union[datetime, int, float, str]] = None, pattern = '%Y-%m-%d %H:%M:%S', /) :
        super().__init__()
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
        return self.datetime.year

    @cached_property
    def month(self) :
        return self.datetime.month

    @cached_property
    def day(self) :
        return self.datetime.day

    def dateStr(self, pattern, /) :
        return self.__format__(pattern)

    @cached_property
    def time_str(self) :
        return self.__format__('%H:%M:%S')

    @cached_property
    def hour(self) :
        return self.datetime.hour

    @cached_property
    def minute(self) :
        return self.datetime.minute

    @cached_property
    def second(self) :
        return self.datetime.second

    @cached_property
    def microsecond(self) :
        return self.datetime.microsecond

    def timeStr(self, pattern, /) :
        return self.__format__(pattern)

    def __format__(self, pattern) :
        if pattern == '' : pattern = '%Y-%m-%d %H:%M:%S' # Microsecond %f
        return strftime(pattern, self.datetime.timetuple())

    @_print
    def printFormat(self) :
        return f'{self}', False

    def __str__(self) :
        return f'DateTime({self.__format__("")})'

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


class Date(DateTime) :

    def __init__(self, year, month, day) :
        DateTime.__init__(f'{year:04}-{month:02}-{day:02}', pattern = '%Y-%m-%d')
        
