# -*- coding: utf-8 -*-  
from util import *
from functools import wraps

class Base() : # Requester

    _config   = Dict()
    _is_login = False

    @classmethod
    def __init__(cls, login_filename = None) :
        if not self._is_login : self.login(login_filename)

    @classmethod
    @Timer.timeitOnce
    def login(cls, login_filename = None) :
        if login_filename is None :
            config_login = File('../../../Taleopard-Operation/config/login.json').loadJson()
        else :
            config_login = File(login_filename).loadJson()
        cls.updateConfig(config_login)
        username, password = cls._config.Username, cls._config.Password
        print('尝试获取教师 {} 的token...'.format(username), end = '')
        url = 'https://v.helloword.cn/hw/api/v2/u/login'
        post_data = Dict( Username = username, Password = password )

        response = cls.post(url, data = post_data, timeout = 2)
        if response.status_code == 200 :
            token = Dict(response.json()).data.Token
            print(G, '成功', token, E, end = '')
            cls.updateConfig({ 'token' : { 'token' : token } })
            cls._is_login = True
        else :
            print(R, '失败', response.status_code, E)
            exit()
        print()

    @classmethod
    def updateConfig(cls, config) :
        cls._config.update(config)
        return cls

    def request(func, log = True) :
        @wraps(func)
        def wrapper(cls, *args, **kwargs) :
            kwargs['params'].update(cls._config.token)
            response = func(cls, *args, **kwargs)
            json_data = Dict(response.json())
            if response.status_code != 200 or json_data.code != 2 :
                print(json_data.j())
                print(R, response.status_code, json_data.code, E)
            else :
                print(G, response.status_code, json_data.code, E)
            return response
        return wrapper

    @classmethod
    @request
    def get(cls, url, params = {}, timeout = None) :
        return requests.get(url, params = params, timeout = timeout)

    @classmethod
    @request
    def post(cls, url, data = None, params = {}, timeout = None) :
        return requests.post(url, data = data.j().encode('utf-8'), params = params, timeout = timeout)

if __name__ == '__main__':
    pass