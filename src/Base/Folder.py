# -*- coding: utf-8 -*-  
from util import List, Dict, Str, Object, UserTypeError, _print
from File import File, realpath
from os import path, rename, listdir, remove, makedirs, walk
from Timer import Timer

class Folder(Object) :

    def __init__(self, folder_path, /) :
        super().__init__()
        self._registerProperty(['path', 'name'])
        try :
            self._path, self._sub_folder_name_list, self._sub_file_name_list = list(walk(folder_path))[0]
            self._path, self._sub_folder_name_list, self._sub_file_name_list = Str(self._path), List(self._sub_folder_name_list), List(self._sub_file_name_list)
            self._sub_file_name_list.filter(lambda file_name : file_name != '.DS_Store')
        except Exception as e :
            raise e
            # raise Exception(f'Fail to walk folder path: {folder_path=}')
        self._path.rstrip('/')
        self._name = self._path.split('/')[-1]
        self._sub_folder_list = self._sub_folder_name_list.mapped(lambda folder_name : Folder(f'{self._path}/{folder_name}'))
        self._sub_file_list   = self._sub_file_name_list.mapped(lambda file_name : File(f'{self._path}/{file_name}', self))

    def len(self) :
        return self.flattern_sub_file_list.len()

    def __format__(self, code) :
        return f'Folder({realpath(self._path)})'

    @_print
    def printFormat(self) :
        return f'{self}', False

    def __str__(self) :
        return self.__format__('')

    @_print
    def printStr(self) :
        return f'{str(self)}', False

    def jsonSerialize(self) :
        return f'{self}'

    # 可读化
    def j(self) :
        from util import j
        return j(self.jsonSerialize())

    @_print
    def printJ(self) :
        _ = self.flattern_sub_file_list.path.join('\n')
        return f'{self.j()}\n{_}', True

    def mkdir(folder_path) :
        makedirs(folder_path, exist_ok = True)
        return Folder

    def exists(folder_path) :
        return path.exists(folder_path)

    def notExists(folder_path) :
        return not Folder.exists(folder_path)

    @property
    def sub_file_list(self) :
        return self._sub_file_list.copy()

    @property
    def sub_folder_list(self) :
        return self.sub_folder_list.copy()

    @property
    def flattern_sub_file_list(self) :
        result = self._sub_file_list.copy()
        for folder in self._sub_folder_list :
            result.extend(folder.flattern_sub_file_list)
        return result

    def printFilePathList(self) :
        self.flattern_sub_file_list.path.printLine()
        return self
