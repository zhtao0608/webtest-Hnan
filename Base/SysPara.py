# -*- coding:utf-8 -*-
# __author:zhoutao2
# 从mysql数据库获取对应的系统参数
# date: 2019/12/28


import os,time,datetime
import time
from Base.Mylog import LogManager
from Base.MyDBOper import DbManager
from Base import ReadConfig

rc = ReadConfig.ReadConfig("ngboss_config.ini")
# 加入日志
# 获取logger实例
logger = LogManager('MyDBOper').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

class SysPara():
    '''获取系统参数的类'''
    def getSysParaByCode(self,paramCode,paramAttr,provCode='HNAN'):
        '''
        根据定义的编码获取系统参数
        :param paramCode: 参数编码
        :param paramAttr: 参数属性
        :param provCode: 省份，默认  QHAI
        :return: 返回paramValue
        '''
        if paramCode == '' or paramAttr=='':
            raise RuntimeError('paramCode和paramAttr入参不允许空')

        sql = """select param_value from autotest_sys_para where prov_Code ='{}' and  param_Attr ='{}'  and  param_Code ='{}' ;  
              """.format(provCode,paramAttr,paramCode)
        logger.info(sql)
        try:
            result = DbManager().select(sql)[0]['param_value']
            return result
        except:
            logger.info('查询结果为空')
            raise



    def get_ngboss(self,args):
        '''
        args 登录入参
        :return:
        '''
        if args =='url':
            paramCode = 'env.Url'
        elif args =='username':
            paramCode = 'env.LoginName'
        elif args =='password':
            paramCode = 'env.LoginPwd'
        paras = self.getSysParaByCode(paramAttr='NGBOSS',paramCode=paramCode)
        logger.info('登录参数{}'.format(paras))
        return paras

    def get_oracle(self,route):
        '''
        route 路由
        :return:
        '''
        if route == '':
            raise RuntimeError('必须传入路由编码')
        paras = self.getSysParaByCode(paramAttr='DBRoute',paramCode=route)
        return paras

    def get_IntfUrl(self,center):
        '''
        center 模块
        :return:
        '''
        return self.getSysParaByCode(paramAttr='IntfUrl',paramCode=center)




if __name__ == '__main__':
    Para = SysPara()
    # url = Para.get_ngboss('url')
    # username = Para.get_ngboss('username')
    # password = Para.get_ngboss('password')
    # print(password)
    # passwd = Para.get_ngboss('password')
    # print('登录地址:{},用户名:{},密码:{}'.format(url,username,password))
    jour42 = Para.get_oracle('jour42')
    print(jour42)
    orderIntfUrl = Para.get_IntfUrl('order')
    print(orderIntfUrl)