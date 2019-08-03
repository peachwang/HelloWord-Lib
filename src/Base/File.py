# -*- coding: utf-8 -*-  
from util import *
from os.path import getsize, join, isfile, realpath

class File(Object) :

    def __init__(self, file_path, folder = None) :
        Object.__init__(self)
        self.folder = folder
        self.path   = file_path
        _ = file_path.split('/')
        self.name   = _[-1]
        self.ext    = self.name.split('.')[-1]
        self.name   = self.name[ : - len(self.ext) - 1]

    def extIs(self, ext) :
        return self.ext == ext

    @classmethod
    def exists(cls, path) :
        return os.path.exists(path)

    def write(self, string, append = False) :
        open(self.path, 'a' if append else 'w').write(string)
        return self

    def writeLineList(self, line_list, append = False) :
        return self.write(List(line_list).join('\n'), append)

    def writeData(self, data, append = False) :
        if type(data) in [ List, Dict ] :
            return self.write(data.j(), append)
        else : raise Exception('Unexpected type of data: {}'.format(data))

    def readLineList(self) :
        pass

    def load(self) :
        pass

    def dump(self) :
        pass

    def loadTxt(self) :
        pass

    def dumpTxt(self) :
        pass

    def loadJson(self) :
        pass

    def dumpJson(self) :
        pass

    def loadTable(self) :
        pass

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
        pass

    def loadMapping(self) :
        pass

    def dumpMapping(self) :
        pass

    def json(self) :
        return {
            'Path'       : self.path,
            'FolderName' : self.folder.name if self.folder is not None else None,
            'Name'       : self.name,
            'Extension'  : self.ext,
        }