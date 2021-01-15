import time
from Base.base import Base
from selenium.webdriver.common.by import By
from Base import ReadConfig
from Base.Mylog import LogManager
from Check.PageCheck import PageAssert
from Common.TestAsserts import Assertion as Assert
from Data.DataMgnt.DataOper import DataOper as DTO


logger = LogManager('RealNamePart').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

#================处理实名制认证组件=====================#

class RealNamePart(Base):
    '''实名制认证'''
    def openUserVerify(self,accessNum):
        '''
        用户开户实名认证
        :param accessNum: 手机号码
        :return:
        '''
        self.selectVerifyMode()  #选择在线认证方式
        # self.selectPsptType() #证件类型选择身份证
        self.tradeSend()  #下发工单
        self.verifyRealNameNew(accessNum) #根据手机号码自动更新实名制信息
        self.sleep(1)
        self.tradeQry()  #点击认证检索

    def existUserVerify(self,accessNum):
        '''
        存量用户实名认证
        :param accessNum: 手机号码
        :return:
        '''
        self.selectVerifyMode()  #选择在线认证方式
        self.tradeSend()  #下发工单
        self.verifyRealNameExist(accessNum)
        self.sleep(1)
        self.tradeQry()  #点击认证检索


    def selectVerifyMode(self,verifyMode='人证比对一体机'):
        '''
        选择认证方式
        :param verifyMode: 选择枚举： 人证比对一体机，NFC模式,一般智能手机+二代身份证识别仪 两种方式，人证比对一体机
        :return:
        '''
        # sel_VerifyMode = (By.ID,'VERIFY_MODEL_USER_span') #VERIFY_MODEL_span
        sel_VerifyMode = (By.ID,'VERIFY_MODEL_span') # 湖南认证组件ID修改
        VerifyModeFloatStr = "//*[@id='VERIFY_MODEL_float']/div[2]/div/div/ul/li[contains(@title,'%s')]" %verifyMode
        sel_VerifyModeFloat = (By.XPATH,VerifyModeFloatStr)  #当前写死是在线验证方式
        self.isElementDisplay(sel_VerifyMode,'click')
        self.sleep(1)
        self.isElementDisplay(sel_VerifyModeFloat,'click')

    def selectPsptType(self,psptType='身份证'):
        '''
        选择下单证件类型
        :param psptType:身份证、外国人永久居留身份证、港澳台居民居住证 【默认身份证】
        :return:
        '''
        sel_PsptType = (By.ID,'SEND_PSPT_TYPE_CODE_span')
        PsptTypeStr = "//*[@id='SEND_PSPT_TYPE_CODE_float']/div[2]/div/div/ul/li[contains(@title,'%s')]" %psptType
        sel_PsptTypeFloat = (By.XPATH,PsptTypeStr)  #当前写死是在线验证方式
        self.isElementDisplay(sel_PsptType,'click')
        self.sleep(1)
        self.isElementDisplay(sel_PsptTypeFloat,'click')

    def tradeSend(self):
        '''
        工单下发
        :return:
        '''
        btn_sendTrade = (By.ID,'tradeSendButton')
        self.isElementDisplay(btn_sendTrade,'click',delay=2)
        PageAssert(self.driver).wait_for_load()  #页面一直加载，直到页面加载结束
        self.sleep(1)


    def tradeQry(self):
        '''点击认证检索'''
        btn_tradeQry = (By.ID,'tradeQueryButton')
        self.isElementDisplay(btn_tradeQry,'click',delay=2)
        PageAssert(self.driver).wait_for_load() #处理下页面加载
        Assert().assertIn('认证检索成功',PageAssert(self.driver).assert_WadePage(),msg='认证检索失败')#先校验一下


    def verifyRealNameExist(self,accessNum):
        '''自动更新存量实名信息'''
        return DTO().updateRealNameInfoExist(accessNum)


    def verifyRealNameNew(self,accessNum):
        '''自动更新存量实名信息'''
        return DTO().updateRealNameInfoNew(accessNum)










