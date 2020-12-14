import os,time
from Base.Mylog import LogManager
from Base.OracleOper import MyOracle
from Base import ReadConfig
from Common.function import retDigitListFromStr
from Data.DataMgnt.DataOper import DataOper as DTO
from Data.DataMgnt.DataMap import DataMap
from Data.DataMgnt.TestResult import TestResultOper as TR

logger = LogManager('DataCheck').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")


class DataCheck(DataMap):
    '''数据检查类'''
    def __init__(self):
        self.ora = MyOracle()

    """====================处理订单、主台账==============="""
    def dealMainOrder(self,orderId):
        '''
        处理主订单信息，场景如：待打印、待支付等订单，直接改成0让AEE调度
        :param orderId:
        :return:
        '''
        orderInfo = self.qryDataMapExcatByCond(tabName='TF_B_ORDER',sqlref='SEL_BY_ORDERID',cond=orderId)
        logger.info('待处理订单数据:{}'.format(orderInfo))
        if len(orderInfo)==0:
            logger.info('没有待处理订单')
        else:
            logger.info('只匹配一条主订单')
            orderState = orderInfo['ORDER_STATE'] #获取主订单状态
            logger.info('当前订单号:{},状态是:{}'.format(orderId,orderState))
            if orderState=='Y' or orderState=='X':
                self.updateData(route='jour1',table='TF_B_ORDER',dt_update={'ORDER_STATE':'0'},
                                dt_condition={'ORDER_ID':orderId})

    def checkOrderFinish(self,orderId):
        '''
        判断工单是否完工
        :return:返回Bool ,如果完工则为True,否则为False
        '''
        tradeList = DTO().getTabColValue(thin='jour1', tabName ='TF_B_TRADE',
                            ColName = 'SUBSCRIBE_STATE,TRADE_ID,TRADE_TYPE_CODE',
                            expr ="ORDER_ID='{}'".format(orderId))
        logger.info(tradeList)
        print('=========len(tradeList)',len(tradeList))

        tradeHisList = DTO().getTabColValue(thin='jour1', tabName ='TF_B_TRADE_{}'.format(time.strftime("%Y")),
                            ColName = 'SUBSCRIBE_STATE,TRADE_ID,TRADE_TYPE_CODE',
                            expr ="ORDER_ID='{}'".format(orderId))
        logger.info(tradeHisList)
        try:
            if (len(tradeHisList)>0 and len(tradeList)==0):  #his表有数据,并且trade表无数据则完工 返回True
                for i in range(len(tradeHisList)):
                    tradeId = tradeHisList[i]['TRADE_ID']
                    subscriberState = tradeHisList[i]['SUBSCRIBE_STATE']
                    if not subscriberState == '9' :
                        logger.info('trade_id = {}工单状态是:{}'.format(tradeId,subscriberState))
                        return False
                        break;
                    else:
                        return True
            else:
                return False   #其余情况全部返回False ,表示有未完工工单
        except:
            logger.info('获取失败')
            return False

    def retOrderTrace(self,orderId):
        '''
        根据OrderId查询工单轨迹,返回工单执行详情
        :param orderId:
        :return:
        '''
        OrderTraceList= self.getTabColValue(thin='jour1', tabName ='TL_B_ORDER_TRACE_{}'.format(time.strftime("%Y")),
                            ColName = 'ACTIVE_CODE,ACTIVE_CODE,RESULT_CODE,RESULT_INFO',
                            expr ="ORDER_ID='{}'".format(orderId))
        return OrderTraceList

if __name__ == '__main__':
    data = DataCheck()
    # res = data.checkOrderFinish(orderId='7420010726686661')
    # result = test.updateRealNameInfoBySerialNum(accessNum='13639750374')
    # result = test.getCasePara(sceneCode='DstUsDeskTopTel')
    data.dealMainOrder(orderId='7120120318684811')
    res = data.retOrderTrace(orderId='7120120318684811')
    print(res)








