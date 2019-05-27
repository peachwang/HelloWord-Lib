# -*- coding: utf-8 -*-  

class Data :

    def __init__(self, raw) :
        self._raw = raw

    def raw(self) :
        return self._raw

    # ===============================================================

    # def __class__(self) :
        '''
        The most base type
        '''

    # def __delattr__(self) :
        '''
        Implement delattr(self, name).
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

    # def __gt__(self) :
        '''
        Return self>value.
        '''

    # def __hash__(self) :
        '''
        Return hash(self).
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

    # def __setattr__(self) :
        '''
        Implement setattr(self, name, value).
        '''

    # def __sizeof__(self) :
        '''
        __sizeof__() -> int
        size of object in memory, in bytes
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

