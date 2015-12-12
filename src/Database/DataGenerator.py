# -*- coding: utf-8 -*-  
from util import *
from MongoDB import *
from Log import *

class DataGenerator :

    def __init__(self, config) :
        self.config = config
        self.log = Log_Processor(config)
        self.m = MongoDB().select_db(self.config['Database'])

    def check_duplicate(self, data) :
        return len(list(self.m.find({'_id' : data['_id']}).limit(1))) == 1

    def check_content(self, element, checklist) :
        return True
        # for item in checklist :
        #     if item == 'Phonetic' :
        #         if (element['Content']['UK'] == 'None' or element['Content']['US'] == 'None') :
        #             self.log.receive_message(('Phonetic missing - word, UK, US, Default: %s, %s, %s, %s' % (element['Content']['Word'], element['Content']['UK'], element['Content']['US'], element['Content']['Default'])), ['error'])
        #             if (element['Content']['Default'] == 'None' and element['Content']['UK'] == 'None' and element['Content']['US'] == 'None') :
        #                 return False
        #             else :
        #                 return True
        #         else :
        #             return True

    def export_data(self, data) :
        if self.check_duplicate(data) :
            sys.stdout.write('%(_id)s duplicate.\n' % data)
        else :
            self.m.save(data)
            sys.stdout.write('%(_id)s done.\n' % data)
        self.log.export_message()
