# -*- coding: utf-8 -*-  

class Dict(dict) :

    def __init__(self, *args) :
        '''Initialize self.  See help(type(self)) for accurate signature.'''
        if len(args) == 0 :
            dict.__init__(self, {})
        elif len(args) == 1 :
            if type(args[0]) is dict :
                for key in args[0] :
                    if type(args[0][key]) is dict :
                        dict.__setitem__(self, key, Dict(args[0][key]))
                    elif type(args[0][key]) is list :
                        from DataModel.List import List
                        dict.__setitem__(self, key, List(args[0][key]))
                    else :
                        dict.__setitem__(self, key, args[0][key])
                # dict.__init__(self, args[0])
            elif type(args[0]) is Dict :
                dict.__init__(self, args[0].data())
            else :
                raise Exception('Unexpected args for Dict.__init__: {}'.format(str(args)))
        else :
            raise Exception('Unexpected args for Dict.__init__: {}'.format(str(args)))

    def data(self) :
        return { key : self[key] for key in self }

    # def fromkeys(self, key_list, value = None) :
        '''
        Returns a new dict with keys from iterable and values equal to value.
        '''

    # def keys(self) :
        '''
        D.keys() -> a set-like object providing a view on D's keys
        '''
    
    # def values(self) :
        '''
        D.values() -> an object providing a view on D's values
        '''

    # def items(self) :
        '''
        D.items() -> a set-like object providing a view on D's items
        '''

    # def __len__(self) :
        '''
        Return len(self).
        '''

    def len(self) :
        return len(self)

    def __setattr__(self, key, value) :
        '''Implement setattr(self, name, value).'''
        self.__setitem__(key, value)
        return value

    def __setitem__(self, key, value) :
        '''Set self[key] to value.'''
        from DataModel.List import List
        if type(value) is list :
            dict.__setitem__(self, key, List(value))
        elif type(value) is dict :
            dict.__setitem__(self, key, Dict(value))
        else :
            dict.__setitem__(self, key, value)
        return value

    # def setdefault(self) :
        '''
        D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D
        '''

    def set(self, key_list, value) :
        if type(key_list) is str :
            self[key_list] = value
        elif type(key_list) is list :
            now = self
            for index, key in enumerate(key_list) :
                if key in now :
                    now = now[key]
                else :
                    if index < len(key_list) - 1 :
                        now[key] = Dict()
                        now = now[key]
                    else :
                        now[key] = value
        else : raise Exception('Unexpected key_list: {}'.format(key_list))
        return self

    def update(self, mapping, **args) :
        '''D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.
        If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]
        If E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v
        In either case, this is followed by: for k in F:  D[k] = F[k]'''
        if type(mapping) is dict :
            dict.update(self, Dict(mapping))
        elif type(mapping) is Dict :
            dict.update(self, mapping.data())
        else : raise Exception('Unexpected mapping: {}'.format(str(mapping)))
        if len(args) > 0 : dict.update(self, args)
        return self

    # def __contains__(self) :
        '''
        True if D has a key k, else False.
        '''

    def has(self, key_list) :
        if type(key_list) is str :
            return dict.__contains__(self, key_list)
        elif type(key_list) is list :
            now = self
            for key in key_list :
                if not dict.__contains__(now, key) : return False
                now = now[key]
            return True
        else :
            raise Exception('Unexpected key_list: {}'.format(str(key_list)))

    # def __getitem__(self) :
        '''
        x.__getitem__(y) <==> x[y]
        '''

    def get(self, key_list, default = None) :
        '''D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None.'''
        if type(key_list) is str :
            return dict.get(self, key_list, default)
        elif type(key_list) is list :
            if not self.has(key_list) :
                return default
            else :
                now = self
                for key in key_list :
                    now = now[key]
                return now
        else :
            raise Exception('Unexpected key_list: {}'.format(str(key_list)))

    # [ (key1,), (key2, None), key3 ]
    def getMulti(self, key_list, default = None) :
        if type(key_list) is list :
            result = Dict()
            for key in key_list :
                if type(key) is tuple :
                    if len(key) not in [1, 2] :
                        raise Exception('Unexpected key_list: {}'.format(str(key_list)))
                    elif len(key) == 1 :
                        if self.has(key[0]) : result[key[0]] = self[key[0]]
                    elif len(key) == 2 :
                        if self.has(key[0]) : result[key[0]] = self[key[0]]
                        else : result[key[0]] = key[1]
                elif type(key) is str :
                    result[key] = self[key]
                else : raise Exception('Unexpected key_list: {}'.format(str(key_list)))
            return result
        else :
            raise Exception('Unexpected key_list: {}'.format(str(key_list)))

    # def __getattribute__(self) :
        '''
        Return getattr(self, name).
        '''

    def __getattr__(self, key) :
        return self[key]

    # def pop(self, key) :
        '''
        D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
        If key is not found, d is returned if given, otherwise KeyError is raised
        '''
    
    # def popitem(self) :
        '''
        D.popitem() -> (k, v), remove and return some (key, value) pair as a
        2-tuple; but raise KeyError if D is empty.
        '''
    
    def clear(self) :
        '''D.clear() -> None.  Remove all items from D.'''
        dict.clear(self)
        return self
    
    def copy(self) :
        '''D.copy() -> a shallow copy of D'''
        return Dict(self)

    def __format__(self, code) :
        '''default object formatter'''
        return "{{{}}}".format((', ').join([ 
            '{} : {}'.format(
                '"{}"'.format(str(key)) if type(key) is str else str(key),
                format(self[key])
            )
            for key in self
        ])) 

    def __str__(self) :
        '''Return str(self).'''
        return 'Dict{{{}}}'.format(', '.join([ 
            '{} : {}'.format(
                '"{}"'.format(str(key)) if type(key) is str else str(key),
                str(self[key])
            )
            for key in self
        ]))
    
    # python2
    # '__class__', '__cmp__', '__contains__', '__delattr__', '__delitem__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'clear', 'copy', 'fromkeys', 'get', 'has_key', 'items', 'iteritems', 'iterkeys', 'itervalues', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values', 'viewitems', 'viewkeys', 'viewvalues'
    # 
    # python3
    # '__class__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'clear', 'copy', 'fromkeys', 'get', 'items', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values'

    # ===============================================================

    # def __class__(self) :
        '''
        dict() -> new empty dictionary
        dict(mapping) -> new dictionary initialized from a mapping object's
            (key, value) pairs
        dict(iterable) -> new dictionary initialized as if via:
            d = {}
            for k, v in iterable:
                d[k] = v
        dict(**kwargs) -> new dictionary initialized with the name=value pairs
            in the keyword argument list.  For example:  dict(one=1, two=2)
        '''

    # def __delattr__(self) :
        '''
        Implement delattr(self, name).
        '''

    # def __delitem__(self) :
        '''
        Delete self[key].
        '''

    # def __dir__(self) :
        '''
        __dir__() -> list
        default dir() implementation
        '''

    # def __doc__(self) :
        '''
        str(object='') -> str
        str(bytes_or_buffer[, encoding[, errors]]) -> str

        Create a new string object from the given object. If encoding or
        errors is specified, then the object must expose a data buffer
        that will be decoded using the given encoding and error handler.
        Otherwise, returns the result of object.__str__() (if defined)
        or repr(object).
        encoding defaults to sys.getdefaultencoding().
        errors defaults to 'strict'.
        '''

    # def __eq__(self) :
        '''
        Return self==value.
        '''

    # def __ge__(self) :
        '''
        Return self>=value.
        '''

    # def __gt__(self) :
        '''
        Return self>value.
        '''

    # def __hash__(self) :
        '''
        None
        '''

    # def __init_subclass__(self) :
        '''
        This method is called when a class is subclassed.

        The default implementation does nothing. It may be
        overridden to extend subclasses.

        '''

    # def __iter__(self) :
        '''
        Implement iter(self).
        '''

    # def __le__(self) :
        '''
        Return self<=value.
        '''

    # def __lt__(self) :
        '''
        Return self<value.
        '''

    # def __ne__(self) :
        '''
        Return self!=value.
        '''

    # def __new__(self) :
        '''
        Create and return a new object.  See help(type) for accurate signature.
        '''

    # def __reduce__(self) :
        '''
        helper for pickle
        '''

    # def __reduce_ex__(self) :
        '''
        helper for pickle
        '''

    # def __repr__(self) :
        '''
        Return repr(self).
        '''

    # def __sizeof__(self) :
        '''
        D.__sizeof__() -> size of D in memory, in bytes
        '''

    # def __subclasshook__(self) :
        '''
        Abstract classes can override this to customize issubclass().

        This is invoked early on by abc.ABCMeta.__subclasscheck__().
        It should return True, False or NotImplemented.  If it returns
        NotImplemented, the normal algorithm is used.  Otherwise, it
        overrides the normal algorithm (and the outcome is cached).

        '''

if __name__ == '__main__':
    a = Dict({'1' : {2 : {'3' : ['4', '5', '6']}}, 'pop' : 11})
    # a = Dict({'1' : 2})
    a.set(['apple', 'peach'], {})
    # import json
    # print(json.dumps(a.items()))
    # print(a.items())
    print('{}'.format(a))
    print(a)

    # print(json.dumps(a))
    # print('apple{0:\n},{1:a}'.format(a, a))
    # print(a)
    # print(type(a))
    # print(a[1])
    # print(type(a[1][2][3]))

