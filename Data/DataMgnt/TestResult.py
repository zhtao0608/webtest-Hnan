import os,time
from Base.Mylog import LogManager
from Base import ReadConfig
from Common.function import getDigitFromStr
from Data.DataMgnt.DataOper import DataOper
from Base.OracleOper import MyOracle
from Common.TestAsserts import Assertion as Assert
from Check.PageCheck import PageAssert

logger = LogManager('DataOper').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")

class TestResultOper():
    '''处理测试结果'''
    def __init__(self):
        self.ora = MyOracle()

    def updateActualResult(self,result,sceneCode):
        '''
        根据sceneCode更新案例执行实际结果
        :param result:实际结果
        :param sceneCode:
        :return:
        '''
        Assert().assertTrue(len(result)>0,msg='result不能为空!')
        Assert().assertTrue(len(sceneCode)>0,msg='sceneCode不能为空!')
        valueDic = {'ACTUAL_RESULT':result}
        condDic  = {'SCENE_CODE':sceneCode}
        self.ora.updateData(route='cen1',dt_update=valueDic,dt_condition=condDic,table='AUTOTEST_CASE')

    def updateOrderId(self,submitMsg,sceneCode):
        '''
        根据sceneCode更新案例执行实际结果
        :param orderId:案例执行成功后将orderId处理后写入
        :param sceneCode:
        :return:
        '''
        Assert().assertTrue(len(submitMsg)>0,msg='submitMsg不能为空!')
        Assert().assertTrue(len(sceneCode)>0,msg='sceneCode不能为空!')
        Assert().assertIn('成功',submitMsg,msg='业务受理失败，不能写入OrderId')
        valueDic = {'ORDER_ID':getDigitFromStr(submitMsg)}
        condDic  = {'SCENE_CODE':sceneCode}
        self.ora.updateData(route='cen1',dt_update=valueDic,dt_condition=condDic,table='AUTOTEST_CASE')

    def updateRuleCheckInfo(self,msg,sceneCode):
        '''
        根据sceneCode更新案例执行实际结果
        :param sceneCode:
        :return:
        '''
        Assert().assertTrue(len(msg)>0,msg='ruleMsg不能为空!')
        Assert().assertTrue(len(sceneCode)>0,msg='sceneCode不能为空!')
        valueDic = {'RULE_CHECK_INFO':msg}
        condDic  = {'SCENE_CODE':sceneCode}
        self.ora.updateData(route='cen1',dt_update=valueDic,dt_condition=condDic,table='AUTOTEST_CASE')


if __name__ == '__main__':
    test = TestResultOper()
    test.updateActualResult(result='错误信息:ASYNC_QUERY_ERROR:执行并行查询异常',sceneCode='CrtUsColorRing')




