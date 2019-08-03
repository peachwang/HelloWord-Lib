# -*- coding: utf-8 -*-  
from util import *
from File import File
from os import rename, listdir, remove, mkdir, makedirs, walk

class Folder(Object) :

    def __init__(self, folder_path) :
        Object.__init__(self)
        self.path, self.sub_folder_name_list, self.sub_file_name_list = list(walk(folder_path))[0]
        self.path.rstrip('/')
        self.name = self.path.split('/')[-1]
        self.sub_folder_list = [ Folder('{}/{}'.format(self.path, folder_name)) for folder_name in self.sub_folder_name_list]
        self.sub_file_list   = [ File('{}/{}'.format(self.path, file_name), self) for file_name in self.sub_file_name_list]

    @classmethod
    def mkdir(cls, path) :
        os.mkdir(path)

    @classmethod
    def exists(cls, path) :
        return os.path.exists(path)

    def getSubFileList(self, ext = None) :
        if suffix is None : return self.sub_file_list
        else :
            return List([ file for file in self.sub_file_list if file.extIs(ext) ])

    def getFlatternSubFileList(self, suffix = None) :
        file_list = self.getSubFileList(suffix)
        for folder in self.sub_folder_list :
            file_list.extend(folder.getFlatternSubFileList(suffix))
        return file_list

    def json(self) :
        return Dict({
            'Path' : self.path,
            'Name' : self.name,
            'SubFolderList' : [ folder.json() for folder in self.sub_folder_list ],
            'SubFileList' : [ file.json() for file in self.sub_file_list ],
        })
