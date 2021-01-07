import time
import ast
import json
from Api.Auth import UserAuth as Auth
from Api.ApiDef import ApiDefine as Api
from Base import ReadConfig
from Base.Mylog import LogManager
from Base.SysPara import SysPara
from Base.OperExcel import write_xlsBycolName_append,write_dict_xls
from Common.function import dict_get
from Common.TestAsserts import Assertion as alert

logger = LogManager('TradeQryService').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

srvCode ='ITradeQueryOpenService'

class TradeQryService(Api):
    '''查询用户相关信息'''
    # def __init__(self):
    #     self.url = SysPara().get_IntfUrl('order')
    #     self.token = Auth().generateByName(userName='SUPERUSR')
    #     self.h = {"Authorization":self.token}
    #     self.session = requests.session()

    def getMainTradeIdBySn(self,serialNum,tradeTypeCode,route='0731'):
        '''
        新接口 根据手机号和工单类型查工单号，返回参数不含cust_name
        :param serialNum:
        :param tradeTypeCode:
        :param routeId:
        :return:
        '''
        url = self.getApiBySrvMethod(srvCode=srvCode,srvMethod='getMainTradeIdBySN')
        params = {"serialNumber":serialNum,"tradeTypeCode": tradeTypeCode,"routeId":route}
        intf_res = self.session.post(url=url ,headers =self.h,data=params)
        logger.info("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        d_intf_res = json.loads(intf_res.content.decode(encoding='utf-8'))
        logger.info("处理接口返回数据....{}".format(d_intf_res))
        return d_intf_res

    def queryTradeBySnRoute(self,serialNum,route='0731'):
        '''
        根据服务号码查询订单信息
        :param serialNum: 服务号码
        :param route: 路由，默认0731
        :return:
        '''
        url = self.getApiBySrvMethod(srvCode=srvCode,srvMethod='queryTradeBySnRoute')
        params = {"serialNumber":serialNum,"route":route,"current":0,"pageSize":20}
        intf_res = self.session.post(url=url ,headers =self.h,data=params)
        logger.info("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        d_intf_res = json.loads(intf_res.content.decode(encoding='utf-8'))
        logger.info("处理接口返回数据....{}".format(d_intf_res))
        return d_intf_res['results']


    def getUnfinishTradeBySerialNum(self,serialNum,route='0731'):
        '''
        新接口 根据手机号和工单类型查工单号，返回参数不含cust_name
        :param serialNum:
        :param routeId:
        :return:
        '''
        url = self.getApiBySrvMethod(srvCode=srvCode,srvMethod='listTradeBySerialNumber')
        params = {"serialNumber":serialNum,"routeId":route}
        intf_res = self.session.post(url=url ,headers =self.h,data=params)
        logger.info("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        d_intf_res = json.loads(intf_res.content.decode(encoding='utf-8'))
        logger.info("处理接口返回数据....{}".format(d_intf_res))
        return d_intf_res

    def queryTradeByOrderIdRoute(self,orderId,route='0731'):
        '''
        根据UserId获取tradeInfo
        :param route:路由标识，默认0731-长沙
        :param orderId:订单编码
        :return:
        '''
        url = self.getApiBySrvMethod(srvCode=srvCode,srvMethod='queryTradeByOrderIdRoute')
        params = {"orderId": orderId,"route":route}
        intf_res = self.session.post(url=url ,headers =self.h,data=params)
        logger.info("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        logger.info("处理接口返回数据....")
        d_intf_res = json.loads(intf_res.content.decode(encoding='utf-8'))
        logger.info("处理接口返回数据....{}".format(d_intf_res))
        return d_intf_res

    def queryHTradeByOrderIdRoute(self,orderId,route='0731'):
        '''
        根据UserId获取tradeInfo
        :param route:路由标识，默认0731-长沙
        :param orderId:订单编码
        :return:
        '''
        url = self.getApiBySrvMethod(srvCode=srvCode,srvMethod='queryHTradeByOrderIdRoute')
        params = {"orderId": orderId,"route":route,"year":time.strftime('%Y')}
        intf_res = self.session.post(url=url ,headers =self.h,data=params)
        logger.info("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        logger.info("处理接口返回数据....")
        d_intf_res = json.loads(intf_res.content.decode(encoding='utf-8'))
        logger.info("处理接口返回数据....{}".format(d_intf_res))
        return d_intf_res

    def getTradeByUserId(self,tradeTypeCode,userId):
        '''
        根据UserId获取tradeInfo
        :param tradeTypeCode:业务编码
        :param userId:用户编码
        :return:
        '''
        url = self.getApiBySrvMethod(srvCode=srvCode,srvMethod='getTradeByUserId')
        params = {"tradeTypeCode": tradeTypeCode,"userId":userId}
        intf_res = self.session.post(url=url ,headers =self.h,data=params)
        logger.info("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        logger.info("处理接口返回数据....")
        d_intf_res = json.loads(intf_res.content.decode(encoding='utf-8'))
        logger.info("处理接口返回数据....{}".format(d_intf_res))
        return d_intf_res

    def queryTradeByTradeId(self,tradeId,route='0731'):
        '''
        根据tradeId查询主台账
        :param tradeId:
        :return:
        '''
        url = self.getApiBySrvMethod(srvCode=srvCode,srvMethod='queryTradeByTradeId')
        params = {"tradeId": tradeId,"route":route}
        intf_res = self.session.post(url=url ,headers =self.h,data=params)
        logger.info("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        logger.info("处理接口返回数据....")
        d_intf_res = json.loads(intf_res.content.decode(encoding='utf-8'))
        logger.info("处理接口返回数据....{}".format(d_intf_res))
        return d_intf_res

    def queryTradeHisByTradeId(self,tradeId,eparchCode='0731'):
        '''
        根据tradeId查询主台账历史
        :param tradeId:
        :return:
        '''
        url = self.getApiBySrvMethod(srvCode=srvCode,srvMethod='queryTradeByTradeId')
        params = {"tradeId": tradeId,"route":eparchCode}
        intf_res = self.session.post(url=url ,headers =self.h,data=params)
        logger.info("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        logger.info("处理接口返回数据....")
        d_intf_res = json.loads(intf_res.content.decode(encoding='utf-8'))
        logger.info("处理接口返回数据....{}".format(d_intf_res))
        return d_intf_res

if __name__ == '__main__':
    TradeQryService = TradeQryService()

    # trade = TradeQryService.queryTradeHisByTradeId(tradeId='3121010287959494')
    # trade = TradeQryService.queryTradeByTradeId(tradeId='3121010287959494')
    # # trade = TradeQryService.queryTradeBySnRoute(serialNum='073183914727')
    # print(trade)
    # print(type(trade))
    # tradeH = TradeQryService.queryHTradeByOrderIdRoute(orderId='3121010238677296')
    # print(tradeH)
    # unFinishTrade=TradeQryService.getUnfinishTradeBySerialNum(serialNum='18711041437')
    # print(unFinishTrade)
    # print(len(unFinishTrade))

    # TradeQryService.getTradeByUserId(tradeTypeCode='90',userId='3106022702310071')
    tradeInfos = TradeQryService.queryTradeByOrderIdRoute(orderId='3121010338677527')
    print(tradeInfos)
