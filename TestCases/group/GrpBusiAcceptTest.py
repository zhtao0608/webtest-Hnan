import unittest,os
from Base import HTMLTestRunnerCNNew
import time,ddt
from selenium import webdriver
from Base import ReadConfig
from Base.Mylog import LogManager
from Check.PageCheck import PageAssert
from Check.DataCheck import DataCheck
from TestCases.suite import mySuitePrefixAdd
from Data.DataMgnt.DataOper import DataOper
from Data.DataMgnt.TestResult import TestResultOper

logger = LogManager('GroupBusiAcceptTest').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")

params = DataOper().getCasePara('GroupBusiAccept')
logger.info(params)


@ddt.ddt
class GroupBusiAcceptTest(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(rc.get_ngboss('url'))     #这里可以切换环境，去ngboss_config.ini配置
        self.driver.maximize_window()

    @ddt.data(*params)
    def test01_OpenGrpAdc(self,dic):
        '''订购ADC集团管家'''
        logger.info("开始参数化......")


        PageAssert(self.driver).assert_submitAfter(file=file,row=get_TestData('OpenGrpAdc')['FuncRow'],index=0) #写入结果到xls
        self.assertIn('业务受理成功',submitMsg)
        # self.driver.close()

    @ddt.data(*paras_GrpBusiCancel)
    def test02_Cancel_GrpOrder(self,dic):
        '''集团商品注销'''
        logger.info("开始参数化......")
        row = get_TestData('CanelGrpIms')['FuncRow']
        groupId = dic.get('GROUP_ID')
        offerid = str(dic.get('OFFER_ID')) #集团主商品ID
        offerInsId = dic.get('GRP_OFFER_INS_ID')
        remark = '自动化测试'
        print("集团商品实例：%s",str(offerInsId))
        logger.info('开始集团用户用例,测试数据：{}'.format( dic))


        self.assertIn('业务受理成功',submitMsg)
        # self.driver.close()




    def tearDown(self):
        print('测试结束，关闭浏览器器!')
        self.driver.close()




if __name__ == '__main__':
    report_title = u'集团商品受理自动化测试报告'
    desc = u'集团商品受理测试详情'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath() + report_title + nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2)
        runner.run(mySuitePrefixAdd(GroupBusiAcceptTest,"test"))
