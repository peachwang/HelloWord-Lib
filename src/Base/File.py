# -*- coding: utf-8 -*-  
from util import List, Dict, Str, Object, json, Optional, Union, ensureArgsType, UserTypeError
from os.path import exists, getsize, isfile, realpath
from Timer import Timer

class File(Object) :

    def __init__(self, file_path, folder = None, /) :
        Object.__init__(self)
        self._registerProperty(['path', 'folder', 'folder_path', 'name', 'ext', 'range'])
        file_path           = Str(file_path)
        self._folder        = folder
        self._path          = file_path
        _                   = file_path.split('/')
        self._name          = _[-1]
        self._ext           = self._name.split('.')[-1] if self._name.has('.') else Str('')
        self._name          = self._name[ : - self._ext.len() - 1]
        self._folder_path   = _[ : -1].join('/')

    @property
    def absolute_path(self):
        return realpath(self._path)

    def jsonSerialize(self) :
        return f'{self}'

    # 可读化
    def j(self) :
        from util import j
        return j(self.jsonSerialize())

    def print(self, *, color = '') :
        from util import E
        print(color, self.j(), E if color != '' else '')
        return self

    def __format__(self, code) :
        return f'File({realpath(self._path)})'

    def __str__(self) :
        return self.__format__('')

    def extIs(self, ext, /) :
        return self._ext == ext

    def isTxt(self) :
        return self.extIs('txt')

    def isJson(self) :
        return self.extIs('json')

    def exists(self) :
        return exists(self._path)

    def notExists(self) :
        return not self.exists()

    @property
    def size(self) :
        return getsize(self._path)

    def readLineList(self, *, filter_white_lines = False) :
        if self._hasProperty('range') :
            start = 0 if self._range.start is None else self._range.start
            stop  = 0 if self._range.stop is None else self._range.stop
            result = List(line.strip('\n\r') for index, line in enumerate(open(self._path)) if start <= index and index < stop)
        else :
            result = List(line.strip('\n\r') for line in open(self._path))
        if filter_white_lines :
            result.filter(lambda line : line.isNotEmpty())
        return result

    def readFieldList(self, *, index, sep = '\t') :
        return self.readLineList(filter_white_lines = True).map(lambda line : line.split(sep)[index])

    def writeString(self, string, /, *, append = False) :
        open(self._path, 'a' if append else 'w').write(string)
        return self

    def writeLineList(self, line_list, /, *, append = False) :
        return self.writeString(List(line_list).join('\n'), append = append)

    # @ensureArgsType
    def writeData(self, data: Union[List, Dict], /) :
        data.writeToFile(self)
        return self

    def writeBytes(self, bytes_content, /) :
        open(self._path, 'wb').write(bytes_content)
        return self

    def loadJson(self, *, encoding = 'utf-8') :
        data = json.loads(''.join([line.strip('\n') for line in open(self._path).readlines()]), encoding = encoding)
        if isinstance(data, list) :
            if self._hasProperty('range') :
                return List(data)[self._range]
            else :
                return List(data)
        elif isinstance(data, dict) :
            if self._hasProperty('range') :
                raise Exception('Dict类File不可以有range')
            return Dict(data)
        else : raise UserTypeError(data)

    def dumpJson(self, data, /) :
        return self.writeData(data)

    def loadData(self) :
        if self.isTxt() :
            return self.readLineList()
        elif self.isJson() :
            return self.loadJson()
        else :
            raise Exception(f'不支持的后缀名：{self._ext=}')

    def __getitem__(self, index) :
        if isinstance(index, slice) :
            if index.step is not None :
                raise UserTypeError(index)
            self._range = index
            return self
        else :
            raise UserTypeError(index)

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

    def loadTable(self) :
        raise NotImplementedError

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

    def dumpTable(self) :
        raise NotImplementedError

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

    def loadMapping(self) :
        raise NotImplementedError
