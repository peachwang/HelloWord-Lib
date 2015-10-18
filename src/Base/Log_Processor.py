# -*- coding: utf-8 -*-  
from util import *


class Log_Processor :
    '''
    应用位置建议：
        log_processor应该是放在哪一个里面；介于其应用于所有的.py，它应该在底层(父类)里面initiate; 
    也就是在data_generator里面 有个self.flog = log_processor(config)
    '''

    
    category_index = {
        'default' :'@',
        'error'   :'#',
        'status'  :'@'
    }

    def __init__(self, config) :
        self.config = config
        self.message_list = [] # list of message

    def create_config_log_name(self) :
        '''
        功能
            创建一个独立的log文件名, 根据时间命名
            NOTE：该function每次跑程序应该只用一次，如果mission程序应该放在mission_generator.py中的_init_里面
        参数表
            self
        返回值
            config，更新过的log
        '''
        # time_id = strftime("%Y%m%d_%H%M%S")
        # if self.config.get('Log_File') is None:
        #     log_name = '%s_%s_%s.txt' % (time_id, self.config.get('Mission_Name'), 'log')
        # else:
        #     log_name = '%s_%s' % (time_id, self.config.get('Log_File'))
        # self.config.update({'Log_File' : log_name})
        return self.config

    def receive_message(self, message, category_list = None) :

        '''
        功能
            接受外界组件传来的信息，存入类内共享数据结构区域
            分类
            NOTE： 将信息加上前缀方面筛选；信息类别的对照表是category_index；
            处理后message根据category_list产生message_list（信息量一样只是前缀不一样）
            i.e: #      2015-07-16 23:23:53    the message body is displayed here
        参数表
            message : 具体的日志字符串
            category: 
        返回值
            方案1 是否成功
            方案2 self
        '''
        datetime = strftime("%Y-%m-%d %H:%M:%S")
        if category_list is None:
            category_list.append['default']
        for category in category_list :
            self.message_list.append('%-2s\t%s\t%s\n' % (self.category_index.get(category), datetime, message))

        return self

    def process_message(self) :
        '''
            功能
                处理
            参数表

            返回值
                self
        '''
        pass
        return self

    def export_message(self, category_list = None) :
        '''
        功能
            把处理好的message写进外部的日志文件
            返回
            可指定类别输出
        参数表
            message
            category LIST OF string : 若干个类别
        返回值
            self
        '''

        self.config = self.create_config_log_name()
        flog = open(join(self.config['Log_Path'], self.config['Log_File']), 'w')
        for index in range(len(self.message_list)):
            flog.write(self.message_list[index])
        self.message_list = []
        return None
        
    def write_log(self, message, category_list = None) :
        '''
            功能
                作为执行程序里面调用的function
                执行class内receive, process, export_message function
                NOTE:适用于读一条写一条，如果是积累一部分message再读取则不适用
                但是方便调取
            参数表
                message_list: string
                category list: list of string
            返回值
                self
        '''
        self.receive_message(message, category_list)
        self.export_message(self.message_list)
