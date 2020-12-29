import unittest,os
import ddt,time
from Base import HTMLTestRunnerCNNew
from selenium.webdriver.common.by import By
from selenium import webdriver
from Base import ReadConfig
from Base.OperExcel import write_dict_xls,write_xlsBycolName_append
from PageObj.order.group.BusiAccept.GroupOfferAccept import GroupOfferAccept
from Base.Mylog import LogManager
from TestCases.suite import mySuitePrefixAdd
# from Check.PageCheck import PageAssert
from Data.DataMgnt.DataOper import DataOper
from Data.DataMgnt.TestResult import TestResultOper
from Check.DataCheck import DataCheck

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('CrtUsDeskTopTelTest').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

params = DataOper().getCasePara('CrtUsDeskTopTel')
logger.info(params)

@ddt.ddt
class CrtUsDeskTopTelTest(unittest.TestCase):
    '''集团多媒体桌面商品订购'''
    @classmethod
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(rc.get_ngboss('url'))     #这里可以切换环境，去ngboss_config.ini配置
        self.driver.maximize_window()

    @ddt.data(*params)
    def testCrtUsDeskTopTel(self,dic):
        '''集团多媒体桌面商品订购'''
        logger.info("开始参数化......")
        logger.info('开始执行案例,案例执行参数：{}'.format(dic))
        sceneCode = dic.get('SCENE_CODE')
        groupId = dic.get('groupId')
        brandCode = str(dic.get('brandCode')) #集团商品归属品牌
        offerCode = dic.get('offerCode')
        contractId = dic.get('contractId')
        elementAttrBizList = dic.get('elementAttrBizList')
        GroupOfferAccept(self.driver).accept_CrtUs(scene=sceneCode,groupId=groupId,brandCode=brandCode,offerCode=offerCode,
                                                   contractId=contractId,elementAttrBizList=elementAttrBizList)
        logger.info('执行完成')

    def tearDown(self):
        print('测试结束，关闭浏览器器!')
        self.driver.close()

if __name__ == '__main__':
    report_title = u'集团多媒体桌面电话商品订购自动化测试报告'
    desc = u'集团多媒体桌面电话商品订购测试详情'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath() + report_title + nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2)
        runner.run(mySuitePrefixAdd(CrtUsDeskTopTelTest,"test"))
