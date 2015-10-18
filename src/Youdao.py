# -*- coding: utf-8 -*-  
from util import *
from MongoDB import *
from Phonetic import *

class Youdao:

    url = {
        'Word' : 'http://dict.youdao.com/search?q=%(Word)s&keyfrom=dict.index',
    }

    pattern = {
        'SimpleSense_ul' : '<div class="trans-container">\s*<ul>\s*(.+?)\s*</ul>',
        'SimpleSense_li' : '<li>(.*?)</li>',
        'Morphy'         : '</ul>\s*<p class="additional">\[\s*(.+)\s*\]</p>',
        'Morphy_pl'      : '复数\s*(\w+)\s*',
        'Morphy_sftp'    : '第三人称单数\s*(\w+)\s*',
        'Morphy_pt'      : '过去式\s*(\w+)\s*',
        'Morphy_pap'     : '过去分词\s*(\w+)\s*',
        'Morphy_prp'     : '现在分词\s*(\w+)\s*',
        'Morphy_cd'      : '比较级\s*(\w+)\s*',
        'Morphy_sd'      : '最高级\s*(\w+)\s*',
    }

    pos_list = ["n.", "vi.", "vt.", "adj.", "adv.", "prep.", "art.", "pron.", "num.", "int.", "conj."]

    morphy_list = ['Morphy_pl','Morphy_sftp','Morphy_pt','Morphy_pap','Morphy_prp','Morphy_cd','Morphy_sd']
    Phonetic = None

    def __init__(self) :
        pass

    def curl_html(self, word) :
        url = self.url['Word'] % {'Word' : word}
        content = request(url)['content']
        return content

    def curl_SimpleSense(self, word, content = None) :
        if content is None : content = self.curl_html(word)
        ul = re.findall(self.pattern['SimpleSense_ul'], content, re.DOTALL)
        if len(ul) > 0 :
            return re.findall(self.pattern['SimpleSense_li'], ul[0])
        else :
            return []

    def get_pos(self, SimpleSense) :

        '''
        curl_SimpleSense() 取得原始字符串列表
        get_pos() 处理字符串列表
            全部成功：返回处理后的字符串列表
            有没成功的：返回['pos error']
        * Resource_Generator 里容错机制的判定条件相应改动
        '''
        return SimpleSense

        # explanation = []
        # for explan_string in SimpleSense :
        #     try :
        #         explan_pair = explan_string.split()
        #         if not (explan_pair[0] in self.pos_list) :
        #             raise LookupError
        #         explanation.extend(explan_pair)
        #     except LookupError :
        #         explanation = ['pos error']
        # return explanation

    def curl_Morphy(self, word, content = None) :
        if content is None : content = self.curl_html(word)
        additional = re.findall(self.pattern['Morphy'], content, re.DOTALL)
        if len(additional) == 1 :
            morphy = {}
            for field in self.morphy_list :
                morphy[field] = re.findall(self.pattern[field], additional[0])
            return morphy
        else :
            if len(additional) > 1 :
                print word
                print additional
                exit()
            return []
    
    def import_Word(self, db, p, word) :
        db.select_collection('Word')
        _ = {}
        _['Phonetic'] = p.get_phonetic(word)
        _['Phonetic'].pop('Word')
        _['SimpleSense'] = self.curl_SimpleSense(word)
        db.save(_)

if __name__ == '__main__':
    y = Youdao()
    p = Phonetic()
    db = MongoDB().select_db('test')
    for line in sys.stdin :
        print line.strip()
        y.import_Word(db, p, line.strip())
    # print y.curl_Morphy('apple')
    # print j(y.curl_SimpleSense('take'))