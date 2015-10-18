# -*- coding: utf-8 -*-  
import sys, os; sys.path.append(os.path.join(sys.path[0], '../../HelloWord-Lib')); from util import *
from Wordbase import *
#import mp3play

class Phonetic :
    path_phonetic = '../data/General/Phonetic.txt'
    path_audio    = '../data/General/Audio'

    url = {
        'phonetic' : 'http://dict.youdao.com/search?q=%(word)s&keyfrom=dict.index',
        'audio'    : {
            'default' : 'http://dict.youdao.com/dictvoice?audio=%(word)s&type=0',
            'uk'      : 'http://dict.youdao.com/dictvoice?audio=%(word)s&type=1',
            'us'      : 'http://dict.youdao.com/dictvoice?audio=%(word)s&type=2',
        },
    }

    pattern = {
        'UK'      : r'<span class="pronounce">\xe8\x8b\xb1\s+<span class="phonetic">([^<]+)</span>',
        'US'      : r'<span class="pronounce">\xe7\xbe\x8e\s+<span class="phonetic">([^<]+)</span>',
        'Default' : r'<span class="pronounce">\s+<span class="phonetic">([^<]+)</span>',
    }

    def __init__(self) :
        self.Phonetics = Wordbase().import_txt(open(self.path_phonetic, 'r')).get_Words()

    def get_Phonetics(self) :
        return self.Phonetics

    def set_Phonetics(self, Phonetics) :
        self.Phonetics = Phonetics
        return self

    def export_Phonetics(self, fout = None) :
        if fout is None : fout = open(self.path_phonetic, 'w')
        Wordbase().set_Words(self.Phonetics).export_txt(fout, field_list = ['Word', 'UK', 'US', 'Default'])
        return self

    def curl_audio(self, word, country = 'default') :
        content    = request(self.url['audio'][country] % {'word' : word, 'country' : country})['content']
        path_audio = join(self.path_audio, '%(word)s_%(country)s.mp3' % {'word' : word, 'country' : country})
        open(path_audio, 'wb').write(content)
        return path_audio

    def get_audio(self, word, country = 'default') :
        path_audio = join(self.path_audio, '%(word)s_%(country)s.mp3' % {'word' : word, 'country' : country})
        if exists(path_audio) : return path_audio
        else : return self.curl_audio(word, country)

    def extract_phonetic(self, html, country) :
        _ = re.findall(self.pattern[country], html)
        if len(_) == 0 : return 'None'
        else : return _[0]

    def curl_phonetic(self, word, timeout = 1) :
        res = request(self.url['phonetic'] % {'word' : word}, timeout = timeout)
        if res['e'] is not None : return False
        else :
            html = res['content']
            country_list = ['UK', 'US', 'Default']
            _ = {'Word' : word}
            _.update({country : self.extract_phonetic(html, country) for country in country_list})
            return _

    def update_phonetic(self, word, phonetic = None) :
        self.Phonetics[word] = self.curl_phonetic(word) if phonetic is None else phonetic
        return self

    def get_phonetic(self, word) :
        if self.Phonetics.get(word) is None :
            self.update_phonetic(word)
        return self.Phonetics[word]
    
if __name__ == '__main__':
    phonetic = Phonetic()
    lines = sys.stdin.readlines()
    for index, line in enumerate(lines) :
        _ = phonetic.get_phonetic(line.strip())
        format = '%(index)4d/%(tot)4d  %(Word)-20s %(UK)-20s %(US)-20s %(Default)-20s\n'
        data   = {'index' : index + 1, 'tot' : len(lines)}
        data.update(_)
        sys.stdout.write((format % data))
        sys.stdout.flush()
        #audio = mp3play.load(phonetic.get_audio(line.strip(), 'default'))
        #audio.play()
        #sleep(min(5, audio.seconds() + 0.5))
        #audio.stop()
        
    # phonetic.export_Phonetics()
    # print phonetic.get_phonetic('apple')