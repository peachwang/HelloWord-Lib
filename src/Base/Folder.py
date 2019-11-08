# -*- coding: utf-8 -*-  
from util import List, Dict, Str, Object
from File import File, realpath
from os import path, rename, listdir, remove, makedirs, walk

class Folder(Object) :

    def __init__(self, folder_path) :
        Object.__init__(self)
        try :
            self._path, self._sub_folder_name_list, self._sub_file_name_list = list(walk(folder_path))[0]
            self._path, self._sub_folder_name_list, self._sub_file_name_list = Str(self._path), List(self._sub_folder_name_list), List(self._sub_file_name_list)
            self._sub_file_name_list.filter(lambda file_name : file_name != '.DS_Store')
        except Exception as e :
            raise Exception('Fail to walk folder path: {}'.format(folder_path))
        self._path.rstrip('/')
        self._name = self._path.split('/')[-1]
        self._sub_folder_list = self._sub_folder_name_list.copy().map(lambda folder_name : Folder('{}/{}'.format(self._path, folder_name)))
        self._sub_file_list   = self._sub_file_name_list.copy().map(lambda file_name : File('{}/{}'.format(self._path, file_name), self))

    def j(self) :
        return '{}'.format(self)

    def __format__(self, code) :
        return 'Folder({})'.format(realpath(self._path))

    def __str__(self) :
        return self.__format__('')

    @classmethod
    def mkdir(cls, path) :
        makedirs(path, exist_ok = True)
        return cls

    @classmethod
    def exists(cls, path) :
        return path.exists(path)

    @property
    def sub_file_list(self) :
        return self._sub_file_list.copy()

    @property
    def flattern_sub_file_list(self) :
        return self._sub_file_list.copy().extend(self._sub_folder_list.copy().batch('flattern_sub_file_list').merge())

    def json(self) :
        return Dict({
            'Path'          : self._path,
            'Name'          : self._name,
            'SubFolderList' : self._sub_folder_list.copy().batch('json'),
            'SubFileList'   : self._sub_file_list.copy().batch('json'),
        })

