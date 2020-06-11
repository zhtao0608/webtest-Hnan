from Base.base import Base
from selenium.webdriver.common.by import By
from Common.function import config_url
import time
from Base.Mylog import LogManager


class LoginPage(Base):
    def open_base_url(self):
        self.driver.get(config_url())
        self.driver.maximize_window()

    def login_user(self):
        return self.findele(By.ID , "STAFF_ID")

    def login_pwd(self):
        return self.findele(By.ID , "PASSWORD")

    def login_btn(self):
        return self.findele(By.ID , "loginBtn")

    def quit_dailog(self):
        loc_dailog = (By.CSS_SELECTOR,"#UI-release > div > div.c_header.c_header-white > div.fn > button > span")
        self.isElementDisplay(loc_dailog,'click')
        return self.driver


    def exit_alert(self):
        loc_UIstep1 = (By.CSS_SELECTOR,'#UI-step1 > div.tip > div > div > div.fn > button:nth-child(1)')
        loc_GRstep1= (By.CSS_SELECTOR,'#GR-step1 > div.tip > div > div > div.fn > button:nth-child(1)')
        flag = self.isElementDisplay(loc_UIstep1)
        try:
            if flag:
                self.isElementDisplay(loc_UIstep1,'click')
            else:
                self.isElementDisplay(loc_GRstep1, 'click')
        except:
            pass   #跳过
            print("测试失败，关闭!")
        return self.driver

    ##登录操作：
    def login(self,username,password):
        '''登录'''
        loc_username = (By.ID, "STAFF_ID")
        loc_password = (By.ID , "PASSWORD")
        btn_loginBtn = (By.ID , "loginBtn")
        self.sendkey(loc_username,username)
        self.sendkey(loc_password,password)
        self.screen_step('登录')
        self.isElementDisplay(btn_loginBtn,'click')
        time.sleep(2)
        #关闭不再显示
        self.quit_dailog()
        #关闭提示
        self.exit_alert()
        return self.dr_url()




