# -*- coding: utf-8 -*-  
import sys, os; _paths = filter(lambda _ : _.split('/')[-1] in ['src', 'HelloWord'], [os.path.realpath(__file__ + '/..' * (_ + 1)) for _ in range(os.path.realpath(__file__).count('/'))]); sys.path.extend([_[0] for _ in os.walk(_paths[0])] + [_[0] for _ in os.walk(_paths[1] + '/HelloWord-Lib/src')])
from util import *

word_form = 'occur to';
url = 'http://dict.youdao.com/dictvoice?type=0&audio=%s'
open('../data/Phonetic/Youdao/%s.mp3' % word_form, 'w').write(request(url % word_form)['content'])