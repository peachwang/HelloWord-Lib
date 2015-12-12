# -*- coding: utf-8 -*-  
from util import *

class Wordbase :
    Words = {}

    def __init__(self) :
        pass

    def get_Words(self) :
        return self.Words

    def set_Words(self, Words) :
        self.Words = Words
        return self

    def init_Words(self) :
        self.Words = {}
        return self

    def print_Words(self, fout = sys.stdout) :
        fout.write(str(len(self.Words)) + '\n')
        fout.write(j(self.Words) + '\n')
        fout.flush()

    def import_db(self, fin) :
        items = [dict(re.findall('\[([^\n\]]+)\]([^\n]*)\n', unicode(item, 'cp936', 'ignore').encode('utf-8'))) \
            for item in re.findall('\{\n([^\}]+)\}\n', '\n'.join([line.strip() \
                for line in fin.readlines()]) + '\n')]
        self.Words.update({item['Word'] : item for item in items})
        return self

    def import_json(self, fin) :
        self.Words.update(load_json(fin, decode_dict))
        return self

    def import_txt(self, fin) :
        fields = fin.readline().strip().split('\t')
        Words = load_txt(fin, fields)
        self.Words.update({(word['Word'] if word.get('Word') != None else word['word']) : word for word in Words})
        return self

    def import_Words(self, filename) :
        ext = split_filename(filename)[1]
        if ext in ['db', 'json', 'txt'] and exists(filename) :
            return {
                'db'   : self.import_db,
                'json' : self.import_json,
                'txt'  : self.import_txt,
            }[ext](open(filename, 'r'))
        else : return self

    def export_db(self, fout, Words = None) :
        if Words is None : Words = self.Words
        if key   is None : lambda (word, fields) : word
        for index, (word, fields) in enumerate(sorted(Words.items(), key = key)) :
            fields['AutoNO'] = index + 1
            format = '{\n%s}\n'
            data   = ''.join(['[%s]%s\n' % (field, content) for field, content in fields.items()])
            fout.write(unicode(format % data, 'utf-8', 'ignore').encode('cp936'))
            fout.flush()
        return self

    def export_json(self, fout, Words = None) :
        if Words is None : Words = self.Words
        for index, (word, fields) in enumerate(sorted(Words.items(), key = lambda (word, fields) : word)) :
            fields['AutoNO'] = index + 1
        fout.write(j(Words))
        fout.flush()
        return self

    def export_txt(self, fout, Words = None, field_list = None) :
        if Words is None : Words = self.Words
        if field_list is None :
            field_list = []
            for fields in Words.values() :
                for field in fields.keys() :
                    if field not in field_list : field_list.append(field)
            for field in ['Word', 'word', 'Index', 'index', 'No', 'no'] :
                if field in field_list :
                    field_list.pop(field_list.index(field))
                    field_list = [field] + field_list
            if 'AutoNO' in field_list : field_list.pop(field_list.index('AutoNO'))
        fout.write('\t'.join(field_list) + '\n')
        key = lambda fields : int(fields['No']) if fields.get('No') != None else (fields['Word'] if fields.get('Word') != None else (fields['word']))
        for fields in sorted(Words.values(), key = key) :
            format = '%s\n'
            data   = '\t'.join(map(lambda field : str(fields.get(field, '')), field_list))
            fout.write(format % data)
            fout.flush()
        return self

if __name__ == '__main__':
    wordbase = Wordbase()
    for line in sys.stdin.readlines() :
        wordbase.import_Words(line.strip())
    wordbase.print_Words()