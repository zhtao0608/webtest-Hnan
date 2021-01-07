from Common.TestAsserts import Assertion as alert
import time,datetime,os
from Base import ReadConfig
from Base.Mylog import LogManager
from Data.DataMgnt.DataOper import DataOper as Dto
from Common.dealParas import ConvertParas


# 获取logger实例
logger = LogManager('dealParas').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

class DealSuiteExec(Dto):
    '''处理测试用例执行套餐处理类'''
    def __init__(self):
        self.tab = 'AUTOTEST_SUITE_EXEC'

    def get_ExecPlanBySuiteCode(self,suiteCode):
        '''
        通过suiteCode 获取案例执行计划
        :param suiteCode:
        :return:
        '''
        # return self.qryDataMapExcatByCond(tabName=self.tab,sqlref='SEL_BY_SUITE_CODE',cond=suiteCode)
        return self.retDataMapListByCond(tabName=self.tab,sqlref='SEL_BY_SUITE_CODE',cond=suiteCode)

    def get_ExecPlanBySuiteAndSceneCode(self,suiteCode,sceneCode):
        '''
        通过suiteCode和sceneCode 获取案例执行计划
        :param suiteCode:
        :return:
        '''
        # return self.qryDataMapExcatByCond(tabName=self.tab,sqlref='SEL_BY_SUITE_CODE',cond=suiteCode)
        return self.retDataMapListByCond(tabName=self.tab,sqlref='SEL_BY_SUITE_SCENE_CODE',cond=(suiteCode,sceneCode))

    def get_execParaBySuiteCode(self,suiteCode):
        '''根据suiteCode先获取案例列表，并返回案例执行参数EXEC_PARAMS'''
        suite = self.get_ExecPlanBySuiteCode(suiteCode)
        logger.info('获取的套件明细数据:{}'.format(suite))
        return ConvertParas(suite)

    def get_ParaBySuiteSceneCode(self,suiteCode,sceneCode):
        '''根据suiteCode和sceneCode获取案例列表，并返回案例执行参数EXEC_PARAMS'''
        suite = self.get_ExecPlanBySuiteAndSceneCode(suiteCode,sceneCode)
        logger.info('获取的套件明细数据:{}'.format(suite))
        return ConvertParas(suite)

    def get_casePathBySuiteCode(self,suiteCode):
        '''
        通过suiteCode 获取案例执行计划
        :param suiteCode:
        :return:
        '''
        # return self.qryDataMapExcatByCond(tabName=self.tab,sqlref='SEL_BY_SUITE_CODE',cond=suiteCode)
        return self.retDataMapListByCond(tabName=self.tab,sqlref='SEL_PATH_BY_CODE',cond=suiteCode)


    # caseParaList = []
    # for i in range(0,len(suite)):
    #     suiteCaseId = suite[i]['PARAMS']
    #     logger.info('获取到案例明细:{}'.format(casePara))
    #     caseParaList.append(casePara)
    # return caseParaList

    def get_execPathBySuiteCode(self,suiteCode):
        '''获取测试套件下所有案例到python文件所在路径'''
        # suite = self.retDataMapListByCond(tabName=self.tab,sqlref='SEL_PATH_BY_CODE',cond=suiteCode)
        suite = self.get_casePathBySuiteCode(suiteCode)
        pathList = []
        for i in range(0,len(suite)):
            if suite[i]['PATH'] is not None:
                pathList.append(suite[i]['PATH'])
        return pathList

    def upd_resultBySuiteCaseId(self,actual_result,suite_case_id):
        '''
        根据suite_case_id更新测试实际结果
        :param actual_result:
        :param suite_case_id:
        :return:
        '''
        self.editDataMapByCond(tabName=self.tab,sqlref='UPD_RES_BY_CASE_ID',cond=(actual_result,suite_case_id))

    def upd_orderIdBySuiteCaseId(self,orderId,suite_case_id):
        '''
        根据suite_case_id更新测试实际结果
        :param actual_result:
        :param suite_case_id:
        :return:
        '''
        self.editDataMapByCond(tabName=self.tab,sqlref='UPD_ORDID_BY_CASE_ID',cond=(orderId,suite_case_id))

    def upd_RuleChkBySuiteCaseId(self,rule_chkmsg,suite_case_id):
        '''
        根据suite_case_id更新测试实际结果
        :param actual_result:
        :param suite_case_id:
        :return:
        '''
        self.editDataMapByCond(tabName=self.tab,sqlref='UPD_RULE_BY_CASE_ID',cond=(rule_chkmsg,suite_case_id))



if __name__ == '__main__':
    su = DealSuiteExec()
    # su.upd_resultBySuiteCaseId(suite_case_id='202012041139501068',actual_result='不通过111313')
    # su.upd_orderIdBySuiteCaseId(suite_case_id='202012041139501068',orderId='20201229003263566')
    # su.upd_RuleChkBySuiteCaseId(suite_case_id='202012041139501068',rule_chkmsg='号码错误')

    # coreSuite = su.get_execPathBySuiteCode(suiteCode='SvcStateChgTest')
    prodChg_suite = su.get_ParaBySuiteSceneCode(suiteCode='ProdChgTest',sceneCode='AddElements')
    print("---------------------------------------")
    print(prodChg_suite)
    # pathSuite = su.get_execPathBySuiteCode(suiteCode='CoreBusiTest')
    # print("=========================")
    # print(pathSuite)



