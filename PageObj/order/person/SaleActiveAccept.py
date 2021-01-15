import time
from Base.base import Base
from selenium import webdriver
from Data.DataMgnt.TestResult import TestResultOper as TR
from Base import ReadConfig
from PageObj.ngboss.mainpage import MainPage
from PageObj.ngboss.login_page import LoginPage
from Base.Mylog import LogManager
from Check.PageCheck import PageAssert
from PageObj.order.BizCommon.ElementPartBase import DealUserCommon
from PageObj.order.BizCommon.ElementPartBase import SaleActivePart
from PageObj.order.BizCommon.ElementPartBase import PageCommonPart
from Check.RuleCheck import RuleCheckBefore
from Common.TestAsserts import Assertion as Assert
from Common.function import getDigitFromStr
from Check.DataCheck import DataCheck as dc


logger = LogManager('SaleActivePage').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

class SaleActivePage(Base):
    '''营销活动办理'''
    def open_base(self):
        # self.driver.get(rc.get_ngboss('url'))
        self.driver.maximize_window()

    def openSaleActive(self):
        LoginPage(self.driver).login()  # 登录
        # MainPage(self.driver).open_CataMenu('crm9000', 'crm9300', 'crmw902',menuPath='order.page.pc.saleActive.accept.SaleActiveAccept')  # 进入产品变更页面
        MainPage(self.driver).open_CataMenuNew(funcId='crm9961')
        logger.info('进入营销活动受理菜单')


    def getSmsCode(self,accessNum):
        '''
        根据手机号码获取验证码
        :param accessNum:
        :return:
        '''


    def accept_addSaleActive(self,accessNum,offerCode,scene='AddSaleActive'):
        '''
        个人业务-新增预存营销活动办理
        :param accessNum:服务号码
        :param OfferCode:营销活动编码
        :return:
        '''
        title = '%s办理营销活动%s_测试记录' % (accessNum,offerCode)
        self.add_dochead(title)
        self.openSaleActive()
        self.screen_step("进入营销活动受理菜单")
        authUser = DealUserCommon(self.driver).AuthUserInfo(accessNum) #用户鉴权,包含了用户鉴权都结果和规则校验信息
        TR().updateRuleCheckInfo(sceneCode=scene,msg=authUser['msg'])
        Assert().assertTrue(authUser['IsAuthSuc'],msg='用户鉴权失败')   #做个鉴权认证
        SaleActivePart(self.driver).addSaleActive(offerCode)
        RuleCheckBefore(self.driver).checkRule(scene)  #规则校验,如果失败则终止，并将校验结果写入到数据库中
        ####校验码的问题######
        PageCommonPart(self.driver).submit() #点击提交
        submitMsg = PageAssert(self.driver).assertSubmit()
        logger.info('业务受理信息：{}'.format(submitMsg))
        if '业务受理成功' in submitMsg:
            dc().dealMainOrder(getDigitFromStr(submitMsg))
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)
        return submitMsg


if __name__ == '__main__':
    driver = webdriver.Chrome()
    test = SaleActivePage(driver)
    test.accept_addSaleActive(accessNum='13974862507',offerCode='99967823',scene='AddSaleActive')


