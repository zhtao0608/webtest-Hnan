import time
from Base.base import Base
from selenium.webdriver.common.by import By
from Base import ReadConfig
from selenium import webdriver
from PageObj.ngboss.login_page import LoginPage
from Base.Mylog import LogManager

rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('MainPage').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )


class MainPage(Base):
    def open_base(self):
        self.driver.get(rc.get_ngboss('url'))     #这里可以切换环境，去ngboss_config.ini配置
        self.driver.maximize_window()
        #self.driver.implicitly_wait(30)

    #切换frame
    def switch_frame(self):
        self.driver.switch_to.default_content()
        ele= self.find((By.ID,'navframe_def'))
        self.driver.switch_to.frame(ele)
        return self.driver

    ##首页Home按钮
    def home_loc(self):
        loc_home = (By.CSS_SELECTOR,"#m_home")
        self.isElementExist(loc_home,'click')

    # 首页->更多
    def main_menu(self):
        loc_main = (By.ID,'welTab_tab_li_6')
        loc_mainByGrpRole = (By.XPATH,'/html/body/div[1]/div[2]/div[3]/span') #政企角色登录
        try:
            print('=====普通角色登录=====')
            self.find_element_click(loc_main)
        except:
            print('=====政企角色登录=====')
            self.find_element_click(loc_mainByGrpRole)
    #更多-订单中心
    def menu_order(self):
        Loc_oc = (By.CSS_SELECTOR,'#menus_tab_li_1')
        self.isElementExist(Loc_oc,'click')
        return self.driver

    def OpenDomain(self,DomainId):
        '''选择中心点击
        :param DomainId: 0-客户中心
        1-订单中心，2-产品商品中心，3-零库存管理中心 4-营销中心 5-基础管理中心
        6-销售中心 7-账务中心 8-渠道中心 9-票据中心 10-统计分析
        11-代理商 12-产品管理(计费账务) 13-计费中心 14-在线中心 15-IFRS15中心
        16-支付中心
        :return:
        '''
        if isinstance(DomainId,int):
            DomainId = str(DomainId)
        domainId_str = 'menus_tab_li_%s' % DomainId
        loc_domain = (By.ID,domainId_str)
        self.home_loc()
        self.iframe('navframe_def')
        self.main_menu() #点击更多
        time.sleep(1)
        self.find_element_click(loc_domain)

    def open_CataMenu(self,domainId,catamenu,parentMenu,MenuId):
        '''
        :param domainId: 归属中心
        :param catamenu: 菜单目录
        :param parentMenu: 父菜单
        :param MenuId: 子菜单
        :return:
        '''
        '''打开菜单'''
        self.open_base()
        LoginPage(self.driver).login(rc.get_ngboss('username'), rc.get_ngboss('password'))  # 登录
        self.OpenDomain(domainId)
        catamenu_str  =  "//li[@menuid='%s']" % catamenu
        self.find_element_click((By.XPATH,catamenu_str)) #菜单目录
        parMenu = "//*[@menuid='%s']" % parentMenu # 父菜单
        logger.info("菜单目录：{}" .format(parentMenu))
        self.find_element_click((By.XPATH,parMenu))
        time.sleep(1)
        # xpath_menu = "//*[@menuid='%s']" % MenuId
        self.Open_menu(MenuId)
        logger.info("菜单ID：{}" .format(MenuId))


    def open_OcCataMenu(self,parentMenu,MenuId):
        '''菜单目录'''
        self.home_loc()
        self.iframe('navframe_def')
        self.main_menu()
        time.sleep(1)
        self.OpenDomain(1)
        parMenu = "//*[@menuid='%s']" %parentMenu
        print("菜单目录：" + parentMenu)
        self.find((By.XPATH,parMenu)).click()
        xpath_menu = "//*[@menuid='%s']" %MenuId
        print("菜单ID：" + MenuId)
        self.find((By.XPATH,xpath_menu)).click()
        return self.driver

    def Open_menu(self,menuId):
        '''menuId传入参数，如果找到则打开，目前只打开订单中心菜单'''
        menu = '#'+ menuId
        loc_menu = (By.CSS_SELECTOR,menu)
        if (self.isElementExist(loc_menu)):
            self.find(loc_menu).click()
            time.sleep(5)
            self.screen_step('进入菜单')
        else:
            print('菜单未找到，不能打开')


    #选择个人用户开户菜单：
    def sel_person_subscriber(self):
        self.open_OcCataMenu('crm9000','crm9100')  #个人业务-开户业务菜单目录
        self.Open_menu('crm9130')   #打开开户菜单
        time.sleep(5)
        return self.driver

    def search_menu(self,menuname):
        self.switch_frame()
        self.findele(By.ID,"menu_search").send_keys(menuname)
        self.findele(By.CSS_SELECTOR,"#button_search > span").click()
        time.sleep(2)
        self.driver.switch_to.default_content()
        #先定位到外层iframe,逐级进入
        self.driver.switch_to.frame(1)
        self.driver.switch_to.frame("main")
        ele = self.findele(By.CSS_SELECTOR,"body > div > div > div.c_list.c_list-hideFn.c_list-line.c_list-border.c_list-col-4 > ul > li > div > div > span")
        ele.click()
        time.sleep(10)
        self.driver.switch_to.default_content()
        return self.driver

    def open_searchFrame(self):
        loc_frame = (By.XPATH,"//iframe[contains(@src,'SearchFrame')]")
        self.iframe(loc_frame)

    def close_search(self):
        ele = self.findele(By.XPATH,"/html/body/div[2]/div[4]/ul/li[1]/div[2]/div[2]")
        ele.click()

    def search_offer(self,offer):
        self.home_loc()
        self.driver.switch_to.default_content()
        self.switch_frame()
        self.sendkey((By.ID,"menu_search"),offer)
        self.isElementDisplay((By.CSS_SELECTOR,"#button_search > span"),'click')
        time.sleep(10)
        self.driver.switch_to.default_content()
        self.open_searchFrame()
        self.iframe("main")
        li_ele = (By.CSS_SELECTOR,"body > div.c_scroll.c_scroll-float > div > div:nth-child(4) > ul > li")
        self.isElementExist(li_ele,'click')
        self.driver.switch_to.default_content()
        return self.driver

    def search_offerNew(self,offerId):
        self.home_loc()
        self.driver.switch_to.default_content()
        self.switch_frame()
        loc_search = (By.ID,"menu_search")
        self.element_sendkey_click(loc_search,offerId)
        time.sleep(2)
        self.isElementExist((By.ID,offerId),'click')
        time.sleep(10)
        self.driver.switch_to.default_content()
        return self.driver

    def search_menuNew(self,menuname):
        self.switch_frame()
        loc_search = (By.ID, "menu_search")
        self.element_sendkey_click(loc_search, menuname)
        time.sleep(2)
        self.isElementExist((By.CSS_SELECTOR, '#menu_search_list > li.link.on'), 'click')
        time.sleep(10)
        self.driver.switch_to.default_content()
        return self.driver

    def daily_busi(self):
        self.open_OcCataMenu('crm9000','crm9200')
        return self.driver

    def qry_busi(self):
        """查询业务"""
        self.open_OcCataMenu('crm9000','crm9900')
        time.sleep(1)
        return self.driver

    def special_busi(self):
        """特殊业务"""
        self.open_OcCataMenu('crm9000','crm9400')
        time.sleep(1)
        return self.driver

    def other_busi(self):
        """其他业务"""
        self.open_OcCataMenu('crm9000','crm9300')
        time.sleep(1)
        return self.driver

if __name__ == '__main__':
    driver = webdriver.Chrome()
    test = MainPage(driver)
    test.open_base()
    # LoginPage(driver).login(rc.get_ngboss('username'),rc.get_ngboss('password'))  #登录
    # LoginPage(driver).login('TESTKM13',rc.get_ngboss('password'))  #登录
    # test.open_OcCataMenu('crm9000','crm9100')
    test.open_CataMenu(1,'crm9000','crm9100','crm9130')


    # test.open_CataMenu(0,'crm5000','crm5300','crm5217')
    # driver.close()