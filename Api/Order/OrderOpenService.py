import time
import requests
import json
from Base import ReadConfig
from Base.Mylog import LogManager
from Api.ApiDef import ApiDefine as Api
from Base.OperExcel import write_xlsBycolName_append,write_dict_xls
from Base.OracleOper import MyOracle
from Common.function import dict_get
from Data.DataMgnt.GenTestData import GenTestData

logger = LogManager('OrderService').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
srvCode ='IOrderOpenService'

class OrderService(Api):
    '''查询订单处理'''
    def queryByOrderId(self,orderId):
        '''
        根据orderId获取订单信息
        :param orderId:订单标识
        :return:
        '''
        url = self.getApiBySrvMethod(srvCode=srvCode,srvMethod='queryByOrderId')
        params = {"orderId": orderId}
        intf_res = self.session.post(url=url ,headers =self.h,data=params)
        logger.info("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        logger.info("处理接口返回数据....")
        d_intf_res = json.loads(intf_res.content.decode(encoding='utf-8'))
        print(d_intf_res)


if __name__ == '__main__':
    OrderService = OrderService()
    OrderService.queryByOrderId(orderId='3120010461227497')