# -*- coding: utf-8 -*-  
import sys, os; sys.path.extend([os.path.abspath(_[0]) for _ in os.walk(os.path.join(os.getcwd(), '../'))]);
from util import *
from Table import *
from openpyxl import Workbook

# class Frequency
# 
# @property dict config
# @property dict _words
#   <WordForm str> {}
#     WordForm str
#     TotalFrequency int
#     Categories {}
#         <CategoryName str> <Frequency int>
#     Sources []
#         <SourceName str>
# @property dict _categories
#   <CategoryName str> <Frequency int>
# @property dict _sources
#   <SourceName str> <Frequency int>
# 
# @method       clear()
# @method       _addWord(str wordForm, str categoryName, str sourceName)
# @method       addSentence(str sentence, str categoryName, str sourceName, str seperator = '[^a-zA-Z]+')
# @method tuple _addByRule(dict rule, *args)
# @method       _addTableRow(dict tableRow, list rules)
# @method       addTable(Table table, list rules)
# @method       addFile(io fin, str filename, list rules)
# @method       addFiles(list filenames, list rules)
# @method       addFolder(str folderName, list rules)
# @method       addFolders(list folderNames, list rules)
# @method tuple getFlattenedData()
class Frequency :

    _words      = None
    _categories = None
    _sources    = None

    def __init__(self, config) :
        self._config = config
        self.clear()

    # Clears the frequency generator.
    def clear(self) :
        self._words      = {}
        self._categories = {}
        self._sources    = {}

    # Adds a single word.
    # @param str wordForm
    # @param str categoryName
    # @param str sourceName
    def _addWord(self, wordForm, categoryName, sourceName) :
        if wordForm == '' : return
        wordForm = wordForm.lower()
        if self._words.get(wordForm) is None :
            self._words[wordForm] = {
                'WordForm'       : wordForm,
                'TotalFrequency' : 0,
                'Categories'     : {categoryName : 1},
                'Sources'        : [],
            }
        elif self._words[wordForm]['Categories'].get(categoryName) is None :
            self._words[wordForm]['Categories'][categoryName] = 1
        else :
            self._words[wordForm]['Categories'][categoryName] += 1
        if sourceName not in self._words[wordForm]['Sources'] :
            self._words[wordForm]['Sources'].append(sourceName)
        self._words[wordForm]['TotalFrequency'] += 1
        if self._categories.get(categoryName) is None :
            self._categories[categoryName] = 1
        else :
            self._categories[categoryName] += 1
        if self._sources.get(sourceName) is None :
            self._sources[sourceName] = 1
        else :
            self._sources[sourceName] += 1

    # Adds a sentence consisting of multiple words.
    # @param str sentence
    # @param str categoryName
    # @param str sourceName
    # @param str seperator
    def addSentence(self, sentence, categoryName, sourceName, seperator = '[^a-zA-Z]+') :
        for wordForm in re.split(seperator, sentence) :
            self._addWord(wordForm, categoryName, sourceName)

    # Adds data generically by using a rule to generate arguments for addSentence(),
    # and returns the arguments generated.
    # @param dict rule
    #   [criterion]  function
    #   sentence     function
    #   categoryName function
    #   sourceName   function
    #   [seperator]  function
    # @return tuple
    #   <criterion bool>
    #   <sentence str>
    #   <categoryName str>
    #   <sourceName str>
    #   <seperator str>
    def _addByRule(self, rule, *args) :
        criterion    = True if rule.get('criterion') is None else rule['criterion'](*args)
        sentence     = rule['sentence'](*args)
        categoryName = rule['categoryName'](*args)
        sourceName   = rule['sourceName'](*args)
        seperator    = '[^a-zA-Z]+' if rule.get('seperator') is None else rule['seperator'](*args)
        if criterion :
            self.addSentence(sentence, categoryName, sourceName, seperator)
        return criterion, sentence, categoryName, sourceName, seperator

    # Adds a tableRow of a table-style data.
    # @param dict tableRow
    #   <fieldName str> <fieldData mixed>
    # @param list rules
    #   <rule>
    def _addTableRow(self, tableRow, rules) :
        for rule in rules :
            self._addByRule(rule, tableRow)

    # Adds a table-style data.
    # @param Table table
    # @param list rules
    #   <rule>
    def addTable(self, table, rules) :
        for tableRow in table.getData() :
            self._addTableRow(tableRow, rules)

    # Adds the content of a file.
    # @param IO   fin
    # @param str  filename
    # @param list rules
    #   <rule>
    def addFile(self, fin, filename, rules) :
        lines = fin.readlines()
        for rule in rules :
            for index, line in enumerate(lines) :
                self._addByRule(rule, filename, index, line)

    # Adds multiple files.
    # @param list filenames
    #   <filename str>
    # @param list rules
    #   <rule>
    def addFiles(self, filenames, rules) :
        for filename in filenames :
            fin = open(filename, 'r')
            self.addFile(fin, filename, rules)

    # Adds all files under a folder.
    # @param str folderName
    # @param list rules
    #   <rule>
    def addFolder(self, folderName, rules) :
        for folder in os.walk(folderName) :
            self.addFiles([join(folder[0], filename) for filename in folder[2]], rules)

    # Adds multiple folders.
    # @param list folderNames
    #   <folderName str>
    # @param list rules
    #   <rule>
    def addFolders(self, folderNames, rules) :
        for folderName in folderNames :
            self.addFolder(folderName, rules)

    # Returns the 2-D form property data that can be written to IO.
    # @return tuple
    #   <fieldNames str>
    #   <words dict>
    #   <categories dict>
    #   <sources dict>
    def getFlattenedData(self) :
        category_name_list = self._categories.keys()
        fieldNames = ['WordForm', 'TotalFrequency'] + category_name_list + ['Sources']
        _words = self._words.copy()
        for wordForm in _words.keys() :
            _words[wordForm]['Sources'] = ','.join(_words[wordForm]['Sources'])
            _words[wordForm].update(dict([(_, 0) for _ in category_name_list]))
            _words[wordForm].update(_words[wordForm]['Categories'])
            _words[wordForm].pop('Categories')
        return fieldNames, _words, self._categories.copy(), self._sources.copy()

    def saveWorkbook(self, filename) :
        fieldNames, words, categories, sources = self.getFlattenedData()
        wb = Workbook()
        ws = wb.active
        ws.append(fieldNames)
        for word in sorted(words.values(), key = lambda _ : _['TotalFrequency'], reverse = True) :
            ws.append(map(word.get, fieldNames))
        wb.save(filename)

if __name__ == '__main__':
    f = Frequency({})
    rule = {
        'sentence' : lambda _1, _2 : _1 + '.' +_2,
        'categoryName' : lambda _1, _2 : _1 + '@' +_2,
        'sourceName'   : lambda _1, _2 : _1 + '#' +_2,
    }
