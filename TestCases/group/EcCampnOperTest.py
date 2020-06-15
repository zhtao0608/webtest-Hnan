import unittest,os
import ddt,time
from Base import HTMLTestRunnerCNNew
from selenium.webdriver.common.by import By
from selenium import webdriver
from Base import ReadConfig
from Base.OperExcel import write_dict_xls,write_xlsBycolName_append
from PageObj.oc.group.EcCampnOper import EcCampnOper
from Base.Mylog import LogManager
from TestCases.suite import mySuitePrefixAdd
from Common.Assert import PageAssert
from Common.TestDataMgnt import get_TestData,get_testDataFile

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('EcCampnOperTest').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

params = get_TestData('SubEcCampnAdd')['params']
file = get_TestData('SubEcCampnAdd')['filename']

@ddt.ddt
class EcCampnOperTest(unittest.TestCase):
    '''集团营销活动'''
    @classmethod
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(rc.get_ngboss('url'))     #这里可以切换环境，去ngboss_config.ini配置
        self.driver.maximize_window()

    @ddt.data(*params)
    def test_acceptSubEcCampn(self,dic):
        '''新增集团营销活动'''
        logger.info("开始参数化......")
        groupId = dic.get('GROUP_ID')
        CampnOfferId = dic.get('CAMPN_ID')  #营销活动ID
        OfferKey = dic.get('OFFER_ID')   #营销活动商品
        prePrice = dic.get('PREPRICE')  # 预存金额
        AcctId = dic.get('ACCT_ID')  #集团账户
        month = dic.get('MONTH')  #合约期
        print('开始执行集团营销活动受理案例,测试数据:{}'.format(dic))
        logger.info('开始执行集团营销活动受理案例,测试数据:{}'.format(dic))
        #开始执行用例
        test = EcCampnOper(self.driver)
        title = '新增集团营销活动受理测试记录'
        test.add_dochead(title)
        test.Open_groupMenu(groupId,'crm8500','crm8097') #点击进入菜单 ,父菜单>子菜单
        test.Open_GrpEcCampnOperframe()  # 进入集团订购iframe
        test.screen_step('进入集团营销活动受理')
        test.choose_EcCampnOffer(CampnOfferId,OfferKey,prePrice,AcctId,month)
        test.screen_step('选择营销活动并设置')
        time.sleep(5)
        test.find_element_click((By.ID,'submitButton')) #点击提交
        time.sleep(2)
        test.sendEnter() #确认
        time.sleep(5)
        submitMsg = PageAssert(test.driver).assert_Submit()  #提交后返回信息，flowId或者报错
        test.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        test.save_docreport(title)
        logger.info('写入测试结果到xls.....')
        PageAssert(self.driver).assert_submitAfter(file=file,row=get_TestData('SubEcCampnAdd')['FuncRow'],index=0) #写入结果到xls
        self.assertIn('受理失败',submitMsg)
        self.driver.close()
        time.sleep(3)

    def tearDown(self):
        print('测试结束，关闭浏览器器!')

if __name__ == '__main__':
    report_title = u'集团营销活动受理自动化测试报告'
    desc = u'集团营销活动受理测试详情'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath() + report_title + nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2)
        runner.run(mySuitePrefixAdd(EcCampnOperTest,"test_acceptSubEcCampn"))
