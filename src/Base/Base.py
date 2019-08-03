# -*- coding: utf-8 -*-  
from util import *

class Base() : # Requester

    config            = {}
    is_login          = False

    def __init__(self, login_filename = None) :
        if not self.is_login : self.login(login_filename)

    @classmethod
    def login(cls, login_filename = None) :
        from util import Timer, load_json, requests, GREEN, RED, END
        Timer.printTiming()
        # print(RED, os.path.realpath('../Taleopard-Operation'), exists('../Taleopard-Operation'), END)
        if login_filename is None :
            config_login = load_json(open('../../../Taleopard-Operation/config/login.json'))
        else :
            config_login = load_json(open(login_filename))
        cls.updateConfig(config_login)
        username, password = cls.config['Username'], cls.config['Password']
        print('尝试获取教师 {} 的token...'.format(username), end = '')
        url = 'https://v.helloword.cn/hw/api/v2/u/login'
        post_data = Dict({ 'Username' : username, 'Password' : password })
        response = requests.post(url, data = post_data.j().encode('utf-8'))
        if response.status_code == 200 :
            print(GREEN, '成功', END, end = '')
            cls.updateConfig({ 'token' : { 'token' : response.json()['data']['Token'] } })
            cls.is_login = True
        else :
            print(RED, '失败', response.status_code, END)
            exit()
        Timer.printLastTiming()
        print()

    @classmethod
    def updateConfig(cls, config) :
        cls.config.update(config)
        return cls

    def get(self, url, params = {}, timeout = None) :
        from util import requests, GREEN, RED, END
        params.update(self.config['token'])
        response = requests.get(url, params = params, timeout = timeout)
        json_data = Dict(response.json())
        if response.status_code != 200 or json_data['code'] != 2 :
            print(json_data.j())
            print(RED, response.status_code, json_data['code'], END)
        else :
            print(GREEN, response.status_code, json_data['code'], END)
        return response

    def post(self, url, data = None, params = {}, timeout = None) :
        from util import requests, GREEN, RED, END
        params.update(self.config['token'])
        response = requests.post(url, data = data.j().encode('utf-8'), params = params, timeout = timeout)
        json_data = Dict(response.json())
        if response.status_code != 200 or json_data['code'] != 2 :
            print(json_data.j())
            print(RED, response.status_code, json_data['code'], END)
        else :
            print(GREEN, response.status_code, json_data['code'], END)
        return response

if __name__ == '__main__':
    pass