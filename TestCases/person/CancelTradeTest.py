import unittest,os
import ddt,time
from selenium.webdriver.common.by import By
from Base import HTMLTestRunnerCNNew
from PageObj.order.person.CancelTrade import CancelTrade
from selenium import webdriver
from Base import ReadConfig
from Base.OperExcel import write_xlsBycolName_append
from Base.Mylog import LogManager
from TestCases.suite import mySuitePrefixAdd
from Check.PageCheck import PageAssert
from Common.TestDataMgnt import get_TestData


os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('CancelTradeTest').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

paras = get_TestData(FuncCode='CancelTradeTest')['params']
file = get_TestData(FuncCode='CancelTradeTest')['filename']
row = get_TestData(FuncCode='CancelTradeTest')['FuncRow']

@ddt.ddt
class CancelTradeTest(unittest.TestCase):
    """[个人业务]返销测试"""
    @classmethod
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(rc.get_ngboss('url'))     #这里可以切换环境，去ngboss_config.ini配置
        self.driver.maximize_window()

    @ddt.data(*paras)
    def test_CancelTrade(self,dic):
        """业务返销"""
        logger.info("开始参数化......")
        accessNum = dic.get('ACCESS_NUM')
        busicode = dic.get('BUSI_ITEM_CODE') #业务操作类型
        logger.info('开始执行第{}个用例,测试数据：{}'.format(row,dic))
        ####测试用例步骤
        test = CancelTrade(self.driver)
        title = '业务返销测试记录'
        test.add_dochead(title)
        Btn_commit = (By.ID, 'CSSUBMIT_BUTTON') #提交按钮
        test.Open_PersonMenu(accessNum,cataMenuId='crm9200',menuId='crm9456') #登录并进入业务返销菜单
        time.sleep(5)
        test.open_CancelTradeFrame() #进入iframe
        test.query_CancelTradeByAccessNum(accessNum,busicode) #查询业务返销信息
        test.screen_step('选择要返销的业务类型')
        RuleMsg = PageAssert(test.driver).check_BusiRule(file,row)
        self.assertNotIn('业务校验失败',RuleMsg)
        time.sleep(3)
        test.find_element_click(Btn_commit)
        helpMsg = PageAssert(test.driver).assert_HelpPage()
        if '校验通过' not in helpMsg:
            logger.info('弹出帮助提示信息:{}'.format(helpMsg))
        submitMsg = PageAssert(self.driver).assert_submitAfter(file=file,row=row,index=0)
        logger.info('业务受理信息：{}'.format(submitMsg))
        print('业务受理信息：{}'.format(submitMsg))
        test.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        test.save_docreport(title)
        self.driver.close()

if __name__ == '__main__':
    report_title = u'业务返销自动化测试报告'
    desc = u'业务返销测试详情：'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath() + report_title +  nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2)
        runner.run(mySuitePrefixAdd(CancelTradeTest,"test_CancelTrade"))
