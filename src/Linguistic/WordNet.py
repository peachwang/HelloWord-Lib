# -*- coding: utf-8 -*-  
from util import *
from MongoDB import *

class WordNet :
    '''
        'WordFinder' = {
            <WordString in lower case> : {
                <WordString> : <WordCode>,
            }
        }

        Words = {
            <WordCode> : {
                'WordCode' : <WordCode>,
                'Word'     : <WordString>,
                'Senses'   : [<SenseCode>],
            }
        }

        Senses = {
            <SenseCode> : {
                'SenseCode'           : <SenseCode>,
                'Sense'               : <SenseString>,
                'PoSCode'             : <PoSCode>,
                'PoS'                 : <PoS>,
                'CategoryCode'        : <CategoryCode>,
                'Category'            : <CategoryString>,
                'CategoryDescription' : <CategoryDescription>,
                'SearchList'          : [<WordString in lower case>],
                'Synset'              : {
                    <WordCode> : {
                        'WordCode' : <WordCode>,
                        'Word'     : <WordString>,
                        'Frequency : <Frequency>,
                    }
                'Examples'            : {
                    <ExampleCode> : <ExampleString>,
                }
            }
        }

        Examples = {
            <ExampleCode> : {
                'ExampleCode' : <ExampleCode>,
                'Example'     : <ExampleString>,
                'SenseCode'   : <SenseCode>,
            }
        }

        Categories = {
            <CategoryCode> : {
                'CategoryCode'        : <CategoryCode>,
                'Category'            : <CategoryString>,
                'CategoryDescription' : <CategoryDescription>,
            }
        }

    '''

    path_data = '../../data/WordNet'

    filename = {
        'Words'          : 'basic/Word.txt',
        'Senses'         : 'basic/Sense.txt',
        'Examples'       : 'basic/Example.txt',
        'Frequency'      : 'basic/Frequency.txt',
        'SenseToWord'    : 'basic/SenseToWord.txt',
        'SenseToExample' : 'basic/SenseToExample.txt',
        'Categories'     : 'basic/Category.txt',
    }

    filename_out = {
        'Senses'     : 'MongoDB/Sense.js',
        'Categories' : 'MongoDB/Category.js',
    }

    fields = {
        'Words'          : ['Code', 'Word'],
        'Senses'         : ['Code', 'CategoryCode', 'Sense'],
        'Examples'       : ['Code', 'Example'],
        'Frequency'      : ['Frequency', 'SenseCode', 'Word'],
        'SenseToWord'    : ['SenseCode', 'WordCode'],
        'SenseToExample' : ['SenseCode', 'ExampleCode'],
        'Categories'     : ['CategoryCode', 'Category', 'CategoryDescription'],
    }

    mapping = {
        'PoS' : {
            '01' : 'Noun',
            '02' : 'Verb',
            '03' : 'Adjective',
            '04' : 'Adverb',
        },
        'PoSAbbr' : {
            '01' : 'Noun',
            '02' : 'Verb',
            '03' : 'Adj.',
            '04' : 'Adv.',
        }
    }

    WordFinder = {}
    Words      = {}
    Senses     = {}
    Examples   = {}
    Categories = {}

    def clean_word(self, word) :
        return word.replace('(a)', '').replace('(p)', '').replace('(ip)', '')

    def __init__(self, load_data = True) :
        if load_data : self.load_data()

    def load_data(self) :
        timing = time()
        _ = dict([
            (__, load_txt(open(join(self.path_data, self.filename[__]), 'r'), self.fields[__]))
                for __ in self.fields.keys()
        ])
        # sys.stdout.write('%.2f\n' % (time() - timing));sys.stdout.flush();
        
        self.Categories.update(dict([(__['CategoryCode'], __) for __ in _['Categories']]))
        
        for word in _['Words'] :
            word_clean = self.clean_word(word['Word'].lower())
            if self.WordFinder.get(word_clean) is None :
                self.WordFinder[word_clean] = {}
            self.WordFinder[word_clean].update({word['Word'] : word['Code']})
            self.Words[word['Code']] = {
                'WordCode' : word['Code'],
                'Word'     : word['Word'],
                'Senses'   : [],
            }
        # sys.stdout.write('%.2f\n' % (time() - timing));sys.stdout.flush();
        
        for sense in _['Senses'] :
            self.Senses[sense['Code']] = {
                'SenseCode'           : sense['Code'],
                'Sense'               : sense['Sense'],
                'PoSCode'             : sense['Code'][:2],
                'PoS'                 : self.mapping['PoS'][sense['Code'][:2]],
                'CategoryCode'        : sense['CategoryCode'],
                'Category'            : self.Categories[sense['CategoryCode']]['Category'],
                'CategoryDescription' : self.Categories[sense['CategoryCode']]['CategoryDescription'],
                'SearchList'          : [],
                'Synset'              : {},
                'Examples'            : {},
            }
        # sys.stdout.write('%.2f\n' % (time() - timing));sys.stdout.flush();
        
        for example in _['Examples'] :
            self.Examples[example['Code']] = {
                'ExampleCode' : example['Code'],
                'Example'     : example['Example'],
            }
        # sys.stdout.write('%.2f\n' % (time() - timing));sys.stdout.flush();
        
        for mapping in _['SenseToWord'] :
            if self.Senses.get(mapping['SenseCode']) != None :
                self.Senses[mapping['SenseCode']]['Synset'].update({
                    mapping['WordCode'] : {
                        'WordCode'  : mapping['WordCode'],
                        'Word'      : self.Words[mapping['WordCode']]['Word'],
                        'Frequency' : None,
                    }
                })
                WordString = self.Words[mapping['WordCode']]['Word'].lower()
                if WordString not in self.Senses[mapping['SenseCode']]['SearchList'] :
                    self.Senses[mapping['SenseCode']]['SearchList'].append(WordString)
            if self.Words.get(mapping['WordCode']) != None :
                self.Words[mapping['WordCode']]['Senses'].append(mapping['SenseCode'])
        # sys.stdout.write('%.2f\n' % (time() - timing));sys.stdout.flush();
        
        for __ in _['Frequency'] :
            WordCodes = self.WordFinder[__['Word'].lower()].values()
            for WordCode in WordCodes :
                # Case Conflict dealed
                if self.Senses[__['SenseCode']]['Synset'].get(WordCode) != None :
                    self.Senses[__['SenseCode']]['Synset'][WordCode]['Frequency'] = int(__['Frequency'])
        # sys.stdout.write('%.2f\n' % (time() - timing));sys.stdout.flush();
        
        for mapping in _['SenseToExample'] :
            if self.Senses.get(mapping['SenseCode']) != None :
                self.Senses[mapping['SenseCode']]['Examples'].update({
                    mapping['ExampleCode'] : self.Examples[mapping['ExampleCode']]['Example'],
                })
                self.Examples[mapping['ExampleCode']]['SenseCode'] = mapping['SenseCode']
        sys.stdout.write('%.2f\n' % (time() - timing));sys.stdout.flush();
        return self
    
    def stat(self) :
        # print j(sorted(self.WordFinder.values(), key = lambda _ : len(_), reverse = True))
        # print map(' '.join(map(str, map(len, self.WordFinder.values()))).count, map(str, range(1, 6)))
        # print j(self.Words)
        print j(self.Senses)
        # print j(self.Examples)
        return self

    def get_Words(self) :
        return self.Words

    def get_Senses(self) :
        return self.Senses

    def get_Categories(self) :
        return self.Categories

    def morphy(self, inflected_form) :
        regex = 'Overview of (\w+) (.+)'
        out, retval = shell('wn "%s" -g -over | grep "Overview of"' % inflected_form.replace(' ', '_'))
        # if retval != 0 : return False
        lines = [line.strip() for line in out]
        # lines = ['Overview of verb better']
        base_forms = [re.findall(regex, line)[0] for line in lines]
        return [(base_form[0], base_form[1].replace('_', ' ')) for base_form in base_forms]

    def get_senses(self, WordString) :
        _ = []
        if self.WordFinder.get(WordString.lower()) is None : return []
        WordCodes = self.WordFinder[WordString.lower()].values()
        for WordCode in WordCodes :
            for SenseCode in self.Words[WordCode]['Senses'] :
                _.append({
                    'WordString'   : self.Words[WordCode]['Word'],
                    'WordCode'     : WordCode,
                    'SenseCode'    : SenseCode, 
                    'Sense'        : self.Senses[SenseCode]['Sense'],
                    'PoSCode'      : self.Senses[SenseCode]['PoSCode'],
                    'PoS'          : self.Senses[SenseCode]['PoS'],
                    'PoSAbbr'      : self.mapping['PoSAbbr'][self.Senses[SenseCode]['PoSCode']],
                    'CategoryCode' : self.Senses[SenseCode]['CategoryCode'],
                    'Category'     : self.Senses[SenseCode]['Category'],
                    'Frequency'    : self.Senses[SenseCode]['Synset'][WordCode]['Frequency'],
                })
        return _

    def import_sense(self, db, sense) :
        timing = time()
        _ = deepcopy(sense)
        _['Synset']   = [word for word in _['Synset'].values()]
        Examples = [{'ExampleCode' : ExampleCode, 'Example' : Example}
            for ExampleCode, Example in _['Examples'].items()]
        _['Examples'] = Examples
        _ = {'Content' : _}
        _['Meta'] = {'Type' : 'Sense'}
        _['_id']      = _['SenseCode']
        db.save(_)
        return self

    def import_category(self, db, category) :
        _ = deepcopy(category)
        _ = {'Content' : _}
        _['Meta'] = {'Type' : 'Category'}
        _['_id'] = category['CategoryCode']
        db.save(_)
        return self

if __name__ == '__main__':
    # db = MongoDB().select_db('test').select_collection('Content')
    # w = WordNet()
    # for category in w.get_Categories().values() :
    #     w.import_category(db, category)
    #     print j(category)
    w = WordNet(False)
    for line in sys.stdin :
        print '%s\t%s' % (line.strip(), str(w.morphy(line.strip())))
