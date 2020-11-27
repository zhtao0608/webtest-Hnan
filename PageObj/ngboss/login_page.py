from Base import ReadConfig
from Base.base import Base
from selenium.webdriver.common.by import By
from Common.function import config_url
import time
from selenium import webdriver

from Base.Mylog import LogManager

rc = ReadConfig.ReadConfig("ngboss_config.ini")

class LoginPage(Base):
    def open_base_url(self):
        self.driver.get(config_url())
        self.driver.maximize_window()

    def login_user(self):
        # return self.findele(By.ID , "STAFF_ID")
        loc_userName = (By.ID,"STAFF_ID")
        return self.find(loc_userName)

    def login_pwd(self):
        loc_passwd = (By.ID,"PASSWORD")
        return self.find(loc_passwd)

    def login_btn(self):
        loc_btnLogin = (By.ID , "loginBtn")
        return self.find(loc_btnLogin)

    ##登录操作：
    def login(self,username,password):
        '''登录'''
        self.open_base_url()
        loc_username = (By.ID, "STAFF_ID")
        loc_password = (By.ID , "PASSWORD")
        btn_loginBtn = (By.ID , "loginBtn")
        self.sendkey(loc_username,username)
        self.sendkey(loc_password,password)
        self.screen_step('登录')
        self.isElementDisplay(btn_loginBtn,'click')
        time.sleep(2)
        return self.dr_url()

if __name__ == '__main__':
    print("=====测试一下登录======")
    driver = webdriver.Chrome()
    # driver = webdriver.Ie()
    test = LoginPage(driver)
    test.open_base_url()
    test.login('SUPERUSR','lc')
    driver.close()

