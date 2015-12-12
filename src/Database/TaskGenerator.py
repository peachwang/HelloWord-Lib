# -*- coding: utf-8 -*-  
from ResourceGenerator import *

class TaskGenerator(DataGenerator) :

    type_list = {
        'clue'      : 'word',
        'target'    : 'simplesense',
        'supplement': 'blablabla'
    }
    typelist_to_typename = {
        'clue'       : 'Clue',
        'target'     : 'Target',
        'supplement' : 'Supplement'
    }

    def __init__(self, config) :
        Data_Generator.__init__(self, config)
        self.config = config
        self.m = MongoDB().select_db(self.config['Database']).select_collection('Task')
        self.r = Resource_Generator(config)
        self.success = False

    def is_success(self):
        return self.success

    def add_resource(self, word, task, r_type):
        # resource_creator = self.r # @PeachWang please check if I can write it in this way
        data = {'_id' : '%s' % word}
        if self.check_duplicate(data) :
            sys.stdout.write('Task %s duplicate.\n' % word)
            self.success = True
            return True
        else :
            random_pause(0.2, 0.22)
            element = self.r.generate_resource(word, r_type)
            if self.r.is_success() :
                sys.stdout.write('Resource success for %s\n' % word)
                self.r.export_data(element)
                content = {
                    'ResourceID' : element['_id'],
                    'Meta' : {
                        'Type' : self.type_list[r_type]
                    }
                }
                type_name = self.typelist_to_typename[r_type]
                task['Content'][type_name].append(content)
                self.success = True
                return True
            else :
                self.sucess = False
                self.log.receive_message(('content failed for type: %s, %s' % (word, r_type)), ['error'])
                return False

    def generate_task(self, word) :
        task = {
            '_id' : word,
            # the _id may have to be changed
            'Content' : {
                'Task' : 'Normal',
                'Supplement' : [],
                'Target' : [],
                'Clue' : []
            },
        }
        
        clue = self.add_resource(word, task, 'clue') 
        target = self.add_resource(word, task, 'target')
        # supplement = 

        if not (clue and target): self.success = False
        
        return task
