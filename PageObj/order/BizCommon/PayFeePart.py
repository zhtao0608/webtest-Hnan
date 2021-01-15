import time
from Base.base import Base
from selenium.webdriver.common.by import By
from Base import ReadConfig
from Base.Mylog import LogManager
from Check.RuleCheck import RuleCheckBefore
from Check.PageCheck import PageAssert
from Common.TestAsserts import Assertion


logger = LogManager('PayFeePart').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

#================处理页面元素公共类，包含主套餐、服务、优惠、平台服务等======================#

class PayFeePart(Base):
    '''支付组件'''
    def confirmPayFee(self):
        '''确认支付'''
        btn_submitFee = (By.ID,'FEEPOPUP_SUBMIT_BTN') #支付提交
        # btn_confirmFee = (By.ID,'CASH_PAY_SUBMIT_BTN') #现金支付
        btn_payCash = (By.XPATH,'//*[@id="FEE_MSG_BTN"]/button[3]') #现金支付
        try:
            self.isElementDisplay(btn_submitFee,'click',delay=2)
            PageAssert(self.driver).wait_for_load()
            self.isElementDisplay(btn_payCash,'click') #点击现金支付
        except :
            logger.info('未弹出支付组件,直接提交！')
