# -*- coding: utf-8 -*-  
import sys, os; sys.path.extend([os.path.abspath(_[0]) for _ in os.walk(os.path.join(os.getcwd(), '../'))]);
from util import *

class Config_Generator :

    '''
    功能
        返回我们需要的配置文件内容
    步骤
        有许多xxx_config.json, 其内含信息的specific程度不同，可能有多支的继承关系
        传入最specific的那个.json的信息
        归并与其有继承性质的config串生成本次需要的配置文件内容
    应用场景
        在某个指挥官task里实例化后用于归并一系列.json 然后返回出本次能用的Dict of config
    '''

    def __init__(self, config_path) :
        '''
        功能
            接受最specific的.json路径，存入类内共享数据区域
        参数表
            config_path string : '../config/XXX.json'
        返回值(产生值?)
            self.config
        '''

        self.config = load_json(open(config_path))

    def merge_config(self) :
        '''
        功能
            归并有继承性质的config串
        参数表
            self
        返回值
            归并更新后的self.config
        NOTE :
            .json中'Parent_Path_List'的value : List of path
            path 如何写，需要考虑应用场景而包含相对路径吗
        '''

        while not (self.config.get('Parent_Path_List') == None) :
            config = {}
            for index in range(len(self.config['Parent_Path_List'])) :
                config.update(load_json(open(self.config['Parent_Path_List'][index])))
            self.config.pop('Parent_Path_List')
            config.update(self.config)
            self.config = config

        return self.config
