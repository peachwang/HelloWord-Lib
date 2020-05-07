# -*- coding: utf-8 -*-  
from .Timer    import Timer
from abc       import ABCMeta, ABC, abstractmethod
from functools import wraps, total_ordering, cached_property as cached_prop; prop = property
from weakref   import WeakValueDictionary
from inspect   import isclass, signature

def print_func(func) :
    @wraps(func)
    def wrapper(self, *args, pattern = '{}', color = None, print_timing = False, **kwargs) :
        content, print_len = func(self, *args)
        content = pattern.format(content)
        if color is not None : content = color(content)
        if print_timing      : Timer.print_timing(content)
        else                 : print(content, **kwargs)
        if print_len         : self.print_len(color = color, **kwargs)
        return self
    return wrapper

def add_print_func(cls) :

    @print_func
    def print_format(self) : return self.__format__(''), False
    cls.print_format = print_format

    @print_func
    def print_str(self) : return self.__str__(), False
    cls.print_str = print_str

    def j(self, *, indent = True) : from ..app.Json import j; return j(self.json_serialize(), indent = indent)
    cls.j = j

    @print_func
    def print_j(self) : return self.j(), False
    cls.print_j = print_j

    return cls

def anti_duplicate_new(func) :
    @wraps(func)
    def wrapper(cls, *args, **kwargs) :
        key = func(cls, *args, **kwargs)
        if not hasattr(cls, '_instance_dict')      : cls._instance_dict = WeakValueDictionary()
        if cls._instance_dict.get(key) is not None : return cls._instance_dict[key]
        else                                       :
            if str(cls.__bases__[0].__new__)[ : -15] != str(func)[ : -15] : new_func = cls.__bases__[0].__new__
            else                                                          : new_func = cls.__bases__[0].__bases__[0].__new__
            instance = new_func(cls)
            cls._instance_dict[key] = instance
            return instance
    return wrapper

def anti_duplicate_init(func) :
    @wraps(func)
    def wrapper(self, *args, **kwargs) :
        if hasattr(self, '_has_init') : return
        func(self, *args, **kwargs)
        object.__setattr__(self, '_has_init', True)
    return wrapper

# =====================            ClassPropertyDescriptor                  =====================
# https://stackoverflow.com/questions/5189699/how-to-make-a-class-property
# https://stackoverflow.com/questions/3203286/how-to-create-a-read-only-class-property-in-python
# https://stackoverflow.com/questions/4037481/caching-class-attributes-in-python
class _ClassPropertyDescriptorBaseClass :

    def __init__(self, fget, name) : self.fget, self.fset, self.fdel, self.name, self.__doc__ = fget, None, None, name, fget.__doc__

    def getter(self, fget)  : self.fget = fget if isinstance(fget, (classmethod, staticmethod)) else classmethod(fget); return self

class _ClassPropertyDescriptor(_ClassPropertyDescriptorBaseClass) :
    
    def __get__(self, obj, klass = None) :
        # print(f'\n_ClassPropertyDescriptor.__get__({self = }, {obj = }, {klass = })')
        if self.fget is None : raise AttributeError(f'类属性 {self.name} 不可读')
        if klass is None : klass = type(obj)
        # print(f'self.fget.__get__(obj, klass)()')
        return self.fget.__get__(obj, klass)() # classmethod.__get__(obj, klass) -> def newfunc(*args): return classmethod.f(klass, *args)

    def __set__(self, obj_or_klass, value) :
        # print(f'\n_ClassPropertyDescriptor.__set__({self = }, {obj_or_klass = }, {value = })')
        if self.fset is None : raise AttributeError(f'类属性 {self.name} 不可写')
        if isclass(obj_or_klass) : obj, klass = None, obj_or_klass
        else                     : obj, klass = obj_or_klass, type(obj_or_klass)
        # print(f'self.fset.__get__(obj, klass)(value)')
        self.fset.__get__(obj, klass)(value)

    def __delete__(self, obj_or_klass) :
        # print(f'\n_ClassPropertyDescriptor.__delete__({self = }, {obj_or_klass = })')
        if self.fdel is None : raise AttributeError(f'类属性 {self.name} 不可删')
        if isclass(obj_or_klass) : obj, klass = None, obj_or_klass
        else                     : obj, klass = obj_or_klass, type(obj_or_klass)
        # print(f'self.fdel.__get__(obj, klass)()')
        self.fdel.__get__(obj, klass)()

    def setter(self, fset)  : self.fset = fset if isinstance(fset, (classmethod, staticmethod)) else classmethod(fset); return self

    def deleter(self, fdel) : self.fdel = fdel if isinstance(fdel, (classmethod, staticmethod)) else classmethod(fdel); return self

class _ClassCachedPropertyDescriptor(_ClassPropertyDescriptorBaseClass) :

    def __get__(self, obj, klass = None) :
        # print(f'\n_ClassCachedPropertyDescriptor.__get__({self = }, {obj = }, {klass = })')
        if self.fget is None : raise AttributeError(f'类缓存属性 {self.name} 不可读')
        if klass is None : klass = type(obj)
        value = self.fget.__get__(obj, klass)()
        # print(f'\n_ClassCachedPropertyDescriptor.__get__: {value = }')
        # print(f'{klass = }, {klass.__mro__ = }')
        # print(f'{type(klass) = }, {type(klass).__mro__ = }')

        # print(func := super().__setattr__, func.__qualname__, signature(func))
        # = super(_ClassCachedPropertyDescriptor, self)
        # <method-wrapper '__setattr__' of _ClassCachedPropertyDescriptor object at 0x106f143a0> object.__setattr__ (name, value, /)
        
        # print(func := super(SingularMetaClass).__setattr__, func.__qualname__, signature(func))
        # <method-wrapper '__setattr__' of super object at 0x106786b40> object.__setattr__ (name, value, /)
        
        # print(func := super(SingularBaseClass).__setattr__, func.__qualname__, signature(func))
        # <method-wrapper '__setattr__' of super object at 0x106ab4100> object.__setattr__ (name, value, /)
        
        # print(func := super(SingularMetaClass, klass).__setattr__, func.__qualname__, signature(func))
        # isinstance(klass, SingularMetaClass) => bound
        # <method-wrapper '__setattr__' of SingularMetaClass object at 0x7fe1170d8720> type.__setattr__ (name, value, /)
        
        # print(func := super(SingularBaseClass, klass).__setattr__, func.__qualname__, signature(func))
        # issubclass(klass, SingularBaseClass) => unbound
        # <slot wrapper '__setattr__' of 'object' objects> object.__setattr__ (self, name, value, /)
        
        # klass.__setattr__ is SingularMetaClass.__setattr__, which has been overridden
        # => __setattr__ of parent class of SingularMetaClass should be called to avoid recursion
        # ABCMeta.__mro__ = (ABCMeta, type, object)
        # ABC.__mro__     = (ABC, object)
        # Because: 1. klass is a instance of SingularMetaClass
        #          2. type(klass).__mro__ = (SingularMetaClass, ABCMeta, type, object)
        #          3. super(SingularMetaClass, klass) is bound
        # => super(SingularMetaClass, klass).__setattr__(self.name, value) = type.__setattr__(klass, self.name, value)
        # print(f'super(SingularMetaClass, klass).__setattr__(self.name, value)')
        super(SingularMetaClass, klass).__setattr__(self.name, value)
        return value

    def __set__(self, obj_or_klass, value) :
        if isclass(obj_or_klass) : obj, klass = None, obj_or_klass
        else                     : obj, klass = obj_or_klass, type(obj_or_klass)
        super(SingularMetaClass, klass).__setattr__(self.name, value)

    def __delete__(self, obj_or_klass)     :
        if isclass(obj_or_klass) : obj, klass = None, obj_or_klass
        else                     : obj, klass = obj_or_klass, type(obj_or_klass)
        super(SingularMetaClass, klass).__delattr__(self.name)

    def setter(self, fset)  : raise AttributeError(f'类缓存属性 {self.name} 不可设置 setter')

    def deleter(self, fdel) : raise AttributeError(f'类缓存属性 {self.name} 不可设置 deleter')

def cls_prop(fget) :
    name = fget.__name__
    if not isinstance(fget, (classmethod, staticmethod)) : fget = classmethod(fget)
    return _ClassPropertyDescriptor(fget, name)

def cls_cached_prop(fget) :
    name = fget.__name__
    if not isinstance(fget, (classmethod, staticmethod)) : fget = classmethod(fget)
    return _ClassCachedPropertyDescriptor(fget, name)

# =====================            cached_property                          =====================
    # https://github.com/python/cpython/blob/3.8/Lib/functools.py#L925
    # _NOT_FOUND = object()
    # class cached_property:
        # computed once per instance, cached as attribute
        # 
        # def __init__(self, func):
        #     self.func = func
        #     self.attrname = None
        #     self.__doc__ = func.__doc__
        #     self.lock = RLock()

        # def __set_name__(self, owner, name):
        #     if self.attrname is None:
        #         self.attrname = name
        #     elif name != self.attrname:
        #         raise TypeError(
        #             "Cannot assign the same cached_property to two different names "
        #             f"({self.attrname!r} and {name!r})."
        #         )

        # def __get__(self, instance, owner=None):
        #     if instance is None:
        #         return self
        #     if self.attrname is None:
        #         raise TypeError(
        #             "Cannot use cached_property instance without calling __set_name__ on it.")
        #     try:
        #         cache = instance.__dict__
        #     except AttributeError:  # not all objects have __dict__ (e.g. class defines slots)
        #         msg = (
        #             f"No '__dict__' attribute on {type(instance).__name__!r} "
        #             f"instance to cache {self.attrname!r} property."
        #         )
        #         raise TypeError(msg) from None
        #     val = cache.get(self.attrname, _NOT_FOUND)
        #     if val is _NOT_FOUND:
        #         with self.lock:
        #             # check if another thread filled cache while we awaited lock
        #             val = cache.get(self.attrname, _NOT_FOUND)
        #             if val is _NOT_FOUND:
        #                 val = self.func(instance)
        #                 try:
        #                     cache[self.attrname] = val
        #                 except TypeError:
        #                     msg = (
        #                         f"The '__dict__' attribute on {type(instance).__name__!r} instance "
        #                         f"does not support item assignment for caching {self.attrname!r} property."
        #                     )
        #                     raise TypeError(msg) from None
        #     return val

# =====================            DynamicClassAttribute                    =====================
    # https://docs.python.org/3/library/types.html#types.DynamicClassAttribute
    # types.DynamicClassAttribute(fget=None, fset=None, fdel=None, doc=None)
        # Route attribute access on a class to __getattr__.

        # This is a descriptor, used to define attributes that act differently when accessed through an instance and through a class.
        # Instance access remains normal, but access to an attribute through a class will be routed to the class’s __getattr__ method;
        # this is done by raising AttributeError.

        # This allows one to have properties active on an instance, and have virtual attributes on the class with the same name (see Enum for an example).
        # 
        # def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        #     self.fget = fget
        #     self.fset = fset
        #     self.fdel = fdel
        #     # next two lines make DynamicClassAttribute act the same as property
        #     self.__doc__ = doc or fget.__doc__
        #     self.overwrite_doc = doc is None
        #     # support for abstract methods
        #     self.__isabstractmethod__ = bool(getattr(fget, '__isabstractmethod__', False))

        # def __get__(self, instance, ownerclass=None):
        #     if instance is None:
        #         if self.__isabstractmethod__:
        #             return self
        #         raise AttributeError()
        #     elif self.fget is None:
        #         raise AttributeError("unreadable attribute")
        #     return self.fget(instance)

# =====================            SingularClass                            =====================
# https://docs.python.org/3/library/abc.html
# https://www.python.org/dev/peps/pep-3115/
class SingularMetaClass(ABCMeta) :

    @classmethod
    def __prepare__(cls, name, bases, **kwds) :
        # Once the appropriate metaclass has been identified, then the class namespace is prepared.
        # If the metaclass has a __prepare__ attribute, it is called as namespace = metaclass.__prepare__(name, bases, **kwds)
        # (where the additional keyword arguments, if any, come from the class definition).
        # The __prepare__ method should be implemented as a classmethod().
        # The namespace returned by __prepare__ is passed in to __new__, but when the final class object is created the namespace is copied into a new dict.
        # If the metaclass has no __prepare__ attribute, then the class namespace is initialised as an empty ordered mapping.
        # 
        # def prepare_class(name, *bases, metaclass=None, **kwargs):
        #     if metaclass is None:
        #         metaclass = compute_default_metaclass(bases)
        #     prepare = getattr(metaclass, '__prepare__', None)
        #     if prepare is not None:
        #         return prepare(name, bases, **kwargs)
        #     else:
        #         return dict()
        return { '_class' : name }
    
    # class.mro(self)
        # This method can be overridden by a metaclass to customize the method resolution order for its instances.
        # It is called at class instantiation, and its result is stored in __mro__.
        # All classes created by metaclass contain this method, while instances of these classes do not.
    
    # The following methods are used to override the default behavior of the isinstance() and issubclass() built-in functions.
        # In particular, the metaclass abc.ABCMeta implements these methods in order to allow the addition of Abstract Base Classes (ABCs)
        # as “virtual base classes” to any class or type (including built-in types), including other ABCs.
    
        # class.__instancecheck__(self, instance)
            # Return true if instance should be considered a (direct or indirect) instance of class.
            # If defined, called to implement isinstance(instance, class).

        # class.__subclasscheck__(self, subclass)
            # Return true if subclass should be considered a (direct or indirect) subclass of class.
            # If defined, called to implement issubclass(subclass, class).
        
        # Note that these methods are looked up on the type (metaclass) of a class. They cannot be defined as class methods in the actual class.
        # This is consistent with the lookup of special methods that are called on instances, only in this case the instance is itself a class.

        # See also
        # PEP 3119 - Introducing Abstract Base Classes
        # Includes the specification for customizing isinstance() and issubclass() behavior through __instancecheck__() and __subclasscheck__(),
        # with motivation for this functionality in the context of adding Abstract Base Classes (see the abc module) to the language.
    
    # class.register(self, subclass)
        # Register subclass as a “virtual subclass” of this ABC.
        # Example:
        # class MyABC(ABC): pass
        # MyABC.register(tuple)
        # assert issubclass(tuple, MyABC)
        # assert isinstance((), MyABC)

    def __call__(self, *args, **kwargs) : raise Exception(f'类 {self} 不支持实例化')
    
    def __setattr__(self, name, value) :
        # print(f'\nSingularMetaClass.__setattr__({self = }, {name = }, {value = })')
        if name in ('__abstractmethods__', '_abc_impl') : type.__setattr__(self, name, value); return
        # print(f'{self = }, {self.__mro__ = }')
        # print(f'{self.__dict__.keys() = }, {self.__dict__.get(name) = }')
        # print(f'{self.__mro__[0].__dict__.keys() = }, {self.__mro__[0].__dict__.get(name) = }')
        for klass in self.__mro__ : # self = class instance of SingularMetaClass
            if issubclass(SingularBaseClass, klass) : break
            obj = klass.__dict__.get(name)
            # print(f'{klass = }, {obj = }')
            if obj is not None :
                if isinstance(obj, _ClassPropertyDescriptorBaseClass) : obj.__set__(self, value); return # 在 self 或 self 的基类中找到了属性描述器
        # print(f'super().__setattr__(name, value)')
        super().__setattr__(name, value) # 常规属性

    def __delattr__(self, name) :
        # print(f'\nSingularMetaClass.__delattr__({self = }, {name = })')
        for klass in self.__mro__ :
            if issubclass(SingularBaseClass, klass) : break
            obj = klass.__dict__.get(name)
            # print(f'{klass = }, {obj = }')
            if obj is not None :
                if isinstance(obj, _ClassPropertyDescriptorBaseClass) : obj.__delete__(self); return # 在 self 或 self 的基类中找到了属性描述器
                elif klass is self                                    :
                    # print(f'super().__delattr__(name)')
                    super().__delattr__(name); return # 删除已缓存在 self 中的类缓存属性的值
        # print(f'super().__delattr__(name)')
        super().__delattr__(name) # 常规属性

class SingularBaseClass(ABC, metaclass = SingularMetaClass) :

    # def __init_subclass__(cls, **kwargs) :
        # https://blog.yuo.be/2018/08/16/__init_subclass__-a-simpler-way-to-implement-class-registries-in-python/
        # https://www.python.org/dev/peps/pep-0487/
        # https://stackoverflow.com/questions/45400284/understanding-init-subclass
        # 
        # Whenever a class inherits from another class, __init_subclass__ is called on that class.
        # This way, it is possible to write classes which change the behavior of subclasses.
        # This is closely related to class decorators, but where class decorators only affect the specific class they’re applied to,
        # __init_subclass__ solely applies to future subclasses of the class defining the method.
        # 
        # This method is called whenever the containing class is subclassed. cls is then the new subclass.
        # If defined as a normal instance method, this method is implicitly converted to a class method.
        # Keyword arguments which are given to a new class are passed to the parent’s class __init_subclass__.
        # For compatibility with other classes using __init_subclass__, one should take out the needed keyword arguments and pass the others over to the base class, as in:
        # 
        # class Philosopher:
        # 
        #     @classmethod
        #     def __init_subclass__(cls, cls, /, default_name, **kwargs):
        #         super().__init_subclass__(**kwargs)
        #         cls.default_name = default_name

        # class AustralianPhilosopher(Philosopher, default_name="Bruce"):
        #     pass
        # 
        # The default implementation object.__init_subclass__ does nothing, but raises an error if it is called with any arguments.
        # 
        # Note: The metaclass hint metaclass is consumed by the rest of the type machinery, and is never passed to __init_subclass__ implementations.
        # The actual metaclass (rather than the explicit hint) can be accessed as type(cls).
        
        # print(f'\nSingularBaseClass.__init_subclass__({cls = })')
        # super().__init_subclass__(**kwargs)
        # from ..datatypes.Str import Str
        # super(SingularMetaClass, cls).__setattr__('_class', Str(cls).split('.')[-1][ : -2])

    # @classmethod
    # class.__subclasshook__(cls, subclass) :
        # Abstract classes can override this to customize issubclass().
        # Check whether subclass is considered a subclass of this ABC.
        # This means that you can customize the behavior of issubclass further without the need to call register() on every class you want to consider a subclass of the ABC.
        # This class method is called from the __subclasscheck__() method of the ABC.
        # This method should return True, False or NotImplemented.
        # If it returns True, the subclass is considered a subclass of this ABC.
        # If it returns False, the subclass is not considered a subclass of this ABC, even if it would normally be one.
        # If it returns NotImplemented, the subclass check is continued with the usual mechanism.
        # For a demonstration of these concepts, look at this example ABC definition:
        # 
        # class Foo:
        #     
        #     def __getitem__(self, index):
        #         ...
        #     
        #     def __len__(self):
        #         ...
        #     
        #     def get_iterator(self):
        #         return iter(self)
        # 
        # class MyIterable(ABC):
        #     
        #     @abstractmethod
        #     def __iter__(self):
        #         while False:
        #             yield None
        #     
        #     def get_iterator(self):
        #         return self.__iter__()
        #     
        #     @classmethod
        #     def __subclasshook__(cls, C):
        #         if cls is MyIterable:
        #             if any("__iter__" in B.__dict__ for B in C.__mro__):
        #                 return True
        #         return NotImplemented
        # 
        # MyIterable.register(Foo)
        # 
        # The ABC MyIterable defines the standard iterable method, __iter__(), as an abstract method. The implementation given here can still be called from subclasses.
        # The get_iterator() method is also part of the MyIterable abstract base class, but it does not have to be overridden in non-abstract derived classes.
        # The __subclasshook__() class method defined here says that any class that has an __iter__() method in its __dict__
        # (or in that of one of its base classes, accessed via the __mro__ list) is considered a MyIterable too.
        # Finally, the last line makes Foo a virtual subclass of MyIterable, even though it does not define an __iter__() method
        # (it uses the old-style iterable protocol, defined in terms of __len__() and __getitem__()).
        # Note that this will not make get_iterator available as a method of Foo, so it is provided separately.

    pass

# =====================            Special Attributes                       =====================
    # https://docs.python.org/3/library/stdtypes.html

    # The implementation adds a few special read-only attributes to several object types, where they are relevant.
    # Some of these are not reported by the dir() built-in function.

    # definition.__name__
        # The name of the class, function, method, descriptor, or generator instance.

    # definition.__qualname__
        # The qualified name of the class, function, method, descriptor, or generator instance.

    # object.__dict__
        # A dictionary or other mapping object used to store an object’s (writable) attributes.

    # object.__sizeof__
        # Size of object in memory, in bytes.

    # instance.__class__
        # The class to which a class instance belongs.

    # class.__base__
        # The immediate base class of a class object.

    # class.__bases__
        # The tuple of base classes of a class object.

    # class.__mro__
        # This attribute is a tuple of classes that are considered when looking for base classes during method resolution.

    # class.__subclasses__(self)
        # Each class keeps a list of weak references to its immediate subclasses. This method returns a list of all those references still alive.
        # Example:
        # >>> int.__subclasses__()
        # [<class 'bool'>]

# =====================            Built-in Functions                       =====================
    # https://docs.python.org/3/library/functions.html
    # https://docs.python.org/3/howto/descriptor.html

    # Functions and Methods
        # Python’s object oriented features are built upon a function based environment. Using non-data descriptors, the two are merged seamlessly.

        # Class dictionaries store methods as functions. In a class definition, methods are written using def or lambda, the usual tools for creating functions.
        # Methods only differ from regular functions in that the first argument is reserved for the object instance.
        # By Python convention, the instance reference is called self but may be called this or any other variable name.

        # To support method calls, functions include the __get__() method for binding methods during attribute access.
        # This means that all functions are non-data descriptors which return bound methods when they are invoked from an object.
        # In pure Python, it works like this:

        # class Function(object):
        #     . . .
        #     def __get__(self, obj, objtype=None):
        #         "Simulate func_descr_get() in Objects/funcobject.c"
        #         if obj is None:
        #             return self
        #         return types.MethodType(self, obj)
        
        # Running the interpreter shows how the function descriptor works in practice:

        # >>>
        # >>> class D(object):
        # ...     def f(self, x):
        # ...         return x
        # ...
        # >>> d = D()

        # Access through the class dictionary does not invoke __get__.
        # It just returns the underlying function object.
        # >>> D.__dict__['f']
        # <function D.f at 0x00C45070>

        # Dotted access from a class calls __get__() which just returns the underlying function unchanged.
        # >>> D.f
        # <function D.f at 0x00C45070>

        # The function has a __qualname__ attribute to support introspection
        # >>> D.f.__qualname__
        # 'D.f'

        # Dotted access from an instance calls __get__() which returns the function wrapped in a bound method object
        # >>> d.f
        # <bound method D.f of <__main__.D object at 0x00B18C90>>

        # Internally, the bound method stores the underlying function, the bound instance, and the class of the bound instance.
        # >>> d.f.__func__
        # <function D.f at 0x1012e5ae8>
        # >>> d.f.__self__
        # <__main__.D object at 0x1012e1f98>
        # >>> d.f.__class__
        # <class 'method'>

    # class property(fget=None, fset=None, fdel=None, doc=None)
        # Return a property attribute.

        # fget is a function for getting an attribute value.
        # fset is a function for setting an attribute value.
        # fdel is a function for deleting an attribute value.
        # And doc creates a docstring for the attribute.

        # A typical use is to define a managed attribute x:

        # class C:
        #     def __init__(self):
        #         self._x = None

        #     def getx(self):
        #         return self._x

        #     def setx(self, value):
        #         self._x = value

        #     def delx(self):
        #         del self._x

        #     x = property(getx, setx, delx, "I'm the 'x' property.")
        
        # If c is an instance of C, c.x will invoke the getter, c.x = value will invoke the setter and del c.x the deleter.

        # If given, doc will be the docstring of the property attribute. Otherwise, the property will copy fget’s docstring (if it exists).
        # This makes it possible to create read-only properties easily using property() as a decorator:

        # class Parrot:
        #     def __init__(self):
        #         self._voltage = 100000

        #     @property
        #     def voltage(self):
        #         """Get the current voltage."""
        #         return self._voltage
        
        # The @property decorator turns the voltage() method into a “getter” for a read-only attribute with the same name,
        # and it sets the docstring for voltage to “Get the current voltage.”

        # A property object has getter, setter, and deleter methods usable as decorators that create a copy of the property
        # with the corresponding accessor function set to the decorated function.
        # This is best explained with an example:

        # class C:
        #     def __init__(self):
        #         self._x = None

        #     @property
        #     def x(self):
        #         """I'm the 'x' property."""
        #         return self._x

        #     @x.setter
        #     def x(self, value):
        #         self._x = value

        #     @x.deleter
        #     def x(self):
        #         del self._x
        # This code is exactly equivalent to the first example. Be sure to give the additional functions the same name as the original property (x in this case.)

        # The returned property object also has the attributes fget, fset, and fdel corresponding to the constructor arguments.

        # Changed in version 3.5: The docstrings of property objects are now writeable.

        # To see how property() is implemented in terms of the descriptor protocol, here is a pure Python equivalent:

        # class Property(object):
        #     "Emulate PyProperty_Type() in Objects/descrobject.c"

        #     def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        #         self.fget = fget
        #         self.fset = fset
        #         self.fdel = fdel
        #         if doc is None and fget is not None:
        #             doc = fget.__doc__
        #         self.__doc__ = doc

        #     def __get__(self, obj, objtype=None):
        #         if obj is None:
        #             return self
        #         if self.fget is None:
        #             raise AttributeError("unreadable attribute")
        #         return self.fget(obj)

        #     def __set__(self, obj, value):
        #         if self.fset is None:
        #             raise AttributeError("can't set attribute")
        #         self.fset(obj, value)

        #     def __delete__(self, obj):
        #         if self.fdel is None:
        #             raise AttributeError("can't delete attribute")
        #         self.fdel(obj)

        #     def getter(self, fget):
        #         return type(self)(fget, self.fset, self.fdel, self.__doc__)

        #     def setter(self, fset):
        #         return type(self)(self.fget, fset, self.fdel, self.__doc__)

        #     def deleter(self, fdel):
        #         return type(self)(self.fget, self.fset, fdel, self.__doc__)
        
        # The property() builtin helps whenever a user interface has granted attribute access and then subsequent changes require the intervention of a method.

        # For instance, a spreadsheet class may grant access to a cell value through Cell('b10').value.
        # Subsequent improvements to the program require the cell to be recalculated on every access;
        # however, the programmer does not want to affect existing client code accessing the attribute directly.
        # The solution is to wrap access to the value attribute in a property data descriptor:

        # class Cell(object):
        #     . . .
        #     def getvalue(self):
        #         "Recalculate the cell before returning value"
        #         self.recalc()
        #         return self._value
        #     value = property(getvalue)

    # Static Methods and Class Methods
        # Non-data descriptors provide a simple mechanism for variations on the usual patterns of binding functions into methods.

        # To recap, functions have a __get__() method so that they can be converted to a method when accessed as attributes.
        # The non-data descriptor transforms an obj.f(*args) call into f(obj, *args). Calling klass.f(*args) becomes f(*args).

        # This chart summarizes the binding and its two most useful variants:

        # Transformation        Called from an Object       Called from a Class
        # function              f(obj, *args)               f(*args)
        # staticmethod          f(*args)                    f(*args)
        # classmethod           f(type(obj), *args)         f(klass, *args)

    # class staticmethod :
        # Transform a method into a static method.

        # A static method does not receive an implicit first argument. To declare a static method, use this idiom:

        # class C:
        #     @staticmethod
        #     def f(arg1, arg2, ...): ...

        # The @staticmethod form is a function decorator – see Function definitions for details.

        # A static method can be called either on the class (such as C.f()) or on an instance (such as C().f()).

        # Static methods in Python are similar to those found in Java or C++. Also see classmethod() for a variant that is useful for creating alternate class constructors.

        # Like all decorators, it is also possible to call staticmethod as a regular function and do something with its result.
        # This is needed in some cases where you need a reference to a function from a class body and you want to avoid the automatic transformation to instance method.
        # For these cases, use this idiom:

        # class C:
        #     builtin_open = staticmethod(open)

        # For more information on static methods, see The standard type hierarchy.
        
        # Static methods return the underlying function without changes.
        # Calling either c.f or C.f is the equivalent of a direct lookup into object.__getattribute__(c, "f") or object.__getattribute__(C, "f").
        # As a result, the function becomes identically accessible from either an object or a class.

        # Good candidates for static methods are methods that do not reference the self variable.

        # For instance, a statistics package may include a container class for experimental data.
        # The class provides normal methods for computing the average, mean, median, and other descriptive statistics that depend on the data.
        # However, there may be useful functions which are conceptually related but do not depend on the data.
        # For instance, erf(x) is handy conversion routine that comes up in statistical work but does not directly depend on a particular dataset.
        # It can be called either from an object or the class: s.erf(1.5) --> .9332 or Sample.erf(1.5) --> .9332.

        # Since staticmethods return the underlying function with no changes, the example calls are unexciting:

        # >>> class E(object):
        # ...     def f(x):
        # ...         print(x)
        # ...     f = staticmethod(f)
        # ...
        # >>> E.f(3)
        # 3
        # >>> E().f(3)
        # 3
        
        # Using the non-data descriptor protocol, a pure Python version of staticmethod() would look like this:
        
        # class StaticMethod(object):
        #     "Emulate PyStaticMethod_Type() in Objects/funcobject.c"

        #     def __init__(self, f):
        #         self.f = f

        #     def __get__(self, obj, objtype=None):
        #         return self.f

    # class classmethod :
        # Transform a method into a class method.
        
        # A class method receives the class as implicit first argument, just like an instance method receives the instance. To declare a class method, use this idiom:
        
        # class C:
        #     @classmethod
        #     def f(cls, arg1, arg2, ...): ...
        
        # The @classmethod form is a function decorator – see Function definitions for details.
        
        # A class method can be called either on the class (such as C.f()) or on an instance (such as C().f()). The instance is ignored except for its class.
        # If a class method is called for a derived class, the derived class object is passed as the implied first argument.
        
        # Class methods are different than C++ or Java static methods. If you want those, see staticmethod().
        
        # For more information on class methods, see The standard type hierarchy.
        
        # Unlike static methods, class methods prepend the class reference to the argument list before calling the function.
        # This format is the same for whether the caller is an object or a class:

        # >>> class E(object):
        # ...     def f(klass, x):
        # ...         return klass.__name__, x
        # ...     f = classmethod(f)
        # ...
        # >>> print(E.f(3))
        # ('E', 3)
        # >>> print(E().f(3))
        # ('E', 3)
        
        # This behavior is useful whenever the function only needs to have a class reference and does not care about any underlying data.
        # One use for classmethods is to create alternate class constructors. In Python 2.3, the classmethod dict.fromkeys() creates a new dictionary from a list of keys.
        # The pure Python equivalent is:

        # class Dict(object):
        #     . . .
        #     def fromkeys(klass, iterable, value=None):
        #         "Emulate dict_fromkeys() in Objects/dictobject.c"
        #         d = klass()
        #         for key in iterable:
        #             d[key] = value
        #         return d
        #     fromkeys = classmethod(fromkeys)
        
        # Now a new dictionary of unique keys can be constructed like this:

        # >>> Dict.fromkeys('abracadabra')
        # {'a': None, 'r': None, 'b': None, 'c': None, 'd': None}
        
        # Using the non-data descriptor protocol, a pure Python version of classmethod() would look like this:
        
        # class ClassMethod(object):
        #     "Emulate PyClassMethod_Type() in Objects/funcobject.c"

        #     def __init__(self, f):
        #         self.f = f

        #     def __get__(self, obj, klass=None):
        #         if klass is None:
        #             klass = type(obj)
        #         def newfunc(*args):
        #             return self.f(klass, *args)
        #         return newfunc

    # class type(object)
    # class type(name, bases, dict)
        # With one argument, return the type of an object. The return value is a type object and generally the same object as returned by object.__class__.
        
        # The isinstance() built-in function is recommended for testing the type of an object, because it takes subclasses into account.
        
        # With three arguments, return a new type object. This is essentially a dynamic form of the class statement.
        # The name string is the class name and becomes the __name__ attribute;
        # the bases tuple itemizes the base classes and becomes the __bases__ attribute;
        # and the dict dictionary is the namespace containing definitions for class body and is copied to a standard dictionary to become the __dict__ attribute.
        # For example, the following two statements create identical type objects:

        # >>>
        # class X:
        #     a = 1

        # X = type('X', (object,), dict(a=1))
        # See also Type Objects.

        # Changed in version 3.6: Subclasses of type which don’t override type.__new__ may no longer use the one-argument form to get the type of an object.

    # class object()
        # Return a new featureless object. object is a base for all classes. It has the methods that are common to all instances of Python classes.
        # This function does not accept any arguments.

        # Note: object does not have a __dict__, so you can’t assign arbitrary attributes to an instance of the object class.

    # isinstance(object, classinfo)
        # Return True if the object argument is an instance of the classinfo argument, or of a (direct, indirect or virtual) subclass thereof.
        # If object is not an object of the given type, the function always returns False.
        # If classinfo is a tuple of type objects (or recursively, other such tuples), return True if object is an instance of any of the types.
        # If classinfo is not a type or tuple of types and such tuples, a TypeError exception is raised.

    # issubclass(class, classinfo)
        # Return True if class is a subclass (direct, indirect or virtual) of classinfo.
        # A class is considered a subclass of itself.
        # classinfo may be a tuple of class objects, in which case every entry in classinfo will be checked.
        # In any other case, a TypeError exception is raised.

    # hasattr(object, name)
        # The arguments are an object and a string. The result is True if the string is the name of one of the object’s attributes, False if not.
        # (This is implemented by calling getattr(object, name) and seeing whether it raises an AttributeError or not.)

    # getattr(object, name[, default])
        # Return the value of the named attribute of object. name must be a string.
        # If the string is the name of one of the object’s attributes, the result is the value of that attribute.
        # For example, getattr(x, 'foobar') is equivalent to x.foobar.
        # If the named attribute does not exist, default is returned if provided, otherwise AttributeError is raised.

    # setattr(object, name, value)
        # This is the counterpart of getattr(). The arguments are an object, a string and an arbitrary value.
        # The string may name an existing attribute or a new attribute.
        # The function assigns the value to the attribute, provided the object allows it.
        # For example, setattr(x, 'foobar', 123) is equivalent to x.foobar = 123.

    # delattr(object, name)
        # This is a relative of setattr(). The arguments are an object and a string.
        # The string must be the name of one of the object’s attributes.
        # The function deletes the named attribute, provided the object allows it.
        # For example, delattr(x, 'foobar') is equivalent to del x.foobar.

    # https://www.python.org/dev/peps/pep-3135/
    # https://rhettinger.wordpress.com/2011/05/26/super-considered-super/
    # super([type[, object-or-type]])
        # Return a proxy object that delegates method calls to a parent or sibling class of type.
        # This is useful for accessing inherited methods that have been overridden in a class.
        # 
        # The object-or-type determines the method resolution order to be searched.
        # The search starts from the class right after the type.

        # For example, if __mro__ of object-or-type is D -> B -> C -> A -> object
        # and the value of type is B, then super() searches C -> A -> object.

        # The __mro__ attribute of the object-or-type lists the method resolution search order used by both getattr() and super().
        # The attribute is dynamic and can change whenever the inheritance hierarchy is updated.

        # If the second argument is omitted, the super object returned is unbound.
        # If the second argument is an object, isinstance(obj, type) must be true.
        # If the second argument is a type, issubclass(type2, type) must be true (this is useful for classmethods).

        # There are two typical use cases for super. In a class hierarchy with single inheritance,
        # super can be used to refer to parent classes without naming them explicitly, thus making the code more maintainable.
        # This use closely parallels the use of super in other programming languages.

        # The second use case is to support cooperative multiple inheritance in a dynamic execution environment.
        # This use case is unique to Python and is not found in statically compiled languages or languages that only support single inheritance.
        # This makes it possible to implement “diamond diagrams” where multiple base classes implement the same method.
        # Good design dictates that this method have the same calling signature in every case
        # (because the order of calls is determined at runtime, because that order adapts to changes in the class hierarchy,
        # and because that order can include sibling classes that are unknown prior to runtime).

        # For both use cases, a typical superclass call looks like this:

        # class C(B):
        #     def method(self, arg):
        #         super().method(arg)    # This does the same thing as:
        #                                # super(C, self).method(arg)

        # In addition to method lookups, super() also works for attribute lookups.
        # One possible use case for this is calling descriptors in a parent or sibling class.

        # Note that super() is implemented as part of the binding process for explicit dotted attribute lookups such as super().__getitem__(name).
        # It does so by implementing its own __getattribute__() method for searching classes in a predictable order that supports cooperative multiple inheritance.
        # Accordingly, super() is undefined for implicit lookups using statements or operators such as super()[name].

        # Also note that, aside from the zero argument form, super() is not limited to use inside methods.
        # The two argument form specifies the arguments exactly and makes the appropriate references.
        # The zero argument form only works inside a class definition, as the compiler fills in the necessary details to correctly retrieve the class being defined,
        # as well as accessing the current instance for ordinary methods.

        # For practical suggestions on how to design cooperative classes using super(), see guide to using super().

    # dir([object])
        # Without arguments, return the list of names in the current local scope.
        # With an argument, attempt to return a list of valid attributes for that object.

        # If the object has a method named __dir__(), this method will be called and must return the list of attributes.
        # This allows objects that implement a custom __getattr__() or __getattribute__() function to customize the way dir() reports their attributes.

        # If the object does not provide __dir__(), the function tries its best to gather information from the object’s __dict__ attribute,if defined, and from its type object.
        # The resulting list is not necessarily complete, and may be inaccurate when the object has a custom __getattr__().

        # The default dir() mechanism behaves differently with different types of objects, as it attempts to produce the most relevant, rather than complete, information:
        # If the object is a module object, the list contains the names of the module’s attributes.
        # If the object is a type or class object, the list contains the names of its attributes, and recursively of the attributes of its bases.
        # Otherwise, the list contains the object’s attributes’ names, the names of its class’s attributes, and recursively of the attributes of its class’s base classes.

        # The resulting list is sorted alphabetically. For example:

        # >>>
        # import struct
        # dir()   # show the names in the module namespace  
        # ['__builtins__', '__name__', 'struct']
        # dir(struct)   # show the names in the struct module 
        # ['Struct', '__all__', '__builtins__', '__cached__', '__doc__', '__file__',
        #  '__initializing__', '__loader__', '__name__', '__package__',
        #  '_clearcache', 'calcsize', 'error', 'pack', 'pack_into',
        #  'unpack', 'unpack_from']
        # class Shape:
        #     def __dir__(self):
        #         return ['area', 'perimeter', 'location']
        # s = Shape()
        # dir(s)
        # ['area', 'location', 'perimeter']
        # Note: Because dir() is supplied primarily as a convenience for use at an interactive prompt, it tries to supply an interesting set of names more than
        # it tries to supply a rigorously or consistently defined set of names, and its detailed behavior may change across releases.
        # For example, metaclass attributes are not in the result list when the argument is a class.

    # vars([object])
        # Return the __dict__ attribute for a module, class, instance, or any other object with a __dict__ attribute.

        # Objects such as modules and instances have an updateable __dict__ attribute;
        # however, other objects may have write restrictions on their __dict__ attributes
        # (for example, classes use a types.MappingProxyType to prevent direct dictionary updates).

        # Without an argument, vars() acts like locals(). Note, the locals dictionary is only useful for reads since updates to the locals dictionary are ignored.

# ===================== 3.3.       Special method names                     =====================
    # https://docs.python.org/3/reference/datamodel.html
    # 

# ===================== 3.3.1.     Basic customization                      =====================

    # object.__new__(cls[, ...])
        # Called to create a new instance of class cls.
        # __new__() is a static method (special-cased so you need not declare it as such)
        # that takes the class of which an instance was requested as its first argument.
        # The remaining arguments are those passed to the object constructor expression (the call to the class).
        # The return value of __new__() should be the new object instance (usually an instance of cls).

        # Typical implementations create a new instance of the class by invoking the superclass’s __new__() method
        # using super().__new__(cls[, ...]) with appropriate arguments
        # and then modifying the newly-created instance as necessary before returning it.

        # If __new__() is invoked during object construction and it returns an instance or subclass of cls,
        # then the new instance’s __init__() method will be invoked like __init__(self[, ...]),
        # where self is the new instance and the remaining arguments are the same as were passed to the object constructor.

        # If __new__() does not return an instance of cls, then the new instance’s __init__() method will not be invoked.

        # __new__() is intended mainly to allow subclasses of immutable types (like int, str, or tuple) to customize instance creation.
        # It is also commonly overridden in custom metaclasses in order to customize class creation.

    # object.__init__(self[, ...])
        # Called after the instance has been created (by __new__()), but before it is returned to the caller.
        # The arguments are those passed to the class constructor expression.
        # If a base class has an __init__() method, the derived class’s __init__() method, if any,
        # must explicitly call it to ensure proper initialization of the base class part of the instance;
        # for example: super().__init__([args...]).

        # Because __new__() and __init__() work together in constructing objects (__new__() to create it, and __init__() to customize it),
        # no non-None value may be returned by __init__(); doing so will cause a TypeError to be raised at runtime.

    # object.__del__(self)
        # Called when the instance is about to be destroyed. This is also called a finalizer or (improperly) a destructor.
        # If a base class has a __del__() method, the derived class’s __del__() method, if any,
        # must explicitly call it to ensure proper deletion of the base class part of the instance.

        # It is possible (though not recommended!) for the __del__() method to postpone destruction of the instance by creating a new reference to it.
        # This is called object resurrection. It is implementation-dependent whether __del__() is called a second time
        # when a resurrected object is about to be destroyed; the current CPython implementation only calls it once.

        # It is not guaranteed that __del__() methods are called for objects that still exist when the interpreter exits.

        # Note del x doesn’t directly call x.__del__() — the former decrements the reference count for x by one,
        # and the latter is only called when x’s reference count reaches zero.
        
        # CPython implementation detail: It is possible for a reference cycle to prevent the reference count of an object from going to zero.
        # In this case, the cycle will be later detected and deleted by the cyclic garbage collector.
        # A common cause of reference cycles is when an exception has been caught in a local variable.
        # The frame’s locals then reference the exception, which references its own traceback,
        # which references the locals of all frames caught in the traceback.

        # See also Documentation for the gc module.
        
        # Warning Due to the precarious circumstances under which __del__() methods are invoked,
        # exceptions that occur during their execution are ignored, and a warning is printed to sys.stderr instead.
        # In particular:
        # __del__() can be invoked when arbitrary code is being executed, including from any arbitrary thread.
        # If __del__() needs to take a lock or invoke any other blocking resource,
        # it may deadlock as the resource may already be taken by the code that gets interrupted to execute __del__().

        # __del__() can be executed during interpreter shutdown.
        # As a consequence, the global variables it needs to access (including other modules) may already have been deleted or set to None.
        # Python guarantees that globals whose name begins with a single underscore are deleted from their module before other globals are deleted;
        # if no other references to such globals exist, this may help in assuring that imported modules are still available at the time when the __del__() method is called.

    # object.__repr__(self)
        # Called by the repr() built-in function to compute the “official” string representation of an object.
        # If at all possible, this should look like a valid Python expression that could be used to recreate an object with the same value (given an appropriate environment).
        # If this is not possible, a string of the form <...some useful description...> should be returned. The return value must be a string object.
        # If a class defines __repr__() but not __str__(), then __repr__() is also used when an “informal” string representation of instances of that class is required.

        # This is typically used for debugging, so it is important that the representation is information-rich and unambiguous.

    # object.__str__(self)
        # Called by str(object) and the built-in functions format() and print() to compute the “informal” or nicely printable string representation of an object.
        # The return value must be a string object.

        # This method differs from object.__repr__() in that there is no expectation that __str__() return a valid Python expression:
        # a more convenient or concise representation can be used.

        # The default implementation defined by the built-in type object calls object.__repr__().

    # object.__bytes__(self)
        # Called by bytes to compute a byte-string representation of an object. This should return a bytes object.

    # object.__format__(self, format_spec)
        # Called by the format() built-in function, and by extension, evaluation of formatted string literals and the str.format() method,
        # to produce a “formatted” string representation of an object.
        # The format_spec argument is a string that contains a description of the formatting options desired.
        # The interpretation of the format_spec argument is up to the type implementing __format__(),
        # however most classes will either delegate formatting to one of the built-in types, or use a similar formatting option syntax.
        
        # See Format Specification Mini-Language for a description of the standard formatting syntax.
        
        # The return value must be a string object.

        # Changed in version 3.4: The __format__ method of object itself raises a TypeError if passed any non-empty string.
        # Changed in version 3.7: object.__format__(x, '') is now equivalent to str(x) rather than format(str(self), '').

    # object.__lt__(self, other)
    # object.__le__(self, other)
    # object.__eq__(self, other)
    # object.__ne__(self, other)
    # object.__gt__(self, other)
    # object.__ge__(self, other)
        # These are the so-called “rich comparison” methods. The correspondence between operator symbols and method names is as follows:
        # x<y calls x.__lt__(y), x<=y calls x.__le__(y), x==y calls x.__eq__(y), x!=y calls x.__ne__(y), x>y calls x.__gt__(y), and x>=y calls x.__ge__(y).

        # A rich comparison method may return the singleton NotImplemented if it does not implement the operation for a given pair of arguments.
        # By convention, False and True are returned for a successful comparison.
        # However, these methods can return any value, so if the comparison operator is used in a Boolean context (e.g., in the condition of an if statement),
        # Python will call bool() on the value to determine if the result is true or false.

        # By default, __ne__() delegates to __eq__() and inverts the result unless it is NotImplemented.
        # There are no other implied relationships among the comparison operators, for example, the truth of (x<y or x==y) does not imply x<=y.
        # To automatically generate ordering operations from a single root operation, see functools.total_ordering().

        # See the paragraph on __hash__() for some important notes on creating hashable objects which support custom comparison operations and are usable as dictionary keys.

        # There are no swapped-argument versions of these methods (to be used when the left argument does not support the operation but the right argument does); rather, __lt__() and __gt__() are each other’s reflection, __le__() and __ge__() are each other’s reflection, and __eq__() and __ne__() are their own reflection. If the operands are of different types, and right operand’s type is a direct or indirect subclass of the left operand’s type, the reflected method of the right operand has priority, otherwise the left operand’s method has priority. Virtual subclassing is not considered.

    # object.__hash__(self)
        # Called by built-in function hash() and for operations on members of hashed collections including set, frozenset, and dict.
        # __hash__() should return an integer. The only required property is that objects which compare equal have the same hash value;
        # it is advised to mix together the hash values of the components of the object that also play a part in comparison of objects by packing them into a tuple and hashing the tuple.
        # Example:
        # def __hash__(self):
        #     return hash((self.name, self.nick, self.color))
        
        # Note hash() truncates the value returned from an object’s custom __hash__() method to the size of a Py_ssize_t.
        # This is typically 8 bytes on 64-bit builds and 4 bytes on 32-bit builds.
        # If an object’s __hash__() must interoperate on builds of different bit sizes, be sure to check the width on all supported builds.
        # An easy way to do this is with python -c "import sys; print(sys.hash_info.width)".
        # If a class does not define an __eq__() method it should not define a __hash__() operation either;
        # if it defines __eq__() but not __hash__(), its instances will not be usable as items in hashable collections.
        # If a class defines mutable objects and implements an __eq__() method, it should not implement __hash__(),
        # since the implementation of hashable collections requires that a key’s hash value is immutable
        # (if the object’s hash value changes, it will be in the wrong hash bucket).

        # User-defined classes have __eq__() and __hash__() methods by default; with them, all objects compare unequal (except with themselves)
        # and x.__hash__() returns an appropriate value such that x == y implies both that x is y and hash(x) == hash(y).

        # A class that overrides __eq__() and does not define __hash__() will have its __hash__() implicitly set to None.
        # When the __hash__() method of a class is None, instances of the class will raise an appropriate TypeError when a program attempts to retrieve their hash value,
        # and will also be correctly identified as unhashable when checking isinstance(obj, collections.abc.Hashable).

        # If a class that overrides __eq__() needs to retain the implementation of __hash__() from a parent class,
        # the interpreter must be told this explicitly by setting __hash__ = <ParentClass>.__hash__.

        # If a class that does not override __eq__() wishes to suppress hash support, it should include __hash__ = None in the class definition.
        # A class which defines its own __hash__() that explicitly raises a TypeError would be incorrectly identified as hashable by an isinstance(obj, collections.abc.Hashable) call.

        # Note: By default, the __hash__() values of str and bytes objects are “salted” with an unpredictable random value.
        # Although they remain constant within an individual Python process, they are not predictable between repeated invocations of Python.
        # This is intended to provide protection against a denial-of-service caused by carefully-chosen inputs that exploit the worst case performance of a dict insertion, O(n^2) complexity.
        # See http://www.ocert.org/advisories/ocert-2011-003.html for details.

        # Changing hash values affects the iteration order of sets. Python has never made guarantees about this ordering (and it typically varies between 32-bit and 64-bit builds).

        # See also PYTHONHASHSEED.

        # Changed in version 3.3: Hash randomization is enabled by default.

    # object.__bool__(self)
        # Called to implement truth value testing and the built-in operation bool(); should return False or True.
        # When this method is not defined, __len__() is called, if it is defined, and the object is considered true if its result is nonzero.
        # If a class defines neither __len__() nor __bool__(), all its instances are considered true.

# ===================== 3.3.2.     Customizing attribute access             =====================
    # The following methods can be defined to customize the meaning of attribute access (use of, assignment to, or deletion of x.name) for class instances.

    # object.__getattr__(self, name)
        # Called when the default attribute access fails with an AttributeError
        # (either __getattribute__() raises an AttributeError because name is not an instance attribute or an attribute in the class tree for self;
        # or __get__() of a name property raises AttributeError).
        # This method should either return the (computed) attribute value or raise an AttributeError exception.

        # Note that if the attribute is found through the normal mechanism, __getattr__() is not called.
        # (This is an intentional asymmetry between __getattr__() and __setattr__().)
        # This is done both for efficiency reasons and because otherwise __getattr__() would have no way to access other attributes of the instance.
        # Note that at least for instance variables, you can fake total control by not inserting any values in the instance attribute dictionary
        # (but instead inserting them in another object).

    # object.__getattribute__(self, name)
        # Called unconditionally to implement attribute accesses for instances of the class.
        # If the class also defines __getattr__(), the latter will not be called unless __getattribute__() either calls it explicitly or raises an AttributeError.
        # This method should return the (computed) attribute value or raise an AttributeError exception.
        # In order to avoid infinite recursion in this method, its implementation should always call the base class method with the same name to access any attributes it needs,
        # for example, object.__getattribute__(self, name).

        # Note: This method may still be bypassed when looking up special methods as the result of implicit invocation via language syntax or built-in functions.
        # See Special method lookup.

    # object.__setattr__(self, name, value)
        # Called when an attribute assignment is attempted. This is called instead of the normal mechanism (i.e. store the value in the instance dictionary).
        # name is the attribute name, value is the value to be assigned to it.

        # If __setattr__() wants to assign to an instance attribute, it should call the base class method with the same name,
        # for example, object.__setattr__(self, name, value).

    # object.__delattr__(self, name)
        # Like __setattr__() but for attribute deletion instead of assignment. This should only be implemented if del obj.name is meaningful for the object.

    # object.__dir__(self)
        # Called when dir() is called on the object. A sequence must be returned.
        # dir() converts the returned sequence to a list and sorts it.

# ===================== 3.3.2.1.   Customizing module attribute access      =====================
    # Special names __getattr__ and __dir__ can be also used to customize access to module attributes.
    # The __getattr__ function at the module level should accept one argument which is the name of an attribute and return the computed value or raise an AttributeError.
    # If an attribute is not found on a module object through the normal lookup, i.e. object.__getattribute__(),
    # then __getattr__ is searched in the module __dict__ before raising an AttributeError.
    # If found, it is called with the attribute name and the result is returned.

    # The __dir__ function should accept no arguments, and return a sequence of strings that represents the names accessible on module.
    # If present, this function overrides the standard dir() search on a module.

    # For a more fine grained customization of the module behavior (setting attributes, properties, etc.),
    # one can set the __class__ attribute of a module object to a subclass of types.ModuleType. For example:

    # import sys
    # from types import ModuleType

    # class VerboseModule(ModuleType):
    #     def __repr__(self):
    #         return f'Verbose {self.__name__}'

    #     def __setattr__(self, attr, value):
    #         print(f'Setting {attr}...')
    #         super().__setattr__(attr, value)

    # sys.modules[__name__].__class__ = VerboseModule

    # Note: Defining module __getattr__ and setting module __class__ only affect lookups made using the attribute access syntax
    #  – directly accessing the module globals (whether by code within the module, or via a reference to the module’s globals dictionary) is unaffected.

    # Changed in version 3.5: __class__ module attribute is now writable.
    # New in version 3.7: __getattr__ and __dir__ module attributes.

    # See also
    # PEP 562 - Module __getattr__ and __dir__
    # Describes the __getattr__ and __dir__ functions on modules.

# ===================== 3.3.2.2.   Implementing Descriptors                 =====================
    # The following methods only apply when an instance of the class containing the method (a so-called descriptor class) appears in an owner class
    # (the descriptor must be in either the owner’s class dictionary or in the class dictionary for one of its parents).
    # In the examples below, “the attribute” refers to the attribute whose name is the key of the property in the owner class’ __dict__.

    # object.__get__(self, instance, owner=None)
        # Called to get the attribute of the owner class (class attribute access) or of an instance of that class (instance attribute access).
        # The optional owner argument is the owner class, while instance is the instance that the attribute was accessed through,
        # or None when the attribute is accessed through the owner.

        # This method should return the computed attribute value or raise an AttributeError exception.

        # PEP 252 specifies that __get__() is callable with one or two arguments.
        # Python’s own built-in descriptors support this specification; however, it is likely that some third-party tools have descriptors that require both arguments.
        # Python’s own __getattribute__() implementation always passes in both arguments whether they are required or not.

    # object.__set__(self, instance, value)
        # Called to set the attribute on an instance instance of the owner class to a new value, value.

        # Note, adding __set__() or __delete__() changes the kind of descriptor to a “data descriptor”.
        # See Invoking Descriptors for more details.

    # object.__delete__(self, instance)
        # Called to delete the attribute on an instance instance of the owner class.

    # object.__set_name__(self, owner, name)
        # Called at the time the owning class owner is created. The descriptor has been assigned to name.

        # Note: __set_name__() is only called implicitly as part of the type constructor,
        # so it will need to be called explicitly with the appropriate parameters when a descriptor is added to a class after initial creation:
        # class A:
        #    pass
        # descr = custom_descriptor()
        # A.attr = descr
        # descr.__set_name__(A, 'attr')

        # See Creating the class object for more details.

        # New in version 3.6.

        # The attribute __objclass__ is interpreted by the inspect module as specifying the class where this object was defined
        # (setting this appropriately can assist in runtime introspection of dynamic class attributes).
        # For callables, it may indicate that an instance of the given type (or a subclass) is expected or required as the first positional argument
        # (for example, CPython sets this attribute for unbound methods that are implemented in C).

# ===================== 3.3.2.3.   Invoking Descriptors                     =====================
    # In general, a descriptor is an object attribute with “binding behavior”,
    # one whose attribute access has been overridden by methods in the descriptor protocol:
    # __get__(), __set__(), and __delete__().
    # If any of those methods are defined for an object, it is said to be a descriptor.

    # The default behavior for attribute access is to get, set, or delete the attribute from an object’s dictionary.
    # For instance, a.x has a lookup chain starting with a.__dict__['x'], then type(a).__dict__['x'], and continuing through the base classes of type(a) excluding metaclasses.

    # However, if the looked-up value is an object defining one of the descriptor methods, then Python may override the default behavior and invoke the descriptor method instead.
    # Where this occurs in the precedence chain depends on which descriptor methods were defined and how they were called.

    # The starting point for descriptor invocation is a binding, a.x. How the arguments are assembled depends on a:

    # Direct Call
    # The simplest and least common call is when user code directly invokes a descriptor method: x.__get__(a).

    # Instance Binding
    # If binding to an object instance, a.x is transformed into the call: type(a).__dict__['x'].__get__(a, type(a)).

    # Class Binding
    # If binding to a class, A.x is transformed into the call: A.__dict__['x'].__get__(None, A).

    # Super Binding
    # If a is an instance of super, then the binding super(B, obj).m() searches obj.__class__.__mro__
    # for the base class A immediately preceding B and then invokes the descriptor with the call:
    # A.__dict__['m'].__get__(obj, obj.__class__).

    # For instance bindings, the precedence of descriptor invocation depends on the which descriptor methods are defined.
    # A descriptor can define any combination of __get__(), __set__() and __delete__().
    # If it does not define __get__(), then accessing the attribute will return the descriptor object itself
    # unless there is a value in the object’s instance dictionary.
    # If the descriptor defines __set__() and/or __delete__(), it is a data descriptor; if it defines neither, it is a non-data descriptor.
    # Normally, data descriptors define both __get__() and __set__(), while non-data descriptors have just the __get__() method.
    # Data descriptors with __set__() and __get__() defined always override a redefinition in an instance dictionary.
    # In contrast, non-data descriptors can be overridden by instances.

    # Python methods (including staticmethod() and classmethod()) are implemented as non-data descriptors.
    # Accordingly, instances can redefine and override methods.
    # This allows individual instances to acquire behaviors that differ from other instances of the same class.

    # The property() function is implemented as a data descriptor.
    # Accordingly, instances cannot override the behavior of a property.

# ===================== 3.3.2.4.   __slots__                                =====================
    # __slots__ allow us to explicitly declare data members (like properties) and deny the creation of __dict__ and __weakref__
    # (unless explicitly declared in __slots__ or available in a parent.)

    # The space saved over using __dict__ can be significant. Attribute lookup speed can be significantly improved as well.

    # object.__slots__
        # This class variable can be assigned a string, iterable, or sequence of strings with variable names used by instances.
        # __slots__ reserves space for the declared variables and prevents the automatic creation of __dict__ and __weakref__ for each instance.

# ===================== 3.3.2.4.1. Notes on using __slots__                 =====================
    # When inheriting from a class without __slots__, the __dict__ and __weakref__ attribute of the instances will always be accessible.

    # Without a __dict__ variable, instances cannot be assigned new variables not listed in the __slots__ definition.
    # Attempts to assign to an unlisted variable name raises AttributeError.
    # If dynamic assignment of new variables is desired, then add '__dict__' to the sequence of strings in the __slots__ declaration.

    # Without a __weakref__ variable for each instance, classes defining __slots__ do not support weak references to its instances.
    # If weak reference support is needed, then add '__weakref__' to the sequence of strings in the __slots__ declaration.

    # __slots__ are implemented at the class level by creating descriptors (Implementing Descriptors) for each variable name.
    # As a result, class attributes cannot be used to set default values for instance variables defined by __slots__;
    # otherwise, the class attribute would overwrite the descriptor assignment.

    # The action of a __slots__ declaration is not limited to the class where it is defined.
    # __slots__ declared in parents are available in child classes.
    # However, child subclasses will get a __dict__ and __weakref__ unless they also define __slots__
    # (which should only contain names of any additional slots).

    # If a class defines a slot also defined in a base class, the instance variable defined by the base class slot is inaccessible
    # (except by retrieving its descriptor directly from the base class). This renders the meaning of the program undefined.
    # In the future, a check may be added to prevent this.

    # Nonempty __slots__ does not work for classes derived from “variable-length” built-in types such as int, bytes and tuple.

    # Any non-string iterable may be assigned to __slots__.
    # Mappings may also be used; however, in the future, special meaning may be assigned to the values corresponding to each key.

    # __class__ assignment works only if both classes have the same __slots__.

    # Multiple inheritance with multiple slotted parent classes can be used, but only one parent is allowed to have attributes created by slots
    # (the other bases must have empty slot layouts) - violations raise TypeError.

    # If an iterator is used for __slots__ then a descriptor is created for each of the iterator’s values.
    # However, the __slots__ attribute will be an empty iterator.

# ===================== 3.3.3.     Customizing class creation               =====================
    # Whenever a class inherits from another class, __init_subclass__ is called on that class.
    # This way, it is possible to write classes which change the behavior of subclasses.
    # This is closely related to class decorators, but where class decorators only affect the specific class they’re applied to,
    # __init_subclass__ solely applies to future subclasses of the class defining the method.

    # classmethod object.__init_subclass__(cls)
        # This method is called whenever the containing class is subclassed. cls is then the new subclass.
        # If defined as a normal instance method, this method is implicitly converted to a class method.

        # Keyword arguments which are given to a new class are passed to the parent’s class __init_subclass__.
        # For compatibility with other classes using __init_subclass__,
        # one should take out the needed keyword arguments and pass the others over to the base class, as in:

        # class Philosopher:
        #     def __init_subclass__(cls, /, default_name, **kwargs):
        #         super().__init_subclass__(**kwargs)
        #         cls.default_name = default_name

        # class AustralianPhilosopher(Philosopher, default_name="Bruce"):
        #     pass
        
        # The default implementation object.__init_subclass__ does nothing, but raises an error if it is called with any arguments.

        # Note: The metaclass hint metaclass is consumed by the rest of the type machinery, and is never passed to __init_subclass__ implementations.
        # The actual metaclass (rather than the explicit hint) can be accessed as type(cls).
        # New in version 3.6.

# ===================== 3.3.3.1.   Metaclasses                              =====================
    # By default, classes are constructed using type().
    # The class body is executed in a new namespace and the class name is bound locally to the result of type(name, bases, namespace).

    # The class creation process can be customized by passing the metaclass keyword argument in the class definition line,
    # or by inheriting from an existing class that included such an argument.
    # In the following example, both MyClass and MySubclass are instances of Meta:

        # class Meta(type):
        #     pass

        # class MyClass(metaclass=Meta):
        #     pass

        # class MySubclass(MyClass):
        #     pass

    # Any other keyword arguments that are specified in the class definition are passed through to all metaclass operations described below.
    # When a class definition is executed, the following steps occur:
        # MRO entries are resolved;
        # the appropriate metaclass is determined;
        # the class namespace is prepared;
        # the class body is executed;
        # the class object is created.

# ===================== 3.3.3.2.   Resolving MRO entries                    =====================
    # If a base that appears in class definition is not an instance of type, then an __mro_entries__ method is searched on it.
    # If found, it is called with the original bases tuple.
    # This method must return a tuple of classes that will be used instead of this base.
    # The tuple may be empty, in such case the original base is ignored.

    # See also PEP 560 - Core support for typing module and generic types

# ===================== 3.3.3.3.   Determining the appropriate metaclass    =====================
    # The appropriate metaclass for a class definition is determined as follows:

    # if no bases and no explicit metaclass are given, then type() is used;
    # if an explicit metaclass is given and it is not an instance of type(), then it is used directly as the metaclass;
    # if an instance of type() is given as the explicit metaclass, or bases are defined, then the most derived metaclass is used.

    # The most derived metaclass is selected from the explicitly specified metaclass (if any) and the metaclasses (i.e. type(cls)) of all specified base classes.
    # The most derived metaclass is one which is a subtype of all of these candidate metaclasses.
    # If none of the candidate metaclasses meets that criterion, then the class definition will fail with TypeError.

# ===================== 3.3.3.4.   Preparing the class namespace            =====================
    # Once the appropriate metaclass has been identified, then the class namespace is prepared.
    # If the metaclass has a __prepare__ attribute, it is called as namespace = metaclass.__prepare__(name, bases, **kwds)
    # (where the additional keyword arguments, if any, come from the class definition).
    # The __prepare__ method should be implemented as a classmethod().
    # The namespace returned by __prepare__ is passed in to __new__, but when the final class object is created the namespace is copied into a new dict.

    # If the metaclass has no __prepare__ attribute, then the class namespace is initialised as an empty ordered mapping.

    # See also
    # PEP 3115 - Metaclasses in Python 3000
    # Introduced the __prepare__ namespace hook

# ===================== 3.3.3.5.   Executing the class body                 =====================
    # The class body is executed (approximately) as exec(body, globals(), namespace).
    # The key difference from a normal call to exec() is that lexical scoping allows the class body (including any methods) to reference names from the current
    # and outer scopes when the class definition occurs inside a function.

    # However, even when the class definition occurs inside the function, methods defined inside the class still cannot see names defined at the class scope.
    # Class variables must be accessed through the first parameter of instance or class methods,
    # or through the implicit lexically scoped __class__ reference described in the next section.

# ===================== 3.3.3.6.   Creating the class object                =====================
    # Once the class namespace has been populated by executing the class body, the class object is created by calling metaclass(name, bases, namespace, **kwds)
    # (the additional keywords passed here are the same as those passed to __prepare__).

    # This class object is the one that will be referenced by the zero-argument form of super().
    # __class__ is an implicit closure reference created by the compiler if any methods in a class body refer to either __class__ or super.
    # This allows the zero argument form of super() to correctly identify the class being defined based on lexical scoping,
    # while the class or instance that was used to make the current call is identified based on the first argument passed to the method.

    # CPython implementation detail: In CPython 3.6 and later, the __class__ cell is passed to the metaclass as a __classcell__ entry in the class namespace.
    # If present, this must be propagated up to the type.__new__ call in order for the class to be initialised correctly.
    # Failing to do so will result in a RuntimeError in Python 3.8.

    # When using the default metaclass type, or any metaclass that ultimately calls type.__new__,
    # the following additional customisation steps are invoked after creating the class object:

    # first, type.__new__ collects all of the descriptors in the class namespace that define a __set_name__() method;
    # second, all of these __set_name__ methods are called with the class being defined and the assigned name of that particular descriptor;
    # finally, the __init_subclass__() hook is called on the immediate parent of the new class in its method resolution order.

    # After the class object is created, it is passed to the class decorators included in the class definition (if any)
    # and the resulting object is bound in the local namespace as the defined class.

    # When a new class is created by type.__new__, the object provided as the namespace parameter is copied to a new ordered mapping
    # and the original object is discarded.
    # The new copy is wrapped in a read-only proxy, which becomes the __dict__ attribute of the class object.

    # See also
    # PEP 3135 - New super
    # Describes the implicit __class__ closure reference

# ===================== 3.3.3.7.   Uses for metaclasses                     =====================
    # The potential uses for metaclasses are boundless. Some ideas that have been explored include
    # enum, logging, interface checking, automatic delegation, automatic property creation, proxies, frameworks, and automatic resource locking/synchronization.

# ===================== 3.3.4.     Customizing instance and subclass checks =====================
    # The following methods are used to override the default behavior of the isinstance() and issubclass() built-in functions.

    # In particular, the metaclass abc.ABCMeta implements these methods in order to allow the addition of Abstract Base Classes (ABCs) as “virtual base classes”
    # to any class or type (including built-in types), including other ABCs.

    # class.__instancecheck__(self, instance)
        # Return true if instance should be considered a (direct or indirect) instance of class. If defined, called to implement isinstance(instance, class).

    # class.__subclasscheck__(self, subclass)
        # Return true if subclass should be considered a (direct or indirect) subclass of class. If defined, called to implement issubclass(subclass, class).

    # Note that these methods are looked up on the type (metaclass) of a class. They cannot be defined as class methods in the actual class.
    # This is consistent with the lookup of special methods that are called on instances, only in this case the instance is itself a class.

    # See also
    # PEP 3119 - Introducing Abstract Base Classes
    # Includes the specification for customizing isinstance() and issubclass() behavior through __instancecheck__() and __subclasscheck__(),
    # with motivation for this functionality in the context of adding Abstract Base Classes (see the abc module) to the language.

# ===================== 3.3.5.     Emulating generic types                  =====================
    # One can implement the generic class syntax as specified by PEP 484 (for example List[int]) by defining a special method:

    # classmethod object.__class_getitem__(cls, key)
        # Return an object representing the specialization of a generic class by type arguments found in key.

    # This method is looked up on the class object itself, and when defined in the class body, this method is implicitly a class method.
    # Note, this mechanism is primarily reserved for use with static type hints, other usage is discouraged.

    # See also PEP 560 - Core support for typing module and generic types

# ===================== 3.3.6.     Emulating callable objects               =====================
    # object.__call__(self[, args...])
        # Called when the instance is “called” as a function; if this method is defined, x(arg1, arg2, ...) is a shorthand for x.__call__(arg1, arg2, ...).

# ===================== 3.3.8.     Emulating numeric types                  =====================
    # The following methods can be defined to emulate numeric objects.
    # Methods corresponding to operations that are not supported by the particular kind of number implemented
    # (e.g., bitwise operations for non-integral numbers) should be left undefined.

    # object.__add__(self, other)
    # object.__sub__(self, other)
    # object.__mul__(self, other)
    # object.__matmul__(self, other)
    # object.__truediv__(self, other)
    # object.__floordiv__(self, other)
    # object.__mod__(self, other)
    # object.__divmod__(self, other)
    # object.__pow__(self, other[, modulo])
    # object.__lshift__(self, other)
    # object.__rshift__(self, other)
    # object.__and__(self, other)
    # object.__xor__(self, other)
    # object.__or__(self, other)
        # These methods are called to implement the binary arithmetic operations (+, -, *, @, /, //, %, divmod(), pow(), **, <<, >>, &, ^, |).
        # For instance, to evaluate the expression x + y, where x is an instance of a class that has an __add__() method, x.__add__(y) is called.
        # The __divmod__() method should be the equivalent to using __floordiv__() and __mod__(); it should not be related to __truediv__().
        # Note that __pow__() should be defined to accept an optional third argument if the ternary version of the built-in pow() function is to be supported.

        # If one of those methods does not support the operation with the supplied arguments, it should return NotImplemented.

    # object.__radd__(self, other)
    # object.__rsub__(self, other)
    # object.__rmul__(self, other)
    # object.__rmatmul__(self, other)
    # object.__rtruediv__(self, other)
    # object.__rfloordiv__(self, other)
    # object.__rmod__(self, other)
    # object.__rdivmod__(self, other)
    # object.__rpow__(self, other[, modulo])
    # object.__rlshift__(self, other)
    # object.__rrshift__(self, other)
    # object.__rand__(self, other)
    # object.__rxor__(self, other)
    # object.__ror__(self, other)
        # These methods are called to implement the binary arithmetic operations (+, -, *, @, /, //, %, divmod(), pow(), **, <<, >>, &, ^, |) with reflected (swapped) operands.
        # These functions are only called if the left operand does not support the corresponding operation and the operands are of different types.
        # For instance, to evaluate the expression x - y, where y is an instance of a class that has an __rsub__() method, y.__rsub__(x) is called if x.__sub__(y) returns NotImplemented.

        # Note that ternary pow() will not try calling __rpow__() (the coercion rules would become too complicated).

        # Note: If the right operand’s type is a subclass of the left operand’s type and that subclass provides the reflected method for the operation,
        # this method will be called before the left operand’s non-reflected method.
        # This behavior allows subclasses to override their ancestors’ operations.

    # object.__iadd__(self, other)
    # object.__isub__(self, other)
    # object.__imul__(self, other)
    # object.__imatmul__(self, other)
    # object.__itruediv__(self, other)
    # object.__ifloordiv__(self, other)
    # object.__imod__(self, other)
    # object.__ipow__(self, other[, modulo])
    # object.__ilshift__(self, other)
    # object.__irshift__(self, other)
    # object.__iand__(self, other)
    # object.__ixor__(self, other)
    # object.__ior__(self, other)
        # These methods are called to implement the augmented arithmetic assignments (+=, -=, *=, @=, /=, //=, %=, **=, <<=, >>=, &=, ^=, |=).
        # These methods should attempt to do the operation in-place (modifying self) and return the result (which could be, but does not have to be, self).
        # If a specific method is not defined, the augmented assignment falls back to the normal methods.
        # For instance, if x is an instance of a class with an __iadd__() method, x += y is equivalent to x = x.__iadd__(y) .
        # Otherwise, x.__add__(y) and y.__radd__(x) are considered, as with the evaluation of x + y.
        # In certain situations, augmented assignment can result in unexpected errors (see Why does a_tuple[i] += [‘item’] raise an exception when the addition works?),
        # but this behavior is in fact part of the data model.

    # object.__neg__(self)
    # object.__pos__(self)
    # object.__abs__(self)
    # object.__invert__(self)
        # Called to implement the unary arithmetic operations (-, +, abs() and ~).

    # object.__complex__(self)
    # object.__int__(self)
    # object.__float__(self)
        # Called to implement the built-in functions complex(), int() and float(). Should return a value of the appropriate type.

    # object.__index__(self)
        # Called to implement operator.index(), and whenever Python needs to losslessly convert the numeric object to an integer object
        # (such as in slicing, or in the built-in bin(), hex() and oct() functions).
        # Presence of this method indicates that the numeric object is an integer type. Must return an integer.

        # If __int__(), __float__() and __complex__() are not defined then corresponding built-in functions int(), float() and complex() fall back to __index__().

    # object.__round__(self[, ndigits])
    # object.__trunc__(self)
    # object.__floor__(self)
    # object.__ceil__(self)
        # Called to implement the built-in function round() and math functions trunc(), floor() and ceil().
        # Unless ndigits is passed to __round__() all these methods should return the value of the object truncated to an Integral (typically an int).

        # If __int__() is not defined then the built-in function int() falls back to __trunc__().

# ===================== 3.3.9.     With Statement Context Managers          =====================
    # A context manager is an object that defines the runtime context to be established when executing a with statement.
    # The context manager handles the entry into, and the exit from, the desired runtime context for the execution of the block of code.
    # Context managers are normally invoked using the with statement (described in section The with statement), but can also be used by directly invoking their methods.

    # Typical uses of context managers include saving and restoring various kinds of global state, locking and unlocking resources, closing opened files, etc.

    # For more information on context managers, see Context Manager Types.

    # object.__enter__(self)
        # Enter the runtime context related to this object.
        # The with statement will bind this method’s return value to the target(s) specified in the as clause of the statement, if any.

    # object.__exit__(self, exc_type, exc_value, traceback)
        # Exit the runtime context related to this object.
        # The parameters describe the exception that caused the context to be exited. If the context was exited without an exception, all three arguments will be None.

        # If an exception is supplied, and the method wishes to suppress the exception (i.e., prevent it from being propagated), it should return a true value.
        # Otherwise, the exception will be processed normally upon exit from this method.

        # Note that __exit__() methods should not reraise the passed-in exception; this is the caller’s responsibility.

    # See also
    # PEP 343 - The “with” statement
    # The specification, background, and examples for the Python with statement.

# ===================== 3.3.10.    Special method lookup                    =====================
    # For custom classes, implicit invocations of special methods are only guaranteed to work correctly if defined on an object’s type, not in the object’s instance dictionary.
    # That behaviour is the reason why the following code raises an exception:

    # >>>
    # >>> class C:
    # ...     pass
    # ...
    # >>> c = C()
    # >>> c.__len__ = lambda: 5
    # >>> len(c)
    # Traceback (most recent call last):
    #   File "<stdin>", line 1, in <module>
    # TypeError: object of type 'C' has no len()

    # The rationale behind this behaviour lies with a number of special methods such as __hash__() and __repr__() that are implemented by all objects, including type objects.
    # If the implicit lookup of these methods used the conventional lookup process, they would fail when invoked on the type object itself:

    # >>>
    # >>> 1 .__hash__() == hash(1)
    # True
    # >>> int.__hash__() == hash(int)
    # Traceback (most recent call last):
    #   File "<stdin>", line 1, in <module>
    # TypeError: descriptor '__hash__' of 'int' object needs an argument

    # Incorrectly attempting to invoke an unbound method of a class in this way is sometimes referred to as ‘metaclass confusion’,
    # and is avoided by bypassing the instance when looking up special methods:

    # >>>
    # >>> type(1).__hash__(1) == hash(1)
    # True
    # >>> type(int).__hash__(int) == hash(int)
    # True

    # In addition to bypassing any instance attributes in the interest of correctness,
    # implicit special method lookup generally also bypasses the __getattribute__() method even of the object’s metaclass:

    # >>>
    # >>> class Meta(type):
    # ...     def __getattribute__(*args):
    # ...         print("Metaclass getattribute invoked")
    # ...         return type.__getattribute__(*args)
    # ...
    # >>> class C(object, metaclass=Meta):
    # ...     def __len__(self):
    # ...         return 10
    # ...     def __getattribute__(*args):
    # ...         print("Class getattribute invoked")
    # ...         return object.__getattribute__(*args)
    # ...
    # >>> c = C()
    # >>> c.__len__()                 # Explicit lookup via instance
    # Class getattribute invoked
    # 10
    # >>> type(c).__len__(c)          # Explicit lookup via type
    # Metaclass getattribute invoked
    # 10
    # >>> len(c)                      # Implicit lookup
    # 10

    # Bypassing the __getattribute__() machinery in this fashion provides significant scope for speed optimisations within the interpreter,
    # at the cost of some flexibility in the handling of special methods (the special method must be set on the class object itself in order to be consistently invoked by the interpreter).
