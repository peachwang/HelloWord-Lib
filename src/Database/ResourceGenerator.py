# -*- coding: utf-8 -*-  
from Phonetic import *
from Youdao import *
from DataGenerator import *

class ResourceGenerator(DataGenerator) :

    def __init__(self, config) :
        Data_Generator.__init__(self, config)
        self.config = config
        self.m = MongoDB().select_db(self.config['Database']).select_collection('Resource')
        self.p = Phonetic()
        self.y = Youdao()
        self.explanation_patch = load_json(open(self.config['Path_ExplanationPatch']))
        self.success = False

    def is_success(self):
        return self.success

    def cut_word(self, word, length):
        if len(word) <= length:
            return word
        try:
            word = re.findall('(.*;).+', word)[0]
        except:
            return word
        return cut_word(word,length)  

    def generate_resource(self, word, resource_type) :
        data = {'_id' : '%s_%s' % (word, resource_type)}
        if self.check_duplicate(data) :
            sys.stdout.write('Resource %s_%s duplicate.\n' % (word, resource_type))
            self.success = True
            return data
        else :
            self.success = False
            if resource_type == 'clue' :
                resource = {
                    '_id' : word + '_clue',
                    'Content' : {
                        'Word' : word,
                    },
                    'Meta' : {
                        'Type' : 'Word',
                    }
                }
                # if self.config['Need_Check_Duplicate'] and self.check_duplicate(resource):
                #     self.success = True
                # else:
                phonetic = self.p.get_phonetic(word)
                if phonetic == False :
                    self.success = False
                    sys.stdout.write('Getting phonetic failed: %s\n' % word)
                    self.log.receive_message(('Getting phonetic failed: %s' % (word)), ['error'])
                else :
                    resource['Content'].update(phonetic)
                    self.success = self.check_content(resource, ['Phonetic'])
            if resource_type == 'target' :
                resource = {
                    '_id' : word + '_target',
                    'Content' : {
                        'Word' : word,
                        'Explanation' : None
                    },
                    'Meta' : {
                        'Type' : 'Explanation',
                    }
                }
                # this part is temporary for July 19 project, need improvement afterwards
                # if self.config['Need_Check_Duplicate'] and self.check_duplicate(resource):
                #     self.success = True
                
                if self.config['Target'] == 'Youdao_SimpleSense' :

                    if self.explanation_patch.has_key(word) :
                        explanation = self.y.get_pos(self.explanation_patch[word])
                    else :
                        explanation = self.y.get_pos(self.y.curl_SimpleSense(word))

                    if len(explanation) == 0 or len(explanation[0]) < 2:
                        sys.stdout.write('explanation not found for word: %s : %s\n' % (word, explanation))
                        self.log.receive_message(('explanation not found for word: %s : %s' % (word, explanation)), ['error'])
                        self.success = False
                    elif explanation[0] == 'pos error' :
                        self.log.receive_message(('Pos not exist: %s' % word), ['error'])
                        self.success = False
                    else:
                        resource['Content']['Explanation'] = explanation
                        self.success = True
                else :
                    pass
            if resource_type == 'supplement':
                pass

            self.log.export_message()
            return resource
