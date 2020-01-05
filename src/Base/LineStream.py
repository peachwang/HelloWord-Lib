# -*- coding: utf-8 -*-
import sys, os; sys.path.append(os.path.realpath(__file__ + '/../../../../HelloWord-Lib/src/Base')); from util import *
from functools import cached_property

class LineStream(Object) :

    class Line(Object) :

        @Timer.timeitTotal('Line.__init__')
        def __init__(self, index, raw_line, tag_format_list = None, /) :
            Object.__init__(self)
            self._registerProperty(['index', 'raw_line', 'tag_format'])
            self._index, self._raw_line = index, Str(raw_line)
            tag_format_list = List(tag_format_list)
            if tag_format_list.isNotEmpty() :
                for tag_format in tag_format_list :
                    if (tag_format == '[]' and (m := self._raw_line.fullMatch(r'^\[(?P<tag_name>[^\[\]]+)\](?P<content>.*)$')))\
                    or (tag_format == '【】' and (m := self._raw_line.fullMatch(r'^【(?P<tag_name>[^【】]+)】(?P<content>.*)$')))\
                    or (tag_format == '#' and (m := self._raw_line.fullMatch(r'^#(?P<tag_name>[^ ]+) *(?P<content>.*)$'))) :
                        self._tag_name, self._content, self._tag_format = m.tag_name, m.content, tag_format
                        return
                raise Exception(f'{index + 1}.[{self._raw_line}]不匹配{tag_format_list=}')
            else :
                self._content = self._raw_line

        @property
        def raw(self):
            return (self._index, self._raw_line, self._tag_format)

        @cached_property
        def tag_name(self) :
            return self._data['_tag_name'] # 直接访问字典效率最高

        @cached_property
        def content(self) :
            return self._data['_content']

        @property
        def tag_type(self):
            return self._content.split(' ')[0]

        def __format__(self, code) :
            return f'[index = {self._index}; tag_name = {self._tag_name}; content = [{self._content}]]'

    # @Timer.timeitTotal('LineStream.__init__')
    def __init__(self, raw_line_list = [], /, *, tag_format_list = None) :
        Object.__init__(self)
        self._registerProperty(['raw_line_list', 'line_list', 'tag_line', 'sub_stream_list'])
        self._raw_line_list = List(raw_line_list)
        self._line_list = List([ self.Line(index + 1, raw_line, tag_format_list) for (index, raw_line) in self._raw_line_list.enumerate() if raw_line.isNotEmpty() ])

    @cached_property
    def tag_name(self) :
        return self._tag_line.tag_name

    @cached_property
    def tag_type(self) :
        return self._tag_line.tag_type

    def _isOneLine(self) :
        return self._line_list.isEmpty()

    @cached_property
    def one_line_content(self) :
        if not self._isOneLine() :
            raise Exception(f'多余的line({self._line_list.raw})')
        return self._tag_line.content

    def __getitem__(self, name) :
        return self.__getattr__(name)

    def __getattr__(self, name) :
        value = Object.__getattr__(self, name)
        if isinstance(value, LineStream) :
            if value._isOneLine() : return value.one_line_content
            else : return value
        else : return value

    def _setTagLine(self, line, /) :
        self._setProperty('tag_line', line)
        self._setProperty(line.tag_name, line.content)
        return self

    def _appendSubStream(self, sub_stream, /, *, is_list) :
        if is_list :
            self._appendProperty(sub_stream.tag_name, sub_stream)
        else :
            self._setProperty(sub_stream.tag_name, sub_stream)
        self._appendProperty('sub_stream_list', sub_stream)
        return self

    def groupSubStreamByTagList(self, tag_list, /, *, is_ordered = True) :
        # tag_list = [(<tag_name>, <is_list>)]
        tag_list = List(tag_list)
        for index, line in self._line_list.enumerate() :
            # print(f'{index + 1}.[{line}]')
            tag_0 = (line.tag_name, 0)
            tag_1 = (line.tag_name, 1)
            # print(f'{tag_list=} {tag_0=} {tag_1=}')
            if tag_list.has(tag_0) : # 一次性出现的一级tag
                self._appendSubStream(LineStream()._setTagLine(line), is_list = False)
                if is_ordered : tag_list = tag_list[tag_list.index(tag_0) + 1 : ]
            elif tag_list.has(tag_1) : # 会多次出现的一级tag
                self._appendSubStream(LineStream()._setTagLine(line), is_list = True)
                if is_ordered : tag_list = tag_list[tag_list.index(tag_1) : ]
            else : # 二级及以下的tag
                if not self._hasProperty('sub_stream_list') :
                    raise Exception(f'位置错误的line({line.raw})')
                self._sub_stream_list[-1]._appendProperty('line_list', line)
        return self

    def hasSubStream(self, tag_name, /) :
        return self._hasProperty(tag_name)

    def print(self) :
        print(f'tag_line = {self._tag_line}')
        for line in self._line_list :
            print(f'{line}')

    def __format__(self, code) :
        if self._isOneLine() : return self.one_line_content
        else : return Object.__format__(self, code)
