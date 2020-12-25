import unittest,os
import time,ddt
from PageObj.ngboss.login_page import LoginPage
from PageObj.ngboss.mainpage import MainPage
from Data.DataMgnt.DataOper import DataOper as Dto
from selenium import webdriver
from Base import HTMLTestRunnerCNNew
from Base import HwTestReport
from Base import ReadConfig
from Common.function import convertDicList,convert_to_diclistUpper
from Base.Mylog import LogManager
from TestCases.suite import mySuitePrefixAdd
from Check.PageCheck import PageAssert
from Base.base import Base
from Base.OperExcel import create_workbook
from Base.OperExcel import write_dict_xls,writeToExcelByRows,write_xlsBycolName,getRowIndex



logger = LogManager('FayMenuTest').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")


PersonCoreMenu = convert_to_diclistUpper(Dto().getCoreMenuByCataId(cataId='crm9000')) #同意转换成大写
logger.info('========个人业务核心菜单列表：{}'.format(PersonCoreMenu))
dataFile = create_workbook(fileName='个人业务重点菜单冒烟测试', value=convertDicList(PersonCoreMenu),sheet='个人业务')
print('#####x写入的xls文件名:', dataFile)




@ddt.ddt
class PersonMenuTest(unittest.TestCase):
    """个人业务菜单冒烟"""
    @classmethod
    def setUp(self):
        self.imgs = []
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.file = dataFile

    def get_screenshot(self):
        self.imgs.append(self.driver.get_screenshot_as_base64())
        return True

    @ddt.data(*PersonCoreMenu)
    def test_PersonCoreMenu(self,dict):
        '''家庭业务核心菜单冒烟测试'''
        ##参数化
        logger.info("开始参数化......")
        funcId = dict.get('FUNC_ID')
        menuPath = dict.get('MENU_PATH')
        menuUrl = dict.get('DLL_PATH')
        '''开始菜单冒烟测试'''
        logger.info('测试的菜单路径:{}'.format(menuPath))
        logger.info('测试的菜单编码:{}'.format(funcId))
        logger.info('测试的菜单URL:{}'.format(menuUrl))
        print('====测试的菜单路径:',menuPath)
        print('====测试的菜单URL:',menuUrl)
        if dict.get('IS_LEAF') =='1': #只测末级菜单
            test = MainPage(self.driver)
            LoginPage(self.driver).login()
            test.open_CataMenuNew(funcId=funcId)
            self.get_screenshot()
            chkPageMsg = PageAssert(self.driver).assert_WadeFullMsg()
            if '校验通过' in chkPageMsg:
                testResult = '通过'
            else:
                testResult = chkPageMsg
            write_xlsBycolName(file=self.file, row=getRowIndex(file=self.file, value=funcId, sheet='个人业务'),
                               colName='TEST_RESULT',value=testResult, sheet='个人业务')
            self.assertIn('校验通过',chkPageMsg,msg='菜单打开失败')
        else:
            print('===执行的菜单目录，直接通过')
            pass

    def tearDown(self):
        print('测试结束，关闭浏览器器!')
        self.driver.close()

if __name__ == '__main__':
    report_title = u'个人业务重点菜单冒烟自动化测试报告自动化测试报告'
    desc = u'个人业务重点菜单冒烟自动化测试报告测试详情'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath() + report_title + nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2)
        runner.run(mySuitePrefixAdd(PersonMenuTest,"test_PersonCoreMenu"))
