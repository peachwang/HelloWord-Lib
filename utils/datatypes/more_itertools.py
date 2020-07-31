
import warnings
from collections import Counter, defaultdict, deque, abc
from collections.abc import Sequence
from functools import partial, wraps
from heapq import merge, heapify, heapreplace, heappop
from math import exp, floor, log
from random import random, randrange, uniform, sample, choice
import operator
from operator import itemgetter, sub, gt, lt
from sys import maxsize
from time import monotonic

def accumulate(iterable, func=operator.add, *, initial=None):
    'Return running totals'
    # accumulate([1,2,3,4,5]) --> 1 3 6 10 15
    # accumulate([1,2,3,4,5], initial=100) --> 100 101 103 106 110 115
    # accumulate([1,2,3,4,5], operator.mul) --> 1 2 6 24 120
    it = iter(iterable)
    total = initial
    if initial is None:
        try:
            total = next(it)
        except StopIteration:
            return
    yield total
    for element in it:
        total = func(total, element)
        yield total

def chain(*iterables):
    # chain('ABC', 'DEF') --> A B C D E F
    for it in iterables:
        for element in it:
            yield element

def from_iterable(iterables):
    # chain.from_iterable(['ABC', 'DEF']) --> A B C D E F
    for it in iterables:
        for element in it:
            yield element

def combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)

def combinations(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    for indices in permutations(range(n), r):
        if sorted(indices) == list(indices):
            yield tuple(pool[i] for i in indices)

def combinations_with_replacement(iterable, r):
    # combinations_with_replacement('ABC', 2) --> AA AB AC BB BC CC
    pool = tuple(iterable)
    n = len(pool)
    if not n and r:
        return
    indices = [0] * r
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != n - 1:
                break
        else:
            return
        indices[i:] = [indices[i] + 1] * (r - i)
        yield tuple(pool[i] for i in indices)

def combinations_with_replacement(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    for indices in product(range(n), repeat=r):
        if sorted(indices) == list(indices):
            yield tuple(pool[i] for i in indices)

def compress(data, selectors):
    # compress('ABCDEF', [1,0,1,0,1,1]) --> A C E F
    return (d for d, s in zip(data, selectors) if s)

def count(start=0, step=1):
    # count(10) --> 10 11 12 13 14 ...
    # count(2.5, 0.5) -> 2.5 3.0 3.5 ...
    n = start
    while True:
        yield n
        n += step

def cycle(iterable):
    # cycle('ABCD') --> A B C D A B C D A B C D ...
    saved = []
    for element in iterable:
        yield element
        saved.append(element)
    while saved:
        for element in saved:
              yield element

def dropwhile(predicate, iterable):
    # dropwhile(lambda x: x<5, [1,4,6,4,1]) --> 6 4 1
    iterable = iter(iterable)
    for x in iterable:
        if not predicate(x):
            yield x
            break
    for x in iterable:
        yield x

def filterfalse(predicate, iterable):
    # filterfalse(lambda x: x%2, range(10)) --> 0 2 4 6 8
    if predicate is None:
        predicate = bool
    for x in iterable:
        if not predicate(x):
            yield x

class groupby:
    # [k for k, g in groupby('AAAABBBCCDAABBB')] --> A B C D A B
    # [list(g) for k, g in groupby('AAAABBBCCD')] --> AAAA BBB CC D
    def __init__(self, iterable, key=None):
        if key is None:
            key = lambda x: x
        self.keyfunc = key
        self.it = iter(iterable)
        self.tgtkey = self.currkey = self.currvalue = object()
    
    def __iter__(self):
        return self
    
    def __next__(self):
        self.id = object()
        while self.currkey == self.tgtkey:
            self.currvalue = next(self.it)    # Exit on StopIteration
            self.currkey = self.keyfunc(self.currvalue)
        self.tgtkey = self.currkey
        return (self.currkey, self._grouper(self.tgtkey, self.id))
    
    def _grouper(self, tgtkey, id):
        while self.id is id and self.currkey == tgtkey:
            yield self.currvalue
            try:
                self.currvalue = next(self.it)
            except StopIteration:
                return
            self.currkey = self.keyfunc(self.currvalue)

def islice(iterable, *args):
    # islice('ABCDEFG', 2) --> A B
    # islice('ABCDEFG', 2, 4) --> C D
    # islice('ABCDEFG', 2, None) --> C D E F G
    # islice('ABCDEFG', 0, None, 2) --> A C E G
    s = slice(*args)
    start, stop, step = s.start or 0, s.stop or sys.maxsize, s.step or 1
    it = iter(range(start, stop, step))
    try:
        nexti = next(it)
    except StopIteration:
        # Consume *iterable* up to the *start* position.
        for i, element in zip(range(start), iterable):
            pass
        return
    try:
        for i, element in enumerate(iterable):
            if i == nexti:
                yield element
                nexti = next(it)
    except StopIteration:
        # Consume to *stop*.
        for i, element in zip(range(i + 1, stop), iterable):
            pass

def permutations(iterable, r=None):
    # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
    # permutations(range(3)) --> 012 021 102 120 201 210
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return
    indices = list(range(n))
    cycles = list(range(n, n-r, -1))
    yield tuple(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return

def permutations(iterable, r=None):
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    for indices in product(range(n), repeat=r):
        if len(set(indices)) == r:
            yield tuple(pool[i] for i in indices)

def product(*args, repeat=1):
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    pools = [tuple(pool) for pool in args] * repeat
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)

def repeat(object, times=None):
    # repeat(10, 3) --> 10 10 10
    if times is None:
        while True:
            yield object
    else:
        for i in range(times):
            yield object

def starmap(function, iterable):
    # starmap(pow, [(2,5), (3,2), (10,3)]) --> 32 9 1000
    for args in iterable:
        yield function(*args)

def takewhile(predicate, iterable):
    # takewhile(lambda x: x<5, [1,4,6,4,1]) --> 1 4
    for x in iterable:
        if predicate(x):
            yield x
        else:
            break

def tee(iterable, n=2):
    it = iter(iterable)
    deques = [collections.deque() for i in range(n)]
    def gen(mydeque):
        while True:
            if not mydeque:             # when the local deque is empty
                try:
                    newval = next(it)   # fetch a new value and
                except StopIteration:
                    return
                for d in deques:        # load it to all the deques
                    d.append(newval)
            yield mydeque.popleft()
    return tuple(gen(d) for d in deques)

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

_marker = object()

def chunked(iterable, n) : return iter(partial(take, n, iter(iterable)), [])

def first(iterable, default = _marker) :
    try :
        return next(iter(iterable))
    except StopIteration :
        # I'm on the edge about raising ValueError instead of StopIteration. At
        # the moment, ValueError wins, because the caller could conceivably
        # want to do something different with flow control when I raise the
        # exception, and it's weird to explicitly catch StopIteration.
        if default is _marker :
            raise ValueError(
                'first() was called on an empty iterable, and no '
                'default value was provided.'
            )
        return default

def last(iterable, default = _marker) :
    try :
        try :
            # Try to access the last item directly
            return iterable[-1]
        except (TypeError, AttributeError, KeyError) :
            # If not slice-able, iterate entirely using length-1 deque
            return deque(iterable, maxlen = 1)[0]
    except IndexError:  # If the iterable was empty
        if default is _marker :
            raise ValueError(
                'last() was called on an empty iterable, and no '
                'default value was provided.'
            )
        return default

def nth_or_last(iterable, n, default = _marker) : return last(islice(iterable, n + 1), default = default)

class peekable :

    def __init__(self, iterable) :
        self._it = iter(iterable)
        self._cache = deque()

    def __iter__(self) :
        return self

    def __bool__(self) :
        try :
            self.peek()
        except StopIteration :
            return False
        return True

    def peek(self, default = _marker) :
        """Return the item that will be next returned from ``next()``.
        Return ``default`` if there are no items left. If ``default`` is not
        provided, raise ``StopIteration``.
        """
        if not self._cache :
            try :
                self._cache.append(next(self._it))
            except StopIteration :
                if default is _marker :
                    raise
                return default
        return self._cache[0]

    def prepend(self, *items) :
        """Stack up items to be the next ones returned from ``next()`` or
        ``self.peek()``. The items will be returned in
        first in, first out order: :
            >>> p = peekable([1, 2, 3])
            >>> p.prepend(10, 11, 12)
            >>> next(p)
            10
            >>> list(p)
            [11, 12, 1, 2, 3]
        It is possible, by prepending items, to "resurrect" a peekable that
        previously raised ``StopIteration``.
            >>> p = peekable([])
            >>> next(p)
            Traceback (most recent call last) :
              ...
            StopIteration
            >>> p.prepend(1)
            >>> next(p)
            1
            >>> next(p)
            Traceback (most recent call last) :
              ...
            StopIteration
        """
        self._cache.extendleft(reversed(items))

    def __next__(self) :
        if self._cache :
            return self._cache.popleft()
        return next(self._it)

    def _get_slice(self, index) :
        # Normalize the slice's arguments
        step = 1 if (index.step is None) else index.step
        if step > 0 :
            start = 0 if (index.start is None) else index.start
            stop = maxsize if (index.stop is None) else index.stop
        elif step < 0 :
            start = -1 if (index.start is None) else index.start
            stop = (-maxsize - 1) if (index.stop is None) else index.stop
        else :
            raise ValueError('slice step cannot be zero')

        # If either the start or stop index is negative, we'll need to cache the rest of the iterable in order to slice from the right side.
        if (start < 0) or (stop < 0) :
            self._cache.extend(self._it)
        # Otherwise we'll need to find the rightmost index and cache to that point.
        else :
            n = min(max(start, stop) + 1, maxsize)
            cache_len = len(self._cache)
            if n >= cache_len :
                self._cache.extend(islice(self._it, n - cache_len))

        return list(self._cache)[index]

    def __getitem__(self, index) :
        if isinstance(index, slice) :
            return self._get_slice(index)

        cache_len = len(self._cache)
        if index < 0 :
            self._cache.extend(self._it)
        elif index >= cache_len :
            self._cache.extend(islice(self._it, index + 1 - cache_len))

        return self._cache[index]

def collate(*iterables, **kwargs) :
    warnings.warn(
        "collate is no longer part of more_itertools, use heapq.merge",
        DeprecationWarning,
    )
    return merge(*iterables, **kwargs)

def consumer(func) :
    @wraps(func)
    def wrapper(*args, **kwargs) :
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return wrapper

def ilen(iterable) :
    # This approach was selected because benchmarks showed it's likely the
    # fastest of the known implementations at the time of writing.
    # See GitHub tracker: #236, #230.
    counter = count()
    deque(zip(iterable, counter), maxlen = 0)
    return next(counter)

def iterate(func, start) :
    while True :
        yield start
        start = func(start)

def with_iter(context_manager) :
    with context_manager as iterable :
        yield from iterable

def one(iterable, too_short = None, too_long = None) :
    it = iter(iterable)

    try :
        first_value = next(it)
    except StopIteration :
        raise too_short or ValueError('too few items in iterable (expected 1)')

    try :
        second_value = next(it)
    except StopIteration :
        pass
    else :
        msg = (
            'Expected exactly one item in iterable, but got {!r}, {!r}, '
            'and perhaps more.'.format(first_value, second_value)
        )
        raise too_long or ValueError(msg)

    return first_value

def distinct_permutations(iterable, r = None) :
    # Algorithm: https://w.wiki/Qai
    def _full(A) :
        while True :
            # Yield the permutation we have
            yield tuple(A)

            # Find the largest index i such that A[i] < A[i + 1]
            for i in range(size - 2, -1, -1) :
                if A[i] < A[i + 1] :
                    break
            #  If no such index exists, this permutation is the last one
            else :
                return

            # Find the largest index j greater than j such that A[i] < A[j]
            for j in range(size - 1, i, -1) :
                if A[i] < A[j] :
                    break

            # Swap the value of A[i] with that of A[j], then reverse the
            # sequence from A[i + 1] to form the new permutation
            A[i], A[j] = A[j], A[i]
            A[i + 1:] = A[:i - size:-1]  # A[i + 1:][::-1]

    # Algorithm: modified from the above
    def _partial(A, r) :
        # Split A into the first r items and the last r items
        head, tail = A[:r], A[r:]
        right_head_indexes = range(r - 1, -1, -1)
        left_tail_indexes = range(len(tail))

        while True :
            # Yield the permutation we have
            yield tuple(head)

            # Starting from the right, find the first index of the head with
            # value smaller than the maximum value of the tail - call it i.
            pivot = tail[-1]
            for i in right_head_indexes :
                if head[i] < pivot :
                    break
                pivot = head[i]
            else :
                return

            # Starting from the left, find the first value of the tail
            # with a value greater than head[i] and swap.
            for j in left_tail_indexes :
                if tail[j] > head[i] :
                    head[i], tail[j] = tail[j], head[i]
                    break
            # If we didn't find one, start from the right and find the first
            # index of the head with a value greater than head[i] and swap.
            else :
                for j in right_head_indexes :
                    if head[j] > head[i] :
                        head[i], head[j] = head[j], head[i]
                        break

            # Reverse head[i + 1:] and swap it with tail[:r - (i + 1)]
            tail += head[:i - r:-1]  # head[i + 1:][::-1]
            i += 1
            head[i:], tail[:] = tail[:r - i], tail[r - i:]

    items = sorted(iterable)

    size = len(items)
    if r is None :
        r = size

    if 0 < r <= size :
        return _full(items) if (r == size) else _partial(items, r)

    return iter(() if r else ((),))

def intersperse(e, iterable, n = 1) :
    if n == 0 :
        raise ValueError('n must be > 0')
    elif n == 1 :
        # interleave(repeat(e), iterable) -> e, x_0, e, e, x_1, e, x_2...
        # islice(..., 1, None) -> x_0, e, e, x_1, e, x_2...
        return islice(interleave(repeat(e), iterable), 1, None)
    else :
        # interleave(filler, chunks) -> [e], [x_0, x_1], [e], [x_2, x_3]...
        # islice(..., 1, None) -> [x_0, x_1], [e], [x_2, x_3]...
        # flatten(...) -> x_0, x_1, e, x_2, x_3...
        filler = repeat([e])
        chunks = chunked(iterable, n)
        return flatten(islice(interleave(filler, chunks), 1, None))

def unique_to_each(*iterables) :
    pool = [list(it) for it in iterables]
    counts = Counter(chain.from_iterable(map(set, pool)))
    uniques = {element for element in counts if counts[element] == 1}
    return [list(filter(uniques.__contains__, it)) for it in pool]

def windowed(seq, n, fillvalue = None, step = 1) :
    if n < 0 :
        raise ValueError('n must be >= 0')
    if n == 0 :
        yield tuple()
        return
    if step < 1 :
        raise ValueError('step must be >= 1')

    window = deque(maxlen = n)
    i = n
    for _ in map(window.append, seq) :
        i -= 1
        if not i :
            i = step
            yield tuple(window)

    size = len(window)
    if size < n :
        yield tuple(chain(window, repeat(fillvalue, n - size)))
    elif 0 < i < min(step, n) :
        window += (fillvalue,) * i
        yield tuple(window)

def substrings(iterable) :
    # The length-1 substrings
    seq = []
    for item in iter(iterable) :
        seq.append(item)
        yield (item,)
    seq = tuple(seq)
    item_count = len(seq)

    # And the rest
    for n in range(2, item_count + 1) :
        for i in range(item_count - n + 1) :
            yield seq[i : i + n]

def substrings_indexes(seq, reverse = False) :
    r = range(1, len(seq) + 1)
    if reverse :
        r = reversed(r)
    return (
        (seq[i : i + L], i, i + L) for L in r for i in range(len(seq) - L + 1)
    )

class bucket :

    def __init__(self, iterable, key, validator = None) :
        self._it = iter(iterable)
        self._key = key
        self._cache = defaultdict(deque)
        self._validator = validator or (lambda x: True)

    def __contains__(self, value) :
        if not self._validator(value) :
            return False

        try :
            item = next(self[value])
        except StopIteration :
            return False
        else :
            self._cache[value].appendleft(item)

        return True

    def _get_values(self, value) :
        """
        Helper to yield items from the parent iterator that match *value*.
        Items that don't match are stored in the local cache as they
        are encountered.
        """
        while True :
            # If we've cached some items that match the target value, emit
            # the first one and evict it from the cache.
            if self._cache[value] :
                yield self._cache[value].popleft()
            # Otherwise we need to advance the parent iterator to search for
            # a matching item, caching the rest.
            else :
                while True :
                    try :
                        item = next(self._it)
                    except StopIteration :
                        return
                    item_value = self._key(item)
                    if item_value == value :
                        yield item
                        break
                    elif self._validator(item_value) :
                        self._cache[item_value].append(item)

    def __iter__(self) :
        for item in self._it :
            item_value = self._key(item)
            if self._validator(item_value) :
                self._cache[item_value].append(item)
        yield from self._cache.keys()

    def __getitem__(self, value) :
        if not self._validator(value) :
            return iter(())
        return self._get_values(value)

def spy(iterable, n = 1) :
    it = iter(iterable)
    head = take(n, it)
    return head.copy(), chain(head, it)

def interleave(*iterables) : return chain.from_iterable(zip(*iterables))

def interleave_longest(*iterables) :
    i = chain.from_iterable(zip_longest(*iterables, fillvalue = _marker))
    return (x for x in i if x is not _marker)

def collapse(iterable, base_type = None, levels = None) :

    def walk(node, level) :
        if (
            ((levels is not None) and (level > levels))
            or isinstance(node, (str, bytes))
            or ((base_type is not None) and isinstance(node, base_type))
        ) :
            yield node
            return

        try :
            tree = iter(node)
        except TypeError :
            yield node
            return
        else :
            for child in tree :
                yield from walk(child, level + 1)

    yield from walk(iterable, 0)

def side_effect(func, iterable, chunk_size = None, before = None, after = None) :
    try :
        if before is not None :
            before()
        if chunk_size is None :
            for item in iterable :
                func(item)
                yield item
        else :
            for chunk in chunked(iterable, chunk_size) :
                func(chunk)
                yield from chunk
    finally :
        if after is not None :
            after()

def sliced(seq, n) : return takewhile(len, (seq[i : i + n] for i in count(0, n)))

def split_at(iterable, pred, maxsplit = -1, keep_separator = False) :
    if maxsplit == 0 :
        yield list(iterable)
        return
    buf = []
    it = iter(iterable)
    for item in it :
        if pred(item) :
            yield buf
            if keep_separator :
                yield [item]
            if maxsplit == 1 :
                yield list(it)
                return
            buf = []
            maxsplit -= 1
        else :
            buf.append(item)
    yield buf

def split_before(iterable, pred, maxsplit = -1) :
    if maxsplit == 0 :
        yield list(iterable)
        return
    buf = []
    it = iter(iterable)
    for item in it :
        if pred(item) and buf :
            yield buf
            if maxsplit == 1 :
                yield [item] + list(it)
                return
            buf = []
            maxsplit -= 1
        buf.append(item)
    yield buf

def split_after(iterable, pred, maxsplit = -1) :
    if maxsplit == 0 :
        yield list(iterable)
        return
    buf = []
    it = iter(iterable)
    for item in it :
        buf.append(item)
        if pred(item) and buf :
            yield buf
            if maxsplit == 1 :
                yield list(it)
                return
            buf = []
            maxsplit -= 1
    if buf :
        yield buf

def split_when(iterable, pred, maxsplit = -1) :
    if maxsplit == 0 :
        yield list(iterable)
        return
    it = iter(iterable)
    try :
        cur_item = next(it)
    except StopIteration :
        return

    buf = [cur_item]
    for next_item in it :
        if pred(cur_item, next_item) :
            yield buf
            if maxsplit == 1 :
                yield [next_item] + list(it)
                return
            buf = []
            maxsplit -= 1
        buf.append(next_item)
        cur_item = next_item

    yield buf

def split_into(iterable, sizes) :
    # convert the iterable argument into an iterator so its contents can
    # be consumed by islice in case it is a generator
    it = iter(iterable)
    for size in sizes :
        if size is None :
            yield list(it)
            return
        else :
            yield list(islice(it, size))

def padded(iterable, fillvalue = None, n = None, next_multiple = False) :
    it = iter(iterable)
    if n is None :
        yield from chain(it, repeat(fillvalue))
    elif n < 1 :
        raise ValueError('n must be at least 1')
    else :
        item_count = 0
        for item in it :
            yield item
            item_count += 1

        remaining = (n - item_count) % n if next_multiple else n - item_count
        for _ in range(remaining) :
            yield fillvalue

def repeat_last(iterable, default = None) :
    item = _marker
    for item in iterable :
        yield item
    final = default if item is _marker else item
    yield from repeat(final)

def distribute(n, iterable) :
    if n < 1 :
        raise ValueError('n must be at least 1')
    children = tee(iterable, n)
    return [islice(it, index, None, n) for index, it in enumerate(children)]

def stagger(iterable, offsets = (-1, 0, 1), longest = False, fillvalue = None) :
    children = tee(iterable, len(offsets))
    return zip_offset(
        *children, offsets = offsets, longest = longest, fillvalue = fillvalue
    )

class UnequalIterablesError(ValueError) :
    def __init__(self, details = None) :
        msg = 'Iterables have different lengths'
        if details is not None :
            msg += (
                ': index 0 has length {}; index {} has length {}'
            ).format(*details)

        super().__init__(msg)

def zip_equal(*iterables) :
    # Check whether the iterables are all the same size.
    try :
        first_size = len(iterables[0])
        for i, it in enumerate(iterables[1:], 1) :
            size = len(it)
            if size != first_size :
                break
        else :
            # If we didn't break out, we can use the built-in zip.
            return zip(*iterables)

        # If we did break out, there was a mismatch.
        raise UnequalIterablesError(details = (first_size, i, size))
    # If any one of the iterables didn't have a length, start reading
    # them until one runs out.
    except TypeError :
        return _zip_equal_generator(iterables)

def _zip_equal_generator(iterables) :
    for combo in zip_longest(*iterables, fillvalue = _marker) :
        for val in combo :
            if val is _marker :
                raise UnequalIterablesError()
        yield combo

def zip_offset(*iterables, offsets, longest = False, fillvalue = None) :
    if len(iterables) != len(offsets) :
        raise ValueError("Number of iterables and offsets didn't match")

    staggered = []
    for it, n in zip(iterables, offsets) :
        if n < 0 :
            staggered.append(chain(repeat(fillvalue, -n), it))
        elif n > 0 :
            staggered.append(islice(it, n, None))
        else :
            staggered.append(it)

    if longest :
        return zip_longest(*staggered, fillvalue = fillvalue)

    return zip(*staggered)

def sort_together(iterables, key_list = (0,), reverse = False) :
    return list(zip(*sorted(zip(*iterables), key = itemgetter(*key_list), reverse = reverse)))

def unzip(iterable) :
    head, iterable = spy(iter(iterable))
    if not head :
        # empty iterable, e.g. zip([], [], [])
        return ()
    # spy returns a one-length iterable as head
    head = head[0]
    iterables = tee(iterable, len(head))

    def itemgetter(i) :
        def getter(obj) :
            try :
                return obj[i]
            except IndexError :
                # basically if we have an iterable like iter([(1, 2, 3), (4, 5), (6,)]), the second unzipped iterable would fail at the third tuple, since it would try to access tup[1]
                # same with the third unzipped iterable and the second tuple to support these "improperly zipped" iterables, we create a custom itemgetter which just stops the unzipped iterables at first length mismatch
                raise StopIteration
        return getter

    return tuple(map(itemgetter(i), it) for i, it in enumerate(iterables))

def divide(n, iterable) :
    if n < 1 :
        raise ValueError('n must be at least 1')

    try :
        iterable[:0]
    except TypeError :
        seq = tuple(iterable)
    else :
        seq = iterable

    q, r = divmod(len(seq), n)

    ret = []
    stop = 0
    for i in range(1, n + 1) :
        start = stop
        stop += q + 1 if i <= r else q
        ret.append(iter(seq[start:stop]))

    return ret

def always_iterable(obj, base_type = (str, bytes)) :
    if obj is None :
        return iter(())

    if (base_type is not None) and isinstance(obj, base_type) :
        return iter((obj,))

    try :
        return iter(obj)
    except TypeError :
        return iter((obj,))

def adjacent(predicate, iterable, distance = 1) :
    # Allow distance = 0 mainly for testing that it reproduces results with map()
    if distance < 0 :
        raise ValueError('distance must be at least 0')

    i1, i2 = tee(iterable)
    padding = [False] * distance
    selected = chain(padding, map(predicate, i1), padding)
    adjacent_to_selected = map(any, windowed(selected, 2 * distance + 1))
    return zip(adjacent_to_selected, i2)

def groupby_transform(iterable, keyfunc = None, valuefunc = None) :
    res = groupby(iterable, keyfunc)
    return ((k, map(valuefunc, g)) for k, g in res) if valuefunc else res

class numeric_range(abc.Sequence, abc.Hashable) :
    _EMPTY_HASH = hash(range(0, 0))

    def __init__(self, *args) :
        argc = len(args)
        if argc == 1 :
            self._stop, = args
            self._start = type(self._stop)(0)
            self._step = type(self._stop - self._start)(1)
        elif argc == 2 :
            self._start, self._stop = args
            self._step = type(self._stop - self._start)(1)
        elif argc == 3 :
            self._start, self._stop, self._step = args
        elif argc == 0 :
            raise TypeError('numeric_range expected at least '
                            '1 argument, got {}'.format(argc))
        else :
            raise TypeError('numeric_range expected at most '
                            '3 arguments, got {}'.format(argc))

        self._zero = type(self._step)(0)
        if self._step == self._zero :
            raise ValueError('numeric_range() arg 3 must not be zero')
        self._growing = self._step > self._zero
        self._init_len()

    def __bool__(self) :
        if self._growing :
            return self._start < self._stop
        else :
            return self._start > self._stop

    def __contains__(self, elem) :
        if self._growing :
            if self._start <= elem < self._stop :
                return (elem - self._start) % self._step == self._zero
        else :
            if self._start >= elem > self._stop :
                return (self._start - elem) % (-self._step) == self._zero

        return False

    def __eq__(self, other) :
        if isinstance(other, numeric_range) :
            empty_self = not bool(self)
            empty_other = not bool(other)
            if empty_self or empty_other :
                return empty_self and empty_other  # True if both empty
            else :
                return (self._start == other._start
                        and self._step == other._step
                        and self._get_by_index(-1) == other._get_by_index(-1))
        else :
            return False

    def __getitem__(self, key) :
        if isinstance(key, int) :
            return self._get_by_index(key)
        elif isinstance(key, slice) :
            step = self._step if key.step is None else key.step * self._step

            if key.start is None or key.start <= -self._len :
                start = self._start
            elif key.start >= self._len :
                start = self._stop
            else:  # -self._len < key.start < self._len
                start = self._get_by_index(key.start)

            if key.stop is None or key.stop >= self._len :
                stop = self._stop
            elif key.stop <= -self._len :
                stop = self._start
            else:  # -self._len < key.stop < self._len
                stop = self._get_by_index(key.stop)

            return numeric_range(start, stop, step)
        else :
            raise TypeError(
                'numeric range indices must be '
                'integers or slices, not {}'.format(type(key).__name__))

    def __hash__(self) :
        if self :
            return hash((self._start, self._get_by_index(-1), self._step))
        else :
            return self._EMPTY_HASH

    def __iter__(self) :
        values = (self._start + (n * self._step) for n in count())
        if self._growing :
            return takewhile(partial(gt, self._stop), values)
        else :
            return takewhile(partial(lt, self._stop), values)

    def __len__(self) :
        return self._len

    def _init_len(self) :
        if self._growing :
            start = self._start
            stop = self._stop
            step = self._step
        else :
            start = self._stop
            stop = self._start
            step = -self._step
        distance = stop - start
        if distance <= self._zero :
            self._len = 0
        else:  # distance > 0 and step > 0: regular euclidean division
            q, r = divmod(distance, step)
            self._len = int(q) + int(r != self._zero)

    def __reduce__(self) :
        return numeric_range, (self._start, self._stop, self._step)

    def __repr__(self) :
        if self._step == 1 :
            return "numeric_range({}, {})".format(repr(self._start),
                                                  repr(self._stop))
        else :
            return "numeric_range({}, {}, {})".format(repr(self._start),
                                                      repr(self._stop),
                                                      repr(self._step))

    def __reversed__(self) :
        return iter(numeric_range(self._get_by_index(-1),
                                  self._start - self._step, -self._step))

    def count(self, value) :
        return int(value in self)

    def index(self, value) :
        if self._growing :
            if self._start <= value < self._stop :
                q, r = divmod(value - self._start, self._step)
                if r == self._zero :
                    return int(q)
        else :
            if self._start >= value > self._stop :
                q, r = divmod(self._start - value, -self._step)
                if r == self._zero :
                    return int(q)

        raise ValueError("{} is not in numeric range".format(value))

    def _get_by_index(self, i) :
        if i < 0 :
            i += self._len
        if i < 0 or i >= self._len :
            raise IndexError("numeric range object index out of range")
        return self._start + i * self._step

def count_cycle(iterable, n = None) :
    iterable = tuple(iterable)
    if not iterable :
        return iter(())
    counter = count() if n is None else range(n)
    return ((i, item) for i in counter for item in iterable)

def locate(iterable, pred = bool, window_size = None) :
    if window_size is None :
        return compress(count(), map(pred, iterable))

    if window_size < 1 :
        raise ValueError('window size must be at least 1')

    it = windowed(iterable, window_size, fillvalue = _marker)
    return compress(count(), starmap(pred, it))

def lstrip(iterable, pred) : return dropwhile(pred, iterable)

def rstrip(iterable, pred) :
    cache = []
    cache_append = cache.append
    cache_clear = cache.clear
    for x in iterable :
        if pred(x) :
            cache_append(x)
        else :
            yield from cache
            cache_clear()
            yield x

def strip(iterable, pred) : return rstrip(lstrip(iterable, pred), pred)

class islice_extended :
    def __init__(self, iterable, *args) :
        it = iter(iterable)
        if args :
            self._iterable = _islice_helper(it, slice(*args))
        else :
            self._iterable = it

    def __iter__(self) :
        return self

    def __next__(self) :
        return next(self._iterable)

    def __getitem__(self, key) :
        if isinstance(key, slice) :
            return islice_extended(_islice_helper(self._iterable, key))

        raise TypeError('islice_extended.__getitem__ argument must be a slice')

def _islice_helper(it, s) :
    start = s.start
    stop = s.stop
    if s.step == 0 :
        raise ValueError('step argument must be a non-zero integer or None.')
    step = s.step or 1

    if step > 0 :
        start = 0 if (start is None) else start

        if start < 0 :
            # Consume all but the last -start items
            cache = deque(enumerate(it, 1), maxlen = -start)
            len_iter = cache[-1][0] if cache else 0

            # Adjust start to be positive
            i = max(len_iter + start, 0)

            # Adjust stop to be positive
            if stop is None :
                j = len_iter
            elif stop >= 0 :
                j = min(stop, len_iter)
            else :
                j = max(len_iter + stop, 0)

            # Slice the cache
            n = j - i
            if n <= 0 :
                return

            for index, item in islice(cache, 0, n, step) :
                yield item
        elif (stop is not None) and (stop < 0) :
            # Advance to the start position
            next(islice(it, start, start), None)

            # When stop is negative, we have to carry -stop items while
            # iterating
            cache = deque(islice(it, -stop), maxlen = -stop)

            for index, item in enumerate(it) :
                cached_item = cache.popleft()
                if index % step == 0 :
                    yield cached_item
                cache.append(item)
        else :
            # When both start and stop are positive we have the normal case
            yield from islice(it, start, stop, step)
    else :
        start = -1 if (start is None) else start

        if (stop is not None) and (stop < 0) :
            # Consume all but the last items
            n = -stop - 1
            cache = deque(enumerate(it, 1), maxlen = n)
            len_iter = cache[-1][0] if cache else 0

            # If start and stop are both negative they are comparable and
            # we can just slice. Otherwise we can adjust start to be negative
            # and then slice.
            if start < 0 :
                i, j = start, stop
            else :
                i, j = min(start - len_iter, -1), None

            for index, item in list(cache)[i:j:step] :
                yield item
        else :
            # Advance to the stop position
            if stop is not None :
                m = stop + 1
                next(islice(it, m, m), None)

            # stop is positive, so if start is negative they are not comparable
            # and we need the rest of the items.
            if start < 0 :
                i = start
                n = None
            # stop is None and start is positive, so we just need items up to
            # the start index.
            elif stop is None :
                i = None
                n = start + 1
            # Both stop and start are positive, so they are comparable.
            else :
                i = None
                n = start - stop
                if n <= 0 :
                    return

            cache = list(islice(it, n))

            yield from cache[i::step]

def always_reversible(iterable) :
    try :
        return reversed(iterable)
    except TypeError :
        return reversed(list(iterable))

def consecutive_groups(iterable, ordering = lambda x: x) :
    for k, g in groupby(
        enumerate(iterable), key = lambda x: x[0] - ordering(x[1])
    ) :
        yield map(itemgetter(1), g)

def difference(iterable, func = sub, *, initial = None) :
    a, b = tee(iterable)
    try :
        first = [next(b)]
    except StopIteration :
        return iter([])

    if initial is not None :
        first = []

    return chain(first, starmap(func, zip(b, a)))

class SequenceView(Sequence) :

    def __init__(self, target) :
        if not isinstance(target, Sequence) :
            raise TypeError
        self._target = target

    def __getitem__(self, index) :
        return self._target[index]

    def __len__(self) :
        return len(self._target)

    def __repr__(self) :
        return '{}({})'.format(self.__class__.__name__, repr(self._target))

class seekable :

    def __init__(self, iterable, maxlen = None) :
        self._source = iter(iterable)
        if maxlen is None :
            self._cache = []
        else :
            self._cache = deque([], maxlen)
        self._index = None

    def __iter__(self) :
        return self

    def __next__(self) :
        if self._index is not None :
            try :
                item = self._cache[self._index]
            except IndexError :
                self._index = None
            else :
                self._index += 1
                return item

        item = next(self._source)
        self._cache.append(item)
        return item

    def elements(self) :
        return SequenceView(self._cache)

    def seek(self, index) :
        self._index = index
        remainder = index - len(self._cache)
        if remainder > 0 :
            consume(self, remainder)

class run_length :

    @staticmethod
    def encode(iterable) :
        return ((k, ilen(g)) for k, g in groupby(iterable))

    @staticmethod
    def decode(iterable) :
        return chain.from_iterable(repeat(k, n) for k, n in iterable)

def exactly_n(iterable, n, predicate = bool) : return len(take(n + 1, filter(predicate, iterable))) == n

def circular_shifts(iterable) :
    lst = list(iterable)
    return take(len(lst), windowed(cycle(lst), len(lst)))

def make_decorator(wrapping_func, result_index = 0) :
    # See https://sites.google.com/site/bbayles/index/decorator_factory for
    # notes on how this works.
    def decorator(*wrapping_args, **wrapping_kwargs) :
        def outer_wrapper(f) :
            def inner_wrapper(*args, **kwargs) :
                result = f(*args, **kwargs)
                wrapping_args_ = list(wrapping_args)
                wrapping_args_.insert(result_index, result)
                return wrapping_func(*wrapping_args_, **wrapping_kwargs)
            return inner_wrapper
        return outer_wrapper
    return decorator

def map_reduce(iterable, keyfunc, valuefunc = None, reducefunc = None) :
    valuefunc = (lambda x: x) if (valuefunc is None) else valuefunc

    ret = defaultdict(list)
    for item in iterable :
        key = keyfunc(item)
        value = valuefunc(item)
        ret[key].append(value)

    if reducefunc is not None :
        for key, value_list in ret.items() :
            ret[key] = reducefunc(value_list)

    ret.default_factory = None
    return ret

def rlocate(iterable, pred = bool, window_size = None) :
    if window_size is None :
        try :
            len_iter = len(iterable)
            return (len_iter - i - 1 for i in locate(reversed(iterable), pred))
        except TypeError :
            pass

    return reversed(list(locate(iterable, pred, window_size)))

def replace(iterable, pred, substitutes, count = None, window_size = 1) :
    if window_size < 1 :
        raise ValueError('window_size must be at least 1')

    # Save the substitutes iterable, since it's used more than once
    substitutes = tuple(substitutes)

    # Add padding such that the number of windows matches the length of the
    # iterable
    it = chain(iterable, [_marker] * (window_size - 1))
    windows = windowed(it, window_size)

    n = 0
    for w in windows :
        # If the current window matches our predicate (and we haven't hit
        # our maximum number of replacements), splice in the substitutes
        # and then consume the following windows that overlap with this one.
        # For example, if the iterable is (0, 1, 2, 3, 4...)
        # and the window size is 2, we have (0, 1), (1, 2), (2, 3)...
        # If the predicate matches on (0, 1), we need to zap (0, 1) and (1, 2)
        if pred(*w) :
            if (count is None) or (n < count) :
                n += 1
                yield from substitutes
                consume(windows, window_size - 1)
                continue

        # If there was no match (or we've reached the replacement limit),
        # yield the first item from the window.
        if w and (w[0] is not _marker) :
            yield w[0]

def partitions(iterable) :
    sequence = list(iterable)
    n = len(sequence)
    for i in powerset(range(1, n)) :
        yield [sequence[i:j] for i, j in zip((0,) + i, i + (n,))]

def set_partitions(iterable, k = None) :
    L = list(iterable)
    n = len(L)
    if k is not None :
        if k < 1 :
            raise ValueError(
                "Can't partition in a negative or zero number of groups"
            )
        elif k > n :
            return

    def set_partitions_helper(L, k) :
        n = len(L)
        if k == 1 :
            yield [L]
        elif n == k :
            yield [[s] for s in L]
        else :
            e, *M = L
            for p in set_partitions_helper(M, k - 1) :
                yield [[e], *p]
            for p in set_partitions_helper(M, k) :
                for i in range(len(p)) :
                    yield p[:i] + [[e] + p[i]] + p[i + 1 :]

    if k is None :
        for k in range(1, n + 1) :
            yield from set_partitions_helper(L, k)
    else :
        yield from set_partitions_helper(L, k)

def time_limited(limit_seconds, iterable) :
    if limit_seconds < 0 :
        raise ValueError('limit_seconds must be positive')

    start_time = monotonic()
    for item in iterable :
        if monotonic() - start_time > limit_seconds :
            break
        yield item

def only(iterable, default = None, too_long = None) :
    it = iter(iterable)
    first_value = next(it, default)

    try :
        second_value = next(it)
    except StopIteration :
        pass
    else :
        msg = (
            'Expected exactly one item in iterable, but got {!r}, {!r}, '
            'and perhaps more.'.format(first_value, second_value)
        )
        raise too_long or ValueError(msg)

    return first_value

def ichunked(iterable, n) :
    source = iter(iterable)

    while True :
        # Check to see whether we're at the end of the source iterable
        item = next(source, _marker)
        if item is _marker :
            return

        # Clone the source and yield an n-length slice
        source, it = tee(chain([item], source))
        yield islice(it, n)

        # Advance the source iterable
        consume(source, n)

def distinct_combinations(iterable, r) :
    if r < 0 :
        raise ValueError('r must be non-negative')
    elif r == 0 :
        yield ()
    else :
        pool = tuple(iterable)
        for i, prefix in unique_everseen(enumerate(pool), key = itemgetter(1)) :
            for suffix in distinct_combinations(pool[i + 1 :], r - 1) :
                yield (prefix,) + suffix

def filter_except(validator, iterable, *exceptions) :
    exceptions = tuple(exceptions)
    for item in iterable :
        try :
            validator(item)
        except exceptions :
            pass
        else :
            yield item

def map_except(function, iterable, *exceptions) :
    exceptions = tuple(exceptions)
    for item in iterable :
        try :
            yield function(item)
        except exceptions :
            pass

def _sample_unweighted(iterable, k) :
    # Implementation of "Algorithm L" from the 1994 paper by Kim-Hung Li :
    # "Reservoir-Sampling Algorithms of Time Complexity O(n(1+log(N/n)))".

    # Fill up the reservoir (collection of samples) with the first `k` samples
    reservoir = take(k, iterable)

    # Generate random number that's the largest in a sample of k U(0,1) numbers
    # Largest order statistic: https://en.wikipedia.org/wiki/Order_statistic
    W = exp(log(random()) / k)

    # The number of elements to skip before changing the reservoir is a random
    # number with a geometric distribution. Sample it using random() and logs.
    next_index = k + floor(log(random()) / log(1 - W))

    for index, element in enumerate(iterable, k) :

        if index == next_index :
            reservoir[randrange(k)] = element
            # The new W is the largest in a sample of k U(0, `old_W`) numbers
            W *= exp(log(random()) / k)
            next_index += floor(log(random()) / log(1 - W)) + 1

    return reservoir

def _sample_weighted(iterable, k, weights) :
    # Implementation of "A-ExpJ" from the 2006 paper by Efraimidis et al.  :
    # "Weighted random sampling with a reservoir".

    # Log-transform for numerical stability for weights that are small/large
    weight_keys = (log(random()) / weight for weight in weights)

    # Fill up the reservoir (collection of samples) with the first `k`
    # weight-keys and elements, then heapify the list.
    reservoir = take(k, zip(weight_keys, iterable))
    heapify(reservoir)

    # The number of jumps before changing the reservoir is a random variable
    # with an exponential distribution. Sample it using random() and logs.
    smallest_weight_key, _ = reservoir[0]
    weights_to_skip = log(random()) / smallest_weight_key

    for weight, element in zip(weights, iterable) :
        if weight >= weights_to_skip :
            # The notation here is consistent with the paper, but we store
            # the weight-keys in log-space for better numerical stability.
            smallest_weight_key, _ = reservoir[0]
            t_w = exp(weight * smallest_weight_key)
            r_2 = uniform(t_w, 1)  # generate U(t_w, 1)
            weight_key = log(r_2) / weight
            heapreplace(reservoir, (weight_key, element))
            smallest_weight_key, _ = reservoir[0]
            weights_to_skip = log(random()) / smallest_weight_key
        else :
            weights_to_skip -= weight

    # Equivalent to [element for weight_key, element in sorted(reservoir)]
    return [heappop(reservoir)[1] for _ in range(k)]

def sample(iterable, k, weights = None) :
    if k == 0 :
        return []

    iterable = iter(iterable)
    if weights is None :
        return _sample_unweighted(iterable, k)
    else :
        weights = iter(weights)
        return _sample_weighted(iterable, k, weights)

def take(n, iterable) : return list(islice(iterable, n))

def tabulate(function, start = 0) : return map(function, count(start))

def tail(n, iterable) : return iter(deque(iterable, maxlen = n))

def consume(iterator, n = None) :
    # Use functions that consume iterators at C speed.
    if n is None :
        # feed the entire iterator into a zero-length deque
        deque(iterator, maxlen = 0)
    else :
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)

def nth(iterable, n, default = None) : return next(islice(iterable, n, None), default)

def all_equal(iterable) :
    g = groupby(iterable)
    return next(g, True) and not next(g, False)

def quantify(iterable, pred = bool) : return sum(map(pred, iterable))

def padnone(iterable) : return chain(iterable, repeat(None))

def ncycles(iterable, n) : return chain.from_iterable(repeat(tuple(iterable), n))

def dotproduct(vec1, vec2) : return sum(map(operator.mul, vec1, vec2))

def flatten(listOfLists) : return chain.from_iterable(listOfLists)

def repeatfunc(func, times = None, *args) :
    if times is None :
        return starmap(func, repeat(args))
    return starmap(func, repeat(args, times))

def pairwise(iterable) :
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def grouper(iterable, n, fillvalue = None) :
    if isinstance(iterable, int) :
        warnings.warn(
            "grouper expects iterable as first parameter", DeprecationWarning
        )
        n, iterable = iterable, n
    args = [iter(iterable)] * n
    return zip_longest(fillvalue = fillvalue, *args)

def roundrobin(*iterables) :
    # Recipe credited to George Sakkis
    pending = len(iterables)
    nexts = cycle(iter(it).__next__ for it in iterables)
    while pending :
        try :
            for next in nexts :
                yield next()
        except StopIteration :
            pending -= 1
            nexts = cycle(islice(nexts, pending))

def partition(pred, iterable) :
    if pred is None :
        pred = bool

    evaluations = ((pred(x), x) for x in iterable)
    t1, t2 = tee(evaluations)
    return (
        (x for (cond, x) in t1 if not cond),
        (x for (cond, x) in t2 if cond),
    )

def powerset(iterable) :
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

def unique_everseen(iterable, key = None) :
    seenset = set()
    seenset_add = seenset.add
    seenlist = []
    seenlist_add = seenlist.append
    iterable, keys = tee(iterable)
    for element, k in zip(iterable, map(key, keys) if key else keys) :
        try :
            if k not in seenset :
                seenset_add(k)
                yield element
        except TypeError :
            if k not in seenlist :
                seenlist_add(k)
                yield element

def unique_justseen(iterable, key = None) : return map(next, map(operator.itemgetter(1), groupby(iterable, key)))

def iter_except(func, exception, first = None) :
    try :
        if first is not None :
            yield first()
        while 1 :
            yield func()
    except exception :
        pass

def first_true(iterable, default = None, pred = None) : return next(filter(pred, iterable), default)

def random_product(*args, repeat = 1) :
    pools = [tuple(pool) for pool in args] * repeat
    return tuple(choice(pool) for pool in pools)

def random_permutation(iterable, r = None) :
    pool = tuple(iterable)
    r = len(pool) if r is None else r
    return tuple(sample(pool, r))

def random_combination(iterable, r) :
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(sample(range(n), r))
    return tuple(pool[i] for i in indices)

def random_combination_with_replacement(iterable, r) :
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(randrange(n) for i in range(r))
    return tuple(pool[i] for i in indices)

def nth_combination(iterable, r, index) :
    pool = tuple(iterable)
    n = len(pool)
    if (r < 0) or (r > n) :
        raise ValueError

    c = 1
    k = min(r, n - r)
    for i in range(1, k + 1) :
        c = c * (n - k + i) // i

    if index < 0 :
        index += c

    if (index < 0) or (index >= c) :
        raise IndexError

    result = []
    while r :
        c, n, r = c * r // n, n - 1, r - 1
        while index >= c :
            index -= c
            c, n = c * (n - r) // n, n - 1
        result.append(pool[-1 - n])

    return tuple(result)

def prepend(value, iterator) : return chain([value], iterator)
