# -*- coding: utf-8 -*-  
from util import List, Dict, Str, Object, UserTypeError, _print, cached_property, enterLog, antiDuplicateNew, antiDuplicateInit
from File import File, realpath
from os import path, makedirs, rmdir, walk
from Timer import Timer

class Folder(Object) :

    def mkdir(folder_path) :
        makedirs(folder_path, exist_ok = True)
        return Folder

    def exists(folder_path) :
        return path.exists(folder_path)

    def notExists(folder_path) :
        return not Folder.exists(folder_path)

    def rmdir(folder_path) :
        '''
        os.rmdir(path, *, dir_fd=None)
        Remove (delete) the directory path. If the directory does not exist or is not empty,
        an FileNotFoundError or an OSError is raised respectively.
        In order to remove whole directory trees, shutil.rmtree() can be used.
        '''
        rmdir(folder_path)
        return Folder

    @antiDuplicateNew
    def __new__(cls, folder_path, **kwargs) :
        return realpath(folder_path)

    @antiDuplicateInit
    def __init__(self, folder_path, /, *, auto_build = True) :
        if Folder.notExists(folder_path) : raise Exception(f'Folder({folder_path} = {realpath(folder_path)}) 不存在')
        super().__init__()
        self._registerProperty(['path', 'name'])
        # self._path       = realpath(folder_path)
        self._path       = folder_path
        self._name       = self._path.split('/')[-1]
        self._auto_build = auto_build
        self._has_walked = False
        self._has_built  = False
        if not auto_build :
            pass
        else :
            self._build()

    @cached_property
    def abs_path(self) : return realpath(self._path)

    @enterLog('{self}')
    def _walk(self) :
        try :
            for path, sub_folder_name_list, sub_file_name_list in walk(self._path) :
                self._path, self._sub_folder_name_list, self._sub_file_name_list = path, sub_folder_name_list, sub_file_name_list
                break
            self._sub_file_name_list.filter(lambda file_name : file_name != '.DS_Store')
            self._path.rstrip('/')
            self._name = self._path.split('/')[-1]
        except Exception as e :
            # raise e
            raise Exception(f'Fail to walk folder path: {self._path} = {self.abs_path}')
        self._has_walked = True
        return self

    @enterLog('{self}')
    def _build(self) :
        if not self._has_walked : self._walk()
        self._sub_folder_list = self._sub_folder_name_list.mapped(lambda folder_name : Folder(f'{self._path}/{folder_name}', auto_build = self._auto_build))
        self._sub_file_list   = self._sub_file_name_list.mapped(lambda file_name, index : File(f'{self._path}/{file_name}', self))#.printFormat(pattern = f'{index + 1} {{}}', timing = True))
        self._has_built = True
        # Timer.printTiming(f'_build {self} 结束')
        return self

    def __format__(self, code) :
        return f'Folder({self._path} = {self.abs_path})'

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
        _ = self.flat_sub_file_list.path.join('\n')
        return f'{self.j()}\n{_}', True

    @property
    def size(self) :
        raise

    @property
    def sub_file_name_list(self) :
        if not self._has_walked : self._walk()
        return self._sub_file_name_list.copy()

    @property
    def sub_folder_name_list(self) :
        if not self._has_walked : self._walk()
        return self._sub_folder_name_list.copy()

    @property
    def sub_file_list(self) :
        if not self._has_built : self._build()
        return self._sub_file_list.copy()

    @property
    def sub_folder_list(self) :
        if not self._has_built : self._build()
        return self._sub_folder_list.copy()

    def getOneSubFile(self, *, name_contains) :
        return File(f'{self._path}/{self.sub_file_name_list.filterOne(lambda name : name.has(name_contains))}', self)

    @property
    def flat_sub_file_list(self) :
        if not self._has_built : self._build()
        result = self._sub_file_list.copy()
        for folder in self._sub_folder_list :
            result.extend(folder.flat_sub_file_list)
        return result

    @property
    def num_flat_sub_file(self) :
        return self.flat_sub_file_list.len()

    def printFlatSubFilePathList(self) :
        self.flat_sub_file_list.path.printLine()
        return self
