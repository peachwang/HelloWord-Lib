# -*- coding: utf-8 -*-  
import time
from datetime import timedelta as timedelta_class, datetime as datetime_class, date as date_class, time as time_class, tzinfo as timezone_class
from ..shared import *
from .Iter import Iter

# https://docs.python.org/zh-cn/3/library/datetime.html
    # %a  当地工作日的缩写。Sun, Mon, ..., Sat (en_US)
    # %A  本地化的星期中每日的完整名称。 Sunday, Monday, ..., Saturday (en_US)
    # %b  本地化的月缩写名称。当地月份的缩写。 Jan, Feb, ..., Dec (en_US)
    # %B  本地化的月完整名称。 January, February, ..., December (en_US)
    # %c  本地化的适当日期和时间表示。 Tue Aug 16 21:30:00 1988 (en_US)
    # %d  十进制数 [01,31] 表示的月中日。补零后，以十进制数显示的月份中的一天。 01, 02, ..., 31
    # %f  以十进制数表示的毫秒，在左侧补零。 000000, 000001, ..., 999999 当与 strptime() 方法一起使用时，%f 指令可接受一至六个数码及左边的零填充。 %f 是对 C 标准中格式字符集的扩展（但单独在 datetime 对象中实现，因此它总是可用）。
    # %H  十进制数 [00,23] 表示的小时（24小时制）。以补零后的十进制数表示的小时（24 小时制）。 00, 01, ..., 23
    # %I  十进制数 [01,12] 表示的小时（12小时制）。以补零后的十进制数表示的小时（12 小时制）。 01, 02, ..., 12
    # %j  十进制数 [001,366] 表示的年中日。以补零后的十进制数表示的一年中的日序号。 001, 002, ..., 366
    # %m  十进制数 [01,12] 表示的月。补零后，以十进制数显示的月份。 01, 02, ..., 12
    # %M  十进制数 [00,59] 表示的分钟。补零后，以十进制数显示的分钟。 00, 01, ..., 59
    # %p  本地化的 AM 或 PM 。 当与 strptime() 函数一起使用时，如果使用 %I 指令来解析小时， %p 指令只影响输出小时字段。 AM, PM (en_US);
    # %S  十进制数 [00,61] 表示的秒。 范围真的是 0 到 61 ；值 60 在表示 leap seconds 的时间戳中有效，并且由于历史原因支持值 61 。补零后，以十进制数显示的秒。 00, 01, ..., 59
    # %U  十进制数 [00,53] 表示的一年中的周数（星期日作为一周的第一天）作为。在第一个星期日之前的新年中的所有日子都被认为是在第0周。 当与 strptime() 函数一起使用时， %U 和 %W 仅用于指定星期几和年份的计算。以补零后的十进制数表示的一年中的周序号（星期日作为每周的第一天）。 00, 01, ..., 53 当与 strptime() 方法一起使用时，%U 和 %W 仅用于指定星期几和日历年份 (%Y) 的计算。
    # %w  十进制数 [0(星期日),6] 表示的周中日。以十进制数显示的工作日，其中0表示星期日，6表示星期六。 0, 1, ..., 6
    # %W  十进制数 [00,53] 表示的一年中的周数（星期一作为一周的第一天）作为。在第一个星期一之前的新年中的所有日子被认为是在第0周。 当与 strptime() 函数一起使用时， %U 和 %W 仅用于指定星期几和年份的计算。以十进制数表示的一年中的周序号（星期一作为每周的第一天）。 00, 01, ..., 53 当与 strptime() 方法一起使用时，%U 和 %W 仅用于指定星期几和日历年份 (%Y) 的计算。
    # %x  本地化的适当日期表示。 08/16/88 (None); 08/16/1988 (en_US)
    # %X  本地化的适当时间表示。 21:30:00 (en_US)
    # %y  十进制数 [00,99] 表示的没有世纪的年份。补零后，以十进制数表示的，不带世纪的年份。 00, 01, ..., 99
    # %Y  十进制数表示的带世纪的年份。十进制数表示的带世纪的年份。 0001, 0002, ..., 2013, 2014, ..., 9998, 9999 strptime() 方法能够解析整个 [1, 9999] 范围内的年份，但 < 1000 的年份必须加零填充为 4 位数字宽度。 strftime() 方法只限于 years >= 1000。
    # %z  时区偏移以格式 +HHMM 或 -HHMM 形式的 UTC/GMT 的正或负时差指示，其中H表示十进制小时数字，M表示小数分钟数字 [-23:59, +23:59] 。UTC 偏移量，格式为 ±HHMM[SS[.ffffff]] （如果是简单型对象则为空字符串）。 (空), +0000, -0400, +1030, +063415, -030712.345216
    # %Z  时区名称（如果不存在时区，则不包含字符）。时区名称（如果对象为简单型则为空字符串）。 (空), UTC, EST, CST
    # %%  字面的 '%' 字符。 %
    # 当于 strptime() 方法一起使用时，前导的零在格式 %d, %m, %H, %I, %M, %S, %J, %U, %W 和 %V 中是可选的。 格式 %y 不要求有前导的零。
    # 
    # tm_year     （例如，1993）
    # tm_mon      range [1, 12]
    # tm_mday     range [1, 31]
    # tm_hour     range [0, 23]
    # tm_min      range [0, 59]
    # tm_sec      range [0, 61]； 见 strftime() 介绍中的 (2)
    # tm_wday     range [0, 6] ，周一为 0
    # tm_yday     range [1, 366]
    # tm_isdst    0, 1 或 -1；如下所示
    # tm_zone     时区名称的缩写
    # tm_gmtoff   以秒为单位的UTC以东偏离

@printable
@total_ordering
class TimeDelta :

    # @class_property min        The most negative timedelta object, timedelta(-999999999).
    # @class_property max        The most positive timedelta object, timedelta(days=999999999, hours=23, minutes=59, seconds=59, microseconds=999999).
    # @class_property resolution 两个不相等的 timedelta 类对象最小的间隔为 timedelta(microseconds=1)。

    # class datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
    def __init__(self, td = None, **kwargs)    :
        if td is None                        : self._timedelta = timedelta_class(**kwargs)
        elif isinstance(td, timedelta_class) : self._timedelta = td
        elif isinstance(td, TimeDelta)       : self._timedelta = td.get_raw()
        else                                 : raise TypeError(td)

    # READ-ONLY PROPERTIES
    # @prop self._timedelta.days         -999999999 至 999999999
    # @prop self._timedelta.seconds               0 至 86399
    # @prop self._timedelta.microseconds          0 至 999999
    
    @cached_prop
    def days(self) -> int                      : return self._timedelta.days

    @cached_prop
    def weeks(self) -> int                     : return self.days // 7

    # 0 至 23
    @cached_prop
    def hours(self) -> int                     : return self._timedelta.seconds // (60 * 60)
    
    # 0 至 59
    @cached_prop
    def minutes(self) -> int                   : return (self._timedelta.seconds - self.hours * (60 * 60)) // 60

    # 0 至 59
    @cached_prop
    def seconds(self) -> int                   : return self._timedelta.seconds - self.hours * (60 * 60) - self.minutes * 60

    # 0 至 999
    @cached_prop
    def milliseconds(self) -> int              : return self.microseconds // 1000
    
    # 0 至 999999
    @cached_prop
    def microseconds(self) -> int              : return self._timedelta.microseconds

    # 返回时间间隔包含了多少秒。等价于 td / timedelta(seconds=1)。对于其它单位可以直接使用除法的形式 (例如 td / timedelta(microseconds=1))。
    @cached_prop
    def total_seconds(self) -> float           : return self._timedelta.total_seconds()

    @cached_prop
    def tuple(self) -> tuple                   : return (self._timedelta.days, self._timedelta.seconds, self._timedelta.microseconds)

    def get_raw(self) -> timedelta_class       : return self._timedelta

    def json_serialize(self) -> dict           : return { 'days' : self._timedelta.days, 'seconds' : self._timedelta.seconds, 'microseconds' : self._timedelta.microseconds }

    def copy(self)                             : return TimeDelta(self.get_raw())

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
    
    def __abs__(self)                          : return TimeDelta(abs(self._timedelta))

    def abs(self)                              : return self.__abs__()

    def __pos__(self)                          : return self

    def __neg__(self)                          : return TimeDelta(- self._timedelta)

    def __add__(self, other)                   :
        if isinstance(other, int) and other == 0 : return self
        elif isinstance(other, TimeDelta)        : return TimeDelta(self._timedelta + other.get_raw())
        else                                     : raise TypeError(other)
        

    def __sub__(self, other)                   :
        if isinstance(other, int) and other == 0 : return self
        elif isinstance(other, TimeDelta)        : return TimeDelta(self._timedelta - other.get_raw())
        else                                     : raise TypeError(other)
        

    def __mul__(self, int_or_float)            :
        if isinstance(int_or_float, (int, float)) : return TimeDelta(self._timedelta * int_or_float)
        else                                      : raise TypeError(int_or_float)
        

    def __rmul__(self, int_or_float)           : return self.__mul__(int_or_float)

    def __truediv__(self, td_or_int_or_float)  :
        if isinstance(td_or_int_or_float, TimeDelta)      : return self._timedelta / td_or_int_or_float.get_raw()
        elif isinstance(td_or_int_or_float, (int, float)) : return TimeDelta(self._timedelta / td_or_int_or_float)
        else                                              : raise TypeError(td_or_int_or_float)

    def __floordiv__(self, td_or_int_or_float) :
        if isinstance(td_or_int_or_float, TimeDelta)      : return self._timedelta // td_or_int_or_float.get_raw()
        elif isinstance(td_or_int_or_float, (int, float)) : return TimeDelta(self._timedelta // td_or_int_or_float)
        else                                              : raise TypeError(td_or_int_or_float)

    def __mod__(self, other)                   :
        if isinstance(other, TimeDelta) : return TimeDelta(self._timedelta % other.get_raw())
        else                            : raise TypeError(other)
        

    def __divmod__(self, other)                :
        if isinstance(other, TimeDelta) : return (self._timedelta // other.get_raw(), TimeDelta(self._timedelta % other.get_raw()))
        else                            : raise TypeError(other)
        

    def __lt__(self, td_or_int)                :
        if isinstance(td_or_int, TimeDelta)                : return self._timedelta.__lt__(td_or_int.get_raw())
        elif isinstance(td_or_int, int) and td_or_int == 0 : return self < TimeDelta()
        else                                               : raise TypeError(td_or_int)

    def __eq__(self, td_or_int)                :
        if isinstance(td_or_int, TimeDelta)                : return self._timedelta.__eq__(td_or_int.get_raw())
        elif isinstance(td_or_int, int) and td_or_int == 0 : return self == TimeDelta()
        else                                               : raise TypeError(td_or_int)
        

    def __hash__(self) -> int                  : return hash(self._timedelta)

    def __format__(self, spec)                 :
        if spec == '时'       : return (f'{self.days * 24 + self.hours + self.minutes / 60:>2.1f}小时' if self.days > 0 or self.hours > 0 or self.minutes > 0 else '    ')
        elif spec == '时分'   : return (f'{self.days * 24 + self.hours:>2}小时' if self.days > 0 or self.hours > 0 else '    ') + (f'{self.minutes + self.seconds / 60:>2.1f}分钟' if self.days > 0 or self.hours > 0 or self.minutes > 0 else '    ')
        elif spec == '时分秒' : return (f'{self.days * 24 + self.hours:>2}时' if self.days > 0 or self.hours > 0 else '    ') + (f'{self.minutes:>2}分' if self.days > 0 or self.hours > 0 or self.minutes > 0 else '    ') + f'{self.seconds:>2}秒'
        elif spec == '分'     : return (f'{self.days * 24 * 60 + self.hours * 60 + self.minutes + self.seconds / 60:>2.1f}分钟' if self.days > 0 or self.hours > 0 or self.minutes > 0 or self.seconds > 0 else '    ')
        elif spec == '分秒'   : return (f'{self.days * 1440 + self.hours * 60 + self.minutes:>2}分钟' if self.days > 0 or self.hours > 0 or self.minutes > 0 else '    ') + f'{self.seconds:>2}秒'
        elif spec == '秒'    : return f'{self.days * 86400 + self.hours * 3600 + self.minutes * 60 + self.seconds:>2}秒'
        else                 : return f'{self._timedelta:{spec}}'

    def __str__(self)                          : return f'{type(self).__name__}({self._timedelta!s})'
    
    def __repr__(self)                         : return f'{type(self).__name__}({self._timedelta!r})'

@printable
@total_ordering
class Date :

    # @class_property min        最小的日期 date(MINYEAR, 1, 1) 。
    # @class_property max        最大的日期 date(MAXYEAR, 12, 31)。
    # @class_property resolution 两个日期对象的最小间隔，timedelta(days=1)。

    @classmethod
    def today(cls)                                      : return cls(date_class.fromtimestamp(time.time()))

    # 返回对应于预期格列高利历序号的日期，其中公元 1 年 1 月 1 日的序号为 1。
    @classmethod
    def from_ordinal_num(cls, ordinal_num, /)           : return cls(date_class.fromordinal(ordinal_num))

    # 返回指定 year, week 和 day 所对应 ISO 历法日期的 date。 这是函数 date.isocalendar() 的逆操作。
    @classmethod
    def from_iso_year_week_day(cls, yaer, week, day, /) : return cls(date_class.fromisocalendar(year, week, day))

    #class datetime.date(year, month, day)
    def __init__(self, ts_or_d_or_str = None, /, pattern = '%Y-%m-%d', **kwargs) :
        if ts_or_d_or_str is None                     :
            if len(kwargs) > 0 : self._date = date_class(**kwargs)
            else               : self._date = date_class.fromtimestamp(time.time())
        elif isinstance(ts_or_d_or_str, date_class)   : self._date = ts_or_d_or_str
        elif isinstance(ts_or_d_or_str, Date)         : self._date = ts_or_d_or_str.get_raw()
        elif isinstance(ts_or_d_or_str, (int, float)) :
            if ts_or_d_or_str < 10000 or ts_or_d_or_str > 2000000000 : raise ValueError(ts_or_d_or_str)
            self._date = date_class.fromtimestamp(timestamp_or_datetime_or_string)
        elif isinstance(ts_or_d_or_str, str)          : self._date = datetime_class.strptime(f'{ts_or_d_or_str} 00:00:00', f'{pattern} %H:%M:%S').date()
        else                                          : raise TypeError(ts_or_d_or_str)

    # 1 <= year <= 9999
    @cached_prop
    def year(self) -> int                               : return self._date.year

    # 1 <= month <= 12
    @cached_prop
    def month(self) -> int                              : return self._date.month
    
    # 1 <= day <= 给定年月对应的天数
    @cached_prop
    def day(self) -> int                                : return self._date.day

    # 返回一个整数代表星期几，星期一为1，星期天为7。例如：date(2002, 12, 4).isoweekday() == 3,表示星期三。
    @cached_prop
    def weekday(self) -> int                            : return self._date.isoweekday()

    @cached_prop
    def iso_week(self) -> int                           : return self.iso_tuple[1]

    # 返回一个三元元组，(ISO year, ISO week number, ISO weekday) 。
    # ISO 历法是一种被广泛使用的格列高利历。
    # ISO 年由 52 或 53 个完整星期构成，每个星期开始于星期一结束于星期日。 一个 ISO 年的第一个星期就是（格列高利）历法的一年中第一个包含星期四的星期。 这被称为 1 号星期，这个星期四所在的 ISO 年与其所在的格列高利年相同。
    # 例如，2004 年的第一天是星期四，因此 ISO 2004 年的第一个星期开始于 2003 年 12 月 29 日星期一，结束于 2004 年 1 月 4 日星期日:
    # date(2003, 12, 29).isocalendar() = (2004, 1, 1)
    # date(2004, 1, 4).isocalendar() = (2004, 1, 7)
    @cached_prop
    def iso_tuple(self) -> tuple                        : return self._date.isocalendar()

    @cached_prop
    def is_workday(self) -> bool                        : return self.weekday in (1, 2, 3, 4, 5)

    @cached_prop
    def is_weekend(self) -> bool                        : return self.weekday in (6, 7)

    @cached_prop
    def tuple(self) -> tuple                            : return (self.year, self.month, self.day)

    def get_raw(self) -> date_class                     : return self._date

    def json_serialize(self) -> str                     : return self.__format__('')
    
    # date.replace(year=self.year, month=self.month, day=self.day)
    def replace(self, **kwargs)                         : return Date(self._date.replace(**kwargs))
    
    def copy(self)                                      : return Date(self._date)

    @cached_prop
    def datetime(self)                                  : return DateTime(year = self.year, month = self.month, day = self.day)

    @cached_prop
    def timestamp(self) -> float                        : return self.datetime.timestamp

    # 返回日期的预期格列高利历序号，其中公元 1 年 1 月 1 日的序号为 1。 对于任意 date 对象 d，date.fromordinal(d.toordinal()) == d。
    @cached_prop
    def ordinal_num(self) -> int                        : return self._date.toordinal()

    def to_year(self)                                   : return Year(year = self.year)

    def to_month(self)                                  : return Month(year = self.year, month = self.month)

    def to_week(self)                                   : return Week(year = self.year, month = self.month, day = self.day)

    def __add__(self, td_or_days, /)                    :
        if isinstance(td_or_days, TimeDelta) : return Date(self.get_raw() + td_or_days.get_raw())
        elif isinstance(td_or_days, int)     : return Date(self.get_raw() + TimeDelta(days = td_or_days).get_raw())
        else                                 : raise TypeError(td_or_days)

    # date2 = date1 - timedelta 计算 date2 的值使得 date2 + timedelta == date1。 timedelta.seconds 和 timedelta.microseconds 会被忽略。
    # timedelta = date1 - date2 此值完全精确且不会溢出。 操作完成后 timedelta.seconds 和 timedelta.microseconds 均为 0，并且 date2 + timedelta == date1。
    def __sub__(self, td_or_d_or_days, /)               :
        if isinstance(td_or_d_or_days, TimeDelta) : return Date(self.get_raw() - td_or_d_or_days.get_raw())
        elif isinstance(td_or_d_or_days, Date)    : return TimeDelta(self.get_raw() - td_or_d_or_days.get_raw())
        elif isinstance(td_or_d_or_days, int)     : return Date(self.get_raw() - TimeDelta(days = td_or_d_or_days).get_raw())
        else                                      : raise TypeError(td_or_d_or_days)

    def __lt__(self, other)                             :
        if isinstance(other, Date) : return self._date.__lt__(other.get_raw())
        else                       : raise TypeError(other)
        

    def __eq__(self, other)                             :
        if isinstance(other, Date) : return self._date.__eq__(other.get_raw())
        else                       : raise TypeError(other)
        

    def __hash__(self) -> int                           : return hash(self._date)

    def __format__(self, spec)                          : return f'{self._date:{spec}}'

    def __str__(self)                                   : return f'{type(self).__name__}({self._date!s})'
    
    def __repr__(self)                                  : return f'{type(self).__name__}({self._date!r})'

    @cached_prop
    def with_weekday(self) -> str                       :
        weekday = {1 : '一', 2 : '二', 3 : '三', 4 : '四', 5 : '五', 6 : '六', 7 : '日'}[self.weekday]
        return f'{self}({weekday})'

@printable
@total_ordering
class Time :

    # @class_property min        早最的可表示 time, time(0, 0, 0, 0)。
    # @class_property max        最晚的可表示 time, time(23, 59, 59, 999999)。
    # @class_property resolution 两个不相等的 time 对象之间可能的最小间隔，timedelta(microseconds=1)，但是请注意 time 对象并不支持算术运算。

    @classmethod
    def now(cls)                    : return cls(DateTime().time)

    # class datetime.time(hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0)
    def __init__(self, t_or_str = None, /, pattern = '%H:%M:%S', **kwargs) :
        if t_or_str is None                   :
            if len(kwargs) > 0 : self._time = time_class(**kwargs)
            else               : self._time = datetime_class.fromtimestamp(time.time()).time()
        elif isinstance(t_or_str, time_class) : self._time = t_or_str
        elif isinstance(t_or_str, Time)       : self._time = t_or_str.get_raw()
        elif isinstance(t_or_str, str)        : self._time = datetime_class.strptime(t_or_str, pattern).time()
        else                                  : raise TypeError(t_or_str)

    # 0 <= hour < 24
    @cached_prop
    def hour(self) -> int           : return self._time.hour

    # 0 <= minute < 60
    @cached_prop
    def minute(self) -> int         : return self._time.minute

    # 0 <= second < 60
    @cached_prop
    def second(self) -> int         : return self._time.second

    # 0 <= microsecond < 1000000
    @cached_prop
    def microsecond(self) -> int    : return self._time.microsecond

    @cached_prop
    def tuple(self) -> tuple        : return (self._time.hour, self._time.minute, self._time.second, self._time.microsecond)

    def get_raw(self) -> time_class : return self._time

    def json_serialize(self) -> str : return f'{self:%H:%M:%S.%f}'

    # time.replace(hour=self.hour, minute=self.minute, second=self.second, microsecond=self.microsecond, tzinfo=self.tzinfo, * fold=0)
    def replace(self, **kwargs)     : return Time(self._time.replace(**kwargs))
    
    def copy(self)                  : return Time(self._time)
    
    def __lt__(self, t_or_int)      :
        if isinstance(t_or_int, Time)                    : return self._time.__lt__(t_or_int.get_raw())
        elif isinstance(t_or_int, int) and t_or_int == 0 : return self < Time()
        else                                             : raise TypeError(t_or_int)

    def __eq__(self, t_or_int)      :
        if isinstance(t_or_int, Time)                    : return self._time.__eq__(t_or_int.get_raw())
        elif isinstance(t_or_int, int) and t_or_int == 0 : return self == Time()
        else                                             : raise TypeError(t_or_int)

    def __hash__(self) -> int       : return hash(self._time)

    def __format__(self, spec)      : return f'{self._time:{spec}}'

    def __str__(self)               : return f'{type(self).__name__}({self._time!s})'
    
    def __repr__(self)              : return f'{type(self).__name__}({self._time!r})'

@printable
@total_ordering
class DateTime :

    # @class_property min        最早的可表示 datetime，datetime(MINYEAR, 1, 1, tzinfo=None)。
    # @class_property max        最晚的可表示 datetime，datetime(MAXYEAR, 12, 31, 23, 59, 59, 999999, tzinfo=None)。
    # @class_property resolution 两个不相等的 datetime 对象之间可能的最小间隔，timedelta(microseconds=1)。

    # datetime.now(tz=None)
    # datetime.now(timezone.utc)
    @classmethod
    def now(cls)                             : return cls()

    @classmethod
    def combine(cls, date: Date, time: Time) :
        if not isinstance(date, Date) or not isinstance(time, Time) : raise TypeError((date, time))
        return cls(datetime_class.combine(date.get_raw(), time.get_raw()))

    # class datetime.datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0)
    def __init__(self, ts_or_dt_or_str_or_dct = None, /, pattern = '%Y-%m-%d %H:%M:%S', **kwargs) :
        if ts_or_dt_or_str_or_dct is None                       :
            if len(kwargs) > 0 : self._datetime = datetime_class(**kwargs)
            else               : self._datetime = datetime_class.fromtimestamp(time.time())
        elif isinstance(ts_or_dt_or_str_or_dct, datetime_class) : self._datetime = ts_or_dt_or_str_or_dct
        elif isinstance(ts_or_dt_or_str_or_dct, DateTime)       : self._datetime = ts_or_dt_or_str_or_dct.get_raw()
        elif isinstance(ts_or_dt_or_str_or_dct, (int, float))   :
            if ts_or_dt_or_str_or_dct < 10000 or ts_or_dt_or_str_or_dct > 2000000000 : raise ValueError(ts_or_dt_or_str_or_dct)
            self._datetime = datetime_class.fromtimestamp(ts_or_dt_or_str_or_dct)
        elif isinstance(ts_or_dt_or_str_or_dct, str)            : self._datetime = datetime_class.strptime(ts_or_dt_or_str_or_dct, pattern)
        elif (isinstance(ts_or_dt_or_str_or_dct, dict)
            and len(ts_or_dt_or_str_or_dct) == 2
            and 'sec' in ts_or_dt_or_str_or_dct
            and 'usec' in ts_or_dt_or_str_or_dct)               :
            self._datetime = datetime_class.fromtimestamp(ts_or_dt_or_str_or_dct['sec'] + ts_or_dt_or_str_or_dct['usec'] / 1000000)
        else                                                    : raise CustomTypeError(ts_or_dt_or_str_or_dct)

    # 1 <= year <= 9999
    @cached_prop
    def year(self) -> int                    : return self._datetime.year
    
    # 1 <= month <= 12
    @cached_prop
    def month(self) -> int                   : return self._datetime.month
    
    # 1 <= day <= 指定年月的天数
    @cached_prop
    def day(self) -> int                     : return self._datetime.day

    # 0 <= hour < 24
    @cached_prop
    def hour(self) -> int                    : return self._datetime.hour
    
    # 0 <= minute < 60
    @cached_prop
    def minute(self) -> int                  : return self._datetime.minute

    # 0 <= second < 60
    @cached_prop
    def second(self) -> int                  : return self._datetime.second
    
    # 0 <= microsecond < 1000000
    @cached_prop
    def microsecond(self) -> int             : return self._datetime.microsecond

    # 作为 tzinfo 参数被传给 datetime 构造器的对象，如果没有传入值则为 None。
    @cached_prop
    def tzinfo(self) -> timezone_class       : return self._datetime.tzinfo

    # fold in [0, 1] 用于在重复的时间段中消除边界时间歧义。 （当夏令时结束时回拨时钟或由于政治原因导致当明时区的 UTC 时差减少就会出现重复的时间段。） 取值 0 (1) 表示两个时刻早于（晚于）所代表的同一边界时间。
    @cached_prop
    def fold(self) -> int                    : return self._datetime.fold

    @cached_prop
    def tuple(self) -> tuple                 : return (self.year, self.month, self.day, self.hour, self.minute, self.second, self.microsecond)

    def get_raw(self)                        : return self._datetime

    # def json_serialize(self) -> list : return list(self.tuple)
    def json_serialize(self) -> dict         : return { 'sec' : int(self.timestamp), 'usec' : self.microsecond }

    # datetime.replace(year=self.year, month=self.month, day=self.day, hour=self.hour, minute=self.minute, second=self.second, microsecond=self.microsecond, tzinfo=self.tzinfo, * fold=0)
    def replace(self, **kwargs)              : return DateTime(self._datetime.replace(**kwargs))
    
    def copy(self)                           : return DateTime(self._datetime)

    # datetime.astimezone(tz=None)
    def to_timezone(self, timezone = None)   : return DateTime(self._datetime.astimezone(timezone))

    @cached_prop
    def timestamp(self) -> float             : return self._datetime.timestamp()

    @cached_prop
    def date(self)                           : return Date(self._datetime.date())

    @cached_prop
    def time(self)                           : return Time(self._datetime.timetz())

    def __add__(self, td, /)                 :
        if isinstance(td, TimeDelta) : return DateTime(self._datetime + td.get_raw())
        else                         : raise CustomTypeError(td)

    def __sub__(self, td_or_dt, /)           :
        '''
        从一个 datetime 减去一个 datetime 仅对两个操作数均为简单型或均为感知型时有定义。 如果一个是感知型而另一个是简单型，则会引发 TypeError。
        如果两个操作数都是简单型，或都是感知型并且具有相同的 tzinfo 属性，则 tzinfo 属性会被忽略，并且结果会是一个使得 datetime2 + t == datetime1 的 timedelta 对象 t。 在此情况下不会进行时区调整。
        如果两个操作数都是感知型且具有不同的 tzinfo 属性，a-b 操作的效果就如同 a 和 b 首先被转换为简单型 UTC 日期时间。 结果将是 (a.replace(tzinfo=None) - a.utcoffset()) - (b.replace(tzinfo=None) - b.utcoffset())，除非具体实现绝对不溢出。
        '''
        if isinstance(td_or_dt, TimeDelta)  : return DateTime(self._datetime - td_or_dt.get_raw())
        elif isinstance(td_or_dt, DateTime) : return TimeDelta(self._datetime - td_or_dt.get_raw())
        else                                : raise CustomTypeError(td_or_dt)

    def __lt__(self, other)                  :
        if isinstance(other, DateTime) : return self._datetime.__lt__(other.get_raw())
        else                           : raise CustomTypeError(other)
        

    def __eq__(self, other)                  :
        if isinstance(other, DateTime) : return self._datetime.__eq__(other.get_raw())
        else                           : raise CustomTypeError(other)
        

    def __hash__(self) -> int                : return hash(self._datetime)

    def __format__(self, spec)               :
        if spec == '' : spec = '%Y-%m-%d %H:%M:%S' # Microsecond %f
        return f'{self._datetime:{spec}}'

    def __str__(self)                        : return f'{type(self).__name__}({self._datetime!s})'
    
    def __repr__(self)                       : return f'{type(self).__name__}({self._datetime!r})'

    @cached_prop
    def with_weekday(self) -> str            :
        weekday = {1 : '一', 2 : '二', 3 : '三', 4 : '四', 5 : '五', 6 : '六', 7 : '日'}[self.date.weekday]
        return f'{self}({weekday})'

@iterable
@printable
@total_ordering
class DateList : # Immutable

    def __init__(self, date_iterable, /)        :
        from .List import List
        self._date_list = List(Date(date) for date in date_iterable)
    
    def __iter__(self)                          : return self._date_list.iter

    @prop
    def list(self)                              : raise NotImplementedError # 不允许访问内部数据，以避免 制作副本缓存后被修改 vs 不缓存反复制作副本的开销 之间的矛盾

    def __len__(self) -> int                    : return len(self._date_list)
    
    def __getitem__(self, index) -> Date        : return self._date_list[index]

    # def get_raw(self) -> list                   : return self._date_list.get_raw()
    def get_raw(self) -> list                   : raise NotImplementedError

    def json_serialize(self) -> list            : return self._date_list.json_serialize()

    @prop
    def workday_iter(self)                      : return Iter(date for date in self if date.is_workday)
    
    @prop
    def weekend_iter(self)                      : return Iter(date for date in self if date.is_weekend)

    def get_weekday_iter(self, weekday: int, /) :
        if weekday in range(1, 8) : return Iter(date for date in self._date_list if date.weekday == weekday)
        else                      : raise ValueError(weekday)

    __lt__ = None

    def __eq__(self, other)                     :
        if type(self) == DateList : return self._date_list == other._date_list
        else                      : raise TypeError(other)

    def __format__(self, spec)                  : return f'{self._date_list:{spec}}'

    def __str__(self)                           : return f'{type(self).__name__}({self._date_list!s})'
    
    def __repr__(self)                          : return f'{type(self).__name__}({self._date_list!r})'

@iterable
@sized
@printable
@total_ordering
class DateRange(DateList) : # Immutable

    def __init__(self, start: Union[date_class, Date, str], end: Union[date_class, Date, str], pattern = '%Y-%m-%d', /, *, step_days: int = 1) :
        self._start_date = Date(start, pattern)
        self._end_date   = Date(end, pattern)
        self._step_days  = step_days
        if not isinstance(step_days, int) or step_days == 0 or (self._end_date > self._start_date) != (step_days > 0) :
            raise ValueError((self._start_date, self._end_date, step_days))

    @cached_prop
    def start_date(self) -> Date         : return self._start_date

    @cached_prop
    def end_date(self) -> Date           : return self._end_date

    @cached_prop
    def step_days(self) -> int           : return self._step_days

    def __iter__(self)                   :
        date = self._start_date
        while date < self._end_date : yield date; date = date + self._step_days

    @prop
    def list(self)                       : raise NotImplementedError # 不允许访问内部数据，以避免 制作副本缓存后被修改 vs 不缓存反复制作副本的开销 之间的矛盾

    def __len__(self) -> int             : return (self._end_date - self._start_date).abs().days
    
    def __getitem__(self, index) -> Date : raise NotImplementedError

    # def get_raw(self) -> list            : return List(self._start_date, self._end_date).get_raw()
    def get_raw(self) -> list            : raise NotImplementedError
    
    def json_serialize(self) -> list     : return list(self.tuple) if isinstance(self, (Year, Month, Week)) else [ self._start_date, self._end_date ]

    @prop
    def related_week_iter(self)          : return Iter(Week(date.year, date.month, date.day) for date in self).unique()

    def __lt__(self, other)              :
        if type(self) != DateRange and type(self) == type(other) : return self.tuple < other.tuple
        else                                                     : raise CustomTypeError(other)

    def __eq__(self, other)              : return self._start_date == other.start_date and self._end_date == other.end_date

    # @log_entering
    def __format__(self, spec)           :
        if type(self) == DateRange : return f'{f"{self._start_date} ~ {self._end_date}":{spec}}'
        else                       : return f'{f"{type(self).__name__}{self.tuple}":{spec}}'

    # @log_entering
    def __str__(self)                    :
        if type(self) == DateRange : return f'{type(self).__name__}({self._start_date!s} ~ {self._end_date!s})'
        else                       : return f'{type(self).__name__}{self.tuple}'
    
    # @log_entering
    def __repr__(self)                   :
        if type(self) == DateRange : return f'{type(self).__name__}({self._start_date!r}, {self._end_date!r})'
        else                       : return f'{type(self).__name__}{self.tuple}'

class Year(DateRange) : # Immutable
    
    def __init__(self, year)  :
        self._year = year
        start_date = Date(year = year, month = 1,  day = 1)
        end_date   = Date(year = year + 1, month = 1,  day = 1)
        DateRange.__init__(self, start_date, end_date)

    @cached_prop
    def year(self) -> int     : return self._year

    @cached_prop
    def tuple(self) -> tuple  : return (self._year, )

    def __hash__(self) -> int : return hash(self.tuple)

class Month(DateRange) : # Immutable
    
    def __init__(self, year, month) :
        self._year  = year
        self._month = month
        start_date = Date(year = year, month = month,  day = 1)
        if month == 12 : end_date = Date(year = year + 1, month = 1,  day = 1)
        else           : end_date = Date(year = year, month = month + 1,  day = 1)
        DateRange.__init__(self, start_date, end_date)

    @cached_prop
    def year(self) -> int           : return self._year

    @cached_prop
    def month(self) -> int          : return self._month

    @cached_prop
    def tuple(self) -> tuple        : return (self._year, self._month)

    def __hash__(self) -> int       : return hash(self.tuple)

class Week(DateRange) : # Immutable
    
    def __init__(self, year, month, day) :
        start_date = Date(year = year, month = month, day = day)
        start_date = start_date - (start_date.weekday - 1)
        self._year  = start_date.year
        self._month = start_date.month
        self._day   = start_date.day
        DateRange.__init__(self, start_date, start_date + 7)

    @cached_prop
    def year(self) -> int                : return self._year

    @cached_prop
    def month(self) -> int               : return self._month

    @cached_prop
    def day(self) -> int                 : return self._day

    @cached_prop
    def iso_week(self) -> int            : return self._start_date.iso_week

    @cached_prop
    def tuple(self) -> tuple             : return (self._year, self._month, self._day)

    def __hash__(self) -> int            : return hash(self.tuple)

@printable
class TimeZone :

    # class_property utc UTC 时区，timezone(timedelta(0))。

    # datetime.timezone(offset, name=None)
    # offset 参数必须指定为一个 timedelta 对象，表示本地时间与 UTC 的时差。 它必须严格限制于 -timedelta(hours=24) 和 timedelta(hours=24) 之间，否则会引发 ValueError。
    def __init__(self, offset: TimeDelta, name: str = None, /) : self._timezone = timezone_class(offset, name)

    # 返回当 timezone 实例被构造时指定的固定值。
    # dt 参数会被忽略。 返回值是一个 timedelta 实例，其值等于本地时间与 UTC 之间的时差。
    def utcoffset(self, dt: DateTime, /) -> timedelta_class : return self._timezone.utcoffset(dt)

    # 返回当 timezone 实例被构造时指定的固定值。
    # 如果没有在构造器中提供 name，则 tzname(dt) 所返回的名称将根据 offset 值按以下规则生成。 如果 offset 为 timedelta(0)，则名称为“UTC”，否则为字符串 UTC±HH:MM，其中 ± 为 offset 的正负符号，HH 和 MM 分别为表示 offset.hours 和 offset.minutes 的两个数码。
    # 由 offset=timedelta(0) 生成的名称现在为简单的 'UTC' 而不再是 'UTC+00:00'。
    def tzname(self, dt: DateTime, /) -> str : return self._timezone.tzname(dt)

    # 以下示例定义了一个 tzinfo 子类，它捕获 Kabul, Afghanistan 时区的信息，该时区使用 +4 UTC 直到 1945 年，之后则使用 +4:30 UTC:
    # from datetime import timedelta, datetime, tzinfo, timezone
    # class KabulTz(tzinfo):
    # Kabul used +4 until 1945, when they moved to +4:30
    # UTC_MOVE_DATE = datetime(1944, 12, 31, 20, tzinfo=timezone.utc)

    # def utcoffset(self, dt):
    #     if dt.year < 1945:
    #         return timedelta(hours=4)
    #     elif (1945, 1, 1, 0, 0) <= dt.timetuple()[:5] < (1945, 1, 1, 0, 30):
    #         # An ambiguous ("imaginary") half-hour range representing
    #         # a 'fold' in time due to the shift from +4 to +4:30.
    #         # If dt falls in the imaginary range, use fold to decide how
    #         # to resolve. See PEP495.
    #         return timedelta(hours=4, minutes=(30 if dt.fold else 0))
    #     else:
    #         return timedelta(hours=4, minutes=30)

    # def fromutc(self, dt):
    #     # Follow same validations as in datetime.tzinfo
    #     if not isinstance(dt, datetime):
    #         raise TypeError("fromutc() requires a datetime argument")
    #     if dt.tzinfo is not self:
    #         raise ValueError("dt.tzinfo is not self")

    #     # A custom implementation is required for fromutc as
    #     # the input to this function is a datetime with utc values
    #     # but with a tzinfo set to self.
    #     # See datetime.astimezone or fromtimestamp.
    #     if dt.replace(tzinfo=timezone.utc) >= self.UTC_MOVE_DATE:
    #         return dt + timedelta(hours=4, minutes=30)
    #     else:
    #         return dt + timedelta(hours=4)

    # def dst(self, dt):
    #     # Kabul does not observe daylight saving time.
    #     return timedelta(0)

    # def tzname(self, dt):
    #     if dt >= self.UTC_MOVE_DATE:
    #         return "+04:30"

if __name__ == '__main__':
    print(TimeDelta())
    print(Date())
    print(Time())
    print(DateTime())

