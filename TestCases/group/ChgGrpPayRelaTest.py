import unittest,os
import ddt,time
from Base import HTMLTestRunnerCNNew
from selenium.webdriver.common.by import By
from selenium import webdriver
from Base import ReadConfig
from Base.OperExcel import write_dict_xls,write_xlsBycolName_append
from PageObj.oc.group.PayrelaAdvChg import GrouprelaAdv
from Base.Mylog import LogManager
from TestCases.suite import mySuitePrefixAdd
from Common.Assert import PageAssert
from Common.TestDataMgnt import get_TestData,get_testDataFile

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('ChgGrpPayRelaTest').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

params = get_TestData('GrprelaAdvAdd')['params']
file = get_TestData('GrprelaAdvAdd')['filename']

@ddt.ddt
class ChgGrpPayRelaTest(unittest.TestCase):
    '''集团高级付费管理'''
    @classmethod
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(rc.get_ngboss('url'))     #这里可以切换环境，去ngboss_config.ini配置
        self.driver.maximize_window()

    @ddt.data(*params)
    def test_acceptAddGrpPayRela(self,dic):
        '''新增集团高级付费关系'''
        logger.info("开始参数化......")
        print('用例执行测试数据:{}'.format(dic))
        groupId = dic.get('GROUP_ID')
        acctId = dic.get('ACCT_ID')
        payAcessNum = dic.get('SERIAL_NUM')   #集团成员号码
        '''选择操作类型, 根据operCode判断操作类型
                @operCode = 0 新增
                @operCode = 1 删除
                @operCode = 2 修改
        '''
        operCode = dic.get('OPERCODE')
        itemName = dic.get('ITEM_NAME')  #付费科目
        #开始执行用例
        test = GrouprelaAdv(self.driver)
        '''受理新增集团高级付费关系'''
        title = '新增集团高级付费关系测试记录'
        test.add_dochead(title)
        test.Open_GrprelaAdv(groupId)
        test.choose_grpAcct(acctId)  # 选择付费账户
        test.set_PayCustInfo(payAcessNum) #f 付费成员号码
        test.choose_operAction(operCode)
        test.set_Payitem(itemName)
        test.isElementDisplay((By.ID, 'submitButton'), 'click')  # 点击提交
        submitMsg = PageAssert(test.driver).assert_Submit()  # 提交后返回信息，flowId或者报错
        test.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        test.save_docreport(title)
        logger.info('写入测试结果到xls.....')
        PageAssert(self.driver).write_testResult(file=file,row=get_TestData('GrprelaAdvAdd')['FuncRow'],index=0) #写入结果到xls
        self.driver.close()
        time.sleep(3)

    def tearDown(self):
        print('测试结束，关闭浏览器器!')
        self.driver.close()
if __name__ == '__main__':
    report_title = u'集团高级付费关系管理自动化测试报告'
    desc = u'集团高级付费关系管理受理测试详情'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath() + report_title + nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2,retry=1)
        runner.run(mySuitePrefixAdd(ChgGrpPayRelaTest,"test_acceptAddGrpPayRela"))
