# -*- coding: utf-8 -*-  
import time
from datetime import timedelta as timedelta_class, datetime as datetime_class, date as date_class, time as time_class, tzinfo as timezone_class
from ..shared import *

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

@add_print_func
@total_ordering
class TimeDelta :

    # @class_property min        The most negative timedelta object, timedelta(-999999999).
    # @class_property max        The most positive timedelta object, timedelta(days=999999999, hours=23, minutes=59, seconds=59, microseconds=999999).
    # @class_property resolution 两个不相等的 timedelta 类对象最小的间隔为 timedelta(microseconds=1)。

    # class datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
    def __init__(self, timedelta = None, **kwargs) :
        if timedelta is None                        : self._timedelta = timedelta_class(**kwargs)
        elif isinstance(timedelta, timedelta_class) : self._timedelta = timedelta
        elif isinstance(timedelta, TimeDelta)       : self._timedelta = timedelta.get_raw()
        else                                        : raise CustomTypeError(timedelta)

    # READ-ONLY PROPERTIES
    # @prop self._timedelta.days         -999999999 至 999999999
    # @prop self._timedelta.seconds               0 至 86399
    # @prop self._timedelta.microseconds          0 至 999999
    
    @cached_prop
    def days(self) -> int : return self._timedelta.days

    @cached_prop
    def weeks(self) -> int : return self.days // 7

    # 0 至 23
    @cached_prop
    def hours(self) -> int : return self._timedelta.seconds // (60 * 60)
    
    # 0 至 59
    @cached_prop
    def minutes(self) -> int : return (self._timedelta.seconds - self.hours * (60 * 60)) // 60

    # 0 至 59
    @cached_prop
    def seconds(self) -> int : return self._timedelta.seconds - self.hours * (60 * 60) - self.minutes * 60

    # 0 至 999999
    @cached_prop
    def microseconds(self) -> int : return self._timedelta.microseconds

    # 0 至 999
    @cached_prop
    def milliseconds(self) -> int : return self.microseconds // 1000

    # 返回时间间隔包含了多少秒。等价于 td / timedelta(seconds=1)。对于其它单位可以直接使用除法的形式 (例如 td / timedelta(microseconds=1))。
    @cached_prop
    def total_seconds(self) -> int : return self._timedelta.total_seconds()

    @cached_prop
    def tuple(self) -> tuple : return (self._timedelta.days, self._timedelta.seconds, self._timedelta.microseconds)

    def get_raw(self) -> timedelta_class : return self._timedelta

    def json_serialize(self) -> dict : return { 'days' : self._timedelta.days, 'seconds' : self._timedelta.seconds, 'microseconds' : self._timedelta.microseconds }

    def copy(self) : return TimeDelta(self.get_raw())

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
    
    def __abs__(self) : return TimeDelta(abs(self._timedelta))

    def abs(self) : return self.__abs__()

    def __pos__(self) : return self

    def __neg__(self) : return TimeDelta(- self._timedelta)

    def __add__(self, other) :
        if isinstance(other, int) and other == 0  : return self
        elif not isinstance(other, TimeDelta)     : raise CustomTypeError(other)
        return TimeDelta(self._timedelta + other.get_raw())

    def __sub__(self, other) :
        if isinstance(other, int) and other == 0 : return self
        elif not isinstance(other, TimeDelta)    : raise CustomTypeError(other)
        return TimeDelta(self._timedelta - other.get_raw())

    def __mul__(self, int_or_float) :
        if not isinstance(int_or_float, (int, float)) : raise CustomTypeError(int_or_float)
        return TimeDelta(self._timedelta * int_or_float)

    def __rmul__(self, int_or_float) : return self.__mul__(int_or_float)

    def __truediv__(self, other_or_int_or_float) :
        if isinstance(other_or_int_or_float, TimeDelta)      : return self._timedelta / other_or_int_or_float.get_raw()
        elif isinstance(other_or_int_or_float, (int, float)) : return TimeDelta(self._timedelta / other_or_int_or_float)
        else                                                 : raise CustomTypeError(other_or_int_or_float)

    def __floordiv__(self, other_or_int_or_float) :
        if isinstance(other_or_int_or_float, TimeDelta)      : return self._timedelta // other_or_int_or_float.get_raw()
        elif isinstance(other_or_int_or_float, (int, float)) : return TimeDelta(self._timedelta // other_or_int_or_float)
        else                                                 : raise CustomTypeError(other_or_int_or_float)

    def __mod__(self, other) :
        if not isinstance(other, TimeDelta) : raise CustomTypeError(other)
        return TimeDelta(self._timedelta % other.get_raw())

    def __divmod__(self, other) :
        if not isinstance(other, TimeDelta) : raise CustomTypeError(other)
        return (self._timedelta // other.get_raw(), TimeDelta(self._timedelta % other.get_raw()))

    def __lt__(self, other) :
        if isinstance(other, int) and other == 0 : return self < TimeDelta()
        elif not isinstance(other, TimeDelta)    : raise CustomTypeError(other)
        return self._timedelta.__lt__(other.get_raw())

    def __eq__(self, other) :
        if isinstance(other, int) and other == 0 : return self == TimeDelta()
        elif not isinstance(other, TimeDelta)    : raise CustomTypeError(other)
        return self._timedelta.__eq__(other.get_raw())

    def __format__(self, spec) :
        if spec == '时'       : return (f'{self.days * 24 + self.hours + self.minutes / 60:>2.1f}小时' if self.days > 0 or self.hours > 0 or self.minutes > 0 else '    ')
        elif spec == '时分'   : return (f'{self.days * 24 + self.hours:>2}小时' if self.days > 0 or self.hours > 0 else '    ') + (f'{self.minutes + self.seconds / 60:>2.1f}分钟' if self.days > 0 or self.hours > 0 or self.minutes > 0 else '    ')
        elif spec == '时分秒' : return (f'{self.days * 24 + self.hours:>2}时' if self.days > 0 or self.hours > 0 else '    ') + (f'{self.minutes:>2}分' if self.days > 0 or self.hours > 0 or self.minutes > 0 else '    ') + f'{self.seconds:>2}秒'
        elif spec == '分'     : return (f'{self.days * 24 * 60 + self.hours * 60 + self.minutes + self.seconds / 60:>2.1f}分钟' if self.days > 0 or self.hours > 0 or self.minutes > 0 or self.seconds > 0 else '    ')
        elif spec == '分秒'   : return (f'{self.days * 1440 + self.hours * 60 + self.minutes:>2}分钟' if self.days > 0 or self.hours > 0 or self.minutes > 0 else '    ') + f'{self.seconds:>2}秒'
        elif spec == '秒'    : return f'{self.days * 86400 + self.hours * 3600 + self.minutes * 60 + self.seconds:>2}秒'
        else                 : return f'{self._timedelta:{spec}}'

    def __str__(self) : return f'TimeDelta({self._timedelta!s})'
    
    def __repr__(self) : return f'TimeDelta({self._timedelta!r})'

@add_print_func
@total_ordering
class Date :

    # @class_property min        最小的日期 date(MINYEAR, 1, 1) 。
    # @class_property max        最大的日期 date(MAXYEAR, 12, 31)。
    # @class_property resolution 两个日期对象的最小间隔，timedelta(days=1)。

    @classmethod
    def today(cls) : return cls(date_class.fromtimestamp(time.time()))

    # 返回对应于预期格列高利历序号的日期，其中公元 1 年 1 月 1 日的序号为 1。
    @classmethod
    def from_ordinal_num(cls, ordinal_num, /) : return cls(date_class.fromordinal(ordinal_num))

    # 返回指定 year, week 和 day 所对应 ISO 历法日期的 date。 这是函数 date.isocalendar() 的逆操作。
    @classmethod
    def from_iso_year_week_day(cls, yaer, week, day, /) : return cls(date_class.fromisocalendar(year, week, day))

    #class datetime.date(year, month, day)
    def __init__(self, timestamp_or_date_or_string = None, /, pattern = '%Y-%m-%d', **kwargs) :
        if timestamp_or_date_or_string is None                     :
            if len(kwargs) > 0 : self._date = date_class(**kwargs)
            else               : self._date = date_class.fromtimestamp(time.time())
        elif isinstance(timestamp_or_date_or_string, date_class)   : self._date = timestamp_or_date_or_string
        elif isinstance(timestamp_or_date_or_string, Date)         : self._date = timestamp_or_date_or_string.get_raw()
        elif isinstance(timestamp_or_date_or_string, (int, float)) :
            if timestamp_or_date_or_string < 10000 or timestamp_or_date_or_string > 2000000000 : raise CustomTypeError(timestamp_or_date_or_string)
            self._date = date_class.fromtimestamp(timestamp_or_datetime_or_string)
        elif isinstance(timestamp_or_date_or_string, str)          : self._date = datetime_class.strptime(f'{timestamp_or_date_or_string} 00:00:00', f'{pattern} %H:%M:%S').date()
        else                                                       : raise CustomTypeError(timestamp_or_date_or_string)

    # 1 <= year <= 9999
    @cached_prop
    def year(self) -> int : return self._date.year

    # 1 <= month <= 12
    @cached_prop
    def month(self) -> int : return self._date.month
    
    # 1 <= day <= 给定年月对应的天数
    @cached_prop
    def day(self) -> int : return self._date.day

    # 返回一个整数代表星期几，星期一为1，星期天为7。例如：date(2002, 12, 4).isoweekday() == 3,表示星期三。
    @cached_prop
    def weekday(self) -> int : return self._date.isoweekday()

    @cached_prop
    def iso_week(self) -> int : return self.iso_tuple[1]

    # 返回一个三元元组，(ISO year, ISO week number, ISO weekday) 。
    # ISO 历法是一种被广泛使用的格列高利历。
    # ISO 年由 52 或 53 个完整星期构成，每个星期开始于星期一结束于星期日。 一个 ISO 年的第一个星期就是（格列高利）历法的一年中第一个包含星期四的星期。 这被称为 1 号星期，这个星期四所在的 ISO 年与其所在的格列高利年相同。
    # 例如，2004 年的第一天是星期四，因此 ISO 2004 年的第一个星期开始于 2003 年 12 月 29 日星期一，结束于 2004 年 1 月 4 日星期日:
    # date(2003, 12, 29).isocalendar() = (2004, 1, 1)
    # date(2004, 1, 4).isocalendar() = (2004, 1, 7)
    @cached_prop
    def iso_tuple(self) -> tuple : return self._date.isocalendar()

    @cached_prop
    def is_workday(self) -> bool : return self.weekday in (1, 2, 3, 4, 5)

    @cached_prop
    def is_weekend(self) -> bool : return self.weekday in (6, 7)

    @cached_prop
    def tuple(self) -> tuple : return (self.year, self.month, self.day)

    def get_raw(self) -> date_class : return self._date

    def json_serialize(self) -> str : return self.__format__('')
    
    # date.replace(year=self.year, month=self.month, day=self.day)
    def replace(self, **kwargs) : return Date(self._date.replace(**kwargs))
    
    def copy(self) : return Date(self._date)

    @cached_prop
    def datetime(self) : return DateTime(year = self.year, month = self.month, day = self.day)

    @cached_prop
    def timestamp(self) -> float : return self.datetime.timestamp

    # 返回日期的预期格列高利历序号，其中公元 1 年 1 月 1 日的序号为 1。 对于任意 date 对象 d，date.fromordinal(d.toordinal()) == d。
    @cached_prop
    def ordinal_num(self) -> int : return self._date.toordinal()

    def to_year(self) : return Year(year = self.year)

    def to_month(self) : return Month(year = self.year, month = self.month)

    def to_week(self) : return Week(year = self.year, month = self.month, day = self.day)

    def __lt__(self, other) : 
        if not isinstance(other, Date) : raise CustomTypeError(other)
        return self._date.__lt__(other.get_raw())

    def __eq__(self, other) :
        if not isinstance(other, Date) : raise CustomTypeError(other)
        return self._date.__eq__(other.get_raw())

    def __add__(self, timedelta_or_days, /) :
        if isinstance(timedelta_or_days, TimeDelta) : return Date(self.get_raw() + timedelta_or_days.get_raw())
        elif isinstance(timedelta_or_days, int)     : return Date(self.get_raw() + TimeDelta(days = timedelta_or_days).get_raw())
        else                                        : raise CustomTypeError(timedelta)

    # date2 = date1 - timedelta 计算 date2 的值使得 date2 + timedelta == date1。 timedelta.seconds 和 timedelta.microseconds 会被忽略。
    # timedelta = date1 - date2 此值完全精确且不会溢出。 操作完成后 timedelta.seconds 和 timedelta.microseconds 均为 0，并且 date2 + timedelta == date1。
    def __sub__(self, timedelta_or_date_or_days, /) :
        if isinstance(timedelta_or_date_or_days, TimeDelta) : return Date(self.get_raw() - timedelta_or_date_or_days.get_raw())
        elif isinstance(timedelta_or_date_or_days, Date)    : return TimeDelta(self.get_raw() - timedelta_or_date_or_days.get_raw())
        elif isinstance(timedelta_or_date_or_days, int)     : return Date(self.get_raw() - TimeDelta(days = timedelta_or_date_or_days).get_raw())
        else                                                : raise CustomTypeError(timedelta_or_date_or_days)

    def __format__(self, spec) : return f'{self._date:{spec}}'

    def __str__(self) : return f'Date({self._date!s})'
    
    def __repr__(self) : return f'Date({self._date!r})'

    @cached_prop
    def with_weekday(self) -> str :
        weekday = {1 : '一', 2 : '二', 3 : '三', 4 : '四', 5 : '五', 6 : '六', 7 : '日'}[self.weekday]
        return f'{self}({weekday})'

@add_print_func
@total_ordering
class Time :

    # @class_property min        早最的可表示 time, time(0, 0, 0, 0)。
    # @class_property max        最晚的可表示 time, time(23, 59, 59, 999999)。
    # @class_property resolution 两个不相等的 time 对象之间可能的最小间隔，timedelta(microseconds=1)，但是请注意 time 对象并不支持算术运算。

    @classmethod
    def now(cls) : return cls(DateTime().time)

    # class datetime.time(hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0)
    def __init__(self, time_or_string = None, /, pattern = '%H:%M:%S', **kwargs) :
        if time_or_string is None                   :
            if len(kwargs) > 0 : self._time = time_class(**kwargs)
            else               : self._time = datetime_class.fromtimestamp(time.time()).time()
        elif isinstance(time_or_string, time_class) : self._time = time_or_string
        elif isinstance(time_or_string, Time)       : self._time = time_or_string.get_raw()
        elif isinstance(time_or_string, str)        : self._time = datetime_class.strptime(time_or_string, pattern).time()
        else                                        : raise CustomTypeError(time_or_string)

    # 0 <= hour < 24
    @cached_prop
    def hour(self) -> int : return self._time.hour

    # 0 <= minute < 60
    @cached_prop
    def minute(self) -> int : return self._time.minute

    # 0 <= second < 60
    @cached_prop
    def second(self) -> int : return self._time.second

    # 0 <= microsecond < 1000000
    @cached_prop
    def microsecond(self) -> int : return self._time.microsecond

    @cached_prop
    def tuple(self) -> tuple : return (self._time.hour, self._time.minute, self._time.second, self._time.microsecond)

    def get_raw(self) -> time_class : return self._time

    def json_serialize(self) -> str : return f'{self:%H:%M:%S.%f}'

    # time.replace(hour=self.hour, minute=self.minute, second=self.second, microsecond=self.microsecond, tzinfo=self.tzinfo, * fold=0)
    def replace(self, **kwargs) : return Time(self._time.replace(**kwargs))
    
    def copy(self) : return Time(self._time)
    
    def __lt__(self, other) :
        if isinstance(other, int) and other == 0 : return self < Time()
        elif not isinstance(other, Time)         : raise CustomTypeError(other)
        return self._time.__lt__(other.get_raw())

    def __eq__(self, other) :
        if isinstance(other, int) and other == 0 : return self == Time()
        elif not isinstance(other, Time)         : raise CustomTypeError(other)
        return self._time.__eq__(other.get_raw())

    def __format__(self, spec) : return f'{self._time:{spec}}'

    def __str__(self) : return f'Time({self._time!s})'
    
    def __repr__(self) : return f'Time({self._time!r})'

@add_print_func
@total_ordering
class DateTime :

    # @class_property min        最早的可表示 datetime，datetime(MINYEAR, 1, 1, tzinfo=None)。
    # @class_property max        最晚的可表示 datetime，datetime(MAXYEAR, 12, 31, 23, 59, 59, 999999, tzinfo=None)。
    # @class_property resolution 两个不相等的 datetime 对象之间可能的最小间隔，timedelta(microseconds=1)。

    # datetime.now(tz=None)
    # datetime.now(timezone.utc)
    @classmethod
    def now(cls) : return cls()

    @classmethod
    def combine(cls, date: Date, time: Time) :
        if not isinstance(date, Date) or not isinstance(time, Time) : raise CustomTypeError((date, time))
        return cls(datetime_class.combine(date.get_raw(), time.get_raw()))

    # class datetime.datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0)
    def __init__(self, timestamp_or_datetime_or_string = None, /, pattern = '%Y-%m-%d %H:%M:%S', **kwargs) :
        if timestamp_or_datetime_or_string is None                       :
            if len(kwargs) > 0 : self._datetime = datetime_class(**kwargs)
            else               : self._datetime = datetime_class.fromtimestamp(time.time())
        elif isinstance(timestamp_or_datetime_or_string, datetime_class) : self._datetime = timestamp_or_datetime_or_string
        elif isinstance(timestamp_or_datetime_or_string, DateTime)       : self._datetime = timestamp_or_datetime_or_string.get_raw()
        elif isinstance(timestamp_or_datetime_or_string, (int, float))   :
            if timestamp_or_datetime_or_string < 10000 or timestamp_or_datetime_or_string > 2000000000 : raise CustomTypeError(timestamp_or_datetime_or_string)
            self._datetime = datetime_class.fromtimestamp(timestamp_or_datetime_or_string)
        elif isinstance(timestamp_or_datetime_or_string, str)            : self._datetime = datetime_class.strptime(timestamp_or_datetime_or_string, pattern)
        else                                                             : raise CustomTypeError(timestamp_or_datetime_or_string)

    # 1 <= year <= 9999
    @cached_prop
    def year(self) -> int : return self._datetime.year
    
    # 1 <= month <= 12
    @cached_prop
    def month(self) -> int : return self._datetime.month
    
    # 1 <= day <= 指定年月的天数
    @cached_prop
    def day(self) -> int : return self._datetime.day

    # 0 <= hour < 24
    @cached_prop
    def hour(self) -> int : return self._datetime.hour
    
    # 0 <= minute < 60
    @cached_prop
    def minute(self) -> int : return self._datetime.minute

    # 0 <= second < 60
    @cached_prop
    def second(self) -> int : return self._datetime.second
    
    # 0 <= microsecond < 1000000
    @cached_prop
    def microsecond(self) -> int : return self._datetime.microsecond

    # 作为 tzinfo 参数被传给 datetime 构造器的对象，如果没有传入值则为 None。
    @cached_prop
    def tzinfo(self) -> timezone_class : return self._datetime.tzinfo

    # fold in [0, 1] 用于在重复的时间段中消除边界时间歧义。 （当夏令时结束时回拨时钟或由于政治原因导致当明时区的 UTC 时差减少就会出现重复的时间段。） 取值 0 (1) 表示两个时刻早于（晚于）所代表的同一边界时间。
    @cached_prop
    def fold(self) -> int : return self._datetime.fold

    @cached_prop
    def tuple(self) -> tuple : return (self.year, self.month, self.day, self.hour, self.minute, self.second, self.microsecond)

    def get_raw(self) : return self._datetime

    # def json_serialize(self) -> list : return list(self.tuple)
    def json_serialize(self) -> list : return { 'sec' : int(self.timestamp), 'usec' : self.microsecond }

    # datetime.replace(year=self.year, month=self.month, day=self.day, hour=self.hour, minute=self.minute, second=self.second, microsecond=self.microsecond, tzinfo=self.tzinfo, * fold=0)
    def replace(self, **kwargs) : return DateTime(self._datetime.replace(**kwargs))
    
    def copy(self) : return DateTime(self._datetime)

    # datetime.astimezone(tz=None)
    def to_timezone(self, timezone = None) : return DateTime(self._datetime.astimezone(timezone))

    @cached_prop
    def timestamp(self) -> float : return self._datetime.timestamp()

    @cached_prop
    def date(self) : return Date(self._datetime.date())

    @cached_prop
    def time(self) : return Time(self._datetime.timetz())

    def __lt__(self, other) :
        if not isinstance(other, DateTime) : raise CustomTypeError(other)
        return self._datetime.__lt__(other.get_raw())

    def __eq__(self, other) :
        if not isinstance(other, DateTime) : raise CustomTypeError(other)
        return self._datetime.__eq__(other.get_raw())

    def __add__(self, timedelta, /) :
        if not isinstance(timedelta, TimeDelta) : raise CustomTypeError(timedelta)
        return DateTime(self._datetime + timedelta.get_raw())

    def __sub__(self, timedelta_or_datetime, /) :
        '''
        从一个 datetime 减去一个 datetime 仅对两个操作数均为简单型或均为感知型时有定义。 如果一个是感知型而另一个是简单型，则会引发 TypeError。
        如果两个操作数都是简单型，或都是感知型并且具有相同的 tzinfo 属性，则 tzinfo 属性会被忽略，并且结果会是一个使得 datetime2 + t == datetime1 的 timedelta 对象 t。 在此情况下不会进行时区调整。
        如果两个操作数都是感知型且具有不同的 tzinfo 属性，a-b 操作的效果就如同 a 和 b 首先被转换为简单型 UTC 日期时间。 结果将是 (a.replace(tzinfo=None) - a.utcoffset()) - (b.replace(tzinfo=None) - b.utcoffset())，除非具体实现绝对不溢出。
        '''
        if isinstance(timedelta_or_datetime, TimeDelta)  : return DateTime(self._datetime - timedelta_or_datetime.get_raw())
        elif isinstance(timedelta_or_datetime, DateTime) : return TimeDelta(self._datetime - timedelta_or_datetime.get_raw())
        else                                             : raise CustomTypeError(timedelta_or_datetime)

    def __format__(self, spec) :
        if spec == '' : spec = '%Y-%m-%d %H:%M:%S' # Microsecond %f
        return f'{self._datetime:{spec}}'

    def __str__(self) : return f'DateTime({self._datetime!s})'
    
    def __repr__(self) : return f'DateTime({self._datetime!r})'

    @cached_prop
    def with_weekday(self) -> str :
        weekday = {1 : '一', 2 : '二', 3 : '三', 4 : '四', 5 : '五', 6 : '六', 7 : '日'}[self.date.weekday]
        return f'{self}({weekday})'

@add_print_func
class DateList :

    def __init__(self, date_list, /) :
        from .List import List
        if not isinstance(date_list, list) : raise CustomTypeError(date_list)
        self._date_list = List(date_list)
    
    @cached_prop
    def date_list(self) : return self._date_list

    def get_raw(self) -> list : return self._date_list.get_raw()

    def json_serialize(self) -> list : return self._date_list.json_serialize()
    
    def len(self) -> int : return self._date_list.len()

    def __getitem__(self, index) -> Date : return self._date_list.__getitem__(index)

    def __iter__(self) : return self._date_list.__iter__()

    @cached_prop
    def workday_list(self) : return DateList(self._date_list.filter(lambda date : date.is_workday))
    
    @cached_prop
    def weekend_list(self) : return DateList(self._date_list.filter(lambda date : date.is_weekend))

    def get_weekday_list(self, weekday: int, /) :
        if weekday not in range(1, 8) : raise CustomTypeError(weekday)
        return DateList(self._date_list.filter(lambda date : date.weekday == weekday))

    def __eq__(self, other) : return self._date_list == other.date_list
    
    def __format__(self, spec) : return f'{self._date_list:{spec}}'

    def __str__(self) : return f'DateList({self._date_list!s})'
    
    def __repr__(self) : return f'DateList({self._date_list!r})'

class DateRange(DateList) :

    def __init__(self, start: Union[date_class, Date, str], end: Union[date_class, Date, str], pattern = '%Y-%m-%d', /, *, step = 1) :
        from .List import List
        start_date = Date(start, pattern)
        end_date   = Date(end, pattern)
        if start_date == end_date : DateList.__init__(self, List()); return
        direction  = step if end_date > start_date else - step
        result     = []
        while start_date != end_date : result.append(start_date); start_date = start_date + direction
        DateList.__init__(self, result)

    @cached_prop
    def first_date(self) -> Date : return self[0]

    @cached_prop
    def last_date(self) -> Date : return self[-1]

    def json_serialize(self) -> list :
        if not isinstance(self, (Year, Month, Week)) : return [ self.first_date, self.last_date + 1 ]
        else                                         : return list(self.tuple)
    
    def __eq__(self, other) : return self.first_date == other.first_date and self.last_date == other.last_date

    # @log_entering()
    def __format__(self, spec) :
        if not isinstance(self, (Year, Month, Week)) : return f"{f'{self.first_date} ~ {self.last_date}':{spec}}"
        else                                         : return f"{f'{self._name}{self.tuple}':{spec}}"

    # @log_entering()
    def __str__(self) :
        if not isinstance(self, (Year, Month, Week)) : return f'DateRange({self.first_date!s} ~ {self.last_date!s})'
        else                                         : return f'{self._name}{self.tuple}'
    
    # @log_entering()
    def __repr__(self) :
        if not isinstance(self, (Year, Month, Week)) : return f'DateRange({self.first_date!r}, {self.last_date + 1!r})'
        else                                         : return f'{self._name}{self.tuple}'

class Year(DateRange) :
    
    _name = 'Year'

    def __init__(self, year) :
        self._year = year
        start = Date(year = year, month = 1,  day = 1)
        end   = Date(year = year + 1, month = 1,  day = 1)
        DateRange.__init__(self, start, end)

    @cached_prop
    def year(self) -> int : return self._year

    @cached_prop
    def tuple(self) -> tuple : return (self._year, )

class Month(DateRange) :
    
    _name = 'Month'
    
    def __init__(self, year, month) :
        self._year  = year
        self._month = month
        start = Date(year = year, month = month,  day = 1)
        if month == 12 : end = Date(year = year + 1, month = 1,  day = 1)
        else           : end = Date(year = year, month = month + 1,  day = 1)
        DateRange.__init__(self, start, end)

    @cached_prop
    def year(self) -> int : return self._year

    @cached_prop
    def month(self) -> int : return self._month

    @cached_prop
    def tuple(self) -> tuple : return (self._year, self._month)

class Week(DateRange) :
    
    _name = 'Week'

    def __init__(self, year, month, day) :
        start = Date(year = year, month = month, day = day)
        start = start - (start.weekday - 1)
        self._year  = start.year
        self._month = start.month
        self._day   = start.day
        DateRange.__init__(self, start, start + 6)

    @cached_prop
    def year(self) -> int : return self._year

    @cached_prop
    def month(self) -> int : return self._month

    @cached_prop
    def day(self) -> int : return self._day

    @cached_prop
    def iso_week(self) -> int : return self.first_date.iso_week

    @cached_prop
    def tuple(self) -> tuple : return (self._year, self._month, self._day)

@add_print_func
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

