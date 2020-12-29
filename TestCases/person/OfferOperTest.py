import unittest,os
import time,ddt
from Base import HTMLTestRunnerCNNew
from PageObj.order.person.offerOpers import OfferOperPage
from selenium import webdriver
from selenium.webdriver.common.by import By
from Base import ReadConfig
from Base.OperExcel import write_xlsBycolName_append
from Base.Mylog import LogManager
from Check.PageCheck import PageAssert
from TestCases.suite import mySuitePrefixAdd
from Data.DataMgnt.TestDataMgnt import TestDataExcel as td

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('OfferOperTest').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

# file = ReadConfig.data_path + 'UITest_OfferChg.xls'
# offers = get_exceldata(file,0)
file = td().get_TestData('OfferOperTest')['filename']
offers = td().get_TestData('OfferOperTest')['params']
row = td().get_TestData('OfferOperTest')['FuncRow']
logger.info('测试案例执行数据准备：{}'.format(offers))

@ddt.ddt
class OfferOperTest(unittest.TestCase):
    """个人业务-商品订购测试"""
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(rc.get_ngboss('url'))     #这里可以切换环境，去ngboss_config.ini配置
        self.driver.maximize_window()
        self.driver.implicitly_wait(20)    #暂时设置40s，隐式等待

    @ddt.data(*offers)
    def test_chgMainOffer(self,dic):
        """商品主套餐变更"""
        logger.info("开始参数化......")
        accessNum = str(dic.get('ACCESS_NUM'))
        logger.info("测试号码:"+accessNum)
        offerId = str(dic.get('OFFER_ID'))
        logger.info("主套餐名称:" + offerId)
        subOfferList = dic.get('subOfferList')
        logger.info("可选子商品:" + subOfferList)
        logger.info('开始执行第{}个用例,测试数据：{}'.format(row,dic))
        ##开始执行测试
        test = OfferOperPage(self.driver)
        title = '个人商品订购测试记录'
        test.add_dochead(title)
        test.Open_SubOffer(accessNum, offerId)  # 直接进入商品订购界面
        time.sleep(20)
        ruleMsg = PageAssert(self.driver).assert_error()
        # ruleMsg = PageAssert(self.driver).check_BusiRule(file,row)
        logger.info('进入时校验:{}'.format(ruleMsg))
        ruleMsg = offerId + ' ' + ruleMsg
        if '校验失败' in ruleMsg:
            write_xlsBycolName_append(file,row=row,colName='RULE_CHECK',value=ruleMsg)
        self.assertNotIn('校验失败',ruleMsg)
        time.sleep(5)
        test.choose_subOffer(subOfferList)  # 可选商品列表
        Loc_submit = (By.ID,'CSSUBMIT_BUTTON')
        test.screen_step('点击订购')
        test.find_element_click(Loc_submit)
        time.sleep(10)
        logger.info("处理页面返回信息.....")
        submitMsg = PageAssert(self.driver).assert_submitAfter(file=file,row=row)
        logger.info('业务受理信息：{}'.format(submitMsg))
        test.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        test.save_docreport(title)
        self.assertIn('业务受理成功',submitMsg)

    def tearDown(self):
        print('测试结束，关闭浏览器器!')
        self.driver.close()


if __name__ == '__main__':
    report_title = u'商品订购自动化测试报告'
    desc = u'产品变更测试详情：'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath() + report_title + nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2)
        runner.run(mySuitePrefixAdd(OfferOperTest,"test_chgMainOffer"))

