# -*- coding: utf-8 -*-  
from functools import wraps

# https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-terminal-in-python
from bcolors import OKMSG as OK, PASS as GREEN, WARN as YELLOW, ERR, ERRMSG as ERROR, FAIL as RED, WAITMSG as WAIT, BLUE, BOLD, UNDERLINE as U, HEADER as PINK, ITALIC as I, BITALIC, BLUEIC, ENDC as END
# GREEN = '\x1b[102m\x1b[30m'
WHITE = '\x1b[97m\x1b[1m'
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
                self._now_color = WHITE # 继承无染色
            self._evaluated = False # 未求值
        else :
            self._value     = value # 赋值
            self._now_color = WHITE # 初始无染色
            self._colored   = False # 初始无染色
            if value == NONE :
                self._evaluated = True # 纯颜色标记
            else :
                self._evaluated = False # 非纯颜色标记

    def __str__(self) :
        return self.__format__('')
        # return f'{self._now_color}{self._colored=} {self._evaluated=}{END} {self._color}{self._value=}{END}'

    def __format__(self, code) :
        if self._value == NONE : # 纯颜色标记
            return self._color
        # print(code)
        if isinstance(self._value, (int, float)) :
            if len(code) > 0 :
                if code[0] in '123456789' :
                    code = str(int(code) + 13)
                else :
                    code = code[0] + str(int(code[1:]) + 13)
        # print(code)
        # 非纯颜色标记
        if self._colored : # 已染色
            _ = f'{self._now_color}{self._value}{END}'
            # print(len(_))
            return format(_, code)
        else : # 未染色
            if self._evaluated : # 已求值
                _ = f'{WHITE}{self._value}{END}'
            else : # 未求值
                _ = f'{self._color}{self._value}{END}'
            # print(len(_))
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

class R(_Color) : color = RED
class Y(_Color) : color = YELLOW
class G(_Color) : color = GREEN
class P(_Color) : color = PINK
class B(_Color) : color = BLUE
class W(_Color) : color = WHITE

class E() :

    def __str__(self) : return self.__format__('')

    def __format__(self, code) : return END

