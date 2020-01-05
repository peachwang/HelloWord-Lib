# -*- coding: utf-8 -*-  
import sys, os; sys.path.append(os.path.realpath(__file__ + '/../'));
from functools import wraps, partial, lru_cache, singledispatchmethod
from shared import ensureArgsType, Optional, Union, UserTypeError
from Timer import Timer

class Object() :

    _id_list = [ ]
    NV = P_NON_VACANCY  = 'P_NON_VACANCY'
    
    def __init__(self) :
        from List import List
        from Dict import Dict
        object.__setattr__(self, '_data', Dict())
        object.__setattr__(self, '_property_dict', Dict())

    # @ensureArgsType
    def _registerProperty(self, property_config_list, /) :
        from List import List
        from Dict import Dict
        from Str import Str
        pd = self.__getattribute__('_property_dict')
        for config in property_config_list :
            if isinstance(config, str) :
                pd[config] = Dict()
            elif isinstance(config, tuple) :
                name        = config[0]
                p_default   = config[1]
                p_type      = config[2] if len(config) > 2 else None
                p_validator = config[3] if len(config) > 3 else None
                pd[name] = Dict()
                if p_default != self.P_NON_VACANCY :
                    pd[name].default = p_default
                if p_type is not None :
                    if not isinstance(p_type, (type, tuple)) :
                        raise UserTypeError(p_type)
                    if isinstance(p_type, tuple) :
                        p_type = tuple(type(None) if item is None else item for item in p_type)
                    pd[name].type = p_type
                if p_validator is not None :
                    if not isinstance(p_validator, (str, tuple)) :
                        raise UserTypeError(p_validator)
                    pd[name].validator = Str(p_validator) if isinstance(p_validator, str) else p_validator
            else :
                raise UserTypeError(config)
        return self

    def _hasProperty(self, name, /) :
        return self._data.has(f'_{name}')

    def _hasNotProperty(self, name, /) :
        return not self._hasProperty(name)

    def _ensureHasProperty(self, name, /) :
        if _hasNotProperty(name) :
            raise Exception(f'{self}必须拥有属性{name}.')
        return self

    def _setProperty(self, name, value, /) :
        self._data[f'_{name}'] = value
        return self

    def _appendProperty(self, name, value_or_generator_or_iterator, /, *, filter_none = True) :
        from List import List
        from inspect import isgenerator
        name = f'_{name}'
        def appendValue(value) :
            if filter_none and value == None : return
            if self._data.hasNot(name) :
                self._data[name] = List()
            self._data[name].append(value)
        if isgenerator(value_or_generator_or_iterator) or '__next__' in dir(value_or_generator_or_iterator) :
            for value in value_or_generator_or_iterator :
                appendValue(value)
        else : appendValue(value_or_generator_or_iterator)
        return self

    def updateProperty(self, mapping, /) :
        pd = self.__getattribute__('_property_dict')
        for name, value in mapping.items() :
            if name in pd :
                self._setProperty(name, value)
            else :
                raise Exception(f'{name} 非注册属性')
        return self

    # @Timer.timeitTotal('Object.__getattr__', group_args = True)
    def __getattr__(self, name) :
        from Str import Str
        if name == '_data' : return self.__getattribute__('_data')
        if name == '__class__' : return self.__getattribute__('__class__')
        if name in dir(self) : return self.__getattribute__(name)
        pd = self.__getattribute__('_property_dict')
        if name in pd : name = f'_{name}' # 通过外部访问时，已注册属性前缀化
        if name[0] == '_' and name[1:] in pd : # 确实是已注册属性
            if name not in self._data and pd[name[1:]].has('default') : # 未赋值属性且有设置默认值
                return pd[name[1:]].default
        if name in self._data : return self._data[name]
        if f'_{name}' in self._data : return self._data[f'_{name}'] # 未注册属性

        for prefix in ( 'has', 'hasNot', 'ensureHas', 'set', 'append' ) :
            l = len(prefix)
            suffix_1 = ('List' if prefix == 'append' else '')
            suffix_2 = ('_list' if prefix == 'append' else '')
            if name[:l] == prefix and (name[l].isupper() or name[l] == '_') :
                if (existence_2 := pd.has(name_2 := Str(name[l:]).toSnakeCase() + suffix_2))\
                    or (existence_1 := pd.has(name_1 := Str(name[l:]).toPascalCase() + suffix_1)) :
                    if existence_2 : name_0 = str(name_2)
                    elif existence_1 : name_0 = str(name_1)
                    
                    if pd[name_0].has(prefix) :
                        return pd[name_0][prefix]
                    else :
                        # print(f'<{self.__class__} at {self.getId()}>.{key[0]}({key[1]})')
                        pd[name_0][prefix] = partial(self.__getattribute__(f'_{prefix}Property'), name_0)
                        return pd[name_0][prefix]

        from util import P, E
        raise Exception(f"Object{P}{type(self)}{E}中无{P}{name}{E}属性或方法, 只有这些属性: {(self._data.keys() + dir(self)).filter(lambda name : name not in (['_property_dict', '_data'] + dir(Object)))}\n{pd=}")

    def __getitem__(self, name) :
        return self.__getattr__(name)

    def getPropertyDict(self, name_list, /) :
        raise NotImplementedError
        return self._data.getMulti(name_list, de_underscore = True) # 字段可以不存在

    def validateProperty(self) :
        try :
            pd = self.__getattribute__('_property_dict')
            from DateTime import DateTime, datetime
            for name in pd.keys() :
                if self._data.has(f'_{name}') :
                    value = self._data[f'_{name}']
                    
                    if name[-4:] in ('list', 'List') and not isinstance(value, list) :
                        raise Exception(f'属性 {name} 的值 {value} 不是列表')
                    elif name[-4:] not in ('list', 'List') and isinstance(value, list) :
                        raise Exception(f'值为 {value} 的属性 {name} 后缀不是List/list')
                    elif isinstance(value, list) and len(value) > 0 and 'validateProperty' in dir(value[0]) :
                        for item in value :
                            item.validateProperty()
                    
                    if name[-4:] in ('dict', 'Dict') and not isinstance(value, dict) :
                        raise Exception(f'属性 {name} 的值 {value} 不是字典')
                    elif name[-4:] not in ('dict', 'Dict') and isinstance(value, dict) :
                        raise Exception(f'值为 {value} 的属性 {name} 后缀不是Dict/dict')
                    elif isinstance(value, dict) :
                        for v in value.values() :
                            if 'validateProperty' in dir(v) :
                                v.validateProperty()

                    pt = pd[name].type if pd[name].has('type') else None
                    pv = pd[name].validator if pd[name].has('validator') else None

                    if not isinstance(pv, tuple) and pt is not None :
                        if isinstance(value, list) :
                            if isinstance(pt, type) :
                                if not all(list(map(lambda item : isinstance(item, pt), value))) :
                                    raise Exception(f'属性 {name} 的列表值 {value} 不匹配类型 {pt}')
                            else :
                                raise UserTypeError(pt)
                        else :
                            if isinstance(pt, type) :
                                if not isinstance(value, pt) :
                                    raise Exception(f'属性 {name} 的值 {value} 不匹配类型 {pt}')
                            elif isinstance(pt, tuple) :
                                if not any(list(map(lambda t : ((t is None or t is type(None)) and value is None) or (isinstance(value, t)), pt))) :
                                    raise Exception(f'属性 {name} 的值 {value} 不匹配类型 {pt}')
                            else :
                                raise UserTypeError(pt)

                    if isinstance(pv, tuple) and value not in pv :
                        raise Exception(f'属性 {name} 的值 {value} 不属于 {pv}')
                    elif isinstance(pv, str) and isinstance(value, (int, float, bool, bytes, range, tuple, set, list, dict, DateTime, datetime))\
                        and eval(pv.replace('#', 'value', re_mode = False)) is not True :
                        raise Exception(f'属性 {name} 的值 {value} 不合法: {pv}')
                    elif isinstance(pv, str) and isinstance(value, str) and not value.fullMatch(pv) :
                        raise Exception(f'属性 {name} 的值 {value} 不匹配 {pv}')
        except Exception as e :
            print(self)
            print(e)
        return self

    def _wrapValue(self, value, /) :
        from Dict import Dict
        from List import List
        from Str import Str
        from DateTime import DateTime, datetime
        if isinstance(value, list)        : return List(value)
        elif isinstance(value, dict)      : return Dict(value)
        elif isinstance(value, str)       : return Str(value)
        elif isinstance(value, bytes)     : return Str(value.decode())
        elif isinstance(value, tuple)     : return tuple([ self._wrapValue(_) for _ in value ])
        elif isinstance(value, set)       : return set([ self._wrapValue(_) for _ in value ])
        elif isinstance(value, datetime)  : return DateTime(value)
        else : return value

    def __setattr__(self, name, value) :
        self._data[name] = self._wrapValue(value)
        return value

    def getId(self) :
        '''id(object) -> integer
        Return the identity of an object.  This is guaranteed to be unique among
        simultaneously existing objects.  (Hint: it's the object's memory address.)'''
        return hex(id(self))

    def getRaw(self) :
        return self._data

    def jsonSerialize(self) :
        from util import j
        _ = self._data.jsonSerialize()
        _['__instance__'] = f'<{self.__class__} at {self.getId()}>'
        return _

    # 可读化
    def j(self) :
        from util import j
        return j(self.jsonSerialize())

    def json(self) :
        from Dict import Dict
        return Dict((name, value.json() if 'json' in dir(value := self.__getattr__(name)) else value)
            for name in self.__getattribute__('_property_dict') if self._data.has(f'_{name}') or name in dir(self))

    def print(self, *, color = '', json = False) :
        from util import E
        if json :
            print(color, self.json().j(), E if color != '' else '')
        else :
            print(color, self.j(), E if color != '' else '')
        return self

    def __format__(self, code) :
        # 防止自嵌套死循环
        if self.getId() in Object._id_list :
            return object.__str__(self)
        Object._id_list.append(self.getId())
        result = f'{self._data}'
        Object._id_list.remove(self.getId())
        return result

    def __str__(self) :
        # 防止自嵌套死循环
        if self.getId() in Object._id_list :
            return object.__str__(self)
        Object._id_list.append(self.getId())
        result = f'<{self.__class__} at {self.getId()}>{str(self._data)}'
        Object._id_list.remove(self.getId())
        return result
