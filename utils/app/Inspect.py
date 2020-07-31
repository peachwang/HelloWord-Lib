# -*- coding: utf-8 -*-  
from ..shared         import *
from ..datatypes.Str  import Str
from ..datatypes.List import List
from ..datatypes.Dict import Dict
from ..datatypes.Iter import Iter
from .Json            import j

# DataStructure Module
#   def compatibleTo
#   def validate
#   def difference/delta

class _FieldSlot :
    
    def __init__(self, path_tuple, /) :
        self._path_tuple            = path_tuple
        self._value_list            = []
        self._field_list            = []
        self._type_str_list         = List()
        self._list_len_list         = []
        self._child_field_slot_list = List()

    def set_parent_field_slot(self, field_slot, /) : self._parent_field_slot_ref = ref(field_slot); return self

    @cached_prop
    def is_root(self) : return self._parent_field_slot_ref() is None

    @cached_prop
    def path_str(self) -> str : return '.'.join(self._path_tuple) if len(self._path_tuple) > 0 else 'ROOT'

    @cached_prop
    def name(self) -> str : return 'ROOT' if self.is_root else self._path_tuple[-1]

    @cached_prop
    def child_field_slot_list(self) : return self._child_field_slot_list

    @cached_prop
    def is_list(self) : return self._type_str_list.join(', ') == 'list'

    @cached_prop
    def is_dict(self) : return self._type_str_list.join(', ') == 'dict'

    @cached_prop
    def in_list(self) : return False if self.is_root else self._parent_field_slot_ref().is_list

    def add_field(self, field, /) :
        self._field_list.append(field)
        self._type_str_list.unique_append(field.type_str)

        if field.is_list   : self._list_len_list.append(len(field.value))
        elif field.is_dict : pass
        else               : self._value_list.append(field.value)
        return self

    @cached_prop
    def field_num(self) -> int : return len(self._field_list)

    @cached_prop
    def all_field_slot_list(self) :
        if self._child_field_slot_list.len() == 0 : return List(self)
        else                                      : return self._child_field_slot_list.all_field_slot_list.merged().unique().prepend(self)

    # @cached_prop
    # def existence(self) :
    #     if self.is_root : return True
    #     return self.field_num == self._parent_field_slot_ref().field_num

    def __format__(self, spec) :
        max_len   = 3
        max_width = 25
        result    = f'{self.path_str!s:80}{self.name:>25} {P(Y(self._type_str_list.join(", ")) == "dict") == "list":<10} {"  " if self.is_root or self.in_list else (P("必") if self.field_num == self._parent_field_slot_ref().field_num else Y("可"))}存在{self.field_num:>3} 次'
        if self._child_field_slot_list.len() > 0 or self.is_list or self.is_dict :
            if self.is_list   :
                if len(self._list_len_list) == 0         : result += f' {G("为空")}'
                elif len(self._list_len_list) <= max_len : result += f' 含     {List(self._list_len_list).sort(reverse = True).join(", ")} 个元素'
                else                                     :
                    counter     = List(self._list_len_list).count_by()
                    counter_str = List(f'({length}, {count}次)' for length, count in counter.items().sort(itemgetter(1), reverse = True))[:max_len].join(', ')
                    result      += f' 含     {counter_str}{", etc." if counter.len() > max_len else ""} 个元素'
            elif self.is_dict :
                if len(self._child_field_slot_list) > 0 : result += f' 含字段 {Y(self._child_field_slot_list.name.unique().sort().join(", "))}'
                else                                    : result += f' {G("为空")}'
        else                                                                     :
            if len(self._value_list) == 0         : result += f'{R(" 无取值")}'
            elif len(self._value_list) <= max_len : result += f' 取值   {P(List(self._value_list).sort(lambda _ : f"{_}").format(f"{{!s:.{max_width}}}").join(", "))}'
            else                                  :
                counter     = List(self._value_list).count_by()
                counter_str = List(f'({value!s:.{max_width}}, {count}次)' for value, count in counter.items().sort(itemgetter(1), reverse = True))[:max_len].join(', ')
                result      += f' 取值   {P(counter_str)}{", etc." if counter.len() > max_len else ""}'
        return f'{result:{spec}}'

class _Field :
    
    def __init__(self, parent_field, name: str, value, field_slot_dict, /, **kwargs) :
        self._parent_field_ref = ref(parent_field)
        if '.' in name : raise CustomTypeError(name)
        self._name             = name
        self._value            = value
        self._child_field_list = []
        self._build(field_slot_dict, **kwargs)
        
        self._field_slot = field_slot_dict.setdefault(self.slot_path_tuple, _FieldSlot(self.slot_path_tuple)).add_field(self)
        if not self.is_leaf                            :
            for child_field in self._child_field_list : # 建立双向映射
                self._field_slot.child_field_slot_list.unique_append(child_field.field_slot)
                child_field.field_slot.set_parent_field_slot(self._field_slot)
        if self.is_root                                : self._field_slot.set_parent_field_slot(None)

    def _build(self, field_slot_dict, /) :
        if self.is_root : self._path_tuple = tuple()
        else            : self._path_tuple = tuple(list(self._parent_field_ref().path_tuple) + [self._name])
        if isinstance(self._value, dict)   :
            for name, value in self._value.items() :
                child_field = _Field(self, name, value, field_slot_dict)
                self._child_field_list.append(child_field)
                self._child_field_dict[name] = child_field
        elif isinstance(self._value, list) :
            for index, item in enumerate(self._value) :
                name        = f'#{index}'
                child_field = _Field(self, name, item, field_slot_dict)
                self._child_field_list.append(child_field)
                self._child_field_dict[name] = child_field
        return self

    @cached_prop
    def is_root(self) : return self._parent_field_ref() is None

    @cached_prop
    def name(self) -> str : return self._name

    @cached_prop
    def path_tuple(self) : return self._path_tuple

    @cached_prop
    def path_str(self) -> str : return '.'.join(self._path_tuple) if len(self._path_tuple) > 0 else 'ROOT'

    @cached_prop
    def slot_path_tuple(self) : return tuple('#' if Str(name).full_match(r'#\d+') else name for name in self._path_tuple)

    @cached_prop
    def value(self) : return self._value

    @cached_prop
    def is_leaf(self) : return not isinstance(self._value, (list, dict)) or len(self._value) == 0

    @cached_prop
    def is_list(self) : return isinstance(self._value, list)

    @cached_prop
    def is_dict(self) : return isinstance(self._value, dict)

    def len(self) :
        if self.is_list or self.is_dict : return len(self._value)
        else                            : raise CustomTypeError(self._value)

    @cached_prop
    def type_str(self) -> str :
        return ({
                int   : 'int',
                float : 'float',
                bool  : 'bool',
                Str   : 'str',
                str   : 'str',
                List  : 'list',
                list  : 'list',
                Dict  : 'dict',
                dict  : 'dict',
            }
            .get(type(self._value), Str(str(type(self._value))).full_match(r'<class \'([^\'\.]+\.)?([^\']+)\'>').one_group(2).get_raw())
        )

    @cached_prop
    def child_field_list(self) : return List(self._child_field_list)

    @cached_prop
    def all_field_list(self) : return self.child_field_list.all_field_list.merged().prepend(self)

    def has(self, name, /) : return name in self._child_field_dict

    def __getitem__(self, name, /) : return self._child_field_dict[name]

    @cached_prop
    def field_slot(self) : return self._field_slot

    @cached_prop
    def value_inspect(self) -> str :
        result = f'{Y(P(self.type_str) == "list") == "dict":10} '
        if self.is_leaf and not self.is_list and not self.is_dict : result += f'{P(self._value)}'
        elif len(self._child_field_list) == 0                     : result += f'{G("为空")}'
        elif self.is_list                                         : result += f'含 {len(self._child_field_list)} 个元素'
        elif self.is_dict                                         : result += f'含 {len(self._child_field_list)} 个字段: {Y(self.child_field_list.name.sort().join(", "))}'
        else                                                      : raise CustomTypeError(self._value)
        return result

    @cached_func
    def __format__(self, spec) : return f'{f"{self.path_str!s:80}{self.name:>25} {self.value_inspect}":{spec}}'

class Inspect :

    def __init__(self, raw_data: Union[list, dict, List, Dict], **kwargs) :
        if not isinstance(raw_data, (list, dict)) : raise CustomTypeError(raw_data)
        self._raw_data        = raw_data
        self._field_slot_dict = {}
        self._root_field      = _Field(None, 'ROOT', self._raw_data, self._field_slot_dict, **kwargs)

    @cached_prop
    def root_field(self) : return self._root_field

    @cached_prop
    def all_field_list(self) : return self._root_field.all_field_list

    def print_all_field_list(self) : self.all_field_list.print_format(); return self

    @cached_prop
    def all_field_slot_list(self) : return self._root_field.field_slot.all_field_slot_list.sort('path_str')

    def print_all_field_slot_list(self) : self.all_field_slot_list.print_format(); return self

    def print(self) : self.print_all_field_list(); print('-' * 80); self.print_all_field_slot_list(); return self

class _DiffField(_Field) :

    def __init__(self, parent_diff_field, field_1, field_2, /) :
        self._parent_diff_field_ref = ref(parent_diff_field)
        self._field_1               = field_1
        self._field_2               = field_2
        self._child_diff_field_list = []
        self._build()

    def _build(self) :
        if self._field_1 is None   :
            self._path_tuple = self._field_2.path_tuple
            self._name       = self._field_2.name
            self._status     = Diff.S_ADDED
        elif self._field_2 is None :
            self._path_tuple = self._field_1.path_tuple
            self._name       = self._field_1.name
            self._status     = Diff.S_DELETED
        else                       :
            self._path_tuple = self._field_1.path_tuple
            self._name       = self._field_1.name
            if type(self._field_1.value) != type(self._field_2.value) : self._status = Diff.S_DIFFTYPE
            elif self._field_1.is_dict or self._field_1.is_list       :
                for child_field_1 in self._field_1.child_field_list :
                    if self._field_2.has(child_field_1.name) : child_field_2 = self._field_2[child_field_1.name]
                    else                                     : child_field_2 = None
                    self._child_diff_field_list.append(_DiffField(self, child_field_1, child_field_2))
                for child_field_2 in self._field_2.child_field_list :
                    if self._field_1.has(child_field_2.name) : continue
                    else                                     : child_field_1 = None
                    self._child_diff_field_list.append(_DiffField(self, child_field_1, child_field_2))
                if self._field_1.len() != self._field_2.len()       : self._status = Diff.S_DIFFLEN
                else                                                :
                    if all(diff_field.status == Diff.S_IDENTICAL for diff_field in self._child_diff_field_list) : self._status = Diff.S_IDENTICAL
                    else                                                                                        : self._status = Diff.S_DIFFCHILD
            elif self._field_1.is_leaf and self._field_2.is_leaf      :
                if self._field_1.value == self._field_2.value : self._status = Diff.S_IDENTICAL
                else                                          : self._status = Diff.S_DIFFVALUE
            else                                                      : raise CustomTypeError(self._field_1.value)
        return self

    @cached_prop
    def name(self) -> str : return self._name

    @cached_prop
    def status(self) -> str : return self._status

    @cached_prop
    def child_diff_field_list(self) : return List(self._child_diff_field_list)

    @cached_prop
    def all_diff_field_list(self) : return self.child_diff_field_list.all_diff_field_list.merged().prepend(self)

    def get_different_field_list(self, filter_list = None) :
        if isinstance(filter_list, list) and (self.path_str, self._status) in filter_list : return List()
        result = List(_.get_different_field_list(filter_list = filter_list) for _ in self._child_diff_field_list).merged()
        if (self._status in (Diff.S_DIFFTYPE, Diff.S_DIFFVALUE, Diff.S_ADDED, Diff.S_DELETED)
            or self._status in (Diff.S_DIFFLEN, Diff.S_DIFFCHILD) and not result.is_empty()) :
            result.prepend(self)
        return result

    def __format__(self, spec) :
        result = f'{self.path_str!s:80}{self.name:>25} {S(Y(B(C(P(R(G(self._status) == Diff.S_ADDED) == Diff.S_DELETED) == Diff.S_DIFFVALUE) == Diff.S_DIFFLEN) == Diff.S_DIFFTYPE) == Diff.S_DIFFCHILD) == Diff.S_IDENTICAL:<8}'
        if self._status == Diff.S_DIFFTYPE    : result += f' {self._field_1.type_str} vs. {self._field_2.type_str}\n1: {R(j(self._field_1.value, indent = 4)[:200])}\n2: {G(j(self._field_2.value, indent = 4)[:200])}'
        elif self._status == Diff.S_DIFFLEN   : result += f' {Y(P(self._field_1.type_str) == "list") == "dict":10} {R(self._field_1.len())} vs. {G(self._field_2.len())}'
        elif self._status == Diff.S_DIFFCHILD : result += f' {Y(P(self._field_1.type_str) == "list") == "dict":10}'
        elif self._status == Diff.S_DIFFVALUE : result += f' {Y(P(self._field_1.type_str) == "list") == "dict":10} {R(self._field_1.value):>50} vs. {G(self._field_2.value):50}'
        elif self._status == Diff.S_ADDED     : result += f' {Y(P(self._field_2.type_str) == "list") == "dict":10} 2: {G(j(self._field_2.value, indent = 4)[:200])}'
        elif self._status == Diff.S_DELETED   : result += f' {Y(P(self._field_1.type_str) == "list") == "dict":10} 1: {R(j(self._field_1.value, indent = 4)[:200])}'
        elif self._status == Diff.S_IDENTICAL : result += f' {self._field_1.value_inspect}'
        return f'{result:{spec}}'

# ListDiff: 以 item 作为最小比较单元。降维后可用于StrDiff

class Diff :

    S_DIFFTYPE  = '类型不同'
    S_DIFFLEN   = '数量不同'
    S_DIFFCHILD = '内部不同'
    S_DIFFVALUE = '取值不同'
    S_ADDED     = '新增'
    S_DELETED   = '被删'
    S_IDENTICAL = '相同'

    def __init__(self, raw_data_1: Union[list, dict, List, Dict], raw_data_2: Union[list, dict, List, Dict], /) :
        self._raw_data_1      = raw_data_1
        self._raw_data_2      = raw_data_2
        self._ins_1           = Inspect(raw_data_1)
        self._ins_2           = Inspect(raw_data_2)
        self._root_diff_field = _DiffField(None, self._ins_1.root_field, self._ins_2.root_field)

    @cached_prop
    def all_diff_field_list(self) : return self._root_diff_field.all_diff_field_list

    def print_all_diff_field_list(self) : self.all_diff_field_list.print_format(); return self

    def get_different_field_list(self, **kwargs) : return self._root_diff_field.get_different_field_list(**kwargs)

    def print_different_field_list(self, **kwargs) : self.get_different_field_list(**kwargs).print_format(); return self

    def print(self, **kwargs) : return self.print_different_field_list(**kwargs)
