import os,time
from Base.Mylog import LogManager
from Base.OracleOper import MyOracle
from Base import ReadConfig
from Common.function import retDigitListFromStr
from Data.DataMgnt.OraDataDeal import SelectOraData

logger = LogManager('DataCheck').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")
ora = MyOracle()


class DataCheck():
    '''数据检查类'''
    def checkOrderFinish(self,orderId):
        '''
        判断工单是否完工
        :return:返回Bool ,如果完工则为True,否则为False
        '''
        tradeList = SelectOraData().getTabColValue(thin='jour1', tabName ='TF_B_TRADE',
                            ColName = 'SUBSCRIBE_STATE,TRADE_ID,TRADE_TYPE_CODE',
                            expr ="ORDER_ID='{}'".format(orderId))
        logger.info(tradeList)
        print('=========len(tradeList)',len(tradeList))

        tradeHisList = SelectOraData().getTabColValue(thin='jour1', tabName ='TF_B_TRADE_{}'.format(time.strftime("%Y")),
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
        OrderTraceList= SelectOraData().getTabColValue(thin='jour1', tabName ='TL_B_ORDER_TRACE_{}'.format(time.strftime("%Y")),
                            ColName = 'ACTIVE_CODE,ACTIVE_CODE,RESULT_CODE,RESULT_INFO',
                            expr ="ORDER_ID='{}'".format(orderId))
        return OrderTraceList

if __name__ == '__main__':
    data = DataCheck()
    # res = data.getTabColValue('crm1',tabName='TF_F_USER',ColName='USER_ID,CUST_ID,SERIAL_NUMBER',expr="REMOVE_TAG='0' AND SERIAL_NUMBER = '15297063111'")
    res = data.checkOrderFinish(orderId='7420010726686661')
    # res = data.retOrderTrace(orderId='7420010726686661')
    # res = data.getSmsContent(accessNum='13997400339')
    # smsContent = data.getSmsContent(accessNum='15297063111')
    # print(smsContent)
    # smsCode = data.getSmsCode(accessNum='15297063111')
    # print(smsCode)







