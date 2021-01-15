import time
from Base.base import Base
from Base.OperExcel import write_xlsBycolName_append
from selenium import webdriver
from selenium.webdriver.common.by import By
from Data.DataMgnt.TestResult import TestResultOper as TR
from Base import ReadConfig
from Base.SysPara import SysPara as sp
from PageObj.ngboss.mainpage import MainPage
from PageObj.ngboss.login_page import LoginPage
from Base.Mylog import LogManager
from Check.PageCheck import PageAssert
from Common.TestAsserts import Assertion as alert
from Common.function import isNotBlank,getDigitFromStr
from PageObj.order.BizCommon.ElementPartBase import DealUserCommon
from PageObj.order.BizCommon.ElementPartBase import PageCommonPart
from PageObj.order.BizCommon.PayFeePart import PayFeePart as Pay
from PageObj.order.BizCommon.RealNamePart import RealNamePart as RnPart
from Check.RuleCheck import RuleCheckBefore
from Check.DataCheck import DataCheck as Dc
from Common.SuiteExec import DealSuiteExec as Dse



# logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
logger = LogManager('ChgCard').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

class SimCardChgPage(Base):
    """补换卡页面对象处理"""
    def open_base(self):
        self.driver.maximize_window()

    def openChgSim(self):
        LoginPage(self.driver).login()  # 登录
        MainPage(self.driver).open_CataMenuNew(funcId='crm9283')
        logger.info('进入补卡页面')

    def inputSim(self,simId):
        '''
        输入sim卡并校验
        :param simId: SIM卡
        :return:
        '''
        text_simCardNo = (By.ID,'SIM_CARD_NO')
        self.input(text_simCardNo,simId) #输入SIM
        vaildMsg = self.checkSim()
        logger.info('SIM校验信息:{}'.format(vaildMsg))
        alert().assertIn('校验通过',vaildMsg,msg='SIM卡校验不通过，终止测试！')

    def checkSim(self):
        '''点击校验并判断页面返回'''
        btn_checkSim = (By.XPATH,'//*[contains(@id,"SIM_CARD") and contains(@onclick,"checkWriteCard")]')
        self.isElementDisplay(btn_checkSim,'click',delay=3)
        PageAssert(self.driver).wait_for_load()
        return PageAssert(self.driver).assert_WadePage()


    def accept_ChgSimCard(self,accessNum,simId,scene='ChgSimCard'):
        '''
        补换卡受理
        :param accessNum: 手机号码
        :param simId: SIM卡号
        :param scene: 场景编码
        :return: msg 业务办理信息
        '''
        title = '补换卡业务受理测试记录%s' % accessNum
        self.add_dochead(title)
        self.openChgSim()
        self.screen_step("停开机业务受理")
        authUser = DealUserCommon(self.driver).AuthUserInfo(accessNum) #用户鉴权,包含了用户鉴权都结果和规则校验信息
        if not authUser['IsAuthSuc'] :  #如果鉴权失败，这里要讲错误回写到RULE_CHECK_INFO
            Dse().upd_RuleChkBySuiteCaseId(suite_case_id=scene,rule_chkmsg=authUser['msg'])
        alert().assertTrue(authUser['IsAuthSuc'],msg='用户鉴权失败')   #做个鉴权认证
        RnPart(self.driver).existUserVerify(accessNum)
        self.inputSim(simId)
        PageCommonPart(self.driver).submit() #点击提交
        Pay(self.driver).confirmPayFee() #自动支付组件支付
        submitMsg = PageAssert(self.driver).assertSubmit()
        logger.info('业务受理信息：{}'.format(submitMsg))
        if alert().verifyassertIn('业务受理成功',submitMsg):
            Dc().dealMainOrder(orderId=getDigitFromStr(submitMsg)) #处理主订单，如果状态是Y或者X 修改成0
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)
        return submitMsg


if __name__ == '__main__':
    driver = webdriver.Chrome()
    test = SimCardChgPage(driver)
    # test.acceptSubPlatSvcByOfferCode(accessNum='13787173972',offerCode='99073092')
    test.accept_ChgSimCard(accessNum='13787173972',simId='898600071895F4107365')



