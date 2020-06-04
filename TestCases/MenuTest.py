import unittest,os
import time,ddt
from PageObj.login_page import LoginPage
from PageObj.mainpage import MainPage
from PageObj.oc.person.PersonBase import PersonBase
from PageObj.oc.group.GroupBasePage import BasePage
from selenium import webdriver
from selenium.webdriver.common.by import By
from Common import HTMLTestRunnerCNNew
from Common import ReadConfig
from Common.Mylog import LogManager
from Common.TestDataMgnt import MainPageData
from Common.TestDataMgnt import create_testDataFile
from TestCases.suite import mySuitePrefixAdd
from Common.OperExcel import write_xlsBycolName_append

logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")

person_menu_paras = MainPageData().get_personMenu()  #获取个人菜单测试数据
file_personMenu = ReadConfig.get_data_path() + 'UITest_PersonMenuSmokeTest_%s.xls' % time.strftime("%Y%m%d%H%M%S")
create_testDataFile(paras=person_menu_paras,filename=file_personMenu)


group_menu_paras = MainPageData().get_groupMenu()  #获取个人菜单测试数据
file_GroupMenu = ReadConfig.get_data_path() + 'UITest_GroupMenuSmokeTest_%s.xls' % time.strftime("%Y%m%d%H%M%S")
create_testDataFile(paras=group_menu_paras,filename=file_GroupMenu)

base_url = rc.get_ngboss("url")
username = rc.get_ngboss("username")
password = rc.get_ngboss("password")

@ddt.ddt
class MenuTest(unittest.TestCase):
    """菜单测试"""
    @classmethod
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    @ddt.data(*person_menu_paras)
    def test_PersonMenuSmoke(self,dic):
        '''个人菜单冒烟测试'''
        ##参数化
        logger.info("开始参数化......")
        row = int(dic.get('NO'))  # 标识行号，后续写入xls使用
        accessNum = '13987274867'
        cataMenuId = dic.get('PARENT_ID')  #父菜单
        menuId = dic.get('FUNC_CODE') #子菜单
        MenuName = dic.get('NAME') #菜单名称
        url = dic.get('VIEWNAME') #地址
        logger.info('开始执行{}个菜单，菜单名:{},url:{}'.format(row,MenuName,url))
        '''开始菜单冒烟测试'''
        test = PersonBase(self.driver)
        test.Open_PersonMenu(accessNum,password='123123',cataMenuId =cataMenuId,menuId =menuId)
        logger.info('进入iframe.....')
        self.driver.switch_to.default_content() #记得一定要回到主窗口后再找iframe
        frame_str = "//iframe[contains(@src,'%s')]" % url
        logger.info('frame_str:{}'.format(frame_str))
        loc_frame = (By.XPATH,frame_str)
        test.iframe(loc_frame)
        logger.info("进入{}frame:".format(MenuName))
        # test.iframe(1) #默认进入
        vaildMsg = test.vaild_BusiRule()
        logger.info('进入菜单时校验信息:{}'.format(vaildMsg))
        write_xlsBycolName_append(file=file_personMenu,row=row,colName='RESULT_INFO',value=vaildMsg,index=0)
        self.driver.close()

    @ddt.data(*group_menu_paras)
    def test_GroupMenuSmoke(self,dic):
        '''集团业务菜单冒烟测试'''
        ##参数化
        logger.info("开始参数化......")
        row = int(dic.get('NO'))  # 标识行号，后续写入xls使用
        groupId = '8721420770'
        cataMenuId = dic.get('PARENT_ID')  #父菜单
        menuId = dic.get('FUNC_CODE') #子菜单
        MenuName = dic.get('NAME') #菜单名称
        url = dic.get('VIEWNAME') #地址
        logger.info('开始执行{}个菜单，菜单名:{},url:{}'.format(row,MenuName,url))
        '''开始菜单冒烟测试'''
        test = BasePage(self.driver)
        test.Open_groupMenu(groupId=groupId,parentMenuId=cataMenuId,MenuId = menuId)
        logger.info('进入iframe.....')
        self.driver.switch_to.default_content() #记得一定要回到主窗口后再找iframe
        frame_str = "//iframe[contains(@src,'%s')]" % url
        logger.info('frame_str:{}'.format(frame_str))
        loc_frame = (By.XPATH,frame_str)
        test.iframe(loc_frame)
        logger.info("进入{}frame:".format(MenuName))
        # test.iframe(1) #默认进入
        vaildMsg = test.vaild_GroupBusiRule()
        logger.info('进入菜单时校验信息:{}'.format(vaildMsg))
        write_xlsBycolName_append(file=file_GroupMenu,row=row,colName='RESULT_INFO',value=vaildMsg,index=0)
        self.driver.close()


    def test_menu_01(self):
        """根据菜单路径进入开户业务"""
        driver = self.driver
        driver.get(base_url)
        login = LoginPage(self.driver)
        login.login(username,password)
        Me = MainPage(self.driver)
        Me.sel_person_subscriber()
        self.assertIn('客户关系管理系统CRM', self.driver.title)
        self.driver.close()

    def test_menu_02(self):
        """菜单搜索进入"""
        driver = self.driver
        driver.get(base_url)
        login = LoginPage(self.driver)
        login.login(username,password)
        Me = MainPage(self.driver)
        Me.search_menu("集团商品业务查询")
        self.assertIn(self.driver.title, '客户关系管理系统CRM')
        self.driver.close()

    def test_menu_03(self):
        """根据菜单路径进入查询业务"""
        driver = self.driver
        driver.get(base_url)
        login = LoginPage(self.driver)
        login.login(username,password)
        Me = MainPage(self.driver)
        Me.qry_busi()
        self.assertIn('客户关系管理系统CRM', self.driver.title)
        self.driver.close()

    def test_menu_04(self):
        """根据菜单路径进入日常业务"""
        driver = self.driver
        driver.get(base_url)
        login = LoginPage(self.driver)
        login.login(username,password)
        Me = MainPage(self.driver)
        Me.daily_busi()
        self.assertIn('客户关系管理系统CRM', self.driver.title)
        self.driver.close()


if __name__ == '__main__':
    report_title = u'菜单自动化测试报告自动化测试报告'
    desc = u'菜单自动化测试报告测试详情'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath() + report_title + nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2)
        runner.run(mySuitePrefixAdd(MenuTest,"test_GroupMenuSmoke"))
