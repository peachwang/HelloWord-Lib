# -*- coding: utf-8 -*-  
from util import List, Dict, Str, Object, UserTypeError, G, Y, R, P, cached_property, lru_cache

# DataStructure Module
#   def compatibleTo
#   def validate
#   def difference/delta

class _FieldSlot(Object) :
    
    def __init__(self, path, /) :
        Object.__init__(self)
        self._registerProperty(['parent', 'path', 'field_list', 'type_list', 'value_list', 'list_len_list', 'child_field_slot_list'])
        self._path   = path
        self._field_list = List()

    @cached_property
    def is_root(self) :
        return self._parent is None

    @cached_property
    def path(self) :
        return List(list(self._path)).join('.') if len(self._path) > 0 else 'ROOT'

    @cached_property
    def name(self) :
        if self.is_root : return 'ROOT'
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
    
    def __init__(self, parent, name, value, slot_dict, /) :
        Object.__init__(self)
        self._registerProperty(['parent', 'name', 'value', 'child_field_list', 'field_slot'])
        self._parent   = parent
        self._name     = name
        self._value = value
        self._build(slot_dict)
        if slot_dict.hasNot(self.slot_path) :
            slot_dict[self.slot_path] = _FieldSlot(self.slot_path)
        self._field_slot = slot_dict[self.slot_path].addField(self)
        if not self.is_leaf :
            for child_field in self._child_field_list : # 建立双向映射
                self._field_slot.uniqueAppendChildFieldSlot(child_field.field_slot)
                child_field.field_slot.setParent(self._field_slot)
        if self.is_root :
            self._field_slot.setParent(None)

    def _build(self, slot_dict, /) :
        if self.is_root :
            self._path = List()
        else :
            self._path = self._parent._path.appended(self._name)
        if isinstance(self._value, Dict) :
            for key, value in self._value.items() :
                self.appendChildField(_Field(self, key, value, slot_dict))
        elif isinstance(self._value, List) :
            for index, item in self._value.enum() :
                self.appendChildField(_Field(self, f'#{index}', item, slot_dict))
        return self

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
        return self._path.join('.') if len(self._path) > 0 else 'ROOT'
    
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
        if self.is_leaf :
            return List(self)
        else :
            return self._child_field_list.getAllFieldList.merged().prepend(self)

    def __format__(self, code) :
        result = f'{self.path!s:80}{self.name:>25} {Y(P(self.type) == "List") == "Dict":10} '
        if self.is_leaf and not self.is_list and not self.is_dict :
            result += f'{P(self._value)}'
        else :
            if isinstance(self._value, List) :
                if self.hasChildFieldList() :
                    result += f'含 {self._child_field_list.len()} 个元素'
                else :
                    result += f'{G("为空")}'
            elif isinstance(self._value, Dict) :
                if self.hasChildFieldList() :
                    result += f'含 {self._child_field_list.len()} 个字段: {Y(self._child_field_list.name.sort().join(", "))}'
                else :
                    result += f'{G("为空")}'
        return result

class Inspect(Object) :

    def __init__(self, raw_data) :
        Object.__init__(self)
        self._registerProperty(['raw_data', 'root_field', 'slot_dict'])
        if not isinstance(raw_data, (List, Dict)) :
            raise UserTypeError(raw_data)
        self._raw_data  = raw_data
        self._slot_dict = Dict()
        self._root_field = _Field(None, 'ROOT', self._raw_data, self._slot_dict)

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
