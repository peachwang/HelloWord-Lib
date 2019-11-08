# -*- coding: utf-8 -*-  
from util import List, Dict, Str, Object
from os.path import exists, getsize, isfile, realpath

class File(Object) :

    def __init__(self, file_path, folder = None) :
        Object.__init__(self)
        file_path           = Str(file_path)
        self._folder        = folder
        self._path          = file_path
        _                   = file_path.split('/')
        self._name          = _[-1]
        self._ext           = self._name.split('.')[-1] if '.' in self._name else Str('')
        self._name          = self._name[ : - self._ext.len() - 1]
        self._folder_path   = _[ : -1].join('/')

    def j(self) :
        return '{}'.format(self)

    def __format__(self, code) :
        return 'File({})'.format(realpath(self._path))

    def __str__(self) :
        return self.__format__('')

    @property
    def path(self) :
        return self._path
    
    @property
    def folder(self) :
        return self._folder

    @property
    def folder_path(self) :
        return self._folder_path

    @property
    def name(self) :
        return self._name

    @property
    def ext(self) :
        return self._ext

    def extIs(self, ext) :
        return self._ext == ext

    @classmethod
    def exists(cls, path) :
        return exists(path)

    @property
    def size(self) :
        return getsize(self._path)

    def readLineList(self) :
        return List(open(self._path).readlines()).strip('\n\r')

    def writeString(self, string, append = False) :
        open(self._path, 'a' if append else 'w').write(string)
        return self

    def writeLineList(self, line_list, append = False) :
        return self.writeString(List(line_list).join('\n'), append)

    def writeData(self, data, append = False) :
        if isinstance(data, ( List, Dict )) :
            data.writeToFile(self)
            return self
        else : raise Exception('Unexpected type{} of data: {}'.format(type(data), data))

    def writeBytes(self, bytes_content) :
        open(self._path, 'wb').write(bytes_content)
        return self

    def loadJson(self, encoding = 'utf-8') :
        data = json.loads(''.join([line.strip('\n') for line in open(self._path).readlines()]), encoding = encoding)
        if isinstance(data, list) :
            return List(data)
        elif isinstance(data, dict) :
            return Dict(data)
        else :
            raise

    def dumpJson(self, data) :
        return self.writeData(data)

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
        raise

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
        raise

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
        raise

    def json(self) :
        return Dict({
            'Path'       : self._path,
            'FolderName' : self._folder.name if self._folder is not None else None,
            'Name'       : self._name,
            'Extension'  : self._ext,
        })
