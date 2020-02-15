# -*- coding: utf-8 -*-  
import sys, os; sys.path.append(os.path.realpath(__file__ + '/../'));
import re
from shared import ensureArgsType, Optional, Union, UserTypeError, _print
from Object import Object
# from Timer import Timer



# ListDiff: 以 item 作为最小比较单元。降维后可用于StrDiff



# https://docs.python.org/3/library/re.html

SRE_MATCH_TYPE = type(re.match('', ''))

class Pattern(Object) :

    def __init__(self, pattern, /) :
        super().__init__()
        self._registerProperty(['pattern'])
        self._pattern = Str(pattern)

    @property
    def flags(self) :
        '''
        The regex matching flags. This is a combination of the flags given to compile(),
        any (?...) inline flags in the pattern, and implicit flags such as UNICODE if the
        pattern is a Unicode string.
        '''
        return self._pattern.flags

    @property
    def group_num(self):
        '''The number of capturing groups in the pattern.'''
        return self._pattern.groups
    
    def groupIndex(self, name: str, /) :
        '''
        A dictionary mapping any symbolic group names defined by (?P<id>) to group numbers.
        The dictionary is empty if no symbolic groups were used in the pattern.
        '''
        return self._pattern.groupindex[name]

class _Match(Object) :
    
    def __init__(self, match, /) :
        super().__init__()
        self._registerProperty(['match'])
        self._match = match
        self._data.update(self.namedGroupDict())

    @property
    def string(self) :
        '''The string passed to match() or search().'''
        return Str(self._match.string)

    @property
    def whole_match(self) :
        return Str(self._match.group())

    def format(self, template, /) :
        '''
        Match.expand(template)
        Return the string obtained by doing backslash substitution on the
        template string template, as done by the sub() method. Escapes such as \n
        are converted to the appropriate characters, and numeric backreferences
        (\1, \2) and named backreferences (\g<1>, \g<name>) are replaced by the
        contents of the corresponding group.
        (?P<name>...)
        '''
        return Str(self._match.expand(template))

    def _wrap(self, value, /) :
        return Str(value) if isinstance(value, str) else value

    def groupTuple(self, *groups) :
        '''
        Match.group([group1, ...])
        Returns one or more subgroups of the match.
        If there is a single argument, the result is a single string;
        
        if there are multiple arguments, the result is a tuple with one item per
        argument.
        
        Without arguments, group1 defaults to zero (the whole match is returned).
        
        If a groupN argument is zero, the corresponding return value is the entire
        matching string;
        
        if it is in the inclusive range [1..99], it is the string matching the
        corresponding parenthesized group.
        
        If a group number is negative or larger than the number of groups defined in
        the pattern, an IndexError exception is raised.
        
        If a group is contained in a part of the pattern that did not match, the
        corresponding result is None.
        
        If a group is contained in a part of the pattern that matched multiple times,
        the last match is returned.
        
        If the regular expression uses the (?P<name>...) syntax, the groupN arguments
        may also be strings identifying groups by their group name.
        
        If a string argument is not used as a group name in the pattern, an IndexError
        exception is raised.

        Named groups can also be referred to by their index.
        (?P<name>...)
        '''
        if len(groups) == 0 :
            raise Exception(f'非法{groups=}')
        elif len(groups) == 1 :
            _ = self._match.group(groups[0])
            return tuple(self._wrap(_))
        else :
            return tuple(self._wrap(_) for _ in self._match.group(*groups))

    # @ensureArgsType
    def oneGroup(self, group: Union[int, str], /) :
        _ = self._match.group(group)
        return self._wrap(_)

    def __getitem__(self, group) :
        '''
        Match.__getitem__(g)
        m[group] <--> m.group(group)
        This is identical to m.group(group). This allows easier access to an
        individual group from a match.'''
        return self._wrap(self._match.__getitem__(group))

    def allGroupTuple(self, *, default = None) :
        '''
        Match.groups(default=None)
        Return a tuple containing all the subgroups of the match, from 1 up to
        however many groups are in the pattern. The default argument is used for
        groups that did not participate in the match; it defaults to None.
        (?P<name>...)
        '''
        return tuple(self._wrap(_) for _ in self._match.groups(default))

    def namedGroupDict(self, *, default = None) :
        '''
        Match.groupdict(default=None)
        Return a dictionary containing all the named subgroups of the match,
        keyed by the subgroup name. The default argument is used for groups that
        did not participate in the match; it defaults to None.'''
        from Dict import Dict
        return Dict((key, value) for key, value in self._match.groupdict(default).items() if value is not None)

    def startOfGroup(self, group, /) :
        '''
        Match.start([group])
        Return the indices of the start of the substring matched by group;
        group defaults to zero (meaning the whole matched substring).
        Return -1 if group exists but did not contribute to the match.
        For a match object m, and a group g that did contribute to the match,
        the substring matched by group g (equivalent to m.group(g)) is
        m.string[m.start(g):m.end(g)]. Note that m.start(group) will equal
        m.end(group) if group matched a null string.'''
        return self._match.start(group)

    def endOfGroup(self, group, /) :
        '''
        Match.end([group])
        Return the indices of the end of the substring matched by group;'''
        return self._match.end(group)

    def spanOfGroup(self, group, /) :
        '''
        Match.span([group])
        For a match m, return the 2-tuple (m.start(group), m.end(group)).
        Note that if group did not contribute to the match, this is (-1, -1).
        group defaults to zero, the entire match.'''
        return self._match.span(group)

    def replaceGroup(self, group, repl_str_or_func, /) :
        if self.oneGroup(group) is None :
            return self.string
        if isinstance(repl_str_or_func, str) :
            replacement = repl_str_or_func
        else :
            replacement = repl_str_or_func(self.oneGroup(group))
        return self.string[ : self.startOfGroup(group)] + replacement + self.string[self.endOfGroup(group) : ]

class Str(str) :

    def getId(self) :
        '''
        id(object) -> integer
        Return the identity of an object.  This is guaranteed to be unique among
        simultaneously existing objects.  (Hint: it's the object's memory address.)'''
        return hex(id(self))

    def getRaw(self) :
        return str(self)

    def __iter__(self) :
        '''
        Implement iter(self).
        '''
        for char in str.__iter__(self) :
            yield Str(char)

    def jsonSerialize(self) :
        return f'{self}'

    # 可读化
    def j(self) :
        from util import j
        return j(self.jsonSerialize())

    @_print
    def printJ(self, *, color = '', **kwargs) :
        return f'{self.j()}', False

    # def __format__(self) :
        '''
        S.__format__(format_spec) -> str
        Return a formatted version of S as described by format_spec.'''
        # return str.__str__(self)
    
    def format(self, *args, **kwargs) :
        '''
        S.format(*args, **kwargs) -> str
        Return a formatted version of S, using substitutions from args and kwargs.
        The substitutions are identified by braces ('{' and '}').'''
        '''NOT IN PLACE'''
        return Str(str.format(self, *args, **kwargs))

    # def __str__(self) :
        '''Return str(self).'''
        # return 'Str\'{}\''.format(str.__str__(self))
    
    def center(self, width, fillchar = ' ', /) :
        '''
        S.center(width[, fillchar]) -> str
        Return S centered in a string of length width. Padding is
        done using the specified fill character (default is a space)'''
        '''NOT IN PLACE'''
        return Str(str.center(self, width, fillchar))

    def __getitem__(self, index) :
        '''Return self[key].'''
        return Str(str.__getitem__(self, index))

    def __add__(self, string) :
        '''Return self+value.'''
        '''NOT IN PLACE'''
        return Str(str.__add__(self, string))

    def __rmul__(self, times) :
        '''Return self*value.'''
        '''NOT IN PLACE'''
        return Str(str.__rmul__(self, times))

    def concat(self, string, /) :
        '''NOT IN PLACE'''
        return self.__add__(string)

    def __len__(self) :
        '''
        Return len(self).
        '''
        return str.__len__(self)

    def len(self) :
        return str.__len__(self)

    def isEmpty(self) :
        return self.fullMatch(r'^[ \t\n]*$')

    def ensureEmpty(self) :
        if self.isEmpty() : return self
        else :
            raise Exception(f'{self=}应该为空串')

    def isNotEmpty(self) :
        return not self.isEmpty()

    def ensureNotEmpty(self) :
        if self.isNotEmpty() : return self
        else :
            raise Exception(f'{self=}应该不为空串')

    def isIn(self, *item_list) :
        from List import List
        return List(list(item_list)).has(self)

    def isNotIn(self, *item_list) :
        return not self.isIn(*item_list)

    def __contains__(self, sub, /) :
        '''
        x.__contains__(y) <==> y in x
        '''
        return str.__contains__(self, sub)

    def has(self, sub_or_pattern, /, *, re_mode = False, flags = 0) :
        if not re_mode :
            return str.__contains__(self, sub_or_pattern)
        else :
            return self.count(sub_or_pattern, re_mode = re_mode, flags = flags) > 0

    def hasNot(self, sub_or_pattern, /, *, re_mode = False, flags = 0) :
        return not self.has(sub_or_pattern, re_mode = re_mode, flags = flags)

    def hasAnyOf(self, sub_list, /) :
        if not isinstance(sub_list, list) : raise UserTypeError(sub_list)
        return any(self.has(sub) for sub in sub_list)

    def hasAllOf(self, sub_list, /) :
        if not isinstance(sub_list, list) : raise UserTypeError(sub_list)
        return all(self.has(sub) for sub in sub_list)

    def hasNoneOf(self, sub_list, /) :
        if not isinstance(sub_list, list) : raise UserTypeError(sub_list)
        return all(self.hasNot(sub) for sub in sub_list)

    def matchIn(self, sub_list, /) :
        if not isinstance(sub_list, list) : raise UserTypeError(sub_list)
        from List import List
        return List(sub_list).filtered(lambda _ : _ in self)

    def count(self, sub_or_pattern, /, *, start = 0, end = -1, re_mode = False, flags = 0) :
        '''
        S.count(sub[, start[, end]]) -> int
        Return the number of non-overlapping occurrences of substring sub in
        string S[start:end].  Optional arguments start and end are
        interpreted as in slice notation.'''
        if re_mode :
            return self.findall(sub_or_pattern, flags).len()
        else :
            return str.count(self, sub_or_pattern, start, end)

    def index(self, sub, /, *, start = 0, end = -1, reverse = False) :
        '''
        S.index(sub[, start[, end]]) -> int
        Return the lowest or highest index in S where substring sub is found, 
        such that sub is contained within S[start:end].  Optional
        arguments start and end are interpreted as in slice notation.
        Raises ValueError when the substring is not found.'''
        if not reverse :
            return str.index(sub, start, end)
        else :
            return str.rindex(sub, start, end)

    # def find(self, sub, start = 0, end = -1, reverse = False) :
        '''
        S.find(sub[, start[, end]]) -> int
        Return the lowest or highest index in S where substring sub is found,
        such that sub is contained within S[start:end].  Optional
        arguments start and end are interpreted as in slice notation.
        Return -1 on failure.'''
        # if not reverse :
        #     return str.find(sub, start, end)
        # else :
        #     return str.find(sub, start, end)

    def leftMatch(self, pattern, /, *, flags = 0) :
        '''
        re.match(pattern, string, flags=0)
        If zero or more characters at the beginning of string match the
        regular expression pattern, return a corresponding match object.
        Return None if the string does not match the pattern;
        note that this is different from a zero-length match.
        Note that even in MULTILINE mode, re.match() will only match at the
        beginning of the string and not at the beginning of each line.
        If you want to locate a match anywhere in string, use search() instead'''
        _ = re.match(pattern, self, flags)
        return _Match(_) if _ else None

    def ensureLeftMatch(self, pattern = None, /, *, flags = 0) :
        if self.leftMatch(pattern, flags = flags) : return self
        else :
            raise Exception(f'\n{self=}\n应该左匹配\n{pattern=}')
    
    # @Timer.timeitTotal('fullMatch')
    def fullMatch(self, pattern, /, *, flags = 0) :
        '''
        re.fullmatch(pattern, string, flags=0)
        If the whole string matches the regular expression pattern,
        return a corresponding match object. Return None if the string
        does not match the pattern; note that this is different from
        a zero-length match.'''
        try :
            _ = re.fullmatch(pattern, self, flags)
        except KeyboardInterrupt as e :
            print(f'fullMatch卡住: {self}')
            input()
            return None
        return _Match(_) if _ else None

    def ensureFullMatch(self, pattern = None, /, *, flags = 0) :
        if self.fullMatch(pattern, flags = flags) : return self
        else :
            raise Exception(f'\n{self=}\n应该完全匹配\n{pattern=}')

    def searchOneMatch(self, pattern, /, *, reverse = False, flags = 0) :
        '''
        re.search(pattern, string, flags=0)
        Scan through string looking for the first location where the regular
        expression pattern produces a match, and return a corresponding match
        object. Return None if no position in the string matches the pattern;
        note that this is different from finding a zero-length match at some
        point in the string.'''
        _ = re.search(pattern, self, flags)
        return _Match(_) if _ else None

    def findAllMatchList(self, pattern, /, *, flags = 0) :
        '''
        re.finditer(pattern, string, flags=0)
        Return an iterator yielding match objects over all non-overlapping
        matches for the RE pattern in string. The string is scanned left-to-right,
        and matches are returned in the order found. Empty matches are included
        in the result.'''
        from List import List
        return List(_Match(match) for match in re.finditer(pattern, self, flags))

    # 待废弃！
    def findall(self, pattern, /, *, flags = 0) :
        '''
        re.findall(pattern, string, flags=0)
        Return all non-overlapping matches of pattern in string,
        as a list of strings. The string is scanned left-to-right,
        and matches are returned in the order found. If one or more
        groups are present in the pattern, return a list of groups;
        this will be a list of tuples if the pattern has more than
        one group. Empty matches are included in the result. Non-empty
        matches can now start just after a previous empty match.'''
        from List import List
        return List(re.findall(pattern, self, flags))

    def replace(self, sub_or_pattern, repl_str_func, /, *, re_mode: bool, count = None, flags = 0) :
        '''
        S.replace(old, new[, count]) -> str
        Return a copy of S with all occurrences of substring
        old replaced by new.  If the optional argument count is
        given, only the first count occurrences are replaced.'''
        if re_mode :
            if count is None :
                return self._sub(sub_or_pattern, repl_str_func, flags = flags)
            else :
                return self._sub(sub_or_pattern, repl_str_func, count = count, flags = flags)
        else :
            if count is None :
                return Str(str.replace(self, sub_or_pattern, repl_str_func))
            else :
                return Str(str.replace(self, sub_or_pattern, repl_str_func, count))

    def _sub(self, pattern, repl_str_or_func, /, *, count = 0, flags = 0) :
        '''
        re.sub(pattern, repl, string, count=0, flags=0)
        Return the string obtained by replacing the leftmost
        non-overlapping occurrences of pattern in string by the replacement
        repl. If the pattern isn’t found, string is returned unchanged. repl
        can be a string or a function; if it is a string, any backslash escapes
        in it are processed. That is, \n is converted to a single newline
        character, \r is converted to a carriage return, and so forth. Unknown
        escapes of ASCII letters are reserved for future use and treated as
        errors. Other unknown escapes such as \& are left alone. Backreferences,
        such as \6, are replaced with the substring matched by group 6
        in the pattern.
        If repl is a function, it is called for every non-overlapping occurrence
        of pattern. The function takes a single match object argument, and
        returns the replacement string.
        The pattern may be a string or a pattern object.
        The optional argument count is the maximum number of pattern occurrences
        to be replaced; count must be a non-negative integer. If omitted or zero,
        all occurrences will be replaced. Empty matches for the pattern are
        replaced only when not adjacent to a previous empty match,
        so sub('x*', '-', 'abxd') returns '-a-b--d-'.
        In string-type repl arguments, in addition to the character escapes and
        backreferences described above, \g<name> will use the substring matched
        by the group named name, as defined by the (?P<name>...) syntax.
        \g<number> uses the corresponding group number; \g<2> is therefore
        equivalent to \2, but isn’t ambiguous in a replacement such as \g<2>0.
        \20 would be interpreted as a reference to group 20, not a reference to
        group 2 followed by the literal character '0'. The backreference \g<0>
        substitutes in the entire substring matched by the RE.'''
        return Str(re.sub(pattern, repl_str_or_func, self, count, flags))

    def _subn(self, pattern, repl_str_or_func, /, *, count = 0, flags = 0) :
        '''
        re.subn(pattern, repl, string, count=0, flags=0)
        Perform the same operation as sub(), but return a tuple
        (new_string, number_of_subs_made).'''
        _ = re.subn(pattern, repl_str_or_func, self, count, flags)
        return (Str(_[0]), _[1])

    # @ensureArgsType
    def join(self, str_list: list, /) :
        '''
        S.join(iterable) -> str
        Return a string which is the concatenation of the strings in the
        iterable.  The separator between elements is S.'''
        '''NOT IN PLACE'''
        return Str(str.join(self, [f'{_}' for _ in str_list]))

    # def rsplit(self) :
        '''
        S.rsplit(sep=None, maxsplit=-1) -> list of strings
        Return a list of the words in S, using sep as the
        delimiter string, starting at the end of the string and
        working to the front.  If maxsplit is given, at most maxsplit
        splits are done. If sep is not specified, any whitespace string
        is a separator.
        '''
    
    # @ensureArgsType
    def split(self, sep_or_pattern: str, /, *, maxsplit: int = None, reverse = False, re_mode = False, flags = 0) :
        '''
        S.split(sep=None, maxsplit=-1) -> list of strings
        re.split(pattern, string, maxsplit=0, flags=0)
        Return a list of the words in S, using sep as the
        delimiter string.  If maxsplit is given, at most maxsplit
        splits are done. If sep is not specified or is None, any
        whitespace string is a separator and empty strings are
        removed from the result.
        Split string by the occurrences of pattern. If capturing parentheses
        are used in pattern, then the text of all groups in the pattern are also
        returned as part of the resulting list. If maxsplit is nonzero, at most
        maxsplit splits occur, and the remainder of the string is returned as
        the final element of the list.
        >>> re.split(r'(\W+)', 'Words, words, words.')
        ['Words', ', ', 'words', ', ', 'words', '.', '']
        If there are capturing groups in the separator and it matches at the
        start of the string, the result will start with an empty string.
        The same holds for the end of the string:
        >>> re.split(r'(\W+)', '...words, words...')
        ['', '...', 'words', ', ', 'words', '...', '']
        That way, separator components are always found at the same relative
        indices within the result list. Empty matches for the pattern split
        the string only when not adjacent to a previous empty match.
        >>> re.split(r'\b', 'Words, words, words.')
        ['', 'Words', ', ', 'words', ', ', 'words', '.']
        >>> re.split(r'\W*', '...words...')
        ['', '', 'w', 'o', 'r', 'd', 's', '', '']
        >>> re.split(r'(\W*)', '...words...')
        ['', '...', '', '', 'w', '', 'o', '', 'r', '', 'd', '', 's', '...', '', '', '']
        '''
        from List import List
        if re_mode :
            if maxsplit is None : maxsplit = 0
            if reverse : raise Exception(f'无法通过正则[{sep_or_pattern}]反向切割字符串[{self}]')
            if '(' in sep_or_pattern or ')' in sep_or_pattern :
                raise Exception(f'暂不支持使用带括号的正则[{sep_or_pattern}]切割字符串[{self}]')
            return List(re.split(sep_or_pattern, self, maxsplit, flags))
        else :
            if maxsplit is None : maxsplit = -1
            if not reverse :
                return List(str.split(self, sep_or_pattern, maxsplit))
            else :
                return List(str.rsplit(self, sep_or_pattern, maxsplit))

    # def lstrip(self) :
        '''
        S.lstrip([chars]) -> str
        Return a copy of the string S with leading whitespace removed.
        If chars is given and not None, remove characters in chars instead.
        '''

    # def rstrip(self) :
        '''
        S.rstrip([chars]) -> str
        Return a copy of the string S with trailing whitespace removed.
        If chars is given and not None, remove characters in chars instead.
        '''

    # @ensureArgsType
    def strip(self, string: str = ' \t\n', /, *, left: bool = True, right: bool = True) :
        '''
        S.strip([chars]) -> str
        Return a copy of the string S with leading and trailing whitespace removed.
        If chars is given and not None, remove characters in chars instead.'''
        '''NOT IN PLACE'''
        if (not left) and right : 
            return Str(str.rstrip(self, string))
        elif (not right) and left :
            return Str(str.lstrip(self, string))
        elif left and right :
            return Str(str.strip(self, string))
        else :
            raise Exception(f'非法 {left=} 和 {right=}')

    def range(self) :
        '''NOT IN PLACE'''
        from List import List
        return self.split(r' *, *', re_mode = True).map(
            lambda part : 
                List(range(int(part.split('-')[0]), int(part.split('-')[1]) + 1))
                if part.count('-') == 1
                else List(int(part))
        ).merge()

    def toUrl(self) :
        '''NOT IN PLACE'''
        result = Str()
        for char in self :
            if char == ' ' :
                result += Str('%20')
            elif ord(char) <= 128 :
                result += Str(char)
            else :
                result += Str(hex(ord(char))).upper().replace('0X', '%u')
        return result

    def _splitWordList(self) :
        from List import List
        result = List()
        for char in self :
            if result.len() == 0 :
                if char == '_' : continue
                result.append(char)
            elif char.isLower() :
                result[-1] += char
            elif char.isUpper() :
                result.append(char)
            elif char.isNumber() :
                if result[-1].isNumber() :
                    result[-1] += char
                else :
                    result.append(char)
            elif char == '_' :
                result.append('')
            else :
                raise Exception(f'非法字符[{char=}] in [{self=}]')
        if result.len() == 0 :
            raise Exception(f'无法 splitWord [{self}]')
        return result

    def toPascalCase(self) :
        return self._splitWordList().toCapitalize.join()

    def toCamelCase(self) :
        word_list = self._splitWordList()
        return word_list[0].toLower() + word_list[1:].toCapitalize.join()

    def toSnakeCase(self) :
        return self._splitWordList().toLower.join('_')

    def isNumber(self) :
        '''
        S.isdecimal() -> bool
        Return True if all characters in the string are decimal characters and
        there is at least one character, False otherwise.
        Decimal characters are those that can be used to form numbers in base 10,
        e.g. U+0660, ARABIC-INDIC DIGIT ZERO. Formally a decimal character is
        a character in the Unicode General Category “Nd”.
        '''
        return str.isdecimal(self)

    def isInt(self) :
        return self.isNumber() and self.hasNot('.')

    def ensureInt(self) :
        if self.isInt() : return self
        else : raise Exception(f'[{self=}]不是整数')

    def toInt(self) :
        return int(self.ensureInt())

    def isFloat(self) :
        return self.isNumber() and self.has('.')

    def ensureFloat(self) :
        if self.isFloat() : return self
        else : raise Exception(f'[{self=}]不是浮点数')

    def toFloat(self) :
        return float(self.ensureFloat())

    def isLower(self) :
        '''
        S.islower() -> bool
        Return True if all cased characters in S are lowercase and there is
        at least one cased character in S, False otherwise.
        '''
        return str.islower(self)

    def isUpper(self) :
        '''
        S.isupper() -> bool
        Return True if all cased characters in S are uppercase and there is
        at least one cased character in S, False otherwise.
        '''
        return str.isupper(self)

    def toLower(self) :
        '''
        S.lower() -> str
        Return a copy of the string S converted to lowercase.'''
        '''NOT IN PLACE'''
        return Str(str.lower(self))

    def toUpper(self) :
        '''
        S.upper() -> str
        Return a copy of S converted to uppercase.'''
        '''NOT IN PLACE'''
        return Str(str.upper(self))

    def toTitle(self) :
        '''
        S.title() -> str
        Return a titlecased version of S, i.e. words start with title case
        characters, all remaining cased characters have lower case.'''
        '''NOT IN PLACE'''
        return Str(str.title(self))

    def toCapitalize(self) :
        '''
        S.capitalize() -> str
        Return a capitalized version of S, i.e. make the first character
        have upper case and the rest lower case.'''
        '''NOT IN PLACE'''
        return Str(str.capitalize(self))

    def swapCase(self) :
        '''
        S.swapcase() -> str
        Return a copy of S with uppercase characters converted to lowercase
        and vice versa.'''
        '''NOT IN PLACE'''
        return Str(str.swapcase(self))

    def foldCase(self) :
        '''
        S.casefold() -> str
        Return a version of S suitable for caseless comparisons.'''
        '''NOT IN PLACE'''
        return Str(str.casefold(self))

    def padToWidth(self, width, fillchar = ' ', /, *, reverse = False) :
        '''
        S.ljust(width[, fillchar]) -> str
        S.rjust(width[, fillchar]) -> str
        Return S left-justified or right-justified in a Unicode string of length width. Padding is
        done using the specified fill character (default is a space).'''
        '''NOT IN PLACE'''
        if reverse :
            return Str(str.rjust(self, width, fillchar))
        else :
            return Str(str.ljust(self, width, fillchar))

    # python2
    # ['__add__', '__class__', '__contains__', '__delattr__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__getslice__', '__gt__', '__hash__', '__init__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '_formatter_field_name_split', '_formatter_parser', 'capitalize', 'center', 'count', 'decode', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'index', 'isalnum', 'isalpha', 'isdigit', 'islower', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'partition', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']

    # python3
    # ['__add__', '__class__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'capitalize', 'casefold', 'center', 'count', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'format_map', 'index', 'isalnum', 'isalpha', 'isdecimal', 'isdigit', 'isidentifier', 'islower', 'isnumeric', 'isprintable', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans', 'partition', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']

    # ===============================================================

    # def __class__(self) :
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

    # def __delattr__(self) :
        '''
        Implement delattr(self, name).

        Deletes the named attribute from the given object.

        delattr(x, 'y') is equivalent to ``del x.y''
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

    # def __le__(self) :
        '''
        Return self<=value.
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

    # def format_map(self) :
        '''
        S.format_map(mapping) -> str

        Return a formatted version of S, using substitutions from mapping.
        The substitutions are identified by braces ('{' and '}').
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

    # def rpartition(self) :
        '''
        S.rpartition(sep) -> (head, sep, tail)

        Search for the separator sep in S, starting at the end of S, and return
        the part before it, the separator itself, and the part after it.  If the
        separator is not found, return two empty strings and S.
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

    # def zfill(self) :
        '''
        S.zfill(width) -> str

        Pad a numeric string S with zeros on the left, to fill a field
        of the specified width. The string S is never truncated.
        '''
