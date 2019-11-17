# -*- coding: utf-8 -*-
import sys, os; sys.path.append(os.path.realpath(__file__ + '/../../../../HelloWord-Lib/src/Base')); from util import *

class Stream(Object) :

    def __init__(self, raw_line_list = []) :
        Object.__init__(self)
        self._line_list = List([ _Line(index, raw_line) for (index, raw_line) in raw_line_list ])

    @property
    def line_list(self) :
        return self._line_list.copy()

    def _appendLine(self, line) :
        self._line_list.append(line)
        return self

    @property
    def stream_list(self) :
        return self._stream_list.copy()

    def groupStreamByTagList(self, tag_list, is_ordered = True) :
        # tag_list = [(<tag_name>, <is_list>)]
        self._stream_list = List()
        # existence = List()
        for line in self._line_list :
            tag_0 = (line.tag, 0)
            tag_1 = (line.tag, 1)
            if tag_0 in tag_list : # 一次性出现的一级tag
                # if tag_0 in existence : # 非第一次出现，视为二级及以下的tag
                    # self._stream_list[-1]._appendLine(line)
                # else : # 第一次出现，视为一级tag
                self._stream_list.append(Stream()._setTagLine(line))
                if is_ordered : tag_list = tag_list[tag_list.index(tag_0) + 1 : ]
                    # existence.append(tag_0)
            elif tag_1 in tag_list : # 会多次出现的一级tag
                self._stream_list.append(Stream()._setTagLine(line))
                if is_ordered : tag_list = tag_list[tag_list.index(tag_1) : ]
            else : # 二级及以下的tag
                if self._stream_list.len() == 0 :
                    raise Exception('位置错误的line({})'.format(line.raw))
                self._stream_list[-1]._appendLine(line)
        return self
