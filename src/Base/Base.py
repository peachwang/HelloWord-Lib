# -*- coding: utf-8 -*-  
from util import *
from Timer import *

class Base() :

    config            = {}
    is_login          = False

    def __init__(self) :
        if not self.is_login : self.login()

    @classmethod
    def login(cls) :
        Timer.printTiming()
        config_login = load_json(open('../../../Taleopard-Operation/config/login.json'))
        cls.updateConfig(config_login)
        username, password = cls.config['Username'], cls.config['Password']
        print('尝试获取教师 %s 的token...' % username, end = '')
        url = 'https://v.helloword.cn/hw/api/v2/u/login'
        post_data = { 'Username' : username, 'Password' : password }
        response = requests.post(url, data = j(post_data).encode('utf-8'))
        if response.status_code == 200 :
            print(PASS, '成功', END, end = '')
            cls.updateConfig({ 'token' : { 'token' : response.json()['data']['Token'] } })
            cls.is_login = True
        else :
            print(ERRMSG, '失败', response.status_code, END)
            exit()
        Timer.printLastTiming()
        print()

    @classmethod
    def updateConfig(cls, config) :
        cls.config.update(config)
        return cls

if __name__ == '__main__':
    pass