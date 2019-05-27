# -*- coding: utf-8 -*-  

class List(list) :

    def raw(self) :
        return [item.data() for item in self]

    def append(self, item) :
        list.append(self, Object(item))
        return self

    # def insert(self, item) :
        # list.insert(self, Object(item))
        # return self

    def extend(self, item_list) :
        list.extend(self, map(Object, item_list))
        return self

    # def pop(self, index) :
    #     return list.pop(self, index)
    
    # def remove(self, index) :
    #     return list.remove(self, index)
    
    def reverse(self) :
        list.reverse(self)
        return self

    # def sort(self) :
        # list.sort(self)
        # return self

    def map(self, func) :
        return List([ func(item, index) for index, item in enumerate(self) ])

    def filter(self, func) :
        return List([ item for index, item in enumerate(self) if func(item, index) ])

    def project(self, func) :
        pass

    def aggregate(self, func, ) :
        pass
        return self

    # def index(self, item) :
        # return list.index(list(map(str, self)), str(item))

    def count(self, item) :
        return list.count(list(map(str, self)), str(item))

    def clear(self) :
        list.clear(self)
        return self
    
    # def copy(self) :
        # return list.copy(self)

    # '__class__', '__contains__', '__delitem__', '__eq__', '__ne__', '__ge__', '__gt__', '__le__', '__lt__', '__getattribute__', '__hash__', '__iter__', '__len__', '__sizeof__', '__new__', '__reduce__', '__reduce_ex__', '__format__', '__repr__', '__str__', '__subclasshook__', 'fromkeys', 'setdefault', '__add__', '__iadd__', '__imul__', '__mul__', '__rmul__', '__reversed__', '__delslice__', '__getslice__', '__setslice__', '__cmp__', 'has_key', 'iterkeys', 'itervalues', 'iteritems', 'viewitems', 'viewkeys', 'viewvalues'

    # ===============================================================

    # def __add__(self) :
        '''
        Return self+value.
        '''

    # def __class__(self) :
        '''
        list() -> new empty list
        list(iterable) -> new list initialized from iterable's items
        '''

    # def __contains__(self) :
        '''
        Return key in self.
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

    # def __format__(self) :
        '''
        default object formatter
        '''

    # def __ge__(self) :
        '''
        Return self>=value.
        '''

    # def __getattribute__(self) :
        '''
        Return getattr(self, name).
        '''

    # def __getitem__(self) :
        '''
        x.__getitem__(y) <==> x[y]
        '''

    # def __gt__(self) :
        '''
        Return self>value.
        '''

    # def __hash__(self) :
        '''
        None
        '''

    # def __iadd__(self) :
        '''
        Implement self+=value.
        '''

    # def __imul__(self) :
        '''
        Implement self*=value.
        '''

    # def __init__(self) :
        '''
        Initialize self.  See help(type(self)) for accurate signature.
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

    # def __len__(self) :
        '''
        Return len(self).
        '''

    # def __lt__(self) :
        '''
        Return self<value.
        '''

    # def __mul__(self) :
        '''
        Return self*value.n
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

    # def __reversed__(self) :
        '''
        L.__reversed__() -- return a reverse iterator over the list
        '''

    # def __rmul__(self) :
        '''
        Return self*value.
        '''

    # def __setattr__(self) :
        '''
        Implement setattr(self, name, value).
        '''

    # def __setitem__(self) :
        '''
        Set self[key] to value.
        '''

    # def __sizeof__(self) :
        '''
        L.__sizeof__() -- size of L in memory, in bytes
        '''

    # def __str__(self) :
        '''
        Return str(self).
        '''

    # def __subclasshook__(self) :
        '''
        Abstract classes can override this to customize issubclass().

        This is invoked early on by abc.ABCMeta.__subclasscheck__().
        It should return True, False or NotImplemented.  If it returns
        NotImplemented, the normal algorithm is used.  Otherwise, it
        overrides the normal algorithm (and the outcome is cached).

        '''

    # def append(self) :
        '''
        L.append(object) -> None -- append object to end
        '''

    # def clear(self) :
        '''
        L.clear() -> None -- remove all items from L
        '''

    # def copy(self) :
        '''
        L.copy() -> list -- a shallow copy of L
        '''

    # def count(self) :
        '''
        L.count(value) -> integer -- return number of occurrences of value
        '''

    # def extend(self) :
        '''
        L.extend(iterable) -> None -- extend list by appending elements from the iterable
        '''

    # def index(self) :
        '''
        L.index(value, [start, [stop]]) -> integer -- return first index of value.
        Raises ValueError if the value is not present.
        '''

    # def insert(self) :
        '''
        L.insert(index, object) -- insert object before index
        '''

    # def pop(self) :
        '''
        L.pop([index]) -> item -- remove and return item at index (default last).
        Raises IndexError if list is empty or index is out of range.
        '''

    # def remove(self) :
        '''
        L.remove(value) -> None -- remove first occurrence of value.
        Raises ValueError if the value is not present.
        '''

    # def reverse(self) :
        '''
        L.reverse() -- reverse *IN PLACE*
        '''

    # def sort(self) :
        '''
        L.sort(key=None, reverse=False) -> None -- stable sort *IN PLACE*
        '''

if __name__ == '__main__':
    l = List([1,2,3,4])
    print(1 in l)
