# -*- coding: utf-8 -*-  
from util import List, Dict, Str, Object, UserTypeError, R, Y, G, C, B, P, S, W, E, cached_property, lru_cache

# DataStructure Module
#   def compatibleTo
#   def validate
#   def difference/delta

# class _FieldSlot(Object) :
class _FieldSlot() :
    
    def __init__(self, path_tuple, /) :
        # super().__init__()
        # self._registerProperty(['parent', 'path_tuple', 'value_list', 'field_list', 'type_list', 'list_len_list', 'child_field_slot_list'])
        # self._registerProperty(['parent', 'path_tuple', 'field_list', 'type_list', 'list_len_list', 'child_field_slot_list'])
        self._path_tuple   = path_tuple
        # self._field_list = List()
        object.__setattr__(self, '_value_list', [])
        object.__setattr__(self, '_field_list', [])
        object.__setattr__(self, '_type_list', List())
        object.__setattr__(self, '_list_len_list', [])
        object.__setattr__(self, '_child_field_slot_list', List())

    @cached_property
    def parent(self) : return self._parent

    def setParent(self, field_slot, /) :
        self._parent = field_slot
        return self

    @cached_property
    def is_root(self) : return self._parent is None

    @cached_property
    def path_str(self) : return List(list(self._path_tuple)).join('.') if len(self._path_tuple) > 0 else Str('ROOT')

    @cached_property
    def name(self) :
        if self.is_root : return Str('ROOT')
        else : return self._path_tuple[-1]

    @cached_property
    def value_list(self) : return self._value_list

    @cached_property
    def field_list(self) : return self._field_list

    @cached_property
    def type_list(self) : return self._type_list

    @cached_property
    def list_len_list(self) : return self._list_len_list

    @cached_property
    def child_field_slot_list(self) : return self._child_field_slot_list

    @cached_property
    def is_list(self) :
        # return self.type_list.join(', ') == 'List'
        return self.type_list.join(', ') == 'list'

    @cached_property
    def is_dict(self) :
        # return self.type_list.join(', ') == 'Dict'
        return self.type_list.join(', ') == 'dict'

    @cached_property
    def in_list(self) :
        if self.is_root : return False
        else : return self._parent.is_list

    @cached_property
    def in_dict(self) :
        if self.is_root : return False
        else : return self._parent.is_dict

    def addField(self, field, /) :
        # self.appendField(field).uniqueAppendType(field.type)
        self._field_list.append(field)
        self._type_list.uniqueAppend(field.type)

        # if field.is_list : self.appendListLen(field.value.len())
        # if field.is_list : self.appendListLen(len(field.value))
        if field.is_list : self._list_len_list.append(len(field.value))
        elif field.is_dict : pass
        else :
            # self.appendValue(field.value, filter_none = False)
            self._value_list.append(field.value)
        return self

    @cached_property
    def field_num(self) :
        # return self._field_list.len()
        return len(self._field_list)

    @cached_property
    def sibling_field_slot_list(self) :
        if self.is_root :
            return List()
        else :
            # return self.parent.child_field_slot_list.droppedItem(self)
            return List(self.parent.child_field_slot_list).droppedItem(self)

    @cached_property
    def all_field_slot_list(self) :
        # if self.hasNoChildFieldSlotList() :
        if self._child_field_slot_list.len() == 0 :
            return List(self)
        else :
            # return self._child_field_slot_list.all_field_slot_list.merged().unique().prepend(self)
            return List(self._child_field_slot_list).all_field_slot_list.merged().unique().prepend(self)

    # @cached_property
    # def existence(self) :
    #     if self.is_root : return True
    #     return self.field_num == self._parent.field_num

    def __format__(self, code) :
        max_len = 3
        max_width = 25
        # result = f'{self.path_str!s:80}{self.name:>25} {P(Y(self.type_list.join(", ")) == "Dict") == "List":<10} {"  " if self.is_root or self.in_list else (P("必") if self.field_num == self._parent.field_num else Y("可"))}存在{self.field_num:>3} 次'
        result = f'{self.path_str!s:80}{self.name:>25} {P(Y(self.type_list.join(", ")) == "dict") == "list":<10} {"  " if self.is_root or self.in_list else (P("必") if self.field_num == self._parent.field_num else Y("可"))}存在{self.field_num:>3} 次'
        # if self.hasChildFieldSlotList() or self.is_list or self.is_dict :
        if self._child_field_slot_list.len() > 0 or self.is_list or self.is_dict :
            if self.is_list :
                # if self.hasNoListLenList() :
                if len(self._list_len_list) == 0 :
                    result += f' {G("为空")}'
                # elif self._list_len_list.len() <= max_len :
                elif len(self._list_len_list) <= max_len :
                    # result += f' 含     {self._list_len_list.sort(reverse = True).join(", ")} 个元素'
                    result += f' 含     {List(self._list_len_list).sort(reverse = True).join(", ")} 个元素'
                else :
                    # __ = self._list_len_list.countBy()
                    __ = List(self._list_len_list).countBy()
                    _ = List(f'({length}, {count}次)' for length, count in __.items().sort(itemgetter(1), reverse = True))[:max_len].join(', ')
                    result += f' 含     {_}{", etc." if __.len() > max_len else ""} 个元素'
            elif self.is_dict :
                # if self.hasChildFieldSlotList() :
                if len(self._child_field_slot_list) > 0 :
                    # result += f' 含字段 {Y(self._child_field_slot_list.name.unique().sort().join(", "))}'
                    result += f' 含字段 {Y(List(self._child_field_slot_list).name.unique().sort().join(", "))}'
                else :
                    result += f' {G("为空")}'
        else :
            # if self.hasNoValueList() : 
            if len(self._value_list) == 0 : 
                result += f'{R(" 无取值")}'
            # elif self._value_list.len() <= max_len :
            elif len(self._value_list) <= max_len :
                # result += f' 取值   {P(self._value_list.sort(lambda _ : f"{_}").format(f"{{!s:.{max_width}}}").join(", "))}'
                result += f' 取值   {P(List(self._value_list).sort(lambda _ : f"{_}").format(f"{{!s:.{max_width}}}").join(", "))}'
            else :
                # __ = self._value_list.countBy()
                __ = List(self._value_list).countBy()
                _ = List(f'({value!s:.{max_width}}, {count}次)' for value, count in __.items().sort(itemgetter(1), reverse = True))[:max_len].join(', ')
                result += f' 取值   {P(_)}{", etc." if __.len() > max_len else ""}'
        return result

# class _Field(Object) :
class _Field() :
    
    def __init__(self, parent, name, value, field_slot_dict, /, **kwargs) :
        # super().__init__()
        # self._registerProperty(['parent', 'name', 'value', 'child_field_list', 'field_slot'])
        # self._registerProperty(['parent', 'name', 'child_field_list', 'field_slot'])
        self._parent           = parent
        if '.' in name : raise UserTypeError(name)
        self._name             = name
        # self._value            = value
        object.__setattr__(self, '_value', value)
        object.__setattr__(self, '_child_field_list', [])
        # self._child_field_dict = Dict()
        object.__setattr__(self, '_child_field_dict', {})
        self._build(field_slot_dict, **kwargs)
        
        # if field_slot_dict.hasNo(self.slot_path_tuple) :
        if self.slot_path_tuple not in field_slot_dict :
            field_slot_dict[self.slot_path_tuple] = _FieldSlot(self.slot_path_tuple)
        self._field_slot = field_slot_dict[self.slot_path_tuple].addField(self)
        if not self.is_leaf :
            for child_field in self._child_field_list : # 建立双向映射
                # self._field_slot.uniqueAppendChildFieldSlot(child_field.field_slot)
                self._field_slot.child_field_slot_list.uniqueAppend(child_field.field_slot)
                child_field.field_slot.setParent(self._field_slot)
        if self.is_root :
            self._field_slot.setParent(None)

    @cached_property
    def parent(self) : return self._parent

    @cached_property
    def name(self) : return self._name

    @cached_property
    def value(self) : return self._value

    @cached_property
    def child_field_list(self) : return self._child_field_list

    @cached_property
    def field_slot(self) : return self._field_slot

    def _build(self, field_slot_dict, /) :
        if self.is_root :
            # self._path_tuple = List()
            self._path_tuple = tuple()
        else :
            # self._path_tuple = tuple(List(self._parent._path_tuple).appended(self._name).getRaw())
            self._path_tuple = tuple(list(self._parent._path_tuple) + [self._name])
        # if isinstance(self._value, Dict) :
        if isinstance(self._value, dict) :
            for key, value in self._value.items() :
                name = key
                child_field = _Field(self, name, value, field_slot_dict)
                # self.appendChildField(child_field)
                self._child_field_list.append(child_field)
                self._child_field_dict[name] = child_field
        # elif isinstance(self._value, List) :
        elif isinstance(self._value, list) :
            # for index, item in self._value.enum() :
            for index, item in enumerate(self._value) :
                name = f'#{index}'
                child_field = _Field(self, name, item, field_slot_dict)
                # self.appendChildField(child_field)
                self._child_field_list.append(child_field)
                self._child_field_dict[name] = child_field
        return self

    def has(self, name, /) :
        # return self._child_field_dict.has(name)
        return name in self._child_field_dict

    def __getitem__(self, name, /) :
        return self._child_field_dict[name]

    @cached_property
    def is_root(self) : return self._parent is None

    @cached_property
    def is_leaf(self) :
        # return not isinstance(self._value, (List, Dict)) or self._value.isEmpty()
        return not isinstance(self._value, (list, dict)) or len(self._value) == 0

    @cached_property
    def is_list(self) :
        # return isinstance(self._value, List)
        return isinstance(self._value, list)

    @cached_property
    def is_dict(self) :
        # return isinstance(self._value, Dict)
        return isinstance(self._value, dict)

    @cached_property
    def len(self) :
        if self.is_list or self.is_dict :
            # return self._value.len()
            return len(self._value)
        else :
            raise UserTypeError(self._value)

    @cached_property
    def in_list(self) :
        if self.is_root : return False
        # else : return isinstance(self._parent.value, List)
        else : return isinstance(self._parent.value, list)

    @cached_property
    def in_dict(self) :
        if self.is_root : return False
        # else : return isinstance(self._parent.value, Dict)
        else : return isinstance(self._parent.value, dict)

    @cached_property
    def type(self) :
        return (Dict({
                int          : 'int',
                float        : 'float',
                bool         : 'bool',
                # type(Str())  : 'Str',
                str          : 'str',
                # type(List()) : 'List',
                list         : 'list',
                # type(Dict()) : 'Dict',
                dict         : 'dict',
            })
            .get(type(self._value), Str(str(type(self._value))).fullMatch(r'<class \'([^\'\.]+\.)?([^\']+)\'>').oneGroup(2))
        )

    @cached_property
    def path_tuple(self) : return self._path_tuple

    @cached_property
    def path_str(self) :
        # return List(self._path_tuple).join('.') if len(self._path_tuple) > 0 else Str('ROOT')
        return Str('.'.join(self._path_tuple)) if len(self._path_tuple) > 0 else Str('ROOT')
    
    @cached_property
    def slot_path_tuple(self) :
        # return tuple('#' if name.fullMatch(r'#\d+') else name for name in self._path_tuple)
        return tuple('#' if Str(name).fullMatch(r'#\d+') else name for name in self._path_tuple)

    @cached_property
    def child_field_list(self) :
        # if self.hasNoChildFieldList() : return List()
        # if len(self._child_field_list) == 0 : return List()
        # else : return self._child_field_list
        # else : return List(self._child_field_list)
        return self._child_field_list

    @cached_property
    def sibling_field_list(self) :
        if self.is_root :
            return List()
        else :
            # return self._parent.child_field_list.droppedItem(self)
            return List(self._parent.child_field_list).droppedItem(self)

    @cached_property
    def leaf_field_list(self) :
        if self.is_leaf :
            return List(self)
        else :
            # return self.child_field_list.leaf_field_list.merged()
            return List(self._child_field_list).leaf_field_list.merged()

    @cached_property
    def non_leaf_field_list(self) :
        if self.is_leaf :
            return List()
        else :
            # return self.child_field_list.non_leaf_field_list.merged().prepend(self)
            return List(self._child_field_list).non_leaf_field_list.merged().prepend(self)

    @cached_property
    def all_field_list(self) :
        # return self.child_field_list.all_field_list.merged().prepend(self)
        return List(self._child_field_list).all_field_list.merged().prepend(self)

    @cached_property
    def value_inspect(self) :
        # result = f'{Y(P(self.type) == "List") == "Dict":10} '
        result = f'{Y(P(self.type) == "list") == "dict":10} '
        if self.is_leaf and not self.is_list and not self.is_dict :
            result += f'{P(self._value)}'
        # elif self.hasNoChildFieldList() :
        elif len(self._child_field_list) == 0 :
            result += f'{G("为空")}'
        elif self.is_list :
            # result += f'含 {self._child_field_list.len()} 个元素'
            result += f'含 {len(self._child_field_list)} 个元素'
        elif self.is_dict :
            # result += f'含 {self._child_field_list.len()} 个字段: {Y(self._child_field_list.name.sort().join(", "))}'
            result += f'含 {len(self._child_field_list)} 个字段: {Y(List(self._child_field_list).name.sort().join(", "))}'
        else :
            raise UserTypeError(self._value)
        return result

    @lru_cache
    def __format__(self, code) :
        return f'{self.path_str!s:80}{self.name:>25} {self.value_inspect}'

# class Inspect(Object) :
class Inspect() :

    def __init__(self, raw_data, **kwargs) :
        # super().__init__()
        # self._registerProperty(['raw_data', 'root_field', 'field_slot_dict'])
        # self._registerProperty(['root_field', 'field_slot_dict'])
        # if not isinstance(raw_data, (List, Dict)) :
        if not isinstance(raw_data, (list, dict)) :
            raise UserTypeError(raw_data)
        # self._raw_data   = raw_data
        object.__setattr__(self, '_raw_data', raw_data)
        # self._field_slot_dict  = Dict()
        self._field_slot_dict  = {}
        self._root_field = _Field(None, 'ROOT', self._raw_data, self._field_slot_dict, **kwargs)

    @cached_property
    def raw_data(self) : return self._raw_data

    @cached_property
    def root_field(self) : return self._root_field

    @cached_property
    def field_slot_dict(self) : return self._field_slot_dict

    @cached_property
    def leaf_list(self) : return self._root_field.leaf_field_list

    def printLeafList(self) : self.leaf_list.printFormat(); return self

    @cached_property
    def non_leaf_list(self) : return self._root_field.non_leaf_field_list

    def printNonLeafList(self) : self.non_leaf_list.printFormat(); return self

    @cached_property
    def all_field_list(self) : return self._root_field.all_field_list

    def printAllFieldList(self) : self.all_field_list.printFormat(); return self

    @cached_property
    def all_field_slot_list(self) : return self._root_field.field_slot.all_field_slot_list.sort('path_str')

    def printAllFieldSlotList(self) : self.all_field_slot_list.printFormat(); return self

    def print(self) :
        self.printAllFieldList()
        print('-' * 80)
        self.printAllFieldSlotList()
        return self

class _DiffField(_Field) :

    def __init__(self, parent, field_1, field_2, /) :
        # Object.__init__(self)
        # self._registerProperty(['parent', 'name', 'field_1', 'field_2', 'status', 'child_diff_field_list', 'diff_field_slot'])
        self._parent  = parent
        self._field_1 = field_1
        self._field_2 = field_2
        self._child_diff_field_list = []
        self._build()

    @cached_property
    def parent(self) : return self._parent

    @cached_property
    def name(self) : return self._name

    @cached_property
    def field_1(self) : return self._field_1

    @cached_property
    def field_2(self) : return self._field_2

    @cached_property
    def status(self) : return self._status

    @cached_property
    def child_diff_field_list(self) :
        # if self.hasNoChildDiffFieldList() : return List()
        # else : return self._child_diff_field_list
        return self._child_diff_field_list

    def _build(self, /) :
        if self._field_1 is None :
            self._path_tuple = self._field_2.path_tuple
            self._name       = self._field_2.name
            self._status     = Diff.S_ADDED
        elif self._field_2 is None :
            self._path_tuple = self._field_1.path_tuple
            self._name       = self._field_1.name
            self._status     = Diff.S_DELETED
        else :
            self._path_tuple = self._field_1.path_tuple
            self._name       = self._field_1.name
            if type(self._field_1.value) != type(self._field_2.value) :
                self._status = Diff.S_DIFFTYPE
            elif self._field_1.is_dict or self._field_1.is_list:
                for child_field_1 in self._field_1.child_field_list :
                    if self._field_2.has(child_field_1.name) :
                        child_field_2 = self._field_2[child_field_1.name]
                    else :
                        child_field_2 = None
                    # self.appendChildDiffField(_DiffField(self, child_field_1, child_field_2))
                    self._child_diff_field_list.append(_DiffField(self, child_field_1, child_field_2))
                for child_field_2 in self._field_2.child_field_list :
                    if self._field_1.has(child_field_2.name) :
                        continue
                    else :
                        child_field_1 = None
                    # self.appendChildDiffField(_DiffField(self, child_field_1, child_field_2))
                    self._child_diff_field_list.append(_DiffField(self, child_field_1, child_field_2))
                if self._field_1.len != self._field_2.len :
                    self._status = Diff.S_DIFFLEN
                else :
                    # if all(status == Diff.S_IDENTICAL for status in self.child_diff_field_list.status) :
                    if all(status == Diff.S_IDENTICAL for status in List(self.child_diff_field_list).status) :
                        self._status = Diff.S_IDENTICAL
                    else :
                        self._status = Diff.S_DIFFCHILD
            elif self._field_1.is_leaf and self._field_2.is_leaf :
                if self._field_1.value == self._field_2.value :
                    self._status = Diff.S_IDENTICAL
                else :
                    self._status = Diff.S_DIFFVALUE
            else :
                raise UserTypeError(self._field_1.value)
        return self

    @cached_property
    def all_diff_field_list(self) : return List(self._child_diff_field_list).all_diff_field_list.merged().prepend(self)

    def getDifferentFieldList(self, filter_list = None) :
        if isinstance(filter_list, list) and (self.path_str, self._status) in filter_list :
            return List()
        result = List(_.getDifferentFieldList(filter_list = filter_list) for _ in self._child_diff_field_list).merged()
        if (self._status in (Diff.S_DIFFTYPE, Diff.S_DIFFVALUE, Diff.S_ADDED, Diff.S_DELETED)
            or self._status in (Diff.S_DIFFLEN, Diff.S_DIFFCHILD) and result.isNotEmpty()) :
            result.prepend(self)
        return result

    def __format__(self, code) :
        from util import  j
        result = f'{self.path_str!s:80}{self.name:>25} {S(Y(B(C(P(R(G(self._status) == Diff.S_ADDED) == Diff.S_DELETED) == Diff.S_DIFFVALUE) == Diff.S_DIFFLEN) == Diff.S_DIFFTYPE) == Diff.S_DIFFCHILD) == Diff.S_IDENTICAL:<8}'
        if self._status == Diff.S_DIFFTYPE :
            result += f' {self._field_1.type} vs. {self._field_2.type}\n1: {R(j(self._field_1.value, indent = 4)[:200])}\n2: {G(j(self._field_2.value, indent = 4)[:200])}'
        elif self._status == Diff.S_DIFFLEN :
            # result += f' {Y(P(self._field_1.type) == "List") == "Dict":10} {R(self._field_1.len)} vs. {G(self._field_2.len)}'
            result += f' {Y(P(self._field_1.type) == "list") == "dict":10} {R(self._field_1.len)} vs. {G(self._field_2.len)}'
        elif self._status == Diff.S_DIFFCHILD :
            # result += f' {Y(P(self._field_1.type) == "List") == "Dict":10}'
            result += f' {Y(P(self._field_1.type) == "list") == "dict":10}'
        elif self._status == Diff.S_DIFFVALUE :
            # result += f' {Y(P(self._field_1.type) == "List") == "Dict":10} {R(self._field_1.value):>50} vs. {G(self._field_2.value):50}'
            result += f' {Y(P(self._field_1.type) == "list") == "dict":10} {R(self._field_1.value):>50} vs. {G(self._field_2.value):50}'
        elif self._status == Diff.S_ADDED :
            # result += f' {Y(P(self._field_2.type) == "List") == "Dict":10} 2: {G(j(self._field_2.value, indent = 4)[:200])}'
            result += f' {Y(P(self._field_2.type) == "list") == "dict":10} 2: {G(j(self._field_2.value, indent = 4)[:200])}'
        elif self._status == Diff.S_DELETED :
            # result += f' {Y(P(self._field_1.type) == "List") == "Dict":10} 1: {R(j(self._field_1.value, indent = 4)[:200])}'
            result += f' {Y(P(self._field_1.type) == "list") == "dict":10} 1: {R(j(self._field_1.value, indent = 4)[:200])}'
        elif self._status == Diff.S_IDENTICAL :
            result += f' {self._field_1.value_inspect}'
        return result

# ListDiff: 以 item 作为最小比较单元。降维后可用于StrDiff

# class Diff(Object) :
class Diff() :

    S_DIFFTYPE  = '类型不同'
    S_DIFFLEN   = '数量不同'
    S_DIFFCHILD = '内部不同'
    S_DIFFVALUE = '取值不同'
    S_ADDED     = '新增'
    S_DELETED   = '被删'
    S_IDENTICAL = '相同'

    def __init__(self, raw_data_1, raw_data_2, /) :
        # super().__init__()
        # self._registerProperty(['raw_data_1', 'raw_data_2', 'root_diff_field'])
        # self._registerProperty(['root_diff_field'])
        # self._raw_data_1      = raw_data_1
        object.__setattr__(self, '_raw_data_1', raw_data_1)
        # self._raw_data_2      = raw_data_2
        object.__setattr__(self, '_raw_data_1', raw_data_1)
        self._ins_1           = Inspect(raw_data_1)
        self._ins_2           = Inspect(raw_data_2)
        self._root_diff_field = _DiffField(None, self._ins_1.root_field, self._ins_2.root_field)

    @cached_property
    def all_diff_field_list(self) : return self._root_diff_field.all_diff_field_list

    def printAllDiffFieldList(self) : self.all_diff_field_list.printFormat(); return self

    def getDifferentFieldList(self, **kwargs) : return self._root_diff_field.getDifferentFieldList(**kwargs)

    def printDifferentFieldList(self, **kwargs) : self.getDifferentFieldList(**kwargs).printFormat(); return self

    def print(self, **kwargs) : return self.printDifferentFieldList(**kwargs)
