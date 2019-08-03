# -*- coding: utf-8 -*-  
import sys, os; sys.path.append(os.path.realpath(__file__ + '/../'));
import re

class Str(str) :

    def getRaw(self) :
        return str(self)

    def __add__(self, value) :
        '''Return self+value.'''
        '''NOT IN PLACE'''
        return Str(str.__add__(self, value))

    def copy(self) :
        raise

    def concat(self, value) :
        '''IN PLACE'''
        raise

    def format(self, *args, **kwargs) :
        '''NOT IN PLACE'''
        return Str(str.format(self, *args, **kwargs))

    def len(self) :
        return len(self)

    def join(self, str_list) :
        '''NOT IN PLACE'''
        from List import List
        if type(str_list) not in [ list, List ] :
            raise Exception('Unexpected type of str_list: {}'.format(str_list))
        return Str(str.join(self, str_list))

    def split(self, sep) :
        from List import List
        if type(sep) not in [ str, Str ] :
            raise Exception('Unexpected type of sep: {}'.format(sep))
        return List(str.split(self, sep))

    def strip(self, string, left = True, right = True) :
        '''IN PLACE'''



        if type(string) not in [ str, Str ] :
            raise Exception('Unexpected type of string: {}'.format(string))
        if not left and right : 
            return Str(str.rstrip(self, string))
        elif not right and left :
            return Str(str.lstrip(self, string))
        elif left and right :
            return Str(str.strip(self, string))
        else :
            raise Exception('Unexpected left{} and right{}'.format(left, right))

    def findall(self, pattern) :
        '''Return a list of all non-overlapping matches in the string.
        If one or more capturing groups are present in the pattern, return
        a list of groups; this will be a list of tuples if the pattern
        has more than one group.
        Empty matches are included in the result.'''
        return re.findall()

    def match(self) :
        raise

    def search(self, reverse = False) :
        raise

    # def replace(self, reverse = False) :
    #     raise

    def count(self) :
        raise

    def index(self, reverse = False) :
        raise

    def find(self, reverse = False) :
        raise

    def finditer(self) :
        raise

    def safe(self) :
        raise

    # def safe_print(stream, st, encoding = 'utf-8') :
    #     for ch in st :
    #         if ord(ch) < 128 : stream.write(ch)
    #         else : 
    #             # try :
    #                 # stream.write(ch.encode(encoding))
    #             # except(Exception, e) :
    #             stream.write(ch)
    #     stream.flush()

    def safe_print(self) :
        raise

    # def unicode_to_url_hex(st) :
    #     res = ''
    #     for ch in st :
    #         if ch == ' ' :
    #             res += '%20'
    #         elif ord(ch) <= 128 :
    #             res += ch
    #         else :
    #             res += hex(ord(ch)).upper().replace('0X', '%u')
    #     return res

    # def __format__(self) :
        '''S.__format__(format_spec) -> str
        Return a formatted version of S as described by format_spec.'''
        # return str.__str__(self)

    # def __str__(self) :
        '''Return str(self).'''
        # return 'Str\'{}\''.format(str.__str__(self))

    # ===============================================================

    # def __contains__(self) :
        '''
        Return key in self.
        '''

    # def __dir__(self) :
        '''
        __dir__() -> list
        default dir() implementation
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

    # def __getitem__(self) :
        '''
        Return self[key].
        '''

    # def __getnewargs__(self) :
        '''
        None
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

    # def __mod__(self) :
        '''
        Return self%value.
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

    # def __rmod__(self) :
        '''
        Return value%self.
        '''

    # def __rmul__(self) :
        '''
        Return self*value.
        '''

    # def __setattr__(self) :
        '''
        Implement setattr(self, name, value).
        '''

    # def __sizeof__(self) :
        '''
        S.__sizeof__() -> size of S in memory, in bytes
        '''

    # def __subclasshook__(self) :
        '''
        Abstract classes can override this to customize issubclass().

        This is invoked early on by abc.ABCMeta.__subclasscheck__().
        It should return True, False or NotImplemented.  If it returns
        NotImplemented, the normal algorithm is used.  Otherwise, it
        overrides the normal algorithm (and the outcome is cached).

        '''

    # def capitalize(self) :
        '''
        S.capitalize() -> str

        Return a capitalized version of S, i.e. make the first character
        have upper case and the rest lower case.
        '''

    # def casefold(self) :
        '''
        S.casefold() -> str

        Return a version of S suitable for caseless comparisons.
        '''

    # def center(self) :
        '''
        S.center(width[, fillchar]) -> str

        Return S centered in a string of length width. Padding is
        done using the specified fill character (default is a space)
        '''

    # def count(self) :
        '''
        S.count(sub[, start[, end]]) -> int

        Return the number of non-overlapping occurrences of substring sub in
        string S[start:end].  Optional arguments start and end are
        interpreted as in slice notation.
        '''

    # def encode(self) :
        '''
        S.encode(encoding='utf-8', errors='strict') -> bytes

        Encode S using the codec registered for encoding. Default encoding
        is 'utf-8'. errors may be given to set a different error
        handling scheme. Default is 'strict' meaning that encoding errors raise
        a UnicodeEncodeError. Other possible values are 'ignore', 'replace' and
        'xmlcharrefreplace' as well as any other name registered with
        codecs.register_error that can handle UnicodeEncodeErrors.
        '''

    # def endswith(self) :
        '''
        S.endswith(suffix[, start[, end]]) -> bool

        Return True if S ends with the specified suffix, False otherwise.
        With optional start, test S beginning at that position.
        With optional end, stop comparing S at that position.
        suffix can also be a tuple of strings to try.
        '''

    # def expandtabs(self) :
        '''
        S.expandtabs(tabsize=8) -> str

        Return a copy of S where all tab characters are expanded using spaces.
        If tabsize is not given, a tab size of 8 characters is assumed.
        '''

    # def find(self) :
        '''
        S.find(sub[, start[, end]]) -> int

        Return the lowest index in S where substring sub is found,
        such that sub is contained within S[start:end].  Optional
        arguments start and end are interpreted as in slice notation.

        Return -1 on failure.
        '''

    # def format(self) :
        '''
        S.format(*args, **kwargs) -> str

        Return a formatted version of S, using substitutions from args and kwargs.
        The substitutions are identified by braces ('{' and '}').
        '''

    # def format_map(self) :
        '''
        S.format_map(mapping) -> str

        Return a formatted version of S, using substitutions from mapping.
        The substitutions are identified by braces ('{' and '}').
        '''

    # def index(self) :
        '''
        S.index(sub[, start[, end]]) -> int

        Return the lowest index in S where substring sub is found, 
        such that sub is contained within S[start:end].  Optional
        arguments start and end are interpreted as in slice notation.

        Raises ValueError when the substring is not found.
        '''

    # def isalnum(self) :
        '''
        S.isalnum() -> bool

        Return True if all characters in S are alphanumeric
        and there is at least one character in S, False otherwise.
        '''

    # def isalpha(self) :
        '''
        S.isalpha() -> bool

        Return True if all characters in S are alphabetic
        and there is at least one character in S, False otherwise.
        '''

    # def isdecimal(self) :
        '''
        S.isdecimal() -> bool

        Return True if there are only decimal characters in S,
        False otherwise.
        '''

    # def isdigit(self) :
        '''
        S.isdigit() -> bool

        Return True if all characters in S are digits
        and there is at least one character in S, False otherwise.
        '''

    # def isidentifier(self) :
        '''
        S.isidentifier() -> bool

        Return True if S is a valid identifier according
        to the language definition.

        Use keyword.iskeyword() to test for reserved identifiers
        such as "def" and "class".

        '''

    # def islower(self) :
        '''
        S.islower() -> bool

        Return True if all cased characters in S are lowercase and there is
        at least one cased character in S, False otherwise.
        '''

    # def isnumeric(self) :
        '''
        S.isnumeric() -> bool

        Return True if there are only numeric characters in S,
        False otherwise.
        '''

    # def isprintable(self) :
        '''
        S.isprintable() -> bool

        Return True if all characters in S are considered
        printable in repr() or S is empty, False otherwise.
        '''

    # def isspace(self) :
        '''
        S.isspace() -> bool

        Return True if all characters in S are whitespace
        and there is at least one character in S, False otherwise.
        '''

    # def istitle(self) :
        '''
        S.istitle() -> bool

        Return True if S is a titlecased string and there is at least one
        character in S, i.e. upper- and titlecase characters may only
        follow uncased characters and lowercase characters only cased ones.
        Return False otherwise.
        '''

    # def isupper(self) :
        '''
        S.isupper() -> bool

        Return True if all cased characters in S are uppercase and there is
        at least one cased character in S, False otherwise.
        '''

    # def join(self) :
        '''
        S.join(iterable) -> str

        Return a string which is the concatenation of the strings in the
        iterable.  The separator between elements is S.
        '''

    # def ljust(self) :
        '''
        S.ljust(width[, fillchar]) -> str

        Return S left-justified in a Unicode string of length width. Padding is
        done using the specified fill character (default is a space).
        '''

    # def lower(self) :
        '''
        S.lower() -> str

        Return a copy of the string S converted to lowercase.
        '''

    # def lstrip(self) :
        '''
        S.lstrip([chars]) -> str

        Return a copy of the string S with leading whitespace removed.
        If chars is given and not None, remove characters in chars instead.
        '''

    # def maketrans(self) :
        '''
        Return a translation table usable for str.translate().

        If there is only one argument, it must be a dictionary mapping Unicode
        ordinals (integers) or characters to Unicode ordinals, strings or None.
        Character keys will be then converted to ordinals.
        If there are two arguments, they must be strings of equal length, and
        in the resulting dictionary, each character in x will be mapped to the
        character at the same position in y. If there is a third argument, it
        must be a string, whose characters will be mapped to None in the result.
        '''

    # def partition(self) :
        '''
        S.partition(sep) -> (head, sep, tail)

        Search for the separator sep in S, and return the part before it,
        the separator itself, and the part after it.  If the separator is not
        found, return S and two empty strings.
        '''

    # def replace(self) :
        '''
        S.replace(old, new[, count]) -> str

        Return a copy of S with all occurrences of substring
        old replaced by new.  If the optional argument count is
        given, only the first count occurrences are replaced.
        '''

    # def rfind(self) :
        '''
        S.rfind(sub[, start[, end]]) -> int

        Return the highest index in S where substring sub is found,
        such that sub is contained within S[start:end].  Optional
        arguments start and end are interpreted as in slice notation.

        Return -1 on failure.
        '''

    # def rindex(self) :
        '''
        S.rindex(sub[, start[, end]]) -> int

        Return the highest index in S where substring sub is found,
        such that sub is contained within S[start:end].  Optional
        arguments start and end are interpreted as in slice notation.

        Raises ValueError when the substring is not found.
        '''

    # def rjust(self) :
        '''
        S.rjust(width[, fillchar]) -> str

        Return S right-justified in a string of length width. Padding is
        done using the specified fill character (default is a space).
        '''

    # def rpartition(self) :
        '''
        S.rpartition(sep) -> (head, sep, tail)

        Search for the separator sep in S, starting at the end of S, and return
        the part before it, the separator itself, and the part after it.  If the
        separator is not found, return two empty strings and S.
        '''

    # def rsplit(self) :
        '''
        S.rsplit(sep=None, maxsplit=-1) -> list of strings

        Return a list of the words in S, using sep as the
        delimiter string, starting at the end of the string and
        working to the front.  If maxsplit is given, at most maxsplit
        splits are done. If sep is not specified, any whitespace string
        is a separator.
        '''

    # def rstrip(self) :
        '''
        S.rstrip([chars]) -> str

        Return a copy of the string S with trailing whitespace removed.
        If chars is given and not None, remove characters in chars instead.
        '''

    # def split(self) :
        '''
        S.split(sep=None, maxsplit=-1) -> list of strings

        Return a list of the words in S, using sep as the
        delimiter string.  If maxsplit is given, at most maxsplit
        splits are done. If sep is not specified or is None, any
        whitespace string is a separator and empty strings are
        removed from the result.
        '''

    # def splitlines(self) :
        '''
        S.splitlines([keepends]) -> list of strings

        Return a list of the lines in S, breaking at line boundaries.
        Line breaks are not included in the resulting list unless keepends
        is given and true.
        '''

    # def startswith(self) :
        '''
        S.startswith(prefix[, start[, end]]) -> bool

        Return True if S starts with the specified prefix, False otherwise.
        With optional start, test S beginning at that position.
        With optional end, stop comparing S at that position.
        prefix can also be a tuple of strings to try.
        '''

    # def strip(self) :
        '''
        S.strip([chars]) -> str

        Return a copy of the string S with leading and trailing
        whitespace removed.
        If chars is given and not None, remove characters in chars instead.
        '''

    # def swapcase(self) :
        '''
        S.swapcase() -> str

        Return a copy of S with uppercase characters converted to lowercase
        and vice versa.
        '''

    # def title(self) :
        '''
        S.title() -> str

        Return a titlecased version of S, i.e. words start with title case
        characters, all remaining cased characters have lower case.
        '''

    # def translate(self) :
        '''
        S.translate(table) -> str

        Return a copy of the string S in which each character has been mapped
        through the given translation table. The table must implement
        lookup/indexing via __getitem__, for instance a dictionary or list,
        mapping Unicode ordinals to Unicode ordinals, strings, or None. If
        this operation raises LookupError, the character is left untouched.
        Characters mapped to None are deleted.
        '''

    # def upper(self) :
        '''
        S.upper() -> str

        Return a copy of S converted to uppercase.
        '''

    # def zfill(self) :
        '''
        S.zfill(width) -> str

        Pad a numeric string S with zeros on the left, to fill a field
        of the specified width. The string S is never truncated.
        '''