# -*- coding: utf-8 -*-  
from os        import remove, rename
from os.path   import isfile, realpath, basename, dirname, splitext, exists, getsize, getatime, getmtime
from ..shared  import *
from .DateTime import DateTime
from .Str      import Str
from .Dict     import Dict
from .List     import List
from .Iter     import Iter

@iterable
@printable
class File :
    
    @staticmethod
    def is_file(file_path)                          : return isfile(file_path)

    @anti_duplicate_new
    def __new__(cls, file_path, *args, **kwargs)    : return realpath(file_path)

    @anti_duplicate_init
    def __init__(self, file_path, folder = None, /) :
        self._path        = file_path.get_raw() if isinstance(file_path, Str) else file_path
        self._folder      = folder
        self._full_name   = basename(file_path)
        self._folder_path = dirname(file_path)
        self._ext         = splitext(file_path)[1][1:]
        self._name        = basename(file_path)[ : - len(self._ext) - 1]

    @cached_prop
    def path(self) -> str                           : return self._path

    @cached_prop
    def abs_path(self) -> str                       : return realpath(self._path)

    @cached_prop
    def folder(self)                                : return self._folder

    @cached_prop
    def folder_path(self) -> str                    : return self._folder_path

    @cached_prop
    def full_name(self) -> str                      : return self._full_name

    @cached_prop
    def name(self) -> str                           : return self._name

    @cached_prop
    def ext(self) -> str                            : return self._ext

    def ext_is(self, ext: str, /)                   : return self._ext.lower() == ext.lower()

    def is_txt(self)                                : return self.ext_is('txt')

    def is_json(self)                               : return self.ext_is('json')

    def exists(self)                                : return exists(self._path)

    def ensure_exists(self)                         :
        if not self.exists() : raise FileNotFoundError(f'{self} 不存在')
        return self

    @prop
    def range(self)                                 : return self._range

    @prop
    def size(self) -> int                           : return getsize(self._path)

    @prop
    def last_access_dt(self) -> DateTime            : return DateTime(getatime(self._path))

    @prop
    def last_modification_dt(self) -> DateTime      : return DateTime(getmtime(self._path))

    def rename(self, new_name)                      : raise NotImplementedError # 改 self._path

    def move(self, new_path)                        : raise NotImplementedError # 改 self._path

    # os.remove(path, *, dir_fd=None)
    # Remove (delete) the file path.
    # If path is a directory, an IsADirectoryError is raised.
    # Use rmdir() to remove directories.
    def delete(self)                                : remove(self._path); Timer.print_timing(f'{self} 已删除', color = R); return self

    def json_serialize(self) -> str                 : return self._path

    def __eq__(self, other)                         : return self.abs_path == other.abs_path

    def __ne__(self, other)                         : return not self.__eq__(other)

    def __format__(self, spec)                      : return f'{f"{type(self).__name__}({self.abs_path})":{spec}}'

    def __str__(self)                               : return self.__format__('')
    
    def __repr__(self)                              : return f'{type(self).__name__}({self._path!r})'

    def __getitem__(self, index)                    :
        if isinstance(index, slice) :
            if index.step is not None : raise ValueError(f'{index =} 不可以有step')
            self._range = index
            return self
        else                        : raise TypeError(index)

    def read_raw(self) -> Str                       :
        with open(self._path) as f : return Str(''.join(f.readlines()))

    def __iter__(self)                              :
        with open(self._path) as f :
            for line in f : yield Str(line)

    @iter_func
    def read_line_iter(self, *, raw = False, filter_white_lines = False, replace_abnormal_char = True) :
        start = self._range.start if hasattr(self, '_range') else None
        stop  = self._range.stop if hasattr(self, '_range') else None
        with open(self._path) as f :
            for index, line in enumerate(f) :
                if start is not None and index < start         : continue
                if stop is not None and stop <= index          : break
                if filter_white_lines and Str(line).is_empty() : continue
                if replace_abnormal_char                       : line = line.replace(' ', ' ').replace('．', '.')
                if raw                                         : yield line.strip('\n\r')
                else                                           : yield Str(line.strip('\n\r'))

    def read_field_iter(self, *, index, sep = '\t')                                       :
        return self.read_line_iter(filter_white_lines = True).map(lambda line : line.split(sep)[index])

    def _load_json(self, *, raw = False) -> Union[list, dict, List, Dict]                 :
        from ..app.Json import raw_load_json_file
        with open(self._path) as f : data = raw_load_json_file(open(self._path))
        if isinstance(data, list)   :
            if not raw                 : data = List(data)
            if hasattr(self, '_range') : return data[self._range]
            else                       : return data
        elif isinstance(data, dict) :
            if not raw                 : data = Dict(data)
            if hasattr(self, '_range') : raise RuntimeError('Dict 类 File 不可以有 range')
            else                       : return data
        else                        : raise TypeError(data)

    def load_data(self, **kwargs)                                                         :
        self.ensure_exists()
        if self.is_txt()     : return self.read_line_iter(**kwargs).list
        elif self.is_json()  : return self._load_json(**kwargs)
        else                 : raise RuntimeError(f'不支持的后缀名：{self._ext=}')

    def clear(self)                                                                       :
        with open(self._path, 'w') as f : f.write('')
        return self

    def write_string(self, string, /, *, append = True, ensure_not_exists = False)        :
        with open(self._path, 'x' if ensure_not_exists else ('a' if append else 'w')) as f :
            f.write(string)
        return self

    def write_bytes(self, bytes_content, /, *, append = False, ensure_not_exists = False) :
        with open(self._path, 'xb' if ensure_not_exists else ('ab' if append else 'wb')) as f :
            f.write(bytes_content)
        return self

    def write_line(self, string, /, **kwargs)                                             :
        return self.write_string(f'{string}\n', **kwargs)

    def write_line_iter(self, line_iterable, /, *, append = False, **kwargs)              :
        return self.write_string('\n'.join(line_iterable), append = append, **kwargs)

    def write_json(self, obj, /, *, indent = True, ensure_not_exists = False)             :
        if isinstance(obj, (list, dict)) :
            from ..app.Json import raw_dump_json_file
            with open(self._path, 'x' if ensure_not_exists else 'w') as f :
                raw_dump_json_file(obj, f, indent = indent) # raw_dump_json_file 内部可以处理 List, Dict 类型
        else                             : raise TypeError(obj)
        return self

    # def load_table(fin, fields = None, primary_key = None, cast = None, is_matrix = False, sep = '\t') :
    #     if not is_matrix :
    #         if fields == None :
    #             fields = fin.readline().strip('\n\r').split(sep)
    #         mapping_fields = dict([(_, fields[_]) for _ in range(len(fields))])
    #     if primary_key is None or is_matrix : data = []
    #     else : data = {}
    #     for line in fin :
    #         line = line.strip('\n\r')
    #         if line == '' : continue
    #         record = line.split(sep)
    #         if cast is not None and isinstance(cast, list) :
    #             record = [cast[_](record[_]) for _ in range(len(record))]
    #         if not is_matrix : datum = dict(zip(mapping_fields.values(), record))
    #         else : datum = record
    #         if cast is not None and isinstance(cast, dict) and not is_matrix :
    #             for field in cast.keys() :
    #                 datum[field] = cast[field](datum[field])
    #         if primary_key is None or is_matrix: data.append(datum)
    #         else : data[datum[primary_key]] = datum
    #     return data

    def load_table(self) :
        raise NotImplementedError
        # col_types = [str, float, str, str, float, int]
        # with open('stocks.csv') as f:
        #     f_csv = csv.reader(f)
        #     headers = next(f_csv)
        #     for row in f_csv:
        #         # Apply conversions to the row items
        #         row = tuple(convert(value) for convert, value in zip(col_types, row))
        #         ...
        # field_types = [ ('Price', float),
        #                 ('Change', float),
        #                 ('Volume', int) ]

        # with open('stocks.csv') as f:
        #     for row in csv.DictReader(f):
        #         row.update((key, conversion(row[key]))
        #                 for key, conversion in field_types)
        #         print(row)

    # def dump_table(fout, data, fields = None, primary_key = None, is_matrix = False, sep = '\t', default = '') :
    #     if is_matrix :
    #         for datum in data :
    #             safe_print(fout, sep.join(datum) + '\n')
    #             fout.flush()
    #     else :
    #         if primary_key is not None :
    #             data = data.values()
    #         if fields is None :
    #             fields = union(*(data)).keys()
    #         if primary_key is not None :
    #             fields.remove(primary_key)
    #             fields = [primary_key] + fields
    #         safe_print(fout, sep.join(fields) + '\n')
    #         for datum in data :
    #             safe_print(fout, sep.join([datum.get(field, default) for field in fields]) + '\n')
    #             fout.flush()

    def dump_table(self) : raise NotImplementedError

    # # delete
    # def load_mapping(fin) :
    #     data = {}
    #     current = None
    #     for line in fin :
    #         line = line.strip('\n\r')
    #         if line.strip(' ') == '' : continue
    #         if '\t' not in line :
    #             current = line
    #             if current not in data : data[current] = []
    #             continue
    #         elif current is None : raise
    #         else :
    #             line = line.strip('\t')
    #             line = re.sub(r'\t+', '\t', line)
    #             data[current].append(line.split('\t'))
    #     data = strip(data)
    #     return data

    def load_mapping(self) : raise NotImplementedError
