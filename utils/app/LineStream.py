# -*- coding: utf-8 -*-
from ..shared         import *
from ..datatypes.Str  import Str
from ..datatypes.Iter import Iter
class _Line :

    # @Timer.timeit_total('_Line.__init__')
    def __init__(self, index, raw_line, /) :
        self._index, self._raw_line = index, Str(raw_line)

    def tag_by_format_list(self, tag_format_list, /) :
        for tag_format in tag_format_list :
            if (   tag_format == '[]'  and (m := self._raw_line.full_match(r'^\[(?P<tag_name>[^\[\]]+)\](?P<content>.*)$'))
                or tag_format == '#'   and (m := self._raw_line.full_match(r'^#(?P<tag_name>[^ ]+) *(?P<content>.*)$'))
                or tag_format == '【】' and (m := self._raw_line.full_match(r'^【(?P<tag_name>[^【】]+)】(?P<content>.*)$'))) :
                self._tag_name, self._content, self._tag_format = m.tag_name, m.content, tag_format
                return self
        raise ValueError(f'{self._index + 1:>5}.[{self._raw_line}]不匹配{tag_format_list=}')

    def tag_by_context(self, *, tag_func, raw_line_list) :
        self._tag_name = tag_func(raw_line_list = raw_line_list, index = self._index - 1)
        self._content  = self._raw_line
        return self

    @cached_prop
    def raw(self) :
        if hasattr(self, '_tag_format') : return (self._index, self._raw_line, self._tag_format)
        else                            : return (self._index, self._raw_line)

    @cached_prop
    def tag_name(self) -> str : return str(self._tag_name)

    @cached_prop
    def tag_type(self) -> str : return str(self._content.split(' ')[0])

    def __format__(self, spec) : return f'{f"index = [{self._index}] tag_name = [{self._tag_name}] content = [{self._content}]":{spec}}'

class LineStream :

    # @Timer.timeit_total('LineStream.__init__')
    def __init__(self, raw_line_list = None, /) :
        self._raw_line_list            = raw_line_list or []
        self._tag_name_to_line_content = {}
        self._tag_name_to_sub_stream   = {}
        self._sub_stream_list          = []

    def tag_by_format_list(self, tag_format_list = None, /) :
        self._line_list = [
            _Line(index + 1, raw_line).tag_by_format_list(tag_format_list)
            for index, raw_line in enumerate(self._raw_line_list)
            if not Str(raw_line).is_empty()
        ]
        return self
    
    def tag_by_context(self, *, tag_func) :
        self._line_list = [
            _Line(index + 1, raw_line).tag_by_context(tag_func = tag_func, raw_line_list = self._raw_line_list)
            for index, raw_line in enumerate(self._raw_line_list)
        ]
        return self

    def set_tag_line(self, tag_line, /) :
        self._tag_line                                    = tag_line
        self._tag_name_to_line_content[tag_line.tag_name] = tag_line.content
        self._line_list                                   = []
        return self

    def append_line(self, line, /) : self._line_list.append(line); return self

    def set_tag_name(self, tag_name: str, /) : self._tag_name = tag_name; return self

    @cached_prop
    def tag_name(self) -> str :
        if hasattr(self, '_tag_line') : return self._tag_line.tag_name
        else                          : return self._tag_name

    def _append_sub_stream(self, sub_stream, /, *, is_list: bool) :
        if is_list : self._tag_name_to_sub_stream.setdefault(sub_stream.tag_name, []).append(sub_stream)
        else       : self._tag_name_to_sub_stream[sub_stream.tag_name] = sub_stream
        self._sub_stream_list.append(sub_stream)
        return self

    def has_sub_stream(self, tag_name, /) : return tag_name in self._tag_name_to_sub_stream

    # 可预先枚举tag_name的情况，用此方法
    # tag_list = [(<tag_name>, <is_list>), ...]
    def group_sub_stream_by_tag_list(self, tag_list, /, *, is_ordered = True) :
        for index, line in enumerate(self._line_list) :
            # print(f'{index + 1:>3}.[{line}]')
            tag_0 = (line.tag_name.get_raw(), 0)
            tag_1 = (line.tag_name.get_raw(), 1)
            # print(f'{tag_list=} {tag_0=} {tag_1=}')
            if tag_0 in tag_list : # 一次性出现的一级tag
                self._append_sub_stream(LineStream().set_tag_line(line), is_list = False)
                if is_ordered : tag_list = tag_list[tag_list.index(tag_0) + 1 : ]
            elif tag_list.has(tag_1) : # 会多次出现的一级tag
                self._append_sub_stream(LineStream().set_tag_line(line), is_list = True)
                if is_ordered : tag_list = tag_list[tag_list.index(tag_1) : ]
            else : # 二级及以下的tag
                if len(self._sub_stream_list) == 0 : raise RuntimeError(f'位置错误的 line\n{line.raw}\n{line.tag_name=}, {tag_list=}')
                self._sub_stream_list[-1].append_line(line)
        return self

    def is_one_line(self) : return len(self._line_list) == 0

    @cached_prop
    def one_line_content(self) :
        if not self.is_one_line() : raise RuntimeError(f'多余的line({self._line_list.raw})')
        return self._tag_line.content

    # def __getattr__(self, tag_name) :
    #     if tag_name in self._tag_name_to_sub_stream     :
    #         sub_stream = self._tag_name_to_sub_stream[tag_name]
    #         if sub_stream.is_one_line() : return sub_stream.one_line_content
    #         else                       : return sub_stream
    #     elif tag_name in self._tag_name_to_line_content : return self._tag_name_to_line_content[tag_name]
        # else : raise AttributeError(f'找不到 {tag_name=}')
    
    # def __getitem__(self, tag_name) : return self.__getattr__(tag_name)

    # 无法预先枚举tag_name的情况，用此方法
    def group_sub_stream_by_line_tag_name(self) :
        for index, line in enumerate(self._line_list) :
            Timer.print_timing(f'group_sub_stream_by_line_tag_name.{index + 1:>3}')
            tag_name = line.tag_name
            if tag_name not in self._tag_name_to_sub_stream : self._append_sub_stream(sub_stream := LineStream().set_tag_name(tag_name), is_list = False)
            else                                            : sub_stream = self._tag_name_to_sub_stream[tag_name]
            sub_stream.append_line(line)
        return self

    @cached_prop
    def tag_content(self) :
        if hasattr(self, '_tag_line') : return self._tag_line.content
        else                          : return self.one_line_content

    @cached_prop
    def tag_type(self) : return self._tag_line.tag_type

    def print(self, indent = '') :
        print(f'{indent}{self!a}')
        if hasattr(self, '_tag_line') and not self.is_one_line() : print(f'\n{indent}tag_line = {self._tag_line}')
        if hasattr(self, '_sub_stream_list')                   :
            print()
            for index, sub_stream in enumerate(self._sub_stream_list) :
                print(f'{indent}    {Y(f"No.{index + 1:>3}.{sub_stream.tag_name}.{sub_stream.tag_content}")}')
                sub_stream.print(indent + '    ')
        elif hasattr(self, 'line_list')                        :
            for line in self._line_list : print(f'{indent}{line}')
        else                                                   :
            for line in self._raw_line_list : print(f'{indent}{line}')
        print()
        return self

    def __format__(self, spec) :
        if self.is_one_line() : return f'{self.one_line_content:{spec}}'
        else                  : return f'{self._raw_line_list:{spec}}' # 待完善
