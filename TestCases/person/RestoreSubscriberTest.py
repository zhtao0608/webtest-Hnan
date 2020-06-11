import unittest,os
import ddt,time
from Base import HTMLTestRunnerCNNew
from PageObj.oc.person.RestoreSubscriber import RestoreSubscriber
from selenium import webdriver
from Base import ReadConfig
from Base.OperExcel import write_xlsBycolName_append
from Base.Mylog import LogManager
from TestCases.suite import mySuitePrefixAdd
from Common.Assert import PageAssert
from Common.TestDataMgnt import get_TestData


os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('RestoreSubscriberTest').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

paras = get_TestData(FuncCode='RestoreSubscriberTest')['params']
file = get_TestData(FuncCode='RestoreSubscriberTest')['filename']
row = get_TestData(FuncCode='RestoreSubscriberTest')['FuncRow']

@ddt.ddt
class RestoreSubscriberTest(unittest.TestCase):
    """[个人业务]复机测试"""
    @classmethod
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(rc.get_ngboss('url'))     #这里可以切换环境，去ngboss_config.ini配置
        self.driver.maximize_window()

    @ddt.data(*paras)
    def test_acceptRestoreUser(self,dic):
        """换卡"""
        logger.info("开始参数化......")
        accessNum = str(dic.get('ACCESS_NUM'))
        simId = str(dic.get('SIMID')) #SIM卡号参数化
        logger.info('开始执行第{}个用例,测试数据：{}'.format(row,dic))
        ####测试用例步骤
        test = RestoreSubscriber(self.driver)
        title = '个人业务复机测试记录'
        self.add_dochead(title)
        test.Open_PersonMenu(accessNum,cataMenuId='crm9300',menuId='crm9313') #登录并进入普通付费关系变更菜单
        time.sleep(2)
        test.open_RestoreSubscriberFrame() #进入iframe
        RuleMsg = test.vaild_BusiRule() #验证号码办理规则
        logger.info('复机业务规则验证结果:{}'.format(RuleMsg))
        if '验证失败' in RuleMsg:
            write_xlsBycolName_append(file=file,row=row,colName='RESULT_INFO',value=RuleMsg)
            test.driver.close()
        time.sleep(3)
        test.InputSimAndVaild(simId)
        test.screen_step('复机时输入SIM卡并校验')
        test.submit() #提交
        time.sleep(12)
        submitMsg = PageAssert(self.driver).assert_SubmitPage()
        logger.info('业务受理信息：{}'.format(submitMsg))
        test.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        test.save_docreport(title)
        logger.info('写入测试结果到xls.....')
        PageAssert(self.driver).write_testResult(file=file,row=row,index=0) #写入结果到xls
        self.driver.close()

if __name__ == '__main__':
    report_title = u'复机自动化测试报告'
    desc = u'复机测试详情：'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath() + report_title +  nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2)
        runner.run(mySuitePrefixAdd(RestoreSubscriberTest,"test_acceptRestoreUser"))

