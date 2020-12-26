# -*- coding: utf-8 -*-
__author__ = 'zhoutao2'

import os,time
import yaml
from Base import ReadConfig
from Base.Mylog import LogManager

logger = LogManager('yamlAnalysis').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'



class yamlAnalysis:
    def __init__(self):
        self.data = None
        self.yaml = ReadConfig.conf_path + 'application.yml'

    def get_config(self):
        with open(self.yaml, 'r', encoding="utf-8") as f:
            yml_data = f.read()

            # load方法转出为字典类型
            self.data = yaml.load(yml_data)
        return self.data

    def get_crmRouteConfig(self):
        '''获取crm路由配置'''
        return self.get_config()['route']['crm']

    def get_jourRouteConfig(self):
        '''获取jour路由配置'''
        return self.get_config()['route']['jour']

    def get_tableMappingConfig(self):
        '''获取jour路由配置'''
        return self.get_config()['table-mapping']

    def get_orderMappingConfig(self):
        '''获取jour路由配置'''
        return self.get_config()['table-mapping']['order']['user']
# 打印测试
if __name__ == '__main__':
    y = yamlAnalysis()
    print(y.get_crmRouteConfig())
    print(y.get_jourRouteConfig())
    print(y.get_tableMappingConfig())
    print(y.get_orderMappingConfig())







