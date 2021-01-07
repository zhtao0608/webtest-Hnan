from Base.base import Base
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait  # 用于处理元素等待
from Base import ReadConfig
from Base.Mylog import LogManager
from Common.TestAsserts import Assertion as alert
from Common.function import getDigitFromStr
import time,sys

logger = LogManager('SubmitMsgAssert').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

class SubmitMsgAssert(Base):
    '''页面检查点'''
    def get_submitTitle(self):
        """获取提交信息Title"""
        loc_submitTitle = (By.ID,'SUBMIT_MSG_TITLE')
        title=self.get_submitTitle()
        logger.info('业务受理信息提示:{}'.format(title))
        return self.get(loc_submitTitle)

    def get_submitContent(self):
        '''获取提交信息内容'''
        loc_submitContent=(By.ID,'SUBMIT_MSG_CONTENT')
        content = self.get(loc_submitContent)
        logger.info('业务受理信息:{}'.format(content))
        return content

    def getOrderId(self):
        '''获取订单信息'''
        title=self.get_submitTitle()
        alert().assertIn('业务受理成功',title,msg='业务办理失败！')
        orderId = getDigitFromStr(self.get_submitContent())
        logger.info('业务受理订单号:{}'.format(orderId))
        return orderId



