# -*- coding: utf-8 -*-  
from util import List, Dict, Str, Object, UserTypeError, R, Y, G, C, B, P, S, W, E, cached_property, lru_cache, j

# DataStructure Module
#   def compatibleTo
#   def validate
#   def difference/delta

class _FieldSlot(Object) :
    
    def __init__(self, path, /) :
        super().__init__()
        self._registerProperty(['parent', 'path', 'field_list', 'type_list', 'value_list', 'list_len_list', 'child_field_slot_list'])
        self._path   = path
        self._field_list = List()

    @cached_property
    def is_root(self) :
        return self._parent is None

    @cached_property
    def path(self) :
        return List(list(self._path)).join('.') if len(self._path) > 0 else Str('ROOT')

    @cached_property
    def name(self) :
        if self.is_root : return Str('ROOT')
        else : return self._path[-1]

    @cached_property
    def is_list(self) :
        return self.type_list.join(", ") == "List"

    @cached_property
    def is_dict(self) :
        return self.type_list.join(", ") == "Dict"

    @cached_property
    def in_list(self) :
        if self.is_root : return False
        else : return self._parent.is_list

    @cached_property
    def in_dict(self) :
        if self.is_root : return False
        else : return self._parent.is_dict

    def addField(self, field, /) :
        self.appendField(field).uniqueAppendType(field.type)
        if field.is_list : self.appendListLen(field.value.len())
        elif field.is_dict : pass
        else : self.appendValue(field.value, filter_none = False)
        return self

    @cached_property
    def field_num(self) :
        return self._field_list.len()

    @lru_cache
    def getSiblingFieldSlotList(self) :
        if self.is_root :
            return List()
        else :
            return self.parent.child_field_slot_list.droppedItem(self)

    @lru_cache
    def getAllFieldSlotList(self) :
        if self.hasNotChildFieldSlotList() :
            return List(self)
        else :
            return self._child_field_slot_list.getAllFieldSlotList.merged().unique().prepend(self)

    @cached_property
    def existence(self) :
        if self.is_root : return True
        return self.field_num == self._parent.field_num

    def __format__(self, code) :
        max_len = 3
        max_width = 25
        result = f'{self.path!s:80}{self.name:>25} {P(Y(self.type_list.join(", ")) == "Dict") == "List":<10} {"  " if self.is_root or self.in_list else (P("必") if self.field_num == self._parent.field_num else Y("可"))}存在{self.field_num:>3} 次'
        if self.hasChildFieldSlotList() or self.is_list or self.is_dict :
            if self.is_list :
                if not self.hasListLenList() :
                    result += f' {G("为空")}'
                elif self._list_len_list.len() <= max_len :
                    result += f' 含     {self._list_len_list.sort(reverse = True).join(", ")} 个元素'
                else :
                    __ = self._list_len_list.countBy()
                    _ = List(f'({length}, {count}次)' for length, count in __.items().sort(lambda _ : _[1], reverse = True))[:max_len].join(', ')
                    result += f' 含     {_}{", etc." if __.len() > max_len else ""} 个元素'
            elif self.is_dict :
                if self.hasChildFieldSlotList() :
                    result += f' 含字段 {Y(self._child_field_slot_list.name.unique().sort().join(", "))}'
                else :
                    result += f' {G("为空")}'
        else :
            if self.hasNotValueList() : 
                result += f'{R(" 无取值")}'
            elif self._value_list.len() <= max_len :
                result += f' 取值   {P(self._value_list.sort(lambda _ : f"{_}").format(f"{{!s:.{max_width}}}").join(", "))}'
            else :
                __ = self._value_list.countBy()
                _ = List(f'({value!s:.{max_width}}, {count}次)' for value, count in __.items().sort(lambda _ : _[1], reverse = True))[:max_len].join(', ')
                result += f' 取值   {P(_)}{", etc." if __.len() > max_len else ""}'
        return result

class _Field(Object) :
    
    def __init__(self, parent, name, value, field_slot_dict, /) :
        super().__init__()
        self._registerProperty(['parent', 'name', 'value', 'child_field_list', 'field_slot'])
        self._parent           = parent
        if '.' in name : raise UserTypeError(name)
        self._name             = name
        self._value            = value
        self._child_field_dict = Dict()
        self._build(field_slot_dict)
        
        if field_slot_dict.hasNot(self.slot_path) :
            field_slot_dict[self.slot_path] = _FieldSlot(self.slot_path)
        self._field_slot = field_slot_dict[self.slot_path].addField(self)
        if not self.is_leaf :
            for child_field in self._child_field_list : # 建立双向映射
                self._field_slot.uniqueAppendChildFieldSlot(child_field.field_slot)
                child_field.field_slot.setParent(self._field_slot)
        if self.is_root :
            self._field_slot.setParent(None)

    def _build(self, field_slot_dict, /) :
        if self.is_root :
            self._path = List()
        else :
            self._path = self._parent._path.appended(self._name)
        if isinstance(self._value, Dict) :
            for key, value in self._value.items() :
                name = key
                child_field = _Field(self, name, value, field_slot_dict)
                self.appendChildField(child_field)
                self._child_field_dict[name] = child_field
        elif isinstance(self._value, List) :
            for index, item in self._value.enum() :
                name = f'#{index}'
                child_field = _Field(self, name, item, field_slot_dict)
                self.appendChildField(child_field)
                self._child_field_dict[name] = child_field
        return self

    def has(self, name, /) :
        return self._child_field_dict.has(name)

    def __getitem__(self, name, /) :
        return self._child_field_dict[name]

    @cached_property
    def is_root(self) :
        return self._parent is None

    @cached_property
    def is_leaf(self) :
        return not isinstance(self._value, (List, Dict)) or self._value.isEmpty()

    @cached_property
    def is_list(self) :
        return isinstance(self._value, List)

    @cached_property
    def is_dict(self) :
        return isinstance(self._value, Dict)

    @cached_property
    def len(self) :
        if self.is_list or self.is_dict :
            return self._value.len()
        else :
            raise UserTypeError(self._value)

    @cached_property
    def in_list(self) :
        if self.is_root : return False
        else : return isinstance(self._parent.type, List)

    @cached_property
    def in_dict(self) :
        if self.is_root : return False
        else : return isinstance(self._parent.type, Dict)

    @cached_property
    def type(self) :
        return Dict({int : 'int', float : 'float', bool : 'bool', type(Str()) : 'Str', type(List()) : 'List', type(Dict()) : 'Dict'})\
            .get(type(self._value), Str(str(type(self._value))).fullMatch(r'<class \'([^\'\.]+\.)?([^\']+)\'>').oneGroup(2))

    @cached_property
    def path(self) :
        return self._path.join('.') if len(self._path) > 0 else Str('ROOT')
    
    @cached_property
    def slot_path(self) :
        return tuple('#' if name.fullMatch(r'#\d+') else name for name in self._path)

    @lru_cache
    def getSiblingFieldList(self) :
        if self.is_root :
            return List()
        else :
            return self._parent.child_field_list.droppedItem(self)

    @lru_cache
    def getLeafFieldList(self) :
        if self.is_leaf :
            return List(self)
        else :
            return self._child_field_list.getLeafFieldList.merged()

    @lru_cache
    def getNonLeafFieldList(self) :
        if self.is_leaf :
            return List()
        else :
            return self._child_field_list.getNonLeafFieldList.merged().prepend(self)

    @lru_cache
    def getAllFieldList(self) :
        return self.getChildFieldList([]).getAllFieldList.merged().prepend(self)

    @cached_property
    def value_inspect(self) :
        result = f'{Y(P(self.type) == "List") == "Dict":10} '
        if self.is_leaf and not self.is_list and not self.is_dict :
            result += f'{P(self._value)}'
        elif self.hasNotChildFieldList() :
            result += f'{G("为空")}'
        elif self.is_list :
            result += f'含 {self._child_field_list.len()} 个元素'
        elif self.is_dict :
            result += f'含 {self._child_field_list.len()} 个字段: {Y(self._child_field_list.name.sort().join(", "))}'
        else :
            raise UserTypeError(self._value)
        return result

    @lru_cache
    def __format__(self, code) :
        return f'{self.path!s:80}{self.name:>25} {self.value_inspect}'

class Inspect(Object) :

    def __init__(self, raw_data) :
        super().__init__()
        self._registerProperty(['raw_data', 'root_field', 'field_slot_dict'])
        if not isinstance(raw_data, (List, Dict)) :
            raise UserTypeError(raw_data)
        self._raw_data   = raw_data
        self._field_slot_dict  = Dict()
        self._root_field = _Field(None, 'ROOT', self._raw_data, self._field_slot_dict)

    @lru_cache
    def getLeafList(self) :
        return self._root_field.getLeafFieldList()

    def printLeafList(self) :
        self.getLeafFieldList().printFormat()
        return self

    @lru_cache
    def getNonLeafList(self) :
        return self._root_field.getNonLeafFieldList()

    def printNonLeafList(self) :
        self.getNonLeafFieldList().printFormat()
        return self

    @lru_cache
    def getAllFieldList(self) :
        return self._root_field.getAllFieldList()

    def printAllFieldList(self) :
        self.getAllFieldList().printFormat()
        return self

    @lru_cache
    def getAllFieldSlotList(self) :
        return self._root_field.field_slot.getAllFieldSlotList().sort('path')

    def printAllFieldSlotList(self) :
        self.getAllFieldSlotList().printFormat()
        return self

    def print(self) :
        return self.printAllFieldList().printAllFieldSlotList()

S_DIFFTYPE  = '类型不同'
S_DIFFLEN   = '数量不同'
S_DIFFCHILD = '内部不同'
S_DIFFVALUE = '取值不同'
S_ADDED     = '新增'
S_DELETED   = '被删'
S_IDENTICAL = '相同'

class _DiffField(_Field) :

    def __init__(self, parent, field_1, field_2, /) :
        Object.__init__(self)
        self._registerProperty(['parent', 'name', 'field_1', 'field_2', 'status', 'child_diff_field_list', 'diff_field_slot'])
        self._parent  = parent
        self._field_1 = field_1
        self._field_2 = field_2
        self._build()

    def _build(self, /) :
        if self._field_1 is None :
            self._path = self._field_2._path
            self._name = self._field_2.name
            self._status = S_ADDED
        elif self._field_2 is None :
            self._path = self._field_1._path
            self._name = self._field_1.name
            self._status = S_DELETED
        else :
            self._path = self._field_1._path
            self._name = self._field_1.name
            if type(self._field_1.value) != type(self._field_2.value) :
                self._status = S_DIFFTYPE
            elif self._field_1.is_dict or self._field_1.is_list:
                for child_field_1 in self._field_1.getChildFieldList([]) :
                    if self._field_2.has(child_field_1.name) :
                        child_field_2 = self._field_2[child_field_1.name]
                    else :
                        child_field_2 = None
                    self.appendChildDiffField(_DiffField(self, child_field_1, child_field_2))
                for child_field_2 in self._field_2.getChildFieldList([]) :
                    if self._field_1.has(child_field_2.name) :
                        continue
                    else :
                        child_field_1 = None
                    self.appendChildDiffField(_DiffField(self, child_field_1, child_field_2))
                if self._field_1.len != self._field_2.len :
                    self._status = S_DIFFLEN
                else :
                    if all(status == S_IDENTICAL for status in self.getChildDiffFieldList([]).status) :
                        self._status = S_IDENTICAL
                    else :
                        self._status = S_DIFFCHILD
            elif self._field_1.is_leaf and self._field_2.is_leaf :
                if self._field_1.value == self._field_2.value :
                    self._status = S_IDENTICAL
                else :
                    self._status = S_DIFFVALUE
            else :
                raise UserTypeError(self._field_1.value)
        return self

    @lru_cache
    def getAllDiffFieldList(self) :
        return self.getChildDiffFieldList([]).getAllDiffFieldList.merged().prepend(self)

    def getDifferentFieldList(self, filter_path_list = None, filter_status_list = None) :
        if (isinstance(filter_path_list, list) and self.path.isIn(*filter_path_list))\
        or (isinstance(filter_status_list, list) and self._status.isIn(*filter_status_list)) :
            return List()
        result = List(_.getDifferentFieldList(filter_path_list = filter_path_list) for _ in self.getChildDiffFieldList([])).merged()
        if self.status != S_IDENTICAL :
            result.prepend(self)
        return result

    def __format__(self, code) :
        result = f'{self.path!s:80}{self.name:>25} {S(Y(B(C(P(R(G(self._status) == S_ADDED) == S_DELETED) == S_DIFFVALUE) == S_DIFFLEN) == S_DIFFTYPE) == S_DIFFCHILD) == S_IDENTICAL:<8}'
        if self._status == S_DIFFTYPE :
            result += f' {self._field_1.type} vs. {self._field_2.type}\n1: {R(j(self._field_1.value, indent = 0)[:200])}\n2: {G(j(self._field_2.value, indent = 0)[:200])}'
        elif self._status == S_DIFFLEN :
            result += f' {Y(P(self._field_1.type) == "List") == "Dict":10} {R(self._field_1.len)} vs. {G(self._field_2.len)}'
        elif self._status == S_DIFFCHILD :
            result += f' {Y(P(self._field_1.type) == "List") == "Dict":10}'
        elif self._status == S_DIFFVALUE :
            result += f' {Y(P(self._field_1.type) == "List") == "Dict":10} {R(self._field_1.value):>50} vs. {G(self._field_2.value):50}'
        elif self._status == S_ADDED :
            result += f' {Y(P(self._field_2.type) == "List") == "Dict":10} 2: {G(j(self._field_2.value, indent = 0)[:200])}'
        elif self._status == S_DELETED :
            result += f' {Y(P(self._field_1.type) == "List") == "Dict":10} 1: {R(j(self._field_1.value, indent = 0)[:200])}'
        elif self._status == S_IDENTICAL :
            result += f' {self._field_1.value_inspect}'
        return result

# ListDiff: 以 item 作为最小比较单元。降维后可用于StrDiff

class Diff(Object) :

    def __init__(self, raw_data_1, raw_data_2, /) :
        super().__init__()
        self._registerProperty(['raw_data_1', 'raw_data_2', 'diff_root_field'])
        self._raw_data_1      = raw_data_1
        self._raw_data_2      = raw_data_2
        self._ins_1           = Inspect(raw_data_1)
        self._ins_2           = Inspect(raw_data_2)
        self._diff_root_field = _DiffField(None, self._ins_1.root_field, self._ins_2.root_field)

    @lru_cache
    def getAllDiffFieldList(self) :
        return self._diff_root_field.getAllDiffFieldList()

    def printAllDiffFieldList(self) :
        self.getAllDiffFieldList().printFormat()
        return self

    def getDifferentFieldList(self, **kwargs) :
        return self._diff_root_field.getDifferentFieldList(**kwargs)

    def printDifferentFieldList(self, **kwargs) :
        self.getDifferentFieldList(**kwargs).printFormat()
        return self

    def print(self, **kwargs) :
        return self.printDifferentFieldList(**kwargs)
