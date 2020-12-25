import unittest,os
import time,ddt
from PageObj.ngboss.login_page import LoginPage
from PageObj.ngboss.mainpage import MainPage
from Data.DataMgnt.DataOper import DataOper as Dto
from selenium import webdriver
from Base import HTMLTestRunnerCNNew
from Base import HwTestReport
from Base import ReadConfig
from Common.function import convertDicList
from Base.Mylog import LogManager
from TestCases.suite import mySuitePrefixAdd
from Check.PageCheck import PageAssert
from Base.base import Base
from Base.OperExcel import create_workbook
from Base.OperExcel import write_dict_xls,writeToExcelByRows,write_xlsBycolName,getRowIndex



logger = LogManager('MenuTest').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")



CreatePersonUserMenu = Dto().getSysMenuByParentFuncId(parentFuncId='crm9100')
logger.info('========个人开户菜单列表：{}'.format(CreatePersonUserMenu))
dataFile = create_workbook(fileName='个人业务菜单冒烟测试', value=convertDicList(CreatePersonUserMenu),sheet='开户业务')
print('#####x写入的xls文件名:', dataFile)

EPostInfoMenu = Dto().getSysMenuByParentFuncId(parentFuncId='crm9A00')
logger.info('========个人电子发票菜单列表：{}'.format(EPostInfoMenu))
writeToExcelByRows(fileName=dataFile,sheetName='电子发票',data=convertDicList(EPostInfoMenu))
print('#####写入的xls文件名:', dataFile)

ArticMenu = Dto().getSysMenuByParentFuncId(parentFuncId='crm9830')
logger.info('========引商入柜业务菜单列表：{}'.format(ArticMenu))
writeToExcelByRows(fileName=dataFile,sheetName='引商入柜业务',data=convertDicList(ArticMenu))
print('#####写入的xls文件名:', dataFile)


PersonDailyMenu = Dto().getSysMenuByParentFuncId(parentFuncId='crm9200')
logger.info('========引商入柜业务菜单列表：{}'.format(PersonDailyMenu))
writeToExcelByRows(fileName=dataFile,sheetName='日常业务',data=convertDicList(ArticMenu))
print('#####写入的xls文件名:', dataFile)


@ddt.ddt
class MenuTest(unittest.TestCase):
    """菜单测试"""
    @classmethod
    def setUp(self):
        self.imgs = []
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.file = dataFile

    def get_screenshot(self):
        self.imgs.append(self.driver.get_screenshot_as_base64())
        return True

    @ddt.data(*CreatePersonUserMenu)
    def test_CreatePersonUser(self,dict):
        '''开户菜单冒烟测试'''
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
            write_xlsBycolName(file=self.file, row=getRowIndex(file=self.file, value=funcId, sheet='开户业务'),
                               colName='TEST_RESULT',value=testResult, sheet='开户业务')
            self.assertIn('校验通过',chkPageMsg,msg='菜单打开失败')
        else:
            print('===执行的菜单目录，直接通过')
            pass

    @ddt.data(*EPostInfoMenu)
    def test_EPostInfo(self,dict):
        '''电子发票菜单冒烟测试'''
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
            # write_xlsBycolName(file=dataFile,row=getRowIndex(file=dataFile,value=funcId),colName='TEST_RESULT',value=testResult)
            write_xlsBycolName(file=self.file, row=getRowIndex(file=self.file, value=funcId, sheet='电子发票'),
                               colName='TEST_RESULT',value=testResult, sheet='电子发票')
            self.assertIn('校验通过',chkPageMsg,msg='菜单打开失败')


    @ddt.data(*ArticMenu)
    def test_ArticMenu(self, dict):
        '''引商入柜业务菜单冒烟测试'''
        ##参数化
        logger.info("开始参数化......")
        funcId = dict.get('FUNC_ID')
        menuPath = dict.get('MENU_PATH')
        menuUrl = dict.get('DLL_PATH')
        '''开始菜单冒烟测试'''
        logger.info('测试的菜单路径:{}'.format(menuPath))
        logger.info('测试的菜单编码:{}'.format(funcId))
        logger.info('测试的菜单URL:{}'.format(menuUrl))
        print('====测试的菜单路径:', menuPath)
        print('====测试的菜单URL:', menuUrl)
        if dict.get('IS_LEAF') == '1':  # 只测末级菜单
            test = MainPage(self.driver)
            LoginPage(self.driver).login()
            test.open_CataMenuNew(funcId=funcId)
            self.get_screenshot()
            chkPageMsg = PageAssert(self.driver).assert_WadeFullMsg()
            if '校验通过' in chkPageMsg:
                testResult = '通过'
            else:
                testResult = chkPageMsg
            write_xlsBycolName(file=self.file, row=getRowIndex(file=self.file, value=funcId, sheet='引商入柜业务'),
                               colName='TEST_RESULT',value=testResult, sheet='引商入柜业务')
            self.assertIn('校验通过', chkPageMsg, msg='菜单打开失败')
        else:
            print('===执行的菜单目录，直接通过')
            pass


    def tearDown(self):
        print('测试结束，关闭浏览器器!')
        self.driver.close()

if __name__ == '__main__':
    report_title = u'菜单自动化测试报告自动化测试报告'
    desc = u'菜单自动化测试报告测试详情'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath() + report_title + nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2)

        runner.run(mySuitePrefixAdd(MenuTest,"test_ArticMenu"))
