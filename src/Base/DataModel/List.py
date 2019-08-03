# -*- coding: utf-8 -*-  

class List(list) :

    def __init__(self, *args) :
        '''Initialize self.  See help(type(self)) for accurate signature.'''
        if len(args) == 0 :
            raw_item_list = []
        elif len(args) == 1 :
                list.__init__(self, args[0].data())
            if isinstance(args[0], List) :
                return
            elif type(args[0]) is list :
                raw_item_list = args[0]
            else :
                raw_item_list = args
        else :
            raw_item_list = args
        item_list = []
        for item in raw_item_list :
            if type(item) is list :
                item_list.append(List(item))
            elif type(item) is dict :
                from DataModel.Dict import Dict
                item_list.append(Dict(item))
            else :
                item_list.append(item)
        list.__init__(self, item_list)

    def data(self) :
        return [ item for item in self ]

    def raw(self) :
        from DataModel.Dict import Dict
        return [ item.raw() if type(item) in [ List, Dict ] else item for item in self ]
    
    # def __len__(self) :
        '''
        Return len(self).
        '''

    def len(self) :
        return len(self)

    # def __contains__(self) :
        '''
        'x.__contains__(y) <==> y in x'
        '''

    # def index(self, item) :
        '''
        L.index(value, [start, [stop]]) -> integer -- return first index of value.
        Raises ValueError if the value is not present.
        '''

    # def count(self, item) :
        '''
        L.count(value) -> integer -- return number of occurrences of value
        '''

    def __setitem__(self, key, value) :
        '''Set self[key] to value.'''
        from DataModel.Dict import Dict
        if type(value) is list :
            list.__setitem__(self, key, List(value))
        elif type(value) is dict :
            list.__setitem__(self, key, Dict(value))
        else :
            list.__setitem__(self, key, value)
        return value

    def set(self, key, value) :
        self.__setitem__(key, value)
        return self

    # def __getitem__(self) :
        '''
        x.__getitem__(y) <==> x[y]
        '''

    def append(self, item) :
        '''L.append(object) -> None -- append object to end'''
        if type(item) is list :
            list.append(self, List(item))
        elif type(item) is dict :
            list.append(self, Dict(item))
        else :
            list.append(self, item)
        return self

    def insert(self, index, item) :
        '''L.insert(index, object) -> None -- insert object before index'''
        if type(item) is list :
            list.insert(self, index, List(item))
        elif type(item) is dict :
            list.insert(self, index, Dict(item))
        else :
            list.insert(self, index, item)
        return self

    def extend(self, item_list) :
        '''L.extend(iterable) -> None -- extend list by appending elements from the iterable'''
        '''IN PLACE'''
        if type(item_list) is list :
            list.extend(self, List(item_list))
        elif type(item_list) is List :
            list.extend(self, item_list)
        else : raise Exception('Unexpected item_list: {}'.format(item_list))
        return self

    def __add__(self, item_list) :
        '''Return self+value.'''
        if type(item_list) is list :
            return List(list.__add__(self, List(item_list)))
        elif type(item_list) is List :
            return List(list.__add__(self, item_list))
        else :
            raise Exception('Unexpected item_list: {}'.format(item_list))

    def __iadd__(self, item_list) :
        '''Implement self+=value.'''
        if type(item_list) is list :
            return list.__iadd__(self, List(item_list))
        elif type(item_list) is List :
            return list.__iadd__(self, item_list)
        else :
            raise Exception('Unexpected item_list: {}'.format(item_list))
    
    # def pop(self, index) :
        '''
        L.pop([index]) -> item -- remove and return item at index (default last).
        Raises IndexError if list is empty or index is out of range.
        '''

    def remove(self, item) :
        '''L.remove(value) -> None -- remove first occurrence of value.
        Raises ValueError if the value is not present.'''
        list.remove(self, item)
        return self
    
    # def __reversed__(self) :
        '''
        L.__reversed__() -- return a reverse iterator over the list
        '''

    def reverse(self) :
        '''L.reverse() -> None -- reverse *IN PLACE*'''
        '''IN PLACE'''
        list.reverse(self)
        return self

    def sort(self, key = None, reverse = False) :
        '''L.sort(key=None, reverse=False) -> None -- stable sort *IN PLACE*'''
        '''IN PLACE'''
        list.sort(self, key = key, reverse = reverse)
        return self

    def batch(self, func_name, *args) :
        '''IN PLACE'''
        for index, item in enumerate(self) :
            self[index] = self[index].__getattribute__(func_name)(*args)
        return self

    def map(self, func, *args) :
        '''IN PLACE'''
        for index, item in enumerate(self) :
            self[index] = func(item, index, *args)
        return self

    def enumerate(self) :
        return enumerate(self)

    def reduce(self, func, init, *args) :
        result = init
        for index, item in enumerate(self) :
            result = func(result, item, index, *args)
        return result

    def sum(self, key_list_or_func_name = None) :
        def func(result, item, index, *args) :
            result += item
            return result
        if key_list_or_func_name is None :
            return self.reduce(func, 0)
        elif type(key_list_or_func_name) is list :
            return self.copy().batch('get', key_list_or_func_name).reduce(func, 0)
        elif type(key_list_or_func_name) is str :
            return self.copy().batch(key_list_or_func_name).reduce(func, 0)
        else : raise Exception('Unexpected key_list: {}'.format(key_list))

    def filter(self, func_or_func_name, *args) :
        '''IN PLACE'''
        index = 0
        if type(func_or_func_name) is str :
            while index < len(self) :
                if self[index].__getattribute__(func_or_func_name)(*args) : index += 1
                else : self.pop(index)
        else :
            while index < len(self) :
                if func_or_func_name(self[index], *args) : index += 1
                else : self.pop(index)
        return self

    def join(self, string) :
        pass

    def clear(self) :
        '''L.clear() -> None -- remove all items from L'''
        list.clear(self)
        return self
    
    def copy(self) :
        '''L.copy() -> list -- a shallow copy of L'''
        return List(self)

    def j(self) :
        from util import j
        return j(self.raw())

    def __format__(self, code) :
        '''default object formatter'''
        return '[{}]'.format(', '.join([
            '"{}"'.format(str(item)) if type(item) is str else str(item)
            for item in self
        ]))

    def __str__(self) :
        '''Return str(self).'''
        return 'List[{}]'.format(', '.join([
            '"{}"'.format(str(item)) if type(item) is str else str(item)
            for item in self
        ]))

    # list(map(lambda x : print('\n{}\n{}\n'.format(x, list.__getattribute__([], x).__doc__)), dir(list)))

    # python2
    # '__add__', '__class__', '__contains__', '__delattr__', '__delitem__', '__delslice__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getslice__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__setslice__', '__sizeof__', '__str__', '__subclasshook__', 'append', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort'


    # python3
    # '__add__', '__class__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort'

    # ===============================================================

    # def __class__(self) :
        '''
        list() -> new empty list
        list(iterable) -> new list initialized from iterable's items
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

    # def __getattribute__(self) :
        '''
        Return getattr(self, name).
        '''

    # def __gt__(self) :
        '''
        Return self>value.
        '''

    # def __hash__(self) :
        '''
        None
        '''

    # def __imul__(self) :
        '''
        Implement self*=value.
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

    # def __mul__(self, value) :
        '''
        Return self*value
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

    # def __rmul__(self, value) :
        '''
        Return value*self.
        '''

    # def __setattr__(self) :
        '''
        Implement setattr(self, name, value).
        '''

    # def __sizeof__(self) :
        '''
        L.__sizeof__() -- size of L in memory, in bytes
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
    # a = List([[1,2],[3,4]])
    # a = List(List([5,4,3]), List(6,7,8,4))
    a = [1,2,3]
    # a = List([1,2,3])
    # a = List(1,2,3)
    # a = List(List())
    # b = List([4,5,6])
    b = List([4,5,6])
    print(type(a+b))
    print(a+b)
    print(a)
    print(b)
    a+=b
    print(a)
    print(b)
    exit()
    # b = List(a)
    # b.append(5)
    # c = b.filter(lambda x, i : x % 2 == 0)
    print('{0:\t}'.format(a))
    print(type(a))
    print(b)
    print(type(b))
    # print(c)
    # print(type(c))
    print(a is b)
    # print(b==c)
    # print(a==c)
    print(a.count(4))
