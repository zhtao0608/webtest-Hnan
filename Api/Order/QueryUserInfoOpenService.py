import time
import requests
import json
from Api.Auth import UserAuth as Auth
from Api.ApiDef import ApiDefine as Api
from Base import ReadConfig
from Base.Mylog import LogManager
from Base.SysPara import SysPara
from Base.OperExcel import write_xlsBycolName_append,write_dict_xls
from Base.OracleOper import MyOracle
from Common.function import dict_get
from Data.DataMgnt.GenTestData import GenTestData

logger = LogManager('UserInfoService').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )


class UserInfoService(Api):
    '''查询用户相关信息'''
    # def __init__(self):
    #     self.url = SysPara().get_IntfUrl('order')
    #     self.token = Auth().generateByName(userName='SUPERUSR')
    #     self.h = {"Authorization":self.token}
    #     self.session = requests.session()

    def getUserInfoByUserId(self,userId):
        '''
        根据用户ID查询用户信息
        :param userId:
        :return:
        '''
        intfName = 'IQueryUserInfoOpenService/getByUserId'
        params = {"userId": userId}
        intf_res = self.session.post(url=self.url + intfName ,headers =self.h,data=params)
        logger.info("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        logger.info("处理接口返回数据....")
        d_intf_res = json.loads(intf_res.content.decode(encoding='utf-8'))
        print(d_intf_res)

    def getByInstId(self,instId,route):
        '''
        查询用户指定的优惠信息
        :param instId:优惠实例
        :param route:路由
        :return:
        '''
        intfName = 'IQueryUserInfoOpenService/getByInstId'
        params = {"instId": instId,"route":route}
        intf_res = self.session.post(url=self.url + intfName ,headers =self.h,data=params)
        logger.info("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        logger.info("处理接口返回数据....")
        d_intf_res = json.loads(intf_res.content.decode(encoding='utf-8'))
        print(d_intf_res)


if __name__ == '__main__':
    UserInfoService = UserInfoService()
    # UserInfoService.getUserInfoByUserId(userId='3994031853420379')
    UserInfoService.getByInstId(instId='3120012458228653',route='0731')



