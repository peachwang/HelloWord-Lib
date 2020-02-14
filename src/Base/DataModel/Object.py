# -*- coding: utf-8 -*-  
import sys, os; sys.path.append(os.path.realpath(__file__ + '/../'));
from functools import wraps, partial
from shared import ensureArgsType, Optional, Union, UserTypeError, _print

class Object() :

    __id_list = [ ]
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
    
    def _getProperty(self, name, /, default = None) :
        return self._data.get(f'_{name}', default)

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

    def _uniqueAppendProperty(self, name, value_or_generator_or_iterator, /, *, filter_none = True) :
        from List import List
        from inspect import isgenerator
        name = f'_{name}'
        def uniqueAppendValue(value) :
            if filter_none and value == None : return
            if self._data.hasNot(name) :
                self._data[name] = List()
            self._data[name].uniqueAppend(value)
        if isgenerator(value_or_generator_or_iterator) or '__next__' in dir(value_or_generator_or_iterator) :
            for value in value_or_generator_or_iterator :
                uniqueAppendValue(value)
        else : uniqueAppendValue(value_or_generator_or_iterator)
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

        for prefix in ( 'has', 'hasNot', 'ensureHas', 'get', 'set', 'append', 'uniqueAppend' ) :
            l = len(prefix)
            suffix_1 = ('List' if prefix in ('append', 'uniqueAppend') else '')
            suffix_2 = ('_list' if prefix in ('append', 'uniqueAppend') else '')
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
        raise Exception(f"Object {P(type(self))} 中无 {P(name)} 属性或方法, 只有这些属性: {P((self._data.keys() + dir(self)).filter(lambda name : name not in (['_property_dict', '_data'] + dir(Object))))}\n{pd=}")

    def __getitem__(self, name) :
        return self.__getattr__(name)

    def getPropertyDict(self, name_list, /) :
        raise NotImplementedError
        return self._data.getMulti(name_list, de_underscore = True) # 字段可以不存在

    # 防止自嵌套死循环
    def _antiLoop(func) :
        @wraps(func)
        def wrapper(self, *args, **kwargs) :
            if self.getId() in Object.__id_list :
                result = object.__str__(self)
            else :
                Object.__id_list.append(self.getId())
                result = func(self, *args, **kwargs)
                Object.__id_list.dropItem(self.getId())
            return result
        return wrapper

    @_antiLoop
    def validateProperty(self, index = None) :
        from Timer import Timer
        # if index is not None and index >= 100 and index % 1 == 0 :
        if index is not None and index >= 100 and index % 100 == 0 :
            Timer.printTiming(f'validateProperty.{index}.{self!r}')
        prefix = self.getSignature()
        try :
            pd = self.__getattribute__('_property_dict')
            from DateTime import DateTime, datetime
            for name in pd.keys() :
                if self._data.has(f'_{name}') :
                    value = self._data[f'_{name}']
                    
                    if name[-4:] in ('list', 'List') and not isinstance(value, list) :
                        raise Exception(f'{prefix} 属性 {name} 的值\n[{value}]\n不是列表\n{self}\n')
                    elif name[-4:] not in ('list', 'List') and isinstance(value, list) :
                        raise Exception(f'{prefix} 值为\n[{value}]\n的属性 {name} 后缀不是List/list\n{self}\n')
                    elif isinstance(value, list) and len(value) > 0 and 'validateProperty' in dir(value[0]) :
                        for idx, item in value.enum() :
                            item.validateProperty(idx + 1)
                    
                    if name[-4:] in ('dict', 'Dict') and not isinstance(value, dict) :
                        raise Exception(f'{prefix} 属性 {name} 的值\n[{value}]\n不是字典\n{self}\n')
                    elif name[-4:] not in ('dict', 'Dict') and isinstance(value, dict) :
                        raise Exception(f'{prefix} 值为\n[{value}]\n的属性 {name} 后缀不是Dict/dict\n{self}\n')
                    elif isinstance(value, dict) :
                        for v in value.values() :
                            if 'validateProperty' in dir(v) :
                                v.validateProperty()

                    if isinstance(value, Object) :
                        value.validateProperty()

                    pt = pd[name].type if pd[name].has('type') else None
                    pv = pd[name].validator if pd[name].has('validator') else None

                    if not isinstance(pv, tuple) and pt is not None :
                        if isinstance(value, list) :
                            if isinstance(pt, type) :
                                if not all(list(map(lambda item : isinstance(item, pt), value))) :
                                    raise Exception(f'{prefix} 属性 {name} 的列表值\n[{value}]\n中有值不匹配类型 {pt}\n{self}\n')
                            else :
                                raise UserTypeError(pt)
                        else :
                            if isinstance(pt, type) :
                                if not isinstance(value, pt) :
                                    raise Exception(f'{prefix} 属性 {name} 的值\n[{value}]\n的类型 {type(value)} 不匹配类型 {pt}\n{self}\n')
                            elif isinstance(pt, tuple) :
                                if not any(list(map(lambda t : ((t is None or t is type(None)) and value is None) or (isinstance(value, t)), pt))) :
                                    raise Exception(f'{prefix} 属性 {name} 的值\n[{value}]\n的类型 {type(value)} 不匹配类型 {pt}\n{self}\n')
                            else :
                                raise UserTypeError(pt)

                    # if isinstance(pv, str) and isinstance(value, str) :
                        # print(f'{value=} {pv=}')

                    if isinstance(pv, tuple) and value not in pv :
                        raise Exception(f'{prefix} 属性 {name} 的值\n[{value}]\n不属于: \n{pv}\n{self}\n')
                    elif isinstance(pv, str) and isinstance(value, (int, float, bool, bytes, range, tuple, set, list, dict, DateTime, datetime))\
                        and eval(pv.replace('#', 'value', re_mode = False)) is not True :
                        raise Exception(f'{prefix} 属性 {name} 的值\n[{value}]\n不合法: [{pv}]\n{self}\n')
                    elif isinstance(pv, str) and isinstance(value, str) and not value.fullMatch(pv) :
                        raise Exception(f'{prefix} 属性 {name} 的值\n[{value}]\n不匹配: \n[{pv}]\n[{self}]\n')
        except Exception as e :
            # print(self.j())
            print(e)
            # raise e
        except KeyboardInterrupt :
            if index is not None : Timer.printTiming(f'{index}.{self}.{self._data}')
            raise
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

    def getSignature(self) :
        return f'<{self.__class__} at {self.getId()}>'

    @_antiLoop
    def __format__(self, code) :
        return f'{self._data}'

    @_print
    def printFormat(self) :
        return f'{self}', False

    @_antiLoop
    def __str__(self) :
        return f'<{self.__class__} at {self.getId()}>._data={str(self._data)}'

    @_print
    def printStr(self) :
        return f'{str(self)}', False

    @_antiLoop
    def jsonSerialize(self) :
        result = self._data.jsonSerialize()
        result['__instance__'] = self.getSignature()
        return result

    # 可读化
    def j(self) :
        from util import j
        return j(self.jsonSerialize())

    @_print
    def printJ(self) :
        return f'{self.j()}', False

    @_antiLoop
    def json(self) :
        from Dict import Dict
        return Dict((name, value.json() if 'json' in dir(value := self.__getattr__(name)) else value)
            for name in self.__getattribute__('_property_dict') if self._data.has(f'_{name}') or name in dir(self))

    @_print
    def printJson(self) :
       return f'{_ if isinstance(_ := self.json(), str) else _.j()}', False
