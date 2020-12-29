import os,time
from Base.Mylog import LogManager
from Data.DataMgnt.DataFact import DataFact
from Base.SysPara import SysPara
from Data.DataMgnt.DataOper import DataOper as Dto
from Base import ReadConfig
from Common.dealParas import capital_to_upper
from Common.dealParas import ConvertParas
from Api.Auth import UserAuth as Auth
import requests


# 加入日志
# 获取logger实例
logger = LogManager('ApiDefine').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

class ApiDefine(Dto):
    '''API定义处理类'''
    def __init__(self):
        self.url = SysPara().get_IntfUrl('order')
        self.token = Auth().generateByName(userName='SUPERUSR')
        self.h = {"Authorization":self.token}
        self.tabName = 'AUTOTEST_API_DEF'
        self.session = requests.session()


    def getApiBySrvCode(self,srvCode):
        '''
        根据SERVICE_CODE获取API定义
        :param srvCode: 服务定义
        :return:
        '''
        srvDetail = capital_to_upper(self.qryDataMapExcatByCond(tabName=self.tabName,sqlref='SEL_BY_SERVICE_CODE',cond=srvCode))
        srvCode = srvDetail['SERVICE_CODE'].split('_')
        if len(srvCode)==3:
            srvCode = srvCode[1] + '/' + srvCode[2]
        logger.info('执行到接口名:{}'.format(srvCode))
        return self.url + srvCode

    def getApiBySrvMethod(self,srvCode,srvMethod):
        '''

        :param srvCode:
        :param srvMethod:
        :return:
        '''
        # cond_dict = {'SERVICE_CODE':srvCode,'SRV_METHOD':srvMethod}
        srvDetail = capital_to_upper(self.qryDataMapExcatByCond(tabName=self.tabName,sqlref='SEL_BY_SRVMETHOD',cond=(srvCode,srvMethod)))
        # srvCode = srvDetail['SERVICE_CODE'].replace('_','/')
        srvCode = srvDetail['SERVICE_CODE'].split('_')
        if len(srvCode)==3:
            srvCode = srvCode[1] + '/' + srvCode[2]
        logger.info('执行到接口名:{}'.format(srvCode))
        srvPara = srvDetail['SRV_PARAMS']
        return {'url':self.url + srvCode,'params':srvPara}





if __name__ == '__main__':
    api = ApiDefine()
    # srvCode = api.getApiBySrvCode(srvCode='order_ISendSMSVerificationOpenService_CheckSMSVerificationCode')
    # print(srvCode)

    srvCode2 = api.getApiBySrvMethod(srvCode='IQueryUserInfoOpenService',srvMethod='getByUserId')
    print(srvCode2)


