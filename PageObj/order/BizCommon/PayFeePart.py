import time
from Base.base import Base
from selenium.webdriver.common.by import By
from Base import ReadConfig
from Base.Mylog import LogManager
from Check.RuleCheck import RuleCheckBefore
from Check.PageCheck import PageAssert
from Common.TestAsserts import Assertion


rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('PayFeePart').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

#================处理页面元素公共类，包含主套餐、服务、优惠、平台服务等======================#

class PayFeePart(Base):
    '''支付组件'''
    def confirmPayFee(self):
        '''确认支付'''
        btn_submitFee = (By.ID,'FEEPOPUP_SUBMIT_BTN') #支付提交
        btn_confirmFee = (By.ID,'CASH_PAY_SUBMIT_BTN') #现金支付
        self.isElementDisplay(btn_submitFee,'click')
        time.sleep(2)
        self.isElementDisplay(btn_confirmFee,'click')
