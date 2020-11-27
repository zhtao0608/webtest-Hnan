import time
from Base.base import Base
from selenium.webdriver.common.by import By
from Base import ReadConfig
from PageObj.ngboss.mainpage import MainPage
from PageObj.ngboss.login_page import LoginPage
from PageObj.ngboss.loginPart import LoginPart
from Base.Mylog import LogManager
from Check.PageCheck import PageAssert
# logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
logger = LogManager('CustBasePage').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

rc = ReadConfig.ReadConfig("ngboss_config.ini")

class CustBasePage(Base):
    '''公共方法'''
    def open_base(self):
        self.driver.get(rc.get_ngboss('url'))
        self.driver.maximize_window()


