# -*- coding: utf-8 -*-  
from ..shared         import *
from ..datatypes.File import File

class FileManager :

    @anti_duplicate_new
    def __new__(cls, key = None, /, *args, **kwargs) : return cls.key if key is None else key

    @anti_duplicate_init
    def __init__(self) :
        super().__init__()
        self._file = File(f'{self.file_path}')
        if self._file.not_exists() : self._file.write_data(self.initial_data)

    def save(self, indent = True) :
        self._file.write_data(self._file_data, indent = indent);
        Timer.print_timing(f'{self._class} 已保存', color = G)
        return self