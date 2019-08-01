# -*- coding: utf-8 -*-  
from util import *

class File(Object) :

    def __init__(self, file_path, folder = None) :
        self.folder = folder
        self.path = file_path
        _ = file_path.split('/')
        self.name   = _[-1]
        self.suffix = self.name.split('.')[-1]
        self.name = self.name[ : - len(self.suffix) - 1]

    def suffixIs(self, suffix) :
        return self.suffix == suffix

    def json(self) :
        return {
            'Path'       : self.path,
            'FolderName' : self.folder.name if self.folder is not None else None,
            'Name'       : self.name,
            'Suffix'     : self.suffix,
        }