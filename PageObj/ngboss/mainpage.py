import time,sys
from Base.base import Base
from selenium.webdriver.common.by import By
from Base import ReadConfig
from selenium import webdriver
from PageObj.ngboss.login_page import LoginPage
from Base.Mylog import LogManager
from Data.DataMgnt.DataOper import DataOper as Dto
from Common.TestAsserts import Assertion as Assert
from Common.dealParas import convert_to_diclistLower,capital_to_lower
from Check.PageCheck import PageAssert


logger = LogManager('MainPage').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

class MainPage(Base):
    def open_base(self):
        self.driver.maximize_window()
        #self.driver.implicitly_wait(30)

    #切换frame
    def switch_home(self):
        self.driver.switch_to.default_content()
        loc_home = (By.ID,'navframe_def')
        ele= self.find(loc_home)
        self.driver.switch_to.frame(ele)
        return self.driver

    def click_HomeTab(self,index='6'):
        '''
        根据传入的主参数索引，单击进入
        :param index: 索引号
        0-工作台，  1-商城，   2-办活动，  3-选套餐，  4-开宽带，   5-全菜单
        '''
        self.switch_home()     #先进入首页
        strIndex = "homeTab_tab_li_%s"  % index #传入菜单索引参数
        loc_homeTab = (By.ID,strIndex)
        self.isElementDisplay(loc_homeTab,'click')   #找到即进入

    def click_MenuTab(self,inx='0'):
        '''
        根据传入的主参数索引，单击进入
        :param index: 菜单索引号
        0-CRM   1-帐务管理  2-政企业务运营平台,
        '''
        self.click_HomeTab() #先点击全菜单
        strIndex = "menuTab_tab_li_%s" % inx #传入菜单索引参数
        loc_menuTab = (By.ID,strIndex)
        self.isElementDisplay(loc_menuTab,'click')   #找到即进入

    def click_MenuGroupBusiTab(self,inx='2'):
        '''
        政企业务运营平台
        根据传入的主参数索引，单击进入
        :param index: 菜单索引号
        0-CRM   1-帐务管理  2-政企业务运营平台,
        '''
        self.click_HomeTab() #先点击全菜单
        strIndex = "menuTab_tab_li_%s" % inx #传入菜单索引参数
        loc_menuTab = (By.ID,strIndex)
        self.isElementDisplay(loc_menuTab,'click')   #找到即进入

    def open_CataMenu(self,catamenu,parentMenu,MenuId,menuPath):
        '''
        :param catamenu: 菜单目录
        :param parentMenu: 父菜单
        :param MenuId: 子菜单
        :return:
        '''
        '''打开菜单'''
        self.click_MenuTab()
        catamenu_str  =  "//li[@menuid='%s']" % catamenu
        self.find_element_click((By.XPATH,catamenu_str)) #菜单目录
        parMenu = "//li[@menuid='%s']" % parentMenu # 父菜单
        logger.info("菜单目录：{}" .format(parentMenu))
        self.find_element_click((By.XPATH,parMenu))
        self.sleep(1)
        self.Open_menu(MenuId,menuPath)
        logger.info("菜单ID：{}" .format(MenuId))

    def open_CataMenuNew(self,funcId):
        '''
        :param funcId: 菜单编码
        :return:
        '''
        '''打开菜单'''
        ##先根据传入的funcId获取菜单配置
        menuConfig = Dto().getSysMenu(funcId)
        logger.info('读取的菜单配置:{}'.format(menuConfig))
        if isinstance(menuConfig,dict):
            menuConfig = capital_to_lower(menuConfig)  #先将字典转换成小写
        elif isinstance(menuConfig,list):
            menuConfig = convert_to_diclistLower(menuConfig) #先将字典list转换成小写
        logger.info('转换后菜单配置:{}'.format(menuConfig))
        catamenu = menuConfig['menu_cata']
        parentMenu = menuConfig['parent_func_id']
        MenuId = menuConfig['func_id']
        menuPath = menuConfig['dll_path']
        moduleName = menuConfig['module']
        if moduleName =='集团业务' or moduleName =='ESOP业务' or moduleName=='政企平台V1':
            self.click_MenuTab(inx=2)  #如果是集团业务、ESOP业务或者政企平台V1 则点击政企业务运营平台
            self.sleep(1)
        else:
            self.click_MenuTab()
        catamenu_str  =  "//li[@menuid='%s']" % catamenu
        self.isElementDisplay((By.XPATH,catamenu_str),'click') #菜单目录
        # self.sleep(1)
        parMenu = "//li[@menuid='%s']" % parentMenu # 父菜单
        logger.info("菜单目录：{}" .format(parentMenu))
        self.isElementDisplay((By.XPATH,parMenu),'click')
        self.Open_menu(MenuId,menuPath)
        logger.info("菜单ID：{}" .format(MenuId))


    def Open_menu(self,menuId,menuPath):
        '''menuId传入参数，如果找到则打开，目前只打开订单中心菜单'''
        menu = "//li[@menuid='%s']" %menuId
        loc_menu = (By.XPATH,menu)
        if (self.isElementExist(loc_menu)):
            self.find(loc_menu).click()
            # self.sleep(1)
            self.screen_step('进入菜单')
            title = self.get_attribute(loc_menu,name='title')
            logger.info("进入菜单路径 :" + title)
            self.Open_Menuframe(menuPath)
        else:
            print('菜单未找到，不能打开')


    def Open_Menuframe(self,menuPath):
        '''
        传入菜单路径，进入对应菜单的Iframe页面
        :param menuPath: 菜单路径
        :return:
        '''
        self.driver.switch_to.default_content()
        menuPathStr =  "//iframe[contains(@src,'%s')]" %menuPath   #传入对应的菜单路径
        loc_menuframe = self.find((By.XPATH,menuPathStr))
        self.driver.switch_to.frame(loc_menuframe)
        logger.info("进入菜单Iframe:" + str(loc_menuframe))
        self.sleep(1)   #暂定进入菜单时间1s
        return self.driver

    ##搜索菜单功能
    def search_menu(self,menuname):
        self.switch_home()
        self.findele(By.ID,"menu_search").send_keys(menuname)
        self.findele(By.CSS_SELECTOR,"#button_search > span").click()
        self.sleep(2)
        self.driver.switch_to.default_content()
        #先定位到外层iframe,逐级进入
        self.driver.switch_to.frame(1)
        self.driver.switch_to.frame("main")
        ele = self.findele(By.CSS_SELECTOR,"body > div > div > div.c_list.c_list-hideFn.c_list-line.c_list-border.c_list-col-4 > ul > li > div > div > span")
        ele.click()
        self.sleep(10)
        self.driver.switch_to.default_content()
        return self.driver

    def open_searchFrame(self):
        loc_frame = (By.XPATH,"//iframe[contains(@src,'SearchFrame')]")
        self.iframe(loc_frame)

    def close_search(self):
        ele = self.findele(By.XPATH,"/html/body/div[2]/div[4]/ul/li[1]/div[2]/div[2]")
        ele.click()

    def search_offer(self,offer):
        self.EnterCataMenu()
        self.driver.switch_to.default_content()
        self.switch_home()
        self.input((By.ID,"menu_search"),offer)
        self.isElementDisplay((By.CSS_SELECTOR,"#button_search > span"),'click')
        self.sleep(10)
        self.driver.switch_to.default_content()
        self.open_searchFrame()
        self.iframe("main")
        li_ele = (By.CSS_SELECTOR,"body > div.c_scroll.c_scroll-float > div > div:nth-child(4) > ul > li")
        self.isElementExist(li_ele,'click')
        self.driver.switch_to.default_content()
        return self.driver

    def search_offerNew(self,offerId):
        self.EnterCataMenu()
        self.driver.switch_to.default_content()
        self.switch_home()
        loc_search = (By.ID,"menu_search")
        self.element_sendkey_click(loc_search,offerId)
        self.sleep(2)
        self.isElementExist((By.ID,offerId),'click')
        self.sleep(10)
        self.driver.switch_to.default_content()
        return self.driver

    def search_menuNew(self,menuname):
        self.switch_home()
        loc_search = (By.ID, "menu_search")
        self.element_sendkey_click(loc_search, menuname)
        self.sleep(2)
        self.isElementExist((By.CSS_SELECTOR, '#menu_search_list > li.link.on'), 'click')
        self.sleep(10)
        self.driver.switch_to.default_content()
        return self.driver


if __name__ == '__main__':
    driver = webdriver.Chrome()
    test = MainPage(driver)
    # LoginPage(driver).login(rc.get_ngboss('username'),rc.get_ngboss('password'))  #登录
    LoginPage(driver).login()
    test.open_CataMenuNew(funcId='crm9731')
    # test.open_CataMenu('crm8000','crm8200','crm8207')
    driver.close()
