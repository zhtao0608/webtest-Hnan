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
from PageObj.order.BizCommon.ElementPartBase import MainPlanSelectPart
from PageObj.order.BizCommon.ElementPartBase import DealUserCommon
from PageObj.order.BizCommon.ElementPartBase import PageCommonPart
from Check.RuleCheck import RuleCheckBefore
from Check.DataCheck import DataCheck as Dc


# logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
logger = LogManager('ChgSvcState').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

class SvcStateChgPage(Base):
    def open_base(self):
        # self.driver.get(rc.get_ngboss('url'))
        self.driver.maximize_window()

    def openChgSvcState(self):
        LoginPage(self.driver).login()  # 登录
        MainPage(self.driver).open_CataMenuNew(funcId='crm9221')
        logger.info('进入停开机业务受理页面')

    def get_stopStartOper(self,busiName):
        '''获取停开机类型'''
        alert().assertTrue(isNotBlank(busiName),msg='必须传入业务类型名称！')
        return sp().getSysParaByCode(paramCode=busiName,paramAttr='OptionType')

    def sel_changeOptionType(self,busiName):
        '''
        根据业务名称选择停开机类型
        :param busiName: 业务名称
        :return:
        '''
        optionType = self.get_stopStartOper(busiName)
        changeOptionTypeStr = '//*[@id="radioCheck"]/ul/li[%s]/div' % optionType
        logger.info('停开机业务类型元素:{}'.format(changeOptionTypeStr))
        li_changeOptionType = (By.XPATH,changeOptionTypeStr)
        self.isElementDisplay(li_changeOptionType,'click')


    def accept_ChgSvcState(self,accessNum,busiName,scene='ChgSvcState'):
        '''
        个人业务-停开机业务受理
        :param accessNum:服务号码
        :param busiName:主产品编码
        :return:
        '''
        title = '停开机业务受理测试记录%s' % accessNum
        self.add_dochead(title)
        self.openChgSvcState()
        self.screen_step("停开机业务受理")
        authUser = DealUserCommon(self.driver).AuthUserInfo(accessNum) #用户鉴权,包含了用户鉴权都结果和规则校验信息
        TR().updateRuleCheckInfo(sceneCode=scene,msg=authUser['msg'])
        alert().assertTrue(authUser['IsAuthSuc'],msg='用户鉴权失败')   #做个鉴权认证
        self.sel_changeOptionType(busiName)
        RuleCheckBefore(self.driver).checkRule(scene) #规则校验
        PageCommonPart(self.driver).submit() #点击提交
        submitMsg = PageAssert(self.driver).assertSubmit()
        logger.info('业务受理信息：{}'.format(submitMsg))
        if alert().verifyassertIn('业务受理成功',submitMsg):
            Dc().dealMainOrder(orderId=getDigitFromStr(submitMsg)) #处理主订单，如果状态是Y或者X 修改成0
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)
        return submitMsg


if __name__ == '__main__':
    driver = webdriver.Chrome()
    test = SvcStateChgPage(driver)
    test.accept_ChgSvcState(accessNum='18390996579',busiName='报开')

