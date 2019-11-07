# -*- coding: utf-8 -*-  
import sys, os; sys.path.append(os.path.realpath(__file__ + '/../'));

class List(list) :

    def _wrapItem(self, item) :
        if type(item) is list :
            return List(item)
        elif type(item) is dict :
            from Dict import Dict
            return Dict(item)
        elif type(item) is str :
            from Str import Str
            return Str(item)
        elif type(item) is bytes :
            from Str import Str
            return Str(item.decode())
        else :
            return item

    def __init__(self, *args) :
        '''Initialize self.  See help(type(self)) for accurate signature.'''
        if len(args) == 0 :
            raw_item_list = []
        elif len(args) == 1 :
            if type(args[0]) is list :
                raw_item_list = args[0]
            elif type(args[0]) is range :
                raw_item_list = list(args[0])
            elif isinstance(args[0], List) :
                list.__init__(self, args[0].getData())
                return
            else :
                raw_item_list = args
        else :
            raw_item_list = args
        item_list = []
        for item in raw_item_list :
            item_list.append(self._wrapItem(item))
        list.__init__(self, item_list)

    def getId(self) :
        '''id(object) -> integer
        Return the identity of an object.  This is guaranteed to be unique among
        simultaneously existing objects.  (Hint: it's the object's memory address.)'''
        return hex(id(self))
    
    def getData(self) :
        return [ item for item in self ]

    def getRaw(self) :
        from Dict import Dict
        from Str import Str
        return [ item.getRaw() if isinstance(item, ( List, Dict, Str )) else item for item in self ]

    def copy(self) :
        '''L.copy() -> list -- a shallow copy of L'''
        return List(self)

    def j(self) :
        from util import j
        return j(self.getRaw())

    def __format__(self, code) :
        '''default object formatter'''
        return '[{}]'.format(
            self.copy()\
                .map(lambda item, index : '"{}"'.format(item) if isinstance(item, str) else '{}'.format(item))\
                .join(', ')
        )

    def __str__(self) :
        '''Return str(self).'''
        return 'List[{}]'.format(
            self.copy()\
                .map(lambda item, index : '"{}"'.format(item) if isinstance(item, str) else str(item))\
                .join(', ')
        )

    def inspect(self) :
        pass

    # def __len__(self) :
        '''
        Return len(self).
        '''

    def len(self) :
        return len(self)

    def empty(self) :
        return self.len() == 0

    # def __contains__(self, item) :
        '''
        'x.__contains__(y) <==> y in x'
        '''

    # def index(self, item, start = 0) :
        '''
        L.index(value, [start, [stop]]) -> integer -- return first index of value.
        Raises ValueError if the value is not present.
        '''

    # def count(self, item) :
        '''
        L.count(value) -> integer -- return number of occurrences of value
        '''

    # def __getattribute__(self) :
        '''
        Return getattr(self, name).
        '''

    # def __getattr__(self, index) :
        '''
        getattr(object, name[, default]) -> value
        
        Get a named attribute from an object; getattr(x, 'y') is equivalent to x.y.
        When a default argument is given, it is returned when the attribute doesn't
        exist; without it, an exception is raised in that case.
        '''

    def __getitem__(self, index) :
        '''x.__getitem__(y) <==> x[y]'''
        if isinstance(index, int) : return list.__getitem__(self, index)
        elif isinstance(index, slice) : return List(list.__getitem__(self, index))
        else : raise Exception('Unexpected index: {}'.format(index))

    # def __setattr__(self) :
        '''
        Implement setattr(self, name, value).
        
        Sets the named attribute on the given object to the specified value.
        setattr(x, 'y', v) is equivalent to ``x.y = v''
        '''

    def __setitem__(self, index, item) :
        '''Set self[index] to value.'''
        list.__setitem__(self, index, self._wrapItem(item))
        return item

    def set(self, index, item) :
        self.__setitem__(index, item)
        return self

    def append(self, item) :
        '''L.append(object) -> None -- append object to end'''
        '''IN PLACE'''
        list.append(self, self._wrapItem(item))
        return self

    def insert(self, index, item) :
        '''L.insert(index, object) -> None -- insert object before index'''
        '''IN PLACE'''
        list.insert(self, index, self._wrapItem(item))
        return self

    def __add__(self, item_list) :
        '''Return self+value.'''
        '''NOT IN PLACE'''
        if isinstance(item_list, list) :
            return List(list.__add__(self, self._wrapItem(item_list)))
        else :
            raise Exception('Unexpected item_list: {}'.format(item_list))

    def __iadd__(self, item_list) :
        '''Implement self+=value.'''
        '''IN PLACE'''
        if isinstance(item_list, list) :
            return list.__iadd__(self, self._wrapItem(item_list))
        else :
            raise Exception('Unexpected item_list: {}'.format(item_list))
    
    def extend(self, item_list) :
        '''L.extend(iterable) -> None -- extend list by appending elements from the iterable'''
        '''IN PLACE'''
        if isinstance(item_list, list) :
            list.extend(self, self._wrapItem(item_list))
        else : raise Exception('Unexpected item_list: {}'.format(item_list))
        return self

    # def pop(self, index) :
        '''
        L.pop([index]) -> item -- remove and return item at index (default last).
        Raises IndexError if list is empty or index is out of range.
        '''
        '''IN PLACE'''

    def remove(self, item) :
        '''L.remove(value) -> None -- remove first occurrence of value.
        Raises ValueError if the value is not present.'''
        '''IN PLACE'''
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

    def sort(self, key_func = None, reverse = False) :
        '''L.sort(key_func=None, reverse=False) -> None -- stable sort *IN PLACE*'''
        '''IN PLACE'''
        list.sort(self, key = key_func, reverse = reverse)
        return self

    def batch(self, func_name, *args) :
        '''IN PLACE'''
        if not isinstance(func_name, str) :
            raise Exception('Unexpected func_name: {}'.format(func_name))
        for index, item in enumerate(self) :
            attribute = self[index].__getattribute__(func_name)
            if callable(attribute) : self[index] = attribute(*args)
            else : self[index] = attribute
        return self

    def map(self, func, *args) :
        '''IN PLACE'''
        for index, item in enumerate(self) :
            self[index] = func(item, index, *args)
        return self

    def enumerate(self) :
        return enumerate(self)

    def filter(self, func_or_func_name, *args) :
        '''IN PLACE'''
        index = 0
        if isinstance(func_or_func_name, str) :
            while index < self.len() :
                if self[index].__getattribute__(func_or_func_name)(*args) : index += 1
                else : self.pop(index)
        else :
            while index < self.len() :
                if func_or_func_name(self[index], *args) : index += 1
                else : self.pop(index)
        return self

    def reduce(self, func, initial_value, *args) :
        result = initial_value
        for index, item in enumerate(self) :
            try :
                result = func(result, item, index, *args)
            except Exception as e :
                print(self, result, item, index)
                raise e
        return result

    def _reduce(self, key_list_or_func_name, func, initial_value) :
        from List import List
        if key_list_or_func_name is None :
            return self.reduce(func, initial_value)
        elif isinstance(key_list_or_func_name, list) :
            if self.len() == 0 : return initial_value
            from Object import Object
            if isinstance(self[0], Object) :
                return self.copy().batch('_get', key_list_or_func_name).reduce(func, initial_value)
            else :
                return self.copy().batch('get', key_list_or_func_name).reduce(func, initial_value)
        elif isinstance(key_list_or_func_name, str) :
            return self.copy().batch(key_list_or_func_name).reduce(func, initial_value)
        else : raise Exception('Unexpected key_list_or_func_name: {}'.format(key_list_or_func_name))

    def merge(self) :
        return self.reduce(lambda result, item, index : result.extend(item), List())

    def sum(self, key_list_or_func_name = None) :
        if self.len() == 0 : return 0
        def func(result, item, index, *args) :
            result += item
            return result
        return self._reduce(key_list_or_func_name, func, 0)

    def mean(self, key_list_or_func_name = None, default = None) :
        if self.len() == 0 : return default
        return 1.0 * self.sum(key_list_or_func_name) / self.len()

    def _initialValue(self, key_list_or_func_name) :
        from List import List
        if key_list_or_func_name is None :
            return self[0]
        elif isinstance(key_list_or_func_name, list) :
            from Object import Object
            if isinstance(self[0], Object) :
                return self[0]._get(key_list_or_func_name)
            else :
                return self[0].get(key_list_or_func_name)
        elif isinstance(key_list_or_func_name, str) :
            return self[0].__getattribute__(key_list_or_func_name)()
        else : raise Exception('Unexpected key_list_or_func_name: {}'.format(key_list_or_func_name))

    def max(self, key_list_or_func_name = None) :
        if self.len() == 0 : return None
        def func(result, item, index, *args) :
            if item > result : return item
            else : return result
        return self._reduce(key_list_or_func_name, func, self._initialValue(key_list_or_func_name))

    def min(self, key_list_or_func_name = None) :
        if self.len() == 0 : return None
        def func(result, item, index, *args) :
            if item < result : return item
            else : return result
        return self._reduce(key_list_or_func_name, func, self._initialValue(key_list_or_func_name))

    def join(self, sep) :
        from Str import Str
        if not isinstance(sep, str) :
            raise Exception('Unexpected type of sep: {}'.format(sep))
        return Str(sep).join(self)

    def strip(self, string = ' \t\n') :
        '''IN PLACE'''
        from Dict import Dict
        from Str import Str
        index = 0
        while index < self.len() :
            if type(self[index]) in [ List, Dict, Str ] :
                self[index].strip()
            elif type(self[index]) == tuple :
                self[index] = (strip(datum, chars, encoding) for item in self[index])
            elif type(self[index]) == set :
                self[index] = set([strip(datum, chars, encoding) for datum in data])
            index += 1






        return self

    def unique(self) :
        '''IN PLACE'''
        '''O(N^2)'''
        index = 0
        while index < self.len() :
        # __eq__
            if self.count(self[index]) == 1 : index += 1
            else : self.pop(index)
        return self

    def union(self, item_list) :
        '''Update a set with the union of itself and others.'''
        '''IN PLACE'''
        raise

    def difference(self, item_list) :
        '''Remove all elements of another list from this list.'''
        '''IN PLACE'''
        raise

    def intersection(self, item_list) :
        '''Update itself with the intersection of itself and another.'''
        '''IN PLACE'''
        raise

    def isDisjointFrom(self, item_list) :
        '''Return True if two lists have a null intersection.'''
        raise

    def isSubsetOf(self, item_list) :
        '''Report whether another set contains this set.'''
        raise

    def isSupersetOf(self, item_list) :
        '''Report whether this set contains another set.'''
        raise

    def flatten(self) :
        raise

    def bisect(self) :
        raise

    def clear(self) :
        '''L.clear() -> None -- remove all items from L'''
        '''IN PLACE'''
        list.clear(self)
        return self
    
    def writeToFile(self, file) :
        file.write(self.j())
        return self

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

        Deletes the named attribute from the given object.

        delattr(x, 'y') is equivalent to ``del x.y''
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
        
        iter(iterable) -> iterator
        iter(callable, sentinel) -> iterator

        Get an iterator from an object.  In the first form, the argument must
        supply its own iterator, or be a sequence.
        In the second form, the callable is called until it returns the sentinel.
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
