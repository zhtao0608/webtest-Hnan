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
from Common.TestAsserts import Assertion as Assert
from PageObj.order.BizCommon.ElementPartBase import MainPlanSelectPart
from PageObj.order.BizCommon.ElementPartBase import DealUserCommon
from PageObj.order.BizCommon.ElementPartBase import SelectElements
from PageObj.order.BizCommon.ElementPartBase import PageCommonPart
from Check.RuleCheck import RuleCheckBefore


# logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
logger = LogManager('ProdChangePage').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

rc = ReadConfig.ReadConfig("ngboss_config.ini")

class ProdChangePage(Base):
    def open_base(self):
        self.driver.get(rc.get_ngboss('url'))
        self.driver.maximize_window()

    def openProductChange(self):
        LoginPage(self.driver).login()  # 登录
        MainPage(self.driver).open_CataMenu('crm9000', 'crm9200', 'crmw912',menuPath='page/order.page.pc.person.changeproduct.ChangeProduct')  # 进入产品变更页面
        logger.info('进入产品变更页面')

    def backProdChgPage(self):
        '''新增优惠、服务元素后点击返回'''
        loc_backPopup = (By.XPATH,'//*[@id="elementListpopup-ItemList"]/div[1]/div[1]')
        self.isElementDisplay(loc_backPopup,'click')


    def acceptChgMainProduct(self,accessNum,productId,elementList=[],scene='ChgMainProduct'):
        '''
        个人业务-变更主产品
        :param accessNum:服务号码
        :param productId:主产品编码
        :param elementList:可选组元素列表
        :return:
        '''
        title = '主产品变更测试记录%s' % accessNum
        self.add_dochead(title)
        self.openProductChange()
        self.screen_step("进入产品变更菜单")
        authUser = DealUserCommon(self.driver).AuthUserInfo(accessNum) #用户鉴权,包含了用户鉴权都结果和规则校验信息
        TR().updateRuleCheckInfo(sceneCode=scene,msg=authUser['msg'])
        Assert().assertTrue(authUser['IsAuthSuc'],msg='用户鉴权失败')   #做个鉴权认证
        self.screen_step("点击变更按钮")
        Btn_changeProduct = (By.ID,'changeButton')
        self.isElementDisplay(Btn_changeProduct,'click') #点击产品变更按钮
        time.sleep(2)
        self.screen_step("选择主套餐")
        MainPlanSelectPart(self.driver).MainProductSel(productId,elementList)
        RuleCheckBefore(self.driver).checkRule() #规则校验
        time.sleep(3)
        self.sendEnter()
        PageCommonPart(self.driver).submit() #点击提交
        submitMsg = PageAssert(self.driver).assert_Submit()
        logger.info('业务受理信息：{}'.format(submitMsg))
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)

    def acceptAddElements(self,accessNum,elementList=[],scene='AddElements'):
        '''
        个人业务-新增服务
        :param accessNum:服务号码
        :param productId:主产品编码
        :param elementList:资费和服务列表
        字典数组，包含 OFFER_CODE 和 Offer_type 2个key
        eg :[{"OFFER_CODE":"120000008174","OFFER_TYPE":"S"},{"OFFER_CODE":"120010122813","OFFER_TYPE":"D"}]
        :return:
        '''
        title = '主产品变更测试记录%s' % accessNum
        self.add_dochead(title)
        self.openProductChange()
        self.screen_step("进入产品变更菜单")
        authUser = DealUserCommon(self.driver).AuthUserInfo(accessNum) #用户鉴权,包含了用户鉴权都结果和规则校验信息
        TR().updateRuleCheckInfo(sceneCode=scene,msg=authUser['msg'])
        Assert().assertTrue(authUser['IsAuthSuc'],msg='用户鉴权失败')   #做个鉴权认证
        #新增优惠按钮
        li_addElement = (By.ID,'addElement')
        self.isElementDisplay(li_addElement,'click')
        self.screen_step("选择资费或者服务订购")
        SelectElements(self.driver).addElements(elementList=elementList,scene=scene)
        self.backProdChgPage() #点击回到产品变更主页面
        PageCommonPart(self.driver).submit() #点击提交
        submitMsg = PageAssert(self.driver).assert_Submit()
        logger.info('业务受理信息：{}'.format(submitMsg))
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)

    def acceptDelElements(self,accessNum,elementList=[]):
        '''
        个人业务-新增服务
        :param accessNum:服务号码
        :param productId:主产品编码
        :param elementList:资费和服务列表
        字典数组，包含 OFFER_CODE 和 Offer_type 2个key
        eg :[{"OFFER_CODE":"120000008174","OFFER_TYPE":"S"},{"OFFER_CODE":"120010122813","OFFER_TYPE":"D"}]
        :return:
        '''
        title = '主产品变更测试记录%s' % accessNum
        self.add_dochead(title)
        self.openProductChange()
        self.screen_step("进入产品变更菜单")
        authUser = DealUserCommon(self.driver).AuthUserInfo(accessNum) #用户鉴权,包含了用户鉴权都结果和规则校验信息
        TR().updateRuleCheckInfo(sceneCode=scene,msg=authUser['msg'])
        Assert().assertTrue(authUser['IsAuthSuc'],msg='用户鉴权失败')   #做个鉴权认证
        #删除资费或者服务
        self.screen_step("选择资费或者服务删除")
        SelectElements(self.driver).delElements(elementList)
        PageCommonPart(self.driver).submit() #点击提交
        submitMsg = PageAssert(self.driver).assert_Submit()
        logger.info('业务受理信息：{}'.format(submitMsg))
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)


if __name__ == '__main__':
    driver = webdriver.Chrome()
    test = ProdChangePage(driver)
    # test.acceptChgMainProduct(accessNum='13897492180',productId='18012979',elementList=[])
    test.acceptAddElements(accessNum='18897135437',elementList=[{"OFFER_CODE":"18013676","OFFER_TYPE":"S"},{"OFFER_CODE":"18009531","OFFER_TYPE":"D"}],scene='AddElements')









