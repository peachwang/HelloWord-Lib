# -*- coding: utf-8 -*-  
from shared import *
from Str import Str
from DateTime import timedelta_class, TimeDelta, date_class, Date, time_class, Time, datetime_class, DateTime
from List import List
from Dict import Dict

class Object :

    __id_list           = [ ]
    NV = P_NON_VACANCY  = 'P_NON_VACANCY'

    def _wrapValue(self, value, /) :
        if isinstance(value, (Str, List, Dict))   : return value
        elif isinstance(value, str)               : return Str(value)
        elif isinstance(value, bytes)             : return Str(value.decode())
        elif isinstance(value, timedelta_class)   : return TimeDelta(value)
        elif isinstance(value, date_class)        : return Date(value)
        elif isinstance(value, time_class)        : return Time(value)
        elif isinstance(value, datetime_class)    : return DateTime(value)
        elif isinstance(value, list)              : return List(value)
        elif isinstance(value, dict)              : return Dict(value)
        elif isinstance(value, tuple)             : return tuple([ self._wrapValue(_) for _ in value ])
        elif isinstance(value, set)               : return set([ self._wrapValue(_) for _ in value ])
        else                                      : return value
    
    def __init__(self) :
        object.__setattr__(self, '_data',          Dict())
        object.__setattr__(self, '_property_dict', {})

    # def _registerEnhancedProperty(self, property_config_list, /) :
    def _registerProperty(self, property_config_list, /) :
        pd = self.__getattribute__('_property_dict')
        for config in property_config_list :
            if isinstance(config, str)     : pd[config] = {}
            elif isinstance(config, tuple) :
                name        = config[0]
                p_default   = config[1]
                p_type      = config[2] if len(config) > 2 else None
                p_validator = config[3] if len(config) > 3 else None
                pd[name]    = {}
                if p_default != self.P_NON_VACANCY : pd[name]['default'] = self._wrapValue(p_default)
                if p_type is not None              :
                    if not isinstance(p_type, (type, tuple))     : raise UserTypeError(p_type)
                    if isinstance(p_type, tuple)                 : p_type = tuple(type(None) if item is None else item for item in p_type)
                    pd[name]['type'] = p_type
                if p_validator is not None         :
                    if not isinstance(p_validator, (str, tuple)) : raise UserTypeError(p_validator)
                    # pd[name]['validator'] = Str(p_validator) if isinstance(p_validator, str) else p_validator
                    pd[name]['validator'] = p_validator
            else                           : raise UserTypeError(config)
        return self

    def hasProperty(self, name, /) : return self._data.has(name)

    def hasNoProperty(self, name, /) : return not self.hasProperty(name)

    def ensureHasProperty(self, name, /) :
        if self.hasNoProperty(name) : raise Exception(f'{self} 必须拥有属性 {name}')
        return self

    def getProperty(self, name, /, default = None) : return self._data.get(name, self._wrapValue(default))
    
    def setProperty(self, name, value, /) : self._data[name] = self._wrapValue(value); return self

    def __setattr__(self, name, value) :
        if name[0] != '_' : raise Exception(f'{name =} 应包含下划线前缀')
        self._data[name[1:]] = self._wrapValue(value)
        return value

    def appendProperty(self, name, value_or_generator_or_iterator, /, *, filter_none = True) :
        def appendValue(value) :
            if filter_none and value == None : return
            if self._data.hasNo(name) : self._data[name] = List()
            self._data[name].append(value)
        if (isgenerator(value_or_generator_or_iterator)
            or '__next__' in dir(value_or_generator_or_iterator)) :
            for value in value_or_generator_or_iterator : appendValue(value)
        else                                                      : appendValue(value_or_generator_or_iterator)
        return self

    def uniqueAppendProperty(self, name, value_or_generator_or_iterator, /, *, filter_none = True) :
        def uniqueAppendValue(value) :
            if filter_none and value == None : return
            if self._data.hasNo(name) : self._data[name] = List()
            self._data[name].uniqueAppend(value)
        if (isgenerator(value_or_generator_or_iterator)
            or '__next__' in dir(value_or_generator_or_iterator)) :
            for value in value_or_generator_or_iterator : uniqueAppendValue(value)
        else                                                      : uniqueAppendValue(value_or_generator_or_iterator)
        return self

    def updateProperty(self, mapping, /) :
        pd = self.__getattribute__('_property_dict')
        for name, value in mapping.items() :
            if name in pd : self.setProperty(name, value)
            else          : raise Exception(f'{name} 非注册属性')
        return self

    # 支持：
    #   已注册属性无需显式定义 has, hasNo, ensureHas, get, set, append, uniqueAppend 方法
    #   已注册属性的 append, uniqueAppend 方法支持自动初始化
    #   已注册属性不存在时返回预设默认值
    #   保护私有属性不被外部访问和赋值
    # 访问方式：
    # 已注册（可通过 隐式方法 或 已显式定义为含业务逻辑的 @property/@cached_property 访问）
    #   从外部
    #       [_name]   (1) 不允许如此访问，可通过 find 查到 (?<!self)(?<!cls)(?<!super\(\))\._(?!(_|\.|data\b|getData\b))
    #       [name]    (2) 允许，常规情况
    #   从内部
    #       [_name]   (3) 允许，常规情况
    #       [name]    (4) 不推荐/不允许通过隐式方法访问（靠自觉），无法通过 find 查到！其余情况一定是已显式定义为含业务逻辑的 @property/@cached_property
    # 未注册（仅使用 __setattr__ 赋值过）
    #   从外部
    #       [_name]   (5) 不允许，可通过 find 查到
    #       [name]    (6) 不允许，__setattr__ 规避此类情况
    #   从内部
    #       [_name]   (7) 允许，常规情况，私有属性
    #       [name]    (8) 不允许，__setattr__ 规避了其余情况
    # @Timer.timeitTotal('Object.__getattr__', group_args = True)
    def __getattr__(self, name) :
        if name == '_data'     : return self.__getattribute__('_data')
        if name == '__class__' : return self.__getattribute__('__class__')
        if name in dir(self)   : return self.__getattribute__(name)
        
        pd = self.__getattribute__('_property_dict')
        if name in pd or name[0] == '_' and name[1:] in pd : # (1) (2) (3) (4) 已注册
            if name[0] == '_'         : name = name[1:] # (1) (3) 转为 (2) (4)
            if name not in self._data : # 未赋值
                if 'default' in pd[name] : return pd[name]['default'] # 设有默认值
                else                     : pass # 报错
            else                      : return self._data[name] # 已赋值
        else                                               : # (5) (6) (7) (8) 未注册
            if name[0] != '_'         : pass # (6) (8) 报错
            else                      : name = name[1:] # (5) (7)
            if name not in self._data : pass # 未赋值 报错
            else                      : return self._data[name] # 已赋值

        from functools import partial
        for prefix in ( 'has', 'hasNo', 'ensureHas', 'get', 'set', 'append', 'uniqueAppend' ) :
            l = len(prefix)
            suffix_1 = '_list' if prefix in ('append', 'uniqueAppend') else ''
            suffix_2 = 'List' if prefix in ('append', 'uniqueAppend') else ''
            if name[:l] == prefix and (name[l].isupper() or name[l] == '_') :
                if ((existence_1 := (name_1 := Str(name[l:]).toSnakeCase() + suffix_1) in pd)
                or ((existence_2 := (name_2 := Str(name[l:]).toPascalCase() + suffix_2) in pd))) :
                    if existence_1   : name_0 = str(name_1)
                    elif existence_2 : name_0 = str(name_2)
                    if prefix in pd[name_0] : return pd[name_0][prefix] # 获取已缓存的方法
                    else                    : pd[name_0][prefix] = partial(self.__getattribute__(f'{prefix}Property'), name_0); return pd[name_0][prefix]

        raise Exception(f"Object {P(type(self))} 中无 {P(name)} 属性或方法, 只有这些属性: {P((self._data.keys() + dir(self)).filter(lambda name : name not in (['_property_dict', '_data'] + dir(Object))))}\n{pd=}")

    # def getPropertyDict(self, name_list, /) : return self._data.getMulti(name_list, de_underscore = True) # 字段可以不存在

    # 防止自嵌套死循环
    def _antiLoop(func) :
        @wraps(func)
        def wrapper(self, *args, **kwargs) :
            if self.getId() in Object.__id_list : result = object.__str__(self)
            else                                :
                Object.__id_list.append(self.getId())
                result = func(self, *args, **kwargs)
                Object.__id_list.remove(self.getId())
            return result
        return wrapper

    @_antiLoop
    def validateProperty(self, index = None) :
        # if index is not None and index >= 100 and index % 1 == 0 :
        if index is not None and index >= 100 and index % 100 == 0 : Timer.printTiming(f'validateProperty.{index}.{self!r}')
        prefix = self.getSignature()
        try                      :
            pd = self.__getattribute__('_property_dict')
            for name in pd :
                if self._data.has(name) :
                    value = self._data[name]
                    
                    if name[-4:] in ('list', 'List') and not isinstance(value, list)                        :
                        raise Exception(f'{prefix} 属性 {name} 的值\n[{value}]\n不是列表\n{self}\n')
                    elif name[-4:] not in ('list', 'List') and isinstance(value, list)                      :
                        raise Exception(f'{prefix} 值为\n[{value}]\n的属性 {name} 后缀不是List/list\n{self}\n')
                    elif isinstance(value, list) and len(value) > 0 and 'validateProperty' in dir(value[0]) :
                        for idx, item in value.enum() : item.validateProperty(idx + 1)
                    
                    if name[-4:] in ('dict', 'Dict') and not isinstance(value, dict)                        :
                        raise Exception(f'{prefix} 属性 {name} 的值\n[{value}]\n不是字典\n{self}\n')
                    elif name[-4:] not in ('dict', 'Dict') and isinstance(value, dict)                      :
                        raise Exception(f'{prefix} 值为\n[{value}]\n的属性 {name} 后缀不是Dict/dict\n{self}\n')
                    elif isinstance(value, dict)                                                            :
                        for v in value.values() :
                            if 'validateProperty' in dir(v) : v.validateProperty()

                    if isinstance(value, Object)                                                            : value.validateProperty()

                    pt = pd[name]['type'] if 'type' in pd[name] else None
                    pv = pd[name]['validator'] if 'validator' in pd[name] else None

                    if pt is not None and not isinstance(pv, tuple)                                         :
                        if isinstance(value, list) :
                            if isinstance(pt, type)    :
                                func = lambda item : isinstance(item, pt)
                                if not all(list(map(func, value))) : raise Exception(f'{prefix} 属性 {name} 的列表值\n[{value}]\n中有值不匹配类型 {pt}\n{self}\n')
                            else                       : raise UserTypeError(pt)
                        else                       :
                            if isinstance(pt, type)    :
                                if not isinstance(value, pt)       : raise Exception(f'{prefix} 属性 {name} 的值\n[{value}]\n的类型 {type(value)} 不匹配类型 {pt}\n{self}\n')
                            elif isinstance(pt, tuple) :
                                func = lambda t : ((t is None or t is type(None)) and value is None) or (isinstance(value, t))
                                if not any(list(map(func, pt)))    : raise Exception(f'{prefix} 属性 {name} 的值\n[{value}]\n的类型 {type(value)} 不匹配类型 {pt}\n{self}\n')
                            else                       : raise UserTypeError(pt)

                    type_tuple = (int, float, bool, bytes, range, tuple, set, list, dict, timedelta_class, date_class, time_class, datetime_class)
                    if isinstance(pv, tuple)                                   :
                        if value not in pv                                                  : raise Exception(f'{prefix} 属性 {name} 的值\n[{value}]\n不属于: \n{pv}\n{self}\n')
                    elif isinstance(pv, str) and isinstance(value, type_tuple) :
                        if eval(Str(pv).replace('#', 'value', re_mode = False)) is not True : raise Exception(f'{prefix} 属性 {name} 的值\n[{value}]\n不合法: [{pv}]\n{self}\n')
                    elif isinstance(pv, str) and isinstance(value, str)        :
                        if not value.fullMatch(pv)                                          : raise Exception(f'{prefix} 属性 {name} 的值\n[{value}]\n不匹配: \n[{pv}]\n[{self}]\n')
        except Exception as e    :
            # print(self.j())
            print(e)
            # raise e
        except KeyboardInterrupt :
            if index is not None : Timer.printTiming(f'{index}.{self}.{self._data}')
            raise
        return self

    # id(object) -> integer
    # Return the identity of an object.  This is guaranteed to be unique among
    # simultaneously existing objects.  (Hint: it's the object's memory address.)
    def getId(self) : return hex(id(self))

    # def getRaw(self) : return self._data.getRaw()

    def getSignature(self) : return f'<{self.__class__} at {self.getId()}>'

    @_antiLoop
    def __format__(self, code) : return f'<{self.__class__} at {self.getId()}>._data={self._data}'

    @print_func
    def printFormat(self) : return f'{self}', False

    @_antiLoop
    def __str__(self) : return f'<{self.__class__} at {self.getId()}>._data={str(self._data)}'

    @print_func
    def printStr(self) : return f'{str(self)}', False

    @_antiLoop
    def jsonSerialize(self) : result = self._data.jsonSerialize(); result['__instance__'] = self.getSignature(); return result

    # 可读化
    def j(self) : return j(self.jsonSerialize())

    @print_func
    def printJ(self) : return f'{self.j()}', False

    @_antiLoop
    def json(self) :
        return Dict(
            (name, value.json() if 'json' in dir(value := self.__getattr__(f'_{name}')) else value)
            for name in self.__getattribute__('_property_dict')
            if self._data.has(name) or name in dir(self)
        )

    @print_func
    def printJson(self) : return f'{_ if isinstance(_ := self.json(), str) else _.j()}', False

if __name__ == '__main__':
    o = Object()._registerProperty(['a'])
    data = Dict({'b' : [1,2,3]})
    data2 = Dict(data)
    o.setA(data['b'])
    print(o)
    data['b'].append(4)
    print(data, id(data))
    print(o, id(o.a))
    print(data2, id(data2))
    data['b'].append(5)
    print(data, id(data))
    print(o, id(o.a))
    print(data2, id(data2))
    data.c = 'hello'
    print(data, id(data))
    print(o, id(o.a))
    print(data2, id(data2))


    # print('\n'.join(dir(o)))
    # print(o.ensureHasProperty('a'))
    # print(dir(o))