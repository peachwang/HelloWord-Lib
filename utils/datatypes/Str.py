# -*- coding: utf-8 -*-  
import re
from ..shared import *
# ListDiff: 以 item 作为最小比较单元。降维后可用于StrDiff

# https://docs.python.org/3/library/re.html

SRE_MATCH_TYPE = type(re.match('', ''))

@add_print_func
class _Pattern :

    def __init__(self, pattern, /) : self._pattern = pattern

    def get_raw(self) : return self._pattern

    @cached_prop
    def string(self) : return Str(self._pattern.pattern)

    def __format__(self, spec) : return f'{self._pattern.pattern:{spec}}'

    def __str__(self) : return f'_Pattern({self._pattern.pattern!s})'

    def __repr__(self) : return f'_Pattern({self._pattern!r})'

    # The regex matching flags. This is a combination of the flags given to compile(),
    # any (?...) inline flags in the pattern, and implicit flags such as UNICODE if the
    # pattern is a Unicode string.
    @cached_prop
    def flags(self) : return self._pattern.flags

    # The number of capturing groups in the pattern.
    @cached_prop
    def group_num(self) : return self._pattern.groups
    
    # A dictionary mapping any symbolic group names defined by (?P<id>) to group numbers.
    # The dictionary is empty if no symbolic groups were used in the pattern.
    def group_index(self, name: str, /) : return self._pattern.groupindex[name]


@add_print_func
class _Match :

    _no_value = object()

    def __init__(self, match, /) :
        self._pattern       = _Pattern(match.re)
        self._match         = match

    def get_raw(self) : return self._match

    @cached_prop
    def pattern(self) : return self._pattern

    # The string passed to match() or search().
    @cached_prop
    def string(self) : return Str(self._match.string)

    def __format__(self, spec) : return f'{self.whole_match:{spec}}'
    
    def __str__(self) : return f'_Match(whole_match = [{self.whole_match}], named = {self.named_group_dict()}, indexed = {self.all_group_tuple()}, span = {self.span_of_group(0)}, pattern = [{self._pattern}], string = [{self._match.string}])'

    def __repr__(self) : return f'_Match({self._match!r})'

    @cached_prop
    def whole_match(self) : return Str(self._match.group())

    def __getattr__(self, name) : return self.named_group_dict()[name]
    
    def __getitem__(self, name) : return self.__getattr__(name)

    # Match.expand(template)
    # Return the string obtained by doing backslash substitution on the
    # template string template, as done by the sub() method. Escapes such as \n
    # are converted to the appropriate characters, and numeric backreferences
    # (\1, \2) and named backreferences (\g<1>, \g<name>) are replaced by the
    # contents of the corresponding group.
    # (?P<name>...)
    def format(self, template, /) : return Str(self._match.expand(template))

    def _wrap(self, value, /) : return Str(value) if isinstance(value, str) else value

    # Match.group([group1, ...])
    # Returns one or more subgroups of the match.
    # If there is a single argument, the result is a single string;
    
    # if there are multiple arguments, the result is a tuple with one item per
    # argument.
    
    # Without arguments, group1 defaults to zero (the whole match is returned).
    
    # If a groupN argument is zero, the corresponding return value is the entire
    # matching string;
    
    # if it is in the inclusive range [1..99], it is the string matching the
    # corresponding parenthesized group.
    
    # If a group number is negative or larger than the number of groups defined in
    # the pattern, an IndexError exception is raised.
    
    # If a group is contained in a part of the pattern that did not match, the
    # corresponding result is None.
    
    # If a group is contained in a part of the pattern that matched multiple times,
    # the last match is returned.
    
    # If the regular expression uses the (?P<name>...) syntax, the groupN arguments
    # may also be strings identifying groups by their group name.
    
    # If a string argument is not used as a group name in the pattern, an IndexError
    # exception is raised.

    # Named groups can also be referred to by their index.
    # (?P<name>...)
    def group_tuple(self, *groups) -> tuple :
        if len(groups) == 0   : raise Exception(f'非法{groups=}')
        elif len(groups) == 1 : _ = self._match.group(groups[0]); return tuple(self._wrap(_))
        else                  : return tuple(self._wrap(_) for _ in self._match.group(*groups))

    def one_group(self, group: Union[int, str], /) : _ = self._match.group(group); return self._wrap(_)

    # Match.__getitem__(g)
    # m[group] <--> m.group(group)
    # This is identical to m.group(group). This allows easier access to an
    # individual group from a match.
    def __getitem__(self, group: Union[int, str]) : return self._wrap(self._match.__getitem__(group))

    # Match.groups(default=None)
    # Return a tuple containing all the subgroups of the match, from 1 up to
    # however many groups(indexed and named!!!) are in the pattern. The default argument is used for
    # groups that did not participate in the match; it defaults to None.
    # (?P<name>...)
    def all_group_tuple(self, *, default = None, ignore_missing = True) -> tuple :
        return tuple(self._wrap(_) for _ in self._match.groups(default) if not ignore_missing or _ != default)

    def only_one_group(self, *, default = _no_value) :
        _ = self.all_group_tuple(ignore_missing = True)
        if len(_) > 1    : raise Exception(f'{self} 中出现不止一个 group')
        elif len(_) == 0 :
            if default == self._no_value : raise Exception(f'{self} 中不存在 group')
            else                         : return self._wrap(default)
        else             : return _[0]

    # Match.groupdict(default=None)
    # Return a dictionary containing all the named subgroups (not indexed!!!) of the match,
    # keyed by the subgroup name. The default argument is used for groups that
    # did not participate in the match; it defaults to None.
    def named_group_dict(self, *, default = None, ignore_missing = True) :
        from .Dict import Dict
        return Dict((key, value) for key, value in self._match.groupdict(default).items() if not ignore_missing or value != default)

    # Match.start([group])
    # Return the indices of the start of the substring matched by group;
    # group defaults to zero (meaning the whole matched substring).
    # Return -1 if group exists but did not contribute to the match.
    # For a match object m, and a group g that did contribute to the match,
    # the substring matched by group g (equivalent to m.group(g)) is
    # m.string[m.start(g):m.end(g)]. Note that m.start(group) will equal
    # m.end(group) if group matched a null string.
    def start_of_group(self, group: Union[int, str], /) -> int : return self._match.start(group)

    # Match.end([group])
    # Return the indices of the end of the substring matched by group;
    def end_of_group(self, group: Union[int, str], /) -> int : return self._match.end(group)

    # Match.span([group])
    # For a match m, return the 2-tuple (m.start(group), m.end(group)).
    # Note that if group did not contribute to the match, this is (-1, -1).
    # group defaults to zero, the entire match.
    def span_of_group(self, group: Union[int, str], /) -> tuple : return self._match.span(group)

    def replace_group(self, group: Union[int, str], repl_str_or_func, /) :
        if self.one_group(group) is None      : return self.string
        if isinstance(repl_str_or_func, str) : replacement = repl_str_or_func
        elif callable(repl_str_or_func)      : replacement = repl_str_or_func(self.one_group(group))
        else                                 : raise CustomTypeError(repl_str_or_func)
        return self.string[ : self.start_of_group(group)] + replacement + self.string[self.end_of_group(group) : ]

@add_print_func
class Str(str) :

    _no_value = object()

    # id(object) -> integer
    # Return the identity of an object.  This is guaranteed to be unique among
    # simultaneously existing objects.  (Hint: it's the object's memory address.)
    def get_id(self) -> int : return hex(id(self))

    def get_raw(self) -> str : return str(self)

    json_serialize = get_raw

    # Implement iter(self).
    def __iter__(self) :
        for char in str.__iter__(self) : yield Str(char)

    # S.__format__(format_spec) -> str
    # Return a formatted version of S as described by format_spec.
    # def __format__(self) : return str.__format__(self)
    
    # S.format(*args, **kwargs) -> str
    # Return a formatted version of S, using substitutions from args and kwargs.
    # The substitutions are identified by braces ('{' and '}').
    # NOT IN PLACE
    def format(self, *args, **kwargs) : return Str(str.format(self, *args, **kwargs))

    # Make object readable
    # Return str(self).
    # def __str__(self) : return f'Str\'{str.__str__(self)}\''
    
    # Required code that reproduces object
    # Return repr(self).
    # def __repr__(self) : return f"Str({str.__repr__(self)})"
    
    # S.center(width[, fillchar]) -> str
    # Return S centered in a string of length width. Padding is
    # done using the specified fill character (default is a space)
    # NOT IN PLACE
    def center(self, width, fillchar = ' ', /) : return Str(str.center(self, width, fillchar))

    # Return self[key].
    def __getitem__(self, index) : return Str(str.__getitem__(self, index))

    # Return self+value.
    # NOT IN PLACE
    def __add__(self, string) : return Str(str.__add__(self, string))

    # Return self*value.
    # NOT IN PLACE
    def __rmul__(self, times) : return Str(str.__rmul__(self, times))

    # NOT IN PLACE
    def concat(self, string, /) : return self.__add__(string)

    # Return len(self).
    def __len__(self) : return str.__len__(self)

    def len(self) : return str.__len__(self)

    @log_entering()
    def is_empty(self) : return self.full_match(r'[ \t\r\n]*')

    def ensure_empty(self) :
        if self.is_empty() : return self
        else              : raise Exception(f'{self=}应该为空串')

    def is_not_empty(self) : return not self.is_empty()

    def ensure_not_empty(self) :
        if self.is_not_empty() : return self
        else                 : raise Exception(f'{self=}应该不为空串')

    def is_in(self, *item_list) : return self in item_list

    def is_not_in(self, *item_list) : return not self.is_in(*item_list)

    # x.__contains__(y) <==> y in x
    # sub: Union[str, Str]
    def __contains__(self, sub, /) : return str.__contains__(self, sub)

    def has(self, sub_or_pattern, /, *, re_mode = False, flags = 0) :
        if not re_mode : return str.__contains__(self, sub_or_pattern)
        else           : return self.count(sub_or_pattern, re_mode = re_mode, flags = flags) > 0

    def has_no(self, sub_or_pattern, /, *, re_mode = False, flags = 0) :
        return not self.has(sub_or_pattern, re_mode = re_mode, flags = flags)

    def has_any_of(self, sub_iterable, /) :
        if not isinstance(sub_iterable, Iterable) : raise CustomTypeError(sub_iterable)
        return any(self.has(sub) for sub in sub_iterable)

    def has_all_of(self, sub_iterable, /) :
        if not isinstance(sub_iterable, Iterable) : raise CustomTypeError(sub_iterable)
        return all(self.has(sub) for sub in sub_iterable)

    def has_none_of(self, sub_iterable, /) :
        if not isinstance(sub_iterable, Iterable) : raise CustomTypeError(sub_iterable)
        return all(self.has_no(sub) for sub in sub_iterable)

    # S.count(sub[, start[, end]]) -> int
    # Return the number of non-overlapping occurrences of substring sub in
    # string S[start:end].  Optional arguments start and end are
    # interpreted as in slice notation.
    def count(self, sub_or_pattern, /, *, start = 0, end = -1, re_mode = False, flags = 0) :
        if re_mode : return self.find_all_match_list(sub_or_pattern, flags = flags).len()
        else       : return str.count(self, sub_or_pattern, start, end)

    # S.index(sub[, start[, end]]) -> int
    # Return the lowest or highest index in S where substring sub is found, 
    # such that sub is contained within S[start:end].  Optional
    # arguments start and end are interpreted as in slice notation.
    # Raises ValueError when the substring is not found.
    def index(self, sub, /, *, start = 0, end = -1, reverse = False) :
        if not reverse : return str.index(self, sub, start, end)
        else           : return str.rindex(self, sub, start, end)

    # S.find(sub[, start[, end]]) -> int
    # Return the lowest or highest index in S where substring sub is found,
    # such that sub is contained within S[start:end].  Optional
    # arguments start and end are interpreted as in slice notation.
    # Return -1 on failure.
    # def find(self, sub, start = 0, end = -1, reverse = False) :
        # if not reverse : return str.find(self, sub, start, end)
        # else           : return str.find(self, sub, start, end)

    # re.match(pattern, string, flags=0)
    # If zero or more characters at the beginning of string match the
    # regular expression pattern, return a corresponding match object.
    # Return None if the string does not match the pattern;
    # note that this is different from a zero-length match.
    # Note that even in MULTILINE mode, re.match() will only match at the
    # beginning of the string and not at the beginning of each line.
    # If you want to locate a match anywhere in string, use search() instead
    @log_entering()
    def left_match(self, pattern, /, *, flags = 0) -> Optional[_Match] : return _Match(re.match(pattern, self, flags)) if _ else None

    def ensure_left_match(self, pattern = None, /, *, flags = 0) :
        if self.left_match(pattern, flags = flags) : return self
        else                                      : raise Exception(f'\n{self=}\n应该左匹配\n{pattern=}')

    # S.startswith(prefix[, start[, end]]) -> bool
    # Return True if S starts with the specified prefix, False otherwise.
    # With optional start, test S beginning at that position.
    # With optional end, stop comparing S at that position.
    # prefix can also be a tuple of strings to try.
    def starts_with(self, *prefixes) : return str.startswith(self, tuple(prefixes))
    
    # S.endswith(suffix[, start[, end]]) -> bool
    # Return True if S ends with the specified suffix, False otherwise.
    # With optional start, test S beginning at that position.
    # With optional end, stop comparing S at that position.
    # suffix can also be a tuple of strings to try.
    def ends_with(self, *suffixes) : return str.endswith(self, tuple(suffixes))
    
    # @Timer.timeit_total('full_match')
    # re.fullmatch(pattern, string, flags=0)
    # If the whole string matches the regular expression pattern,
    # return a corresponding match object. Return None if the string
    # does not match the pattern; note that this is different from
    # a zero-length match.
    def full_match(self, pattern, /, *, flags = 0) -> Optional[_Match] :
        try                           : _ = re.fullmatch(pattern, self, flags)
        except KeyboardInterrupt as e : print(R(f'fullMatch卡住: {self}')); input(); return None
        return _Match(_) if _ else None

    def ensure_full_match(self, pattern = None, /, *, flags = 0) :
        if self.full_match(pattern, flags = flags) : return self
        else                                      : raise Exception(f'\n{self=}\n应该完全匹配\n{pattern=}')

    # re.search(pattern, string, flags=0)
    # Scan through string looking for the first location where the regular
    # expression pattern produces a match, and return a corresponding match
    # object. Return None if no position in the string matches the pattern;
    # note that this is different from finding a zero-length match at some
    # point in the string.
    def search_one_match(self, pattern, /, *, reverse = False, flags = 0) -> Optional[_Match] : return _Match(re.search(pattern, self, flags)) if _ else None

    # re.finditer(pattern, string, flags=0)
    # Return an iterator yielding match objects over all non-overlapping
    # matches for the RE pattern in string. The string is scanned left-to-right,
    # and matches are returned in the order found. Empty matches are included
    # in the result.
    def find_all_match_iter(self, pattern, /, *, flags = 0) : from .Iter import Iter; return Iter(_Match(match) for match in re.finditer(pattern, self, flags))
    
    def find_all_match_list(self, *args, **kwargs) : from .List import List; return List(self.find_all_match_iter(*args, **kwargs))
    
    def only_one_match(self, pattern, /, *, flags = 0, default = _no_value) -> _Match :
        matches = self.find_all_match_list(pattern, flags = flags)
        if matches.len() > 1    : raise Exception(f'[{pattern}] 在 [{self}] 中出现不止一次')
        elif matches.len() == 0 :
            if default != self._no_value : return self._wrap(default)
            else                         : raise Exception(f'[{pattern}] 在 [{self}] 中不存在')
        else                    : return matches[0]

    def only_one_group(self, pattern, /, *, flags = 0, default = _no_value) :
        m = self.only_one_match(pattern, flags = flags, default = default)
        if m == default : return self._wrap(default)
        else            : return m.only_one_group(default = default)

    # re.findall(pattern, string, flags=0)
    # Return all non-overlapping matches of pattern in string,
    # as a list of strings. The string is scanned left-to-right,
    # and matches are returned in the order found. If one or more
    # groups are present in the pattern, return a list of groups;
    # this will be a list of tuples if the pattern has more than
    # one group. Empty matches are included in the result. Non-empty
    # matches can now start just after a previous empty match.
    # def findall(self, pattern, /, *, flags = 0) : from List import List; return List(re.findall(pattern, self, flags))

    # re.sub(pattern, repl, string, count=0, flags=0)
    # Return the string obtained by replacing the leftmost
    # non-overlapping occurrences of pattern in string by the replacement
    # repl. If the pattern isn’t found, string is returned unchanged. repl
    # can be a string or a function; if it is a string, any backslash escapes
    # in it are processed. That is, \n is converted to a single newline
    # character, \r is converted to a carriage return, and so forth. Unknown
    # escapes of ASCII letters are reserved for future use and treated as
    # errors. Other unknown escapes such as \& are left alone. Backreferences,
    # such as \6, are replaced with the substring matched by group 6
    # in the pattern.
    # If repl is a function, it is called for every non-overlapping occurrence
    # of pattern. The function takes a single match object argument, and
    # returns the replacement string.
    # The pattern may be a string or a pattern object.
    # The optional argument count is the maximum number of pattern occurrences
    # to be replaced; count must be a non-negative integer. If omitted or zero,
    # all occurrences will be replaced. Empty matches for the pattern are
    # replaced only when not adjacent to a previous empty match,
    # so sub('x*', '-', 'abxd') returns '-a-b--d-'.
    # In string-type repl arguments, in addition to the character escapes and
    # backreferences described above, \g<name> will use the substring matched
    # by the group named name, as defined by the (?P<name>...) syntax.
    # \g<number> uses the corresponding group number; \g<2> is therefore
    # equivalent to \2, but isn’t ambiguous in a replacement such as \g<2>0.
    # \20 would be interpreted as a reference to group 20, not a reference to
    # group 2 followed by the literal character '0'. The backreference \g<0>
    # substitutes in the entire substring matched by the RE.
    # NOT IN PLACE
    def _sub(self, pattern, repl_str_or_func, /, *, count = 0, flags = 0) :
        return Str(re.sub(pattern, repl_str_or_func, self, count, flags))

    # re.subn(pattern, repl, string, count=0, flags=0)
    # Perform the same operation as sub(), but return a tuple
    # (new_string, number_of_subs_made).
    # NOT IN PLACE
    def _subn(self, pattern, repl_str_or_func, /, *, count = 0, flags = 0) -> tuple :
        _ = re.subn(pattern, repl_str_or_func, self, count, flags)
        return (Str(_[0]), _[1])

    # S.replace(old, new[, count]) -> str
    # Return a copy of S with all occurrences of substring
    # old replaced by new.  If the optional argument count is
    # given, only the first count occurrences are replaced.
    # NOT IN PLACE
    def replace(self, sub_or_pattern, repl_str_or_func, /, *, re_mode: bool, count = None, flags = 0) :
        if re_mode :
            if count is None : return self._sub(sub_or_pattern, repl_str_or_func, flags = flags)
            else             : return self._sub(sub_or_pattern, repl_str_or_func, count = count, flags = flags)
        else       :
            if count is None : return Str(str.replace(self, sub_or_pattern, repl_str_or_func))
            else             : return Str(str.replace(self, sub_or_pattern, repl_str_or_func, count))

    # S.join(iterable) -> str
    # Return a string which is the concatenation of the strings in the
    # iterable.  The separator between elements is S.
    # NOT IN PLACE
    def join(self, item_list_or_iter: list, /) : return Str(str.join(self, [f'{_}' for _ in item_list_or_iter]))
    
    # S.split(sep=None, maxsplit=-1) -> list of strings
    # re.split(pattern, string, maxsplit=0, flags=0)
    # Return a list of the words in S, using sep as the
    # delimiter string.  If maxsplit is given, at most maxsplit
    # splits are done. If sep is not specified or is None, any
    # whitespace string is a separator and empty strings are
    # removed from the result.
    # Split string by the occurrences of pattern. If capturing parentheses
    # are used in pattern, then the text of all groups in the pattern are also
    # returned as part of the resulting list. If maxsplit is nonzero, at most
    # maxsplit splits occur, and the remainder of the string is returned as
    # the final element of the list.
    # >>> re.split(r'(\W+)', 'Words, words, words.')
    # ['Words', ', ', 'words', ', ', 'words', '.', '']
    # If there are capturing groups in the separator and it matches at the
    # start of the string, the result will start with an empty string.
    # The same holds for the end of the string:
    # >>> re.split(r'(\W+)', '...words, words...')
    # ['', '...', 'words', ', ', 'words', '...', '']
    # That way, separator components are always found at the same relative
    # indices within the result list. Empty matches for the pattern split
    # the string only when not adjacent to a previous empty match.
    # >>> re.split(r'\b', 'Words, words, words.')
    # ['', 'Words', ', ', 'words', ', ', 'words', '.']
    # >>> re.split(r'\W*', '...words...')
    # ['', '', 'w', 'o', 'r', 'd', 's', '', '']
    # >>> re.split(r'(\W*)', '...words...')
    # ['', '...', '', '', 'w', '', 'o', '', 'r', '', 'd', '', 's', '...', '', '', '']
    # NOT IN PLACE
    def split(self, sep_or_pattern, /, *, maxsplit: int = None, reverse = False, re_mode = False, flags = 0) :
        from .List import List
        if re_mode :
            if maxsplit is None                               : maxsplit = 0
            if reverse                                        : raise Exception(f'无法通过正则[{sep_or_pattern}]反向切割字符串[{self}]')
            if '(' in sep_or_pattern or ')' in sep_or_pattern : raise Exception(f'暂不支持使用带括号的正则[{sep_or_pattern}]切割字符串[{self}]')
            return List(re.split(sep_or_pattern, self, maxsplit, flags))
        else       :
            if maxsplit is None : maxsplit = -1
            if not reverse      : return List(str.split(self, sep_or_pattern, maxsplit))
            else                : return List(str.rsplit(self, sep_or_pattern, maxsplit))

    # S.rsplit(sep=None, maxsplit=-1) -> list of strings
    # Return a list of the words in S, using sep as the
    # delimiter string, starting at the end of the string and
    # working to the front.  If maxsplit is given, at most maxsplit
    # splits are done. If sep is not specified, any whitespace string
    # is a separator.
    # NOT IN PLACE
    def rsplit(self, sep_or_pattern, /, **kwargs) : return self.split(sep_or_pattern, reverse = True, **kwargs)

    # S.strip([chars]) -> str
    # Return a copy of the string S with leading and trailing whitespace removed.
    # If chars is given and not None, remove characters in chars instead.
    # NOT IN PLACE
    def strip(self, string: str = ' \t\n', /, *, left: bool = True, right: bool = True) :
        if (not left) and right   : return Str(str.rstrip(self, string))
        elif (not right) and left : return Str(str.lstrip(self, string))
        elif left and right       : return Str(str.strip(self, string))
        else                      : raise Exception(f'非法 {left=} 和 {right=}')

    # S.lstrip([chars]) -> str
    # Return a copy of the string S with leading whitespace removed.
    # If chars is given and not None, remove characters in chars instead.
    # NOT IN PLACE
    def lstrip(self, string, /) : return self.strip(string, left = False)

    # S.rstrip([chars]) -> str
    # Return a copy of the string S with trailing whitespace removed.
    # If chars is given and not None, remove characters in chars instead.
    # NOT IN PLACE
    def rstrip(self, string, /) : return self.strip(string, right = False)

    # NOT IN PLACE
    def range(self) :
        from .List import List
        return self.split(r' *, *', re_mode = True).map(
            lambda part : 
                List(range(int(part.split('-')[0]), int(part.split('-')[1]) + 1))
                if part.count('-') == 1
                else List(int(part))
        ).merge()

    # NOT IN PLACE
    def to_url(self) :
        result = Str()
        for char in self :
            if char == ' '        : result += Str('%20')
            elif ord(char) <= 128 : result += Str(char)
            else                  : result += Str(hex(ord(char))).upper().replace('0X', '%u')
        return result

    # S.isdecimal() -> bool
    # Return True if all characters in the string are decimal characters and
    # there is at least one character, False otherwise.
    # Decimal characters are those that can be used to form numbers in base 10,
    # e.g. U+0660, ARABIC-INDIC DIGIT ZERO. Formally a decimal character is
    # a character in the Unicode General Category “Nd”.
    def is_number(self) : return str.isdecimal(self)

    def to_datetime(self, pattern = '%Y-%m-%d %H:%M:%S') : from .DateTime import DateTime; return DateTime(self, pattern)

    def is_int(self) : return self.is_number() and self.has_no('.')

    def ensure_int(self) :
        if self.is_int() : return self
        else            : raise Exception(f'[{self=}]不是整数')

    def to_int(self) -> int : return int(self.ensure_int())

    def is_float(self) : return self.is_number() and self.has('.')

    def ensure_float(self) :
        if self.is_float() : return self
        else              : raise Exception(f'[{self=}]不是浮点数')

    def to_float(self) -> float : return float(self.ensure_float())

    # S.islower() -> bool
    # Return True if all cased characters in S are lowercase and there is
    # at least one cased character in S, False otherwise.
    def is_lower(self) : return str.islower(self)

    # S.isupper() -> bool
    # Return True if all cased characters in S are uppercase and there is
    # at least one cased character in S, False otherwise.
    def is_upper(self) : return str.isupper(self)

    # S.lower() -> str
    # Return a copy of the string S converted to lowercase.
    # NOT IN PLACE
    def to_lower(self) : return Str(str.lower(self))

    # S.upper() -> str
    # Return a copy of S converted to uppercase.
    # NOT IN PLACE
    def to_upper(self) : return Str(str.upper(self))

    # S.title() -> str
    # Return a titlecased version of S, i.e. words start with title case
    # characters, all remaining cased characters have lower case.
    # NOT IN PLACE
    def to_title(self) : return Str(str.title(self))

    # S.capitalize() -> str
    # Return a capitalized version of S, i.e. make the first character
    # have upper case and the rest lower case.
    # NOT IN PLACE
    def to_capitalize(self) : return Str(str.capitalize(self))

    # S.swapcase() -> str
    # Return a copy of S with uppercase characters converted to lowercase
    # and vice versa.
    # NOT IN PLACE
    def swap_case(self) : return Str(str.swapcase(self))

    # S.casefold() -> str
    # Return a version of S suitable for caseless comparisons.
    # NOT IN PLACE
    def fold_case(self) : return Str(str.casefold(self))

    def _split_word_list(self) :
        result = []
        for char in self :
            if len(result) == 0 :
                if char == '_' : continue # 过滤头部下划线
                result.append(char)
            elif char.is_lower()  : result[-1] += char
            elif char.is_upper()  : result.append(char)
            elif char.is_number() :
                if result[-1].is_number() : result[-1] += char
                else                     : result.append(char)
            elif char == '_'     :
                if result[-1] == '' : continue
                else                : result.append(Str(''))
            else                 : raise Exception(f'非法字符[{P(char)}] in [{P(self)}]')
        if len(result) == 0 : raise Exception(f'无法 splitWord [{self}]')
        return result

    def to_pascal_case(self) : return Str(''.join([word.to_capitalize() for word in self._split_word_list()]))

    def to_camel_case(self) : word_list = self._split_word_list(); return word_list[0].to_lower() + Str(''.join([word.to_capitalize() for word in word_list[1:]]))

    def to_snake_case(self) : return Str('_'.join([word.to_lower() for word in self._split_word_list()]))

    # S.ljust(width[, fillchar]) -> str
    # S.rjust(width[, fillchar]) -> str
    # Return S left-justified or right-justified in a Unicode string of length width. Padding is
    # done using the specified fill character (default is a space).
    # NOT IN PLACE
    def pad_to_width(self, width: int, fillchar: str = ' ', /, *, reverse = False) :
        if reverse : return Str(str.rjust(self, width, fillchar))
        else       : return Str(str.ljust(self, width, fillchar))

    # python2
    # ['__add__', '__class__', '__contains__', '__delattr__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__getslice__', '__gt__', '__hash__', '__init__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '_formatter_field_name_split', '_formatter_parser', 'capitalize', 'center', 'count', 'decode', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'index', 'isalnum', 'isalpha', 'isdigit', 'islower', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'partition', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']

    # python3
    # ['__add__', '__class__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'capitalize', 'casefold', 'center', 'count', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'format_map', 'index', 'isalnum', 'isalpha', 'isdecimal', 'isdigit', 'isidentifier', 'islower', 'isnumeric', 'isprintable', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans', 'partition', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']

    # ===============================================================

    # str(object='') -> str
    # str(bytes_or_buffer[, encoding[, errors]]) -> str
    # Create a new string object from the given object. If encoding or
    # errors is specified, then the object must expose a data buffer
    # that will be decoded using the given encoding and error handler.
    # Otherwise, returns the result of object.__str__() (if defined)
    # or repr(object).
    # encoding defaults to sys.getdefaultencoding().
    # errors defaults to 'strict'.
    # def __class__(self) :

    # Implement delattr(self, name).
    # Deletes the named attribute from the given object.
    # delattr(x, 'y') is equivalent to ``del x.y''
    # def __delattr__(self) :

    # __dir__() -> list
    # default dir() implementation
    # def __dir__(self) :

    # Return self==value.
    # def __eq__(self) :

    # Return self>=value.
    # def __ge__(self) :

    # Return getattr(self, name).
    # def __getattribute__(self) :

    # None
    # def __getnewargs__(self) :

    # Return self>value.
    # def __gt__(self) :

    # Return hash(self).
    # def __hash__(self) :

    # str(object='') -> str
    # str(bytes_or_buffer[, encoding[, errors]]) -> str
    # Create a new string object from the given object. If encoding or
    # errors is specified, then the object must expose a data buffer
    # that will be decoded using the given encoding and error handler.
    # Otherwise, returns the result of object.__str__() (if defined)
    # or repr(object).
    # encoding defaults to sys.getdefaultencoding().
    # errors defaults to 'strict'.
    # def __init__(self) :

    # This method is called when a class is subclassed.
    # The default implementation does nothing. It may be
    # overridden to extend subclasses.
    # def __init_subclass__(self) :

    # Return self<=value.
    # def __le__(self) :

    # Return self<value.
    # def __lt__(self) :

    # Return self%value.
    # def __mod__(self) :

    # Return self*value.n
    # def __mul__(self) :

    # Return self!=value.
    # def __ne__(self) :

    # Create and return a new object.  See help(type) for accurate signature.
    # def __new__(self) :

    # helper for pickle
    # def __reduce__(self) :

    # helper for pickle
    # def __reduce_ex__(self) :

    # Return value%self.
    # def __rmod__(self) :

    # Implement setattr(self, name, value).
    # def __setattr__(self) :

    # S.__sizeof__() -> size of S in memory, in bytes
    # def __sizeof__(self) :

    # Abstract classes can override this to customize issubclass().
    # This is invoked early on by abc.ABCMeta.__subclasscheck__().
    # It should return True, False or NotImplemented.  If it returns
    # NotImplemented, the normal algorithm is used.  Otherwise, it
    # overrides the normal algorithm (and the outcome is cached).
    # def __subclasshook__(self) :

    # S.encode(encoding='utf-8', errors='strict') -> bytes
    # Encode S using the codec registered for encoding. Default encoding
    # is 'utf-8'. errors may be given to set a different error
    # handling scheme. Default is 'strict' meaning that encoding errors raise
    # a UnicodeEncodeError. Other possible values are 'ignore', 'replace' and
    # 'xmlcharrefreplace' as well as any other name registered with
    # codecs.register_error that can handle UnicodeEncodeErrors.
    # def encode(self) :

    # S.expandtabs(tabsize=8) -> str
    # Return a copy of S where all tab characters are expanded using spaces.
    # If tabsize is not given, a tab size of 8 characters is assumed.
    # def expandtabs(self) :

    # S.format_map(mapping) -> str
    # Return a formatted version of S, using substitutions from mapping.
    # The substitutions are identified by braces ('{' and '}').
    # def format_map(self) :

    # S.isalnum() -> bool
    # Return True if all characters in S are alphanumeric
    # and there is at least one character in S, False otherwise.
    # def isalnum(self) :

    # S.isalpha() -> bool
    # Return True if all characters in S are alphabetic
    # and there is at least one character in S, False otherwise.
    # def isalpha(self) :

    # S.isdigit() -> bool
    # Return True if all characters in S are digits
    # and there is at least one character in S, False otherwise.
    # def isdigit(self) :

    # S.isidentifier() -> bool
    # Return True if S is a valid identifier according
    # to the language definition.
    # Use keyword.iskeyword() to test for reserved identifiers
    # such as "def" and "class".
    # def isidentifier(self) :

    # S.isnumeric() -> bool
    # Return True if there are only numeric characters in S,
    # False otherwise.
    # def isnumeric(self) :

    # S.isprintable() -> bool
    # Return True if all characters in S are considered
    # printable in repr() or S is empty, False otherwise.
    # def isprintable(self) :

    # S.isspace() -> bool
    # Return True if all characters in S are whitespace
    # and there is at least one character in S, False otherwise.
    # def isspace(self) :

    # S.istitle() -> bool
    # Return True if S is a titlecased string and there is at least one
    # character in S, i.e. upper- and titlecase characters may only
    # follow uncased characters and lowercase characters only cased ones.
    # Return False otherwise.
    # def istitle(self) :

    # Return a translation table usable for str.translate().
    # If there is only one argument, it must be a dictionary mapping Unicode
    # ordinals (integers) or characters to Unicode ordinals, strings or None.
    # Character keys will be then converted to ordinals.
    # If there are two arguments, they must be strings of equal length, and
    # in the resulting dictionary, each character in x will be mapped to the
    # character at the same position in y. If there is a third argument, it
    # must be a string, whose characters will be mapped to None in the result.
    # def maketrans(self) :

    # S.partition(sep) -> (head, sep, tail)
    # Search for the separator sep in S, and return the part before it,
    # the separator itself, and the part after it.  If the separator is not
    # found, return S and two empty strings.
    # def partition(self) :

    # S.rpartition(sep) -> (head, sep, tail)
    # Search for the separator sep in S, starting at the end of S, and return
    # the part before it, the separator itself, and the part after it.  If the
    # separator is not found, return two empty strings and S.
    # def rpartition(self) :

    # S.splitlines([keepends]) -> list of strings
    # Return a list of the lines in S, breaking at line boundaries.
    # Line breaks are not included in the resulting list unless keepends
    # is given and true.
    # def splitlines(self) :

    # S.translate(table) -> str
    # Return a copy of the string S in which each character has been mapped
    # through the given translation table. The table must implement
    # lookup/indexing via __getitem__, for instance a dictionary or list,
    # mapping Unicode ordinals to Unicode ordinals, strings, or None. If
    # this operation raises LookupError, the character is left untouched.
    # Characters mapped to None are deleted.
    # def translate(self) :

    # S.zfill(width) -> str
    # Pad a numeric string S with zeros on the left, to fill a field
    # of the specified width. The string S is never truncated.
    # def zfill(self) :

if __name__ == '__main__':
    # print(Str('hello').is_in('hello', 'word'))
    # print(Str('hello') in 'hellword')
    # print('hello' in Str('hellword'))
    # print('@'.join([Str('hello'), Str('word')]))
    print(eval(repr(Str('hello'))) == Str('hello'))
