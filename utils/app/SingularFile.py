# -*- coding: utf-8 -*-  
from ..shared         import *
from ..datatypes.File import File

class SingularFile(SingularBaseClass) :
    
    _save_as_indent = True

    @cls_cached_prop
    def file_path(cls) -> str : return cls._file_path

    @cls_cached_prop
    def _file(cls)            :
        file = File(cls._file_path)
        if file.not_exists() : file.write_json(cls._initial_data)
        return file

    @cls_cached_prop
    def _data(cls)            : return cls._file.load_data(raw = cls._load_as_raw)

    @classmethod
    def save(cls)             :
        cls._file.write_json(cls._data, indent = cls._save_as_indent);
        Timer.print_timing(f'{cls._class} 已保存', color = G)
        return cls
