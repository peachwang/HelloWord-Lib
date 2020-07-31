# -*- coding: utf-8 -*-  
from ..shared import *
from itertools import chain, filterfalse
from more_itertools import consume

# https://more-itertools.readthedocs.io/en/stable/api.html

inspect.getgeneratorstate(generator)
Get current state of a generator-iterator.

Possible states are:
GEN_CREATED: Waiting to start execution.

GEN_RUNNING: Currently being executed by the interpreter.

GEN_SUSPENDED: Currently suspended at a yield expression.

GEN_CLOSED: Execution has completed.

New in version 3.2.

class Iter :

    def __init__(self, iterable, /) :
        self._iterator = iter(iterable)

    def __iter__(self)              : return self

    # ============ 下列方法将消耗部分或全部数据 ============

    # next(iterator[, default])
        # Retrieve the next item from the iterator by calling its __next__() method.
        # If default is given, it is returned if the iterator is exhausted, otherwise StopIteration is raised.
        # next(iterator[, default])
            # Return the next item from the iterator.
            # If default is given and the iterator is exhausted, it is returned instead of raising StopIteration.
    def __next__(self)              : return next(self._iterator)

    def next(self)                  : return self.__next__()

    # Advance iterable by n steps. If n is None, consume it entirely.
    # Efficiently exhausts an iterator without returning values.
    # Defaults to consuming the whole iterator, but an optional second argument may be provided to limit consumption.
    # If the iterator has fewer items remaining than the provided limit, the whole iterator will be consumed.
    # more_itertools.consume(iterator, n=None)
        # # "Advance the iterator n-steps ahead. If n is None, consume entirely."
        # # Use functions that consume iterators at C speed.
        # if n is None:
        #     # feed the entire iterator into a zero-length deque
        #     collections.deque(iterator, maxlen=0)
        # else:
        #     # advance to the empty slice starting at position n
        #     next(islice(iterator, n, n), None)
    def consume(self) -> None       : consume(self)

    @prop
    def list(self)                  : from .List import List; return List(item for item in self)

    # 下列方法通过消耗数据，返回有价值的计算结果

    def __len__(self) -> int        : return len(item for item in self)
    
    def len(self) -> int            : return self.__len__()

    def is_empty(self) -> bool      :
        for item in self : return False
        return True

    max(iterable, *[, key, default])
    max(arg1, arg2, *args[, key])
    Return the largest item in an iterable or the largest of two or more arguments.

    If one positional argument is provided, it should be an iterable. The largest item in the iterable is returned. If two or more positional arguments are provided, the largest of the positional arguments is returned.

    There are two optional keyword-only arguments. The key argument specifies a one-argument ordering function like that used for list.sort(). The default argument specifies an object to return if the provided iterable is empty. If the iterable is empty and default is not provided, a ValueError is raised.

    If multiple items are maximal, the function returns the first one encountered. This is consistent with other sort-stability preserving tools such as sorted(iterable, key=keyfunc, reverse=True)[0] and heapq.nlargest(1, iterable, key=keyfunc).

    New in version 3.4: The default keyword-only argument.

    Changed in version 3.8: The key can be None.

    min(iterable, *[, key, default])
    min(arg1, arg2, *args[, key])
    Return the smallest item in an iterable or the smallest of two or more arguments.

    If one positional argument is provided, it should be an iterable. The smallest item in the iterable is returned. If two or more positional arguments are provided, the smallest of the positional arguments is returned.

    There are two optional keyword-only arguments. The key argument specifies a one-argument ordering function like that used for list.sort(). The default argument specifies an object to return if the provided iterable is empty. If the iterable is empty and default is not provided, a ValueError is raised.

    If multiple items are minimal, the function returns the first one encountered. This is consistent with other sort-stability preserving tools such as sorted(iterable, key=keyfunc)[0] and heapq.nsmallest(1, iterable, key=keyfunc).

    New in version 3.4: The default keyword-only argument.

    Changed in version 3.8: The key can be None.

    # all(iterable)
        # Return True if all elements of the iterable are true (or if the iterable is empty). Equivalent to:
        # def all(iterable):
            # for element in iterable:
            #     if not element:
            #         return False
            # return True
        # all(iterable, /)
            # Return True if bool(x) is True for all values x in the iterable.
            # If the iterable is empty, return True.
    def all(self) -> bool : return all(self)

    # any(iterable)
        # Return True if any element of the iterable is true. If the iterable is empty, return False. Equivalent to:
        # def any(iterable):
            # for element in iterable:
            #     if element:
            #         return True
            # return False
        # any(iterable, /)
            # Return True if bool(x) is True for any x in the iterable.
            # If the iterable is empty, return False.
    def any(self) -> bool : return any(self)
    
    # ============ 下列方法不产生消耗，仅仅叠加一层处理逻辑后，返回一个迭代器 ============

    # enumerate(iterable, start=0)
        # Return an enumerate object.
        # iterable must be a sequence, an iterator, or some other object which supports iteration.
        # The __next__() method of the iterator returned by enumerate() returns a tuple containing
        # a count (from start which defaults to 0) and the values obtained from iterating over iterable.
        # Equivalent to:
        # def enumerate(sequence, start=0):
            # n = start
            # for elem in sequence:
            #     yield n, elem
            #     n += 1
        # enumerate(iterable, start=0)
            # Return an enumerate object.
            #   iterable
            #     an object supporting iteration
            # The enumerate object yields pairs containing a count (from start, which defaults to zero) and a value yielded by the iterable argument.
            # enumerate is useful for obtaining an indexed list:
            #     (0, seq[0]), (1, seq[1]), (2, seq[2]), ...
    def enum(self)                  : return Iter(enumerate(self))

    # class slice(stop)
    # class slice(start, stop[, step])
        # Return a slice object representing the set of indices specified by range(start, stop, step).
        # The start and step arguments default to None.
        # Slice objects have read-only data attributes start, stop and step which merely return the argument values (or their default).
        # They have no other explicit functionality; however they are used by Numerical Python and other third party extensions.
        # Slice objects are also generated when extended indexing syntax is used.
        # For example: a[start:stop:step] or a[start:stop, i].
        # See itertools.islice() for an alternate version that returns an iterator.
        # class slice(object)
            # slice(stop)
            # slice(start, stop[, step])
            # Create a slice object.
            # This is used for extended slicing (e.g. a[0:10:2]).
    
    # itertools.islice(iterable, stop)
    # itertools.islice(iterable, start, stop[, step])
    def islice

    # 可以允许字段不存在
    @wrap
    def value_iter(self, attr_or_func_name: str, /, *, default = None) :
        from .List   import List
        from .Object import Object
        for item in self :
            elif isinstance(attr_or_func_name, str) :
                yield List.get_value(item, attr_or_func_name, default)
            else                                        : raise CustomTypeError(attr_or_func_name)

    def __getattr__(self, attr_or_func_name: Union[list, str], /) : return self.value_iter(attr_or_func_name)

    # pos 为 index 在 func 的参数表里的下标，即本函数在 func 的参数表的下标
    def _left_pad_index_if_needed(self, func, args, index, pos, /) :
        if isclass(func)                  : func = func.__init__; pos += 1
        if not isinstance(func, Callable) : return args
        parameters = list(signature(func).parameters.values())
        return ( index, ) + args if len(parameters) > pos and parameters[pos].name == 'index' else args

    # map(function, iterable, ...)
        # Return an iterator that applies function to every item of iterable, yielding the results.
        # If additional iterable arguments are passed, function must take that many arguments and is applied to the items from all iterables in parallel.
        # With multiple iterables, the iterator stops when the shortest iterable is exhausted.
        # For cases where the function inputs are already arranged into argument tuples, see itertools.starmap().
        # map(func, *iterables) --> map object
            # Make an iterator that computes the function using arguments from each of the iterables.
            # Stops when the shortest iterable is exhausted.
    def map(self, func, /, *args, **kwargs)          : return Iter(func(item, *args, **kwargs) for index, item in enumerate(self))

    # itertools.starmap(function, iterable)
    Make an iterator that computes the function using arguments obtained from the iterable. Used instead of map() when argument parameters are already grouped in tuples from a single iterable (the data has been “pre-zipped”). The difference between map() and starmap() parallels the distinction between function(a,b) and function(*c). Roughly equivalent to:

    def starmap(function, iterable):
        # starmap(pow, [(2,5), (3,2), (10,3)]) --> 32 9 1000
        for args in iterable:
            yield function(*args)

    # itertools.takewhile(predicate, iterable)
    # itertools.dropwhile(predicate, iterable)

    # filter(function, iterable)
        # Construct an iterator from those elements of iterable for which function returns true.
        # iterable may be either a sequence, a container which supports iteration, or an iterator.
        # If function is None, the identity function is assumed, that is, all elements of iterable that are false are removed.
        # Note that filter(function, iterable) is equivalent to the generator expression (item for item in iterable if function(item)) if function is not None
        # and (item for item in iterable if item) if function is None.
        # See itertools.filterfalse() for the complementary function that returns elements of iterable for which function returns false.
        # class filter(object)
            # filter(function or None, iterable) --> filter object
            # Return an iterator yielding those items of iterable for which function(item) is true.
            # If function is None, return the items that are true.
    def filter(self, func, /)       : return Iter(filter(func, self))

    # itertools.filterfalse(predicate, iterable)
        # Make an iterator that filters elements from iterable returning only those for which the predicate is False.
        # If predicate is None, return the items that are false. Roughly equivalent to:
        # def filterfalse(predicate, iterable):
            # # filterfalse(lambda x: x%2, range(10)) --> 0 2 4 6 8
            # if predicate is None:
            #     predicate = bool
            # for x in iterable:
            #     if not predicate(x):
            #         yield x
        # class filterfalse(builtins.object)
            # filterfalse(function, iterable, /)
            # Return those items of iterable for which function(item) is false.
            # If function is None, return the items that are false.
    def filter_false(self, func, /) : return Iter(filterfalse(func, self))


    # itertools.groupby(iterable, key=None)

    def sum(self) : return sum(item for item in self)

    zip
    itertools.zip_longest(*iterables, fillvalue=None)
    Make an iterator that aggregates elements from each of the iterables. If the iterables are of uneven length, missing values are filled-in with fillvalue. Iteration continues until the longest iterable is exhausted. Roughly equivalent to:

    def zip_longest(*args, fillvalue=None):
        # zip_longest('ABCD', 'xy', fillvalue='-') --> Ax By C- D-
        iterators = [iter(it) for it in args]
        num_active = len(iterators)
        if not num_active:
            return
        while True:
            values = []
            for i, it in enumerate(iterators):
                try:
                    value = next(it)
                except StopIteration:
                    num_active -= 1
                    if not num_active:
                        return
                    iterators[i] = repeat(fillvalue)
                    value = fillvalue
                values.append(value)
            yield tuple(values)
    If one of the iterables is potentially infinite, then the zip_longest() function should be wrapped with something that limits the number of calls (for example islice() or takewhile()). If not specified, fillvalue defaults to None.

    # classmethod chain.from_iterable(iterable)
    
    @print_func
    def print_line(self, pattern = None, /) :
        from .List   import List
        return '\n'.join(
            f'{index + 1:>3} {List.wrap_str(item, format)}'
            if pattern is None
            else pattern.format(List.wrap_str(item, format), index)
            for index, item in self.enum()
        ) + '\n', False

    @print_func
    def print_format(self, pattern = None, /) :
        from .List   import List
        return '\n'.join(
            List.wrap_str(item, format)
            if pattern is None
            else pattern.format(List.wrap_str(item, format), index)
            for index, item in self.enum()
        ) + '\n', False

    @print_func
    def print_str(self) :
        from .List   import List
        return '\n'.join(List.wrap_str(item, str) for item in self) + '\n', False

    # itertools.accumulate(iterable, func=operator.add, *, initial=None):
    # itertools.count(start=0, step=1)
    # itertools.tee(iterable, n=2)
    # def take(n, iterable):
    #     "Return first n items of the iterable as a list"
    #     return list(islice(iterable, n))

    # def prepend(value, iterator):
    #     "Prepend a single value in front of an iterator"
    #     # prepend(1, [2, 3, 4]) -> 1 2 3 4
    #     return chain([value], iterator)

    # def tabulate(function, start=0):
    #     "Return function(0), function(1), ..."
    #     return map(function, count(start))

    # def tail(n, iterable):
    #     "Return an iterator over the last n items"
    #     # tail(3, 'ABCDEFG') --> E F G
    #     return iter(collections.deque(iterable, maxlen=n))

    # def nth(iterable, n, default=None):
    #     "Returns the nth item or a default value"
    #     return next(islice(iterable, n, None), default)