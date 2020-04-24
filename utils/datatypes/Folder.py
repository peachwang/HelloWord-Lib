# -*- coding: utf-8 -*-  
from os        import makedirs, rmdir, listdir
from os.path   import isdir, join
from ..shared  import *
from .Str      import Str
from .DateTime import DateTime
from .List     import List
from .File     import File, basename, realpath, exists, getatime, getmtime

@add_print_func
class Folder :

    def mkdir(folder_path) : makedirs(folder_path, exist_ok = True); return Folder

    def exists(folder_path) : return exists(folder_path)

    def not_exists(folder_path) : return not Folder.exists(folder_path)

    def is_folder(folder_path) : return isdir(folder_path)

    @anti_duplicate_new
    def __new__(cls, folder_path, *args, **kwargs) : return realpath(folder_path)

    @anti_duplicate_init
    def __init__(self, folder_path, /, *, auto_build = True) :
        if Folder.not_exists(folder_path) : raise Exception(f'Folder({folder_path} = {realpath(folder_path)}) 不存在')
        self._raw_path   = folder_path
        self._path       = Str(folder_path)
        self._name       = Str(basename(folder_path))
        self._auto_build = auto_build
        self._has_listed = False
        self._has_built  = False
        if not auto_build : pass
        else              : self._build()

    @prop
    def raw_path(self) -> str : return self._raw_path

    @prop
    def path(self) -> Str : return self._path

    @prop
    def abs_path(self) -> Str : return Str(realpath(self._path))

    @prop
    def name(self) -> Str : return self._name

    # @log_entering()
    def _listdir(self) :
        try                   :
            self._sub_folder_name_list = List()
            self._sub_file_name_list   = List()
            for name in listdir(self._path) :
                if isdir(join(self.path, name)) : self._sub_folder_name_list.append(name)
                elif name != '.DS_Store'        : self._sub_file_name_list.append(name)
        except Exception as e : raise Exception(f'Fail to list folder path: {self._path} = {self.abs_path}')
        self._has_listed = True
        return self

    # @log_entering()
    def _build(self) :
        if not self._has_listed : self._listdir()
        self._sub_folder_list = self._sub_folder_name_list.mapped(lambda folder_name : Folder(join(self._path, folder_name), auto_build = self._auto_build))
        self._sub_file_list   = self._sub_file_name_list.mapped(lambda file_name, index : File(join(self._path, file_name), self))#.print_format(pattern = f'{index + 1} {{}}', print_timing = True))
        self._has_built = True
        return self

    @prop
    def size(self) : return self.flat_sub_file_list.size.sum()

    @prop
    def last_access_dt(self) -> DateTime : return DateTime(getatime(self._path))

    @prop
    def last_modification_dt(self) -> DateTime : return DateTime(getmtime(self._path))

    def json_serialize(self) -> str : return self._raw_path

    def __eq__(self, other) : return self.abs_path == other.abs_path

    def __ne__(self, other) : return not self.__eq__(other)

    def __format__(self, spec) : return f"{f'Folder({self.abs_path})':{spec}}"

    def __str__(self) : return self.__format__('')

    def __repr__(self) : return f'Folder({self._raw_path!r})'

    @prop
    def sub_folder_name_list(self) :
        if not self._has_listed : self._listdir()
        return self._sub_folder_name_list.copy()
    
    @prop
    def sub_folder_list(self) :
        if not self._has_built : self._build()
        return self._sub_folder_list.copy()

    @prop
    def flat_sub_folder_list(self) :
        if hasattr(self, '_flat_sub_folder_list') : return self._flat_sub_folder_list
        if not self._has_built : self._build()
        
        self._flat_sub_folder_list = self._sub_folder_list.copy()
        for folder in self._sub_folder_list : self._flat_sub_folder_list.extend(folder.flat_sub_folder_list)
        return self._flat_sub_folder_list
    
    @prop
    def sub_file_name_list(self) :
        if not self._has_listed : self._listdir()
        return self._sub_file_name_list.copy()
    
    @prop
    def sub_file_list(self) :
        if not self._has_built : self._build()
        return self._sub_file_list.copy()

    def get_one_sub_file(self, *, name_contains) : return self.sub_file_list.filter_one(lambda file : file.name.has(name_contains))

    @prop
    def flat_sub_file_list(self) :
        if hasattr(self, '_flat_sub_file_list') : return self._flat_sub_file_list
        if not self._has_built : self._build()
        
        self._flat_sub_file_list = self._sub_file_list.copy()
        for folder in self._sub_folder_list : self._flat_sub_file_list.extend(folder.flat_sub_file_list)
        return self._flat_sub_file_list

    def get_one_flat_sub_file(self, *, name_contains) : return self.flat_sub_file_list.filter_one(lambda file : file.name.has(name_contains))

    # 空目录，无子孙文件
    def has_no_flat_sub_file(self) :
        if self.sub_file_list.is_not_empty()   : return False
        if self.sub_folder_list.is_not_empty() : return all(self.sub_folder_list.value_list('has_no_flat_sub_file'))
        return True

    def print_flat_sub_file_path_list(self) : self.flat_sub_file_list.path.print_line(); return self

    # os.rmdir(path, *, dir_fd=None)
    # Remove (delete) the directory path. If the directory does not exist or is not empty,
    # an FileNotFoundError or an OSError is raised respectively.
    # In order to remove whole directory trees, shutil.rmtree() can be used.
    def delete(self) :
        if self.has_no_flat_sub_file() :
            for folder in self.flat_sub_folder_list.reversed() :
                if Folder.exists(folder.path) :
                    rmdir(folder.path)
                    Timer.print_timing(f'{folder} 已删除', color = R)
            if Folder.exists(self._path) :
                rmdir(self._path)
                Timer.print_timing(f'{self} 已删除', color = R)
        else                       : raise Exception(f'无法删除 {self}，其下有未删除的文件')
        return self


if __name__ == '__main__':
    print(Folder('.').sub_file_name_list)