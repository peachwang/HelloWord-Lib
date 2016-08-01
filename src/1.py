# -*- coding: utf-8 -*-  
import sys, os; _paths = filter(lambda _ : _.split('/')[-1] in ['src', 'HelloWord'], [os.path.realpath(__file__ + '/..' * (_ + 1)) for _ in range(os.path.realpath(__file__).count('/'))]); sys.path.extend([_[0] for _ in os.walk(_paths[0])] + [_[0] for _ in os.walk(_paths[1] + '/HelloWord-Lib/src')])
from util import *

path = '../../../HelloWord-Frontend-Test/dist/audio/%s.mp3'
# path = '../../HelloWord-Thesaurus/data/Phonetic/Youdao/%s.mp3'

def stat(word_form_list) :
    existing = []
    not_existing = []
    for word_form in word_form_list :
        if exists(path % word_form) :
            if getsize(path % word_form) == 0 :
                remove(path % word_form)
                print '0', safe(word_form)
                not_existing.append(word_form)
            else :
                print '1', safe(word_form), getsize(path % word_form)
                existing.append(word_form)
        else :
            print '0', safe(word_form)
            not_existing.append(word_form)
    print len(word_form_list), len(existing), len(not_existing)
    return existing, not_existing


url = 'http://localhost/api/a/c/r/wbe/wf'
count = int(json.loads(request(url, getData = { 'start' : 0, 'offset' : 1})['content'])['data']['countAll'])
word_form_list = []
start = 0
offset = 100
count = 300
while start < count :
    print time()
    word_form_list.extend(json.loads(request(url, getData = { 'start' : start, 'offset' : offset})['content'])['data']['WordFormList'])
    start += offset

existing, not_existing = stat(word_form_list)

url = 'http://dict.youdao.com/dictvoice?type=0&audio=%s'
for word_form in not_existing :
    print ctime(), word_form
    open(path % word_form, 'w').write(request(url % word_form)['content'])
existing, not_existing = stat(word_form_list)

