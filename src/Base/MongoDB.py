# -*- coding: utf-8 -*-  
from util import *
import pymongo

# @todo: add more methods and comments

class MongoDB :
    host       = 'mongodb://119.254.210.63' # @todo
    port       = 27017
    db         = None
    collection = None

    def __init__(self, host = None, port = None) :
        if host is None : host = self.host
        if port is None : port = self.port
        self.client   = pymongo.MongoClient(host, port)

    def select_db(self, db_name) :
        self.db = self.client[db_name]
        return self

    def select_collection(self, collection_name) :
        self.collection = self.db[collection_name]
        return self

    def collection_names(self) :
        return self.db.collection_names()

    def insert(self, document) :
        document = deepcopy(document)
        if document.get('Meta') is None : 
            document['Meta'] = {'CreateTime' : datetime.utcnow()} # TODO ModifyTime
        else :
            document['Meta']['CreateTime'] = datetime.utcnow()
        return self.collection.insert(document)

    def save(self, document) :
        document = deepcopy(document)
        if document.get('Meta') is None : 
            document['Meta'] = {'CreateTime' : datetime.utcnow()}
        else :
            document['Meta']['CreateTime'] = datetime.utcnow()
        return self.collection.save(document)

    def find(self, criterion = {}, projection = None) :
        if projection is None : 
            return self.collection.find(criterion)
        else :
            return self.collection.find(criterion, projection)

    def remove(self, criterion = {}) :
        self.collection.remove(criterion)
        return self

    def set(self, criterion, content_dict) :
        self.collection.update(criterion, {'$set' : content_dict})

    def push(self, criterion, content_dict, options = None) :
        if options == None :
            self.collection.update(criterion, {'$push' : content_dict})
        else :
            self.collection.update(criterion, {'$push' : content_dict}, options)
