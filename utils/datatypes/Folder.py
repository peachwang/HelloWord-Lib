# -*- coding: utf-8 -*-  
from os        import makedirs, rmdir, listdir
from os.path   import isdir, join
from ..shared  import *
from .DateTime import DateTime
from .Str      import Str
from .List     import List
from .Iter     import Iter
from .File     import File, basename, realpath, exists, getatime, getmtime

@printable
class Folder :

    @staticmethod
    def is_folder(folder_path)                        : return isdir(folder_path)

    @anti_duplicate_new
    def __new__(cls, folder_path, *args, **kwargs)    : return realpath(folder_path)

    @anti_duplicate_init
    def __init__(self, folder_path, /)                :
        self._path       = folder_path.get_raw() if isinstance(folder_path, Str) else folder_path
        self._name       = basename(folder_path)
        self._has_listed = False

    @cached_prop
    def path(self) -> str                             : return self._path

    @cached_prop
    def abs_path(self) -> str                         : return realpath(self._path)

    @cached_prop
    def name(self) -> str                             : return self._name

    def mkdir(self, *, exist_ok = True)               : makedirs(self._path, exist_ok = exist_ok); return self

    def exists(self)                                  : return exists(self._path)

    def ensure_exists(self)                           :
        if not self.exists() : raise FileNotFoundError(f'{self} 不存在')
        return self

    def mkdir_if_not_exists(self)                     : return self.mkdir() if not self.exists() else self

    @prop
    def last_access_dt(self) -> DateTime              : return DateTime(getatime(self._path))

    @prop
    def last_modification_dt(self) -> DateTime        : return DateTime(getmtime(self._path))

    def json_serialize(self) -> str                   : return self._path

    def __eq__(self, other)                           : return self.abs_path == other.abs_path

    def __ne__(self, other)                           : return not self.__eq__(other)

    def __format__(self, spec)                        : return f'{f"{type(self).__name__}({self.abs_path})":{spec}}'

    def __str__(self)                                 : return self.__format__('')

    def __repr__(self)                                : return f'{type(self).__name__}({self._path!r})'

    def _listdir(self)                                :
        self.ensure_exists()
        if self._has_listed  : return self
        try                   :
            self._sub_folder_name_list = List()
            self._sub_file_name_list   = List()
            for name in listdir(self._path) :
                if isdir(join(self.path, name)) : self._sub_folder_name_list.append(name)
                elif name != '.DS_Store'        : self._sub_file_name_list.append(name)
        except Exception as e : raise RuntimeError(f'遍历目录失败: {self._path} = {self.abs_path}') from e
        self._has_listed = True
        return self

    @prop
    def sub_folder_name_iter(self)                    : return self._listdir()._sub_folder_name_list.iter

    def has_sub_folder(self) -> bool                  : return not self.sub_folder_name_iter.is_empty()

    @prop
    def sub_folder_iter(self)                         : return self.sub_folder_name_iter.map(lambda folder_name : Folder(join(self._path, folder_name.get_raw())))

    @iter_prop
    def flat_sub_folder_iter(self)                    :
        for sub_folder in self.sub_folder_iter :
            yield sub_folder
            yield from sub_folder.flat_sub_folder_iter

    @prop
    def sub_file_name_iter(self)                      : return self._listdir()._sub_file_name_list.iter

    def has_sub_file(self) -> bool                    : return not self.sub_file_name_iter.is_empty()

    @prop
    def sub_file_iter(self)                           : return self.sub_file_name_iter.map(lambda file_name : File(join(self._path, file_name.get_raw()), self))

    def get_one_sub_file(self, *, name_contains)      : return self.sub_file_iter.filter_one(lambda file : file.name.has(name_contains))

    @iter_prop
    def flat_sub_file_iter(self)                      :
        for sub_file in self.sub_file_iter : yield sub_file
        for sub_folder in self.sub_folder_iter :
            for flat_sub_file in sub_folder.flat_sub_file_iter :
                yield flat_sub_file

    def has_flat_sub_file(self) -> bool               : return not self.flat_sub_file_iter.is_empty()

    def get_one_flat_sub_file(self, *, name_contains) : return self.flat_sub_file_iter.filter_one(lambda file : file.name.has(name_contains))

    def print_flat_sub_file_path_list(self)           : self.flat_sub_file_iter.path.print_line(); return self

    @prop
    def size(self) -> int                             : return self.flat_sub_file_iter.size.sum()

    # os.rmdir(path, *, dir_fd=None)
    # Remove (delete) the directory path.
    # If the directory does not exist or is not empty, an FileNotFoundError or an OSError is raised respectively.
    # In order to remove whole directory trees, shutil.rmtree() can be used.
    def delete(self)                                  :
        if not self.has_flat_sub_file() :
            for folder in self.flat_sub_folder_iter.list.reversed() :
                if folder.exists() : folder.delete()
            if self.exists() :
                rmdir(self._path)
                Timer.print_timing(f'{self} 已删除', color = R)
        else                           : raise FileExistsError(f'无法删除 {self}，其下有未删除的文件')
        return self

if __name__ == '__main__':
    print(Folder('.').sub_file_name_list)