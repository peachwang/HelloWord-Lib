# -*- coding: utf-8 -*-  

import os

class File :

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

class Folder :

    def __init__(self, folder_path) :
        self.path, self.sub_folder_name_list, self.sub_file_name_list = list(os.walk(folder_path))[0]
        self.path.rstrip('/')
        self.name = self.path.split('/')[-1]
        self.sub_folder_list = [ Folder('%s/%s' % (self.path, folder_name)) for folder_name in self.sub_folder_name_list]
        self.sub_file_list   = [ File('%s/%s' % (self.path, file_name), self) for file_name in self.sub_file_name_list]

    def getSubFileList(self, suffix = None) :
        if suffix is None : return self.sub_file_list
        else :
            return [ file for file in self.sub_file_list if file.suffixIs(suffix) ]

    def getFlatternSubFileList(self, suffix = None) :
        file_list = self.getSubFileList(suffix)
        for folder in self.sub_folder_list :
            file_list.extend(folder.getFlatternSubFileList(suffix))
        return file_list

    def json(self) :
        return {
            'Path' : self.path,
            'Name' : self.name,
            'SubFolderList' : [ folder.json() for folder in self.sub_folder_list ],
            'SubFileList' : [ file.json() for file in self.sub_file_list ],
        }
