import time
import ast
import json
from Api.Auth import UserAuth as Auth
from Api.ApiDef import ApiDefine as Api
from Api.Order.QueryUserInfoOpenService import UserInfoService as UCA
from Base import ReadConfig
from Base.Mylog import LogManager
from Base.SysPara import SysPara
from Base.OperExcel import write_xlsBycolName_append,write_dict_xls
from Common.function import dict_get
from Common.function import isNotBlank
from Common.TestAsserts import Assertion as alert

logger = LogManager('UserDiscntQry').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

srvCode ='IUserDiscntQueryOpenService'

class UserDiscntQry(Api):
    '''用户优惠查询处理类'''

    def getDiscntsBySerialNum(self, serialNum):
        '''
        根据用户标识查询用户优惠
        :param SerialNum:
        :return:
        '''
        userInfos = UCA().getByNumberAndTag(serialNum)
        logger.info('获取到用户信息:{}'.format(userInfos))
        alert().assertTrue(isNotBlank(userInfos),msg='查询到用户信息为空或者用户信息不是有效的！')
        return self.getDiscntsByUserId(userId=userInfos['userId'])

    def getDiscntsByUserId(self, userId):
        '''
        根据用户标识查询用户优惠
        :param userId:
        :return:
        '''
        url = self.getApiBySrvMethod(srvCode=srvCode, srvMethod='getDiscntsByUserId')
        params = {"userId": userId}
        intf_res = self.session.post(url=url, headers=self.h, data=params)
        logger.info("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        d_intf_res = json.loads(intf_res.content.decode(encoding='utf-8'))
        logger.info("处理接口返回数据....{}".format(d_intf_res))
        return d_intf_res




if __name__ == '__main__':
    UserDiscnt = UserDiscntQry()
    usrDiscnt = UserDiscnt.getDiscntsBySerialNum(serialNum='15211001547')
    # usrDiscnt = UserDiscnt.getDiscntsByUserId(userId='3119072351450040')
    print(usrDiscnt)

