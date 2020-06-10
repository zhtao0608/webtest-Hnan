import unittest,os
import time,ddt
from Base import HTMLTestRunnerCNNew
from PageObj.oc.person.FamilyNetPage import FamilyNetPage
from selenium import webdriver
from selenium.webdriver.common.by import By
from Base import ReadConfig
from Base.OperExcel import get_exceldata,write_xlsBycolName_append
from Base.Mylog import LogManager
from Common.Assert import PageAssert
from TestCases.suite import mySuitePrefixAdd
from Common.TestDataMgnt import get_testDataFile,get_FuncRow,get_TestData

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('FamilyNetTest').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

# file = ReadConfig.data_path + 'UITest_ShareActive.xls'
# paras = get_exceldata(file,0)
# logger.info('测试案例执行数据准备：{}'.format(paras))
file = get_testDataFile()
paras = get_TestData('FamilyNetTest')['params']
row = get_FuncRow('FamilyNetTest')

@ddt.ddt
class FamilyNetTest(unittest.TestCase):
    """家庭网（省内版）办理"""
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(rc.get_ngboss('url'))     #这里可以切换环境，去ngboss_config.ini配置
        self.driver.maximize_window()
        # self.driver.implicitly_wait(20)    #暂时设置40s，隐式等待

    @ddt.data(*paras)
    def test_acceptMultiOffer(self,dic):
        """亲情网业务办理"""
        logger.info("开始参数化......")
        # row = int(dic.get('No'))   #标识行号，后续写入xls使用
        AccessNum = str(dic.get('ACCESS_NUM')) #家庭主号
        logger.info("主号:{}".format(AccessNum))
        mutiAccessNumList = dic.get('MebNumList').replace(' ','').split(',') #家庭成员列表获取的是Str,转换成List
        logger.info("副号码:{}" .format(mutiAccessNumList))
        logger.info('开始执行第{}个用例,测试数据：{}'.format(row,dic))
        print('开始执行第{}个用例,测试数据：{}'.format(row,dic))
        test = FamilyNetPage(self.driver)
        title = '受理亲情网省内版测试记录'
        test.add_dochead(title)
        Btn_commit = (By.ID, 'CSSUBMIT_BUTTON') #提交按钮
        test.Open_PersonMenu(AccessNum,password='123123',cataMenuId='crm9300',menuId='crmy165') #登录并进入菜单
        time.sleep(5)
        test.open_MultiOfferFrame() #进入iframe
        RuleMsg = test.vaild_BusiRule() #业务检查点（进入菜单时校验）
        print('受理亲情网省内版提交前规则:{}'.format(RuleMsg))
        logger.info('受理亲情网省内版提交前规则:{}'.format(RuleMsg))
        if '业务校验失败' in RuleMsg:
            write_xlsBycolName_append(file=file,row=row,colName='RESULT_INFO',value=RuleMsg)
            test.quit_browse() #业务规则校验失败，直接终止程序
        logger.info('开始设置主号家庭短号服务')
        test.screen_step('进入亲情网办理菜单')
        test.set_mainCard(AccessNum)
        logger.info('新增家庭成员并设置家庭短号服务')
        test.set_mutiCard(mutiAccessNumList)
        time.sleep(2)
        test.find_element_click(Btn_commit)
        time.sleep(10)
        submitMsg = PageAssert(test.driver).assert_SubmitPage()
        logger.info('业务受理信息：{}'.format(submitMsg))
        test.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        PageAssert(self.driver).write_testResult(file=file,row=row)
        test.save_docreport(title)
        time.sleep(3)
        self.driver.close()

if __name__ == '__main__':
    report_title = u'亲情网业务办理自动化测试报告'
    desc = u'亲情网业务办理测试详情：'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath() + report_title + nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2)
        runner.run(mySuitePrefixAdd(FamilyNetTest,"test_acceptMultiOffer"))

