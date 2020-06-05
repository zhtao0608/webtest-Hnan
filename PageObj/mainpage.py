import time
from Base.base import Base
from selenium.webdriver.common.by import By
from Base import ReadConfig
from selenium import webdriver
from PageObj.login_page import LoginPage

rc = ReadConfig.ReadConfig("ngboss_config.ini")

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
        self.isElementExist(loc_main,'click')
        return self.driver

    #更多-订单中心
    def menu_order(self):
        Loc_oc = (By.CSS_SELECTOR,'#menus_tab_li_1')
        self.isElementExist(Loc_oc,'click')
        return self.driver

    def open_OcCataMenu(self,parentMenu,MenuId):
        '''菜单目录'''
        self.home_loc()
        self.iframe('navframe_def')
        self.main_menu()
        time.sleep(1)
        self.menu_order()
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
    LoginPage(driver).login(rc.get_ngboss('username'),rc.get_ngboss('password'))  #登录
    # offerlist = ['99091290','99091387','99091288']
    test.search_offerNew('99091283')
    driver.close()