from Base.base import Base
from selenium.webdriver.common.by import By
from Common.function import config_url

import time

class SearchPage(Base):

    def open_base_url(self,url):
        self.driver.get(config_url())
        self.driver.maximize_window()

    def search_leave(self):
        return self.findele(By.ID,"departCityName")

    def search_arrive(self):
        return self.findele(By.ID,"arriveCityName")

    def search_date(self):
        return self.findele(By.ID, "departDate")

    def search_btn(self):
        return self.findele(By.CLASS_NAME, "searchbtn")

    # def search_current(self):
    #     return self.search_current()

    #search_js修改departDate的值
    def search_js(self):
        jsvalue = "document.getElementById('departDate').removeAttribute('readonly')"
        self.js(jsvalue)

    ###页面元素操作：
    def search_train(self,leave,arrive,leave_date):
        self.search_leave().clear()
        self.search_leave().send_keys(leave)
        time.sleep(3)
        self.search_arrive().clear()
        self.search_arrive().send_keys(arrive)
        time.sleep(3)
        self.search_js()
        self.search_date().clear()
        self.search_date().send_keys(leave_date)
        self.search_btn().click()
        time.sleep(3)
        return self.dr_url()


    # if __name__ == '__main__':
    #     # search_train(leave="北京",arrive="广州",leave_date="2020-04-30")









