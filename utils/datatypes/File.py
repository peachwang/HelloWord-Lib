# -*- coding: utf-8 -*-  
from os       import remove, rename
from os.path  import realpath, exists, getsize
from ..shared import *
from .Str     import Str
from .List    import List
from .Dict    import Dict

class File(base_class) :

    @anti_duplicate_new
    def __new__(cls, file_path, *args, **kwargs) : return realpath(file_path)

    @anti_duplicate_init
    def __init__(self, file_path, folder = None, /) :
        self._raw_path    = file_path
        self._path        = file_path
        self._folder      = folder
        _                 = self._path.split('/')
        self._full_name   = Str(_[-1])
        self._folder_path = Str('/'.join(_[ : -1]))
        self._ext         = Str(_[-1].split('.')[-1] if '.' in _[-1] else '')
        self._name        = Str(_[-1][ : - len(self._ext) - 1])

    @prop
    def raw_path(self) -> str : return self._raw_path

    @prop
    def path(self) -> Str : return self._path

    @prop
    def abs_path(self) -> Str : return Str(realpath(self._path))

    @prop
    def folder(self) : return self._folder

    @prop
    def folder_path(self) -> Str : return self._folder_path

    @prop
    def full_name(self) -> Str : return self._full_name

    @prop
    def name(self) -> Str : return self._name

    @prop
    def ext(self) -> Str : return self._ext

    def ext_is(self, ext, /) : return self._ext.to_lower() == Str(ext).to_lower()

    def is_txt(self) : return self.ext_is('txt')

    def is_json(self) : return self.ext_is('json')

    @prop
    def range(self) : return self._range

    def exists(self) : return exists(self._path)

    def not_exists(self) : return not self.exists()

    @prop
    def size(self) : return getsize(self._path)

    def rename(self, new_name) : raise NotImplementedError # 改 self._path

    def move(self, new_path) : raise NotImplementedError # 改 self._path

    # os.remove(path, *, dir_fd=None)
    # Remove (delete) the file path. If path is a directory, an IsADirectoryError is raised. Use rmdir() to remove directories.
    def delete(self) : remove(self._path); Timer.print_timing(f'{self} 已删除', color = R); return self

    def json_serialize(self) -> str : return self._raw_path

    def __eq__(self, other) : return self.abs_path == other.abs_path

    def __ne__(self, other) : return not self.__eq__(other)

    # @log_entering()
    def __format__(self, spec) : return f"{f'File({self.abs_path})':{spec}}"

    def __str__(self) : return self.__format__('')
    
    # @log_entering()
    def __repr__(self) : return f'File({self._raw_path!r})'

    def __getitem__(self, index) :
        if isinstance(index, slice) :
            if index.step is not None : raise Exception(f'{index =} 不可以有step')
            self._range = index
            return self
        else                        : raise CustomTypeError(index)

    def read_raw(self) : return Str(''.join(open(self._path).readlines()))

    def __iter__(self) :
        for line in open(self._path) : yield Str(line)

    def _read_line_list(self, *, raw = False, filter_white_lines = False, replace_abnormal_char = True) -> Union[list, List] :
        if raw : result = []
        else   : result = List()
        start = self._range.start if hasattr(self, '_range') else None
        stop  = self._range.stop if hasattr(self, '_range') else None
        for index, line in enumerate(open(self._path)) :
            if start is not None and index < start        : continue
            if stop is not None and stop <= index         : break
            if filter_white_lines and Str(line).is_empty() : continue
            if replace_abnormal_char : line = line.replace(' ', ' ').replace('．', '.')
            result.append(line.strip('\n\r'))
        return result

    def read_field_list(self, *, index, sep = '\t') -> List : return self._read_line_list(filter_white_lines = True).map(lambda line : line.split(sep)[index])

    def _load_json(self, *, raw = False) -> Union[list, dict, List, Dict] :
        from ..app.Json import raw_load_json_file
        data = raw_load_json_file(open(self._path))
        if isinstance(data, list)   :
            if not raw                 : data = List(data)
            if hasattr(self, '_range') : return data[self._range]
            else                       : return data
        elif isinstance(data, dict) :
            if not raw                 : data = Dict(data)
            if hasattr(self, '_range') : raise Exception('Dict 类 File 不可以有 range')
            else                       : return data
        else                        : raise CustomTypeError(data)

    def load_data(self, **kwargs) :
        if self.not_exists() : raise Exception(f'{self} 不存在')
        if self.is_txt()     : return self._read_line_list(**kwargs)
        elif self.is_json()  : return self._load_json(**kwargs)
        else                : raise Exception(f'不支持的后缀名：{self._ext=}')

    def write_string(self, string, /, *, append = False) : open(self._path, 'a' if append else 'w').write(string); return self

    def write_bytes(self, bytes_content, /) : open(self._path, 'wb').write(bytes_content); return self

    def write_line(self, string, /, *, append = False) : return self.write_string(f'{string}\n', append = append)

    def write_line_list(self, line_list, /, *, append = False) : return self.write_string('\n'.join(line_list), append = append)

    def _dump_json(self, obj, /, *, indent = True) :
        from ..app.Json import raw_dump_json_file
        raw_dump_json_file(obj, open(self._path, 'w'), indent = indent) # raw_dump_json_file 内部可以处理 List, Dict 类型
        return self

    def write_data(self, data, /, **kwargs) :
        if isinstance(data, (list, dict)) : return self._dump_json(data, **kwargs)
        else                              : raise CustomTypeError(data)

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

    def load_table(self) : raise NotImplementedError

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
