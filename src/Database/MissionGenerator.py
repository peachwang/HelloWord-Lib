# -*- coding: utf-8 -*-  
from TaskGenerator import *

class MissionGenerator(DataGenerator) :

    def __init__(self, config) :
        Data_Generator.__init__(self, config)
        self.config = config
        self.m = MongoDB().select_db(self.config['Database']).select_collection('Mission')
        self.t = Task_Generator(config)
        self.stacklist = [] # store the error words
        self.maxtime = 36000 # I am not sure about the unit of time, is it second? - Ben

    def import_wordlist(self) :
        fin_wordlist = open(join(self.config['Path_WordList'], self.config['Filename_WordList']))
        wordlist = load_txt(fin_wordlist, fields = ['Word'])
        return wordlist

    # Generate task and add task to mission; base on success
    def add_task(self, word, mission):
        random_pause(0.1, 0.12)
        task_creator = self.t
        task = task_creator.generate_task(word['Word'])
        if task_creator.is_success(): # judgement
            self.t.export_data(task)
            task = {
                'TaskID' : task['_id'],
                'Frequency' : 10,
                # Here 'Frequency' should be alterable
            }
            mission['Tasks'].append(task)
            self.m.push({'_id' : self.config['Mission_id']}, {'Tasks' : mission['Tasks'][0]})
            mission['Tasks'] = []
            return True
        else:
            self.stacklist.append(word)
            return False

    def generate_errorlist(self, errorlist) :
        for word in errorlist:
            self.log.receive_message(word['Word'], ['error'])
        self.log.export_message()

    def stack_process(self, errorlist, timing, mission, success, counter):
        sys.stdout.write('start processing stacklist, total: %s for %s time!\n' % (str(len(self.stacklist)), str(counter)))
        
        if success or len(errorlist) == 0 :
            success = True
            return True
        if counter > 2 :
            return False
        if time() - timing > self.maxtime :
            
            return False
        self.stacklist = [] # clear the stack list
        sys.stdout.write('clear the stacklist to length: %s \n' % str(len(self.stacklist)))
        for word in errorlist:
            if self.add_task(word,mission):
                sys.stdout.write('task is added for %s \n' % word['Word'])
            else:
                sys.stdout.write('task encountered error, added to stacklist : %s \n' % word['Word'])
        counter += 1
        return self.stack_process(self.stacklist, timing, mission, success, counter)

    def generate_mission(self, wordlist) :
        mission = {
            '_id'   : self.config['Mission_id'],
            'Tasks' : [],
            'Meta' : {
                'Name'        : self.config['Mission_Name'],
                'Description' : self.config['Mission_Description'],
                'Photo'       : self.config['Photo'],
            },
        }
        self.m.save(mission)
        timing = time() # monitor timing
        count = 0
        for word in wordlist : 
            count += 1
            self.log.receive_message(('%d / %d : %s : %s : %d min' % (count, len(wordlist), word['Word'], ctime(), (time() - timing) / 60)), ['status'])
            sys.stdout.write('%d / %d : %s : %s : %d min \n' % (count, len(wordlist), word['Word'], ctime(), (time() - timing) / 60))
            if self.add_task(word, mission):
                sys.stdout.write('task is added for %s \n' % word['Word'])
            else:
                sys.stdout.write('task encountered error, added to stacklist : %s \n' % word['Word'])

        # start run for error list
        
        if not self.stack_process(self.stacklist, timing, mission, False, 1):
            self.generate_errorlist(self.stacklist)

        self.log.export_message()
        return mission

    def run(self) :
        # self.m.remove()
        # self.t.m.remove()
        # self.t.r.m.remove()
        wordlist = self.import_wordlist()
        mission = self.generate_mission(wordlist)
        # self.export_data(mission)

# if __name__ == '__main__':
#     mapping, sequence = parse_argv(sys.argv)
#     config = load_json(open(mapping['config']))
#     config.update(mapping)
#     m = Mission_Generator(config)
#     m.run()
