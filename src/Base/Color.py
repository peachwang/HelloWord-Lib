# -*- coding: utf-8 -*-  
from functools import wraps

# https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-terminal-in-python
from bcolors import OKMSG as OK, ERRMSG as ERROR, WAITMSG as WAIT

END            = f'\x1b[0m'
FG_BOLD        = f'\x1b[1m'
FG_DISABLE     = f'\x1b[2m'
FG_ITALIC      = f'\x1b[3m'
FG_UNDERLINE   = f'\x1b[4m'
FG_BLINK       = f'\x1b[5m'
FG_REVERSE     = f'\x1b[7m'
FG_HIDE        = f'\x1b[8m'
FG_NORMAL      = f''

FG_RED_DARK    = f'\x1b[31m'
BG_RED_DARK    = f'\x1b[41m'
FG_RED         = f'\x1b[91m'
BG_RED         = f'\x1b[101m'

FG_YELLOW_DARK = f'\x1b[33m'
BG_YELLOW_DARK = f'\x1b[43m'
FG_YELLOW      = f'\x1b[93m'
BG_YELLOW      = f'\x1b[103m'

FG_GREEN_DARK  = f'\x1b[32m'
BG_GREEN_DARK  = f'\x1b[42m'
FG_GREEN       = f'\x1b[92m'
BG_GREEN       = f'\x1b[102m'

FG_CYAN_DARK   = f'\x1b[36m'
BG_CYAN_DARK   = f'\x1b[46m'
FG_CYAN        = f'\x1b[96m'
BG_CYAN        = f'\x1b[106m'

FG_BLUE_DARK   = f'\x1b[34m'
BG_BLUE_DARK   = f'\x1b[44m'
FG_BLUE        = f'\x1b[94m'
BG_BLUE        = f'\x1b[104m'

FG_PINK_DARK   = f'\x1b[35m'
BG_PINK_DARK   = f'\x1b[45m'
FG_PINK        = f'\x1b[95m'
BG_PINK        = f'\x1b[105m'

FG_BLACK       = f'\x1b[30m'
BG_BLACK       = f'\x1b[40m'
FG_GREY        = f'\x1b[90m'
BG_GREY        = f'\x1b[100m'

FG_WHITE_DARK  = f'\x1b[37m'
BG_WHITE_DARK  = f'\x1b[47m'
FG_WHITE       = f'\x1b[97m'
BG_WHITE       = f'\x1b[107m'

NONE = '#NONE#'

class _Color :

    def __init__(self, value = NONE) :
        self._color = self.color # 本色
        if isinstance(value, _Color) : # 样式嵌套
            self._value   = value._value # 继承值
            self._colored = value._colored # 继承是否染色
            if self._colored :
                self._now_color = value._now_color # 继承染色
            else :
                self._now_color = FG_WHITE # 继承无染色
            self._evaluated = False # 未求值
        else :
            self._value     = value # 赋值
            self._now_color = FG_WHITE # 初始无染色
            self._colored   = False # 初始无染色
            if isinstance(value, str) and value == NONE :
                self._evaluated = True # 纯颜色标记
            else :
                self._evaluated = False # 非纯颜色标记

    def __str__(self) :
        return self.__format__('')
        # return f'{self._now_color}{self._colored=} {self._evaluated=}{END} {self._color}{self._value=}{END}'

    def __format__(self, code) :
        if isinstance(self._value, str) and self._value == NONE : # 纯颜色标记
            return self._color
        # 非纯颜色标记
        if self._colored : # 已染色
            _ = f'{self._now_color}{self._value}{END}'
        else : # 未染色
            if self._evaluated : # 已求值
                _ = f'{FG_WHITE}{self._value}{END}'
            else : # 未求值
                _ = f'{self._color}{self._value}{END}'
        delta = len(_) - len(f"{self._value}")
        from Str import Str
        pattern = r'((?P<fill>.)?(?P<align>[<>=^]))?(?P<sign>[+\- ])?(?P<alter>#)?(?P<zero>0)?(?P<width>\d+)?(?P<group>[_,])?(\.(?P<precision>\d+))?(?P<type>[bcdeEfFgGnosxX%])?'
        code = Str(code).fullMatch(pattern).replaceGroup('width', lambda _ : str(int(_) + delta))
        # _ += f'[{code}]'
        return format(_, code)

    def _wrapper(func) :
        @wraps(func)
        def wrapper(self, *args, **kwargs) :
            if self._evaluated and self._colored :
                print(f'{self._value=} {self._colored=} {self._evaluated=}')
                raise Exception('已被求值且染色')
            if func(self, *args, **kwargs) :
                self._colored   = True
                self._now_color = self._color
            self._evaluated = True
            return self
        return wrapper

    @_wrapper
    def __eq__(self, other) : return self._value == other

    @_wrapper
    def __lt__(self, other) : return self._value < other

    @_wrapper
    def __le__(self, other) : return self._value <= other

    @_wrapper
    def __gt__(self, other) : return self._value > other

    @_wrapper
    def __ge__(self, other) : return self._value >= other

class R(_Color) : color = FG_RED
class Y(_Color) : color = FG_YELLOW
class G(_Color) : color = FG_GREEN
class C(_Color) : color = FG_CYAN
class B(_Color) : color = FG_BLUE
class P(_Color) : color = FG_PINK
class S(_Color) : color = FG_GREY # SILVER
class W(_Color) : color = FG_WHITE

class E() :

    def __str__(self) : return self.__format__('')

    def __format__(self, code) : return END
