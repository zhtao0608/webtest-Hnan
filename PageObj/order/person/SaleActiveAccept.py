import time
from Base.base import Base
from Base.OperExcel import write_xlsBycolName_append
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait  # 用于处理元素等待
from Base import ReadConfig
from PageObj.ngboss.mainpage import MainPage
from PageObj.ngboss.login_page import LoginPage
from Base.Mylog import LogManager
from Check.PageCheck import PageAssert
from PageObj.order.BizCommon.PersonOrder.ElementPartBase import DealUserCommon
from PageObj.order.BizCommon.PersonOrder.ElementPartBase import SaleActivePart
from PageObj.order.BizCommon.PersonOrder.ElementPartBase import PageCommonPart
from Check.RuleCheck import RuleCheckBefore



# logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
logger = LogManager('SaleActivePage').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
rc = ReadConfig.ReadConfig("ngboss_config.ini")

class SaleActivePage(Base):
    '''营销活动办理'''
    def open_base(self):
        self.driver.get(rc.get_ngboss('url'))
        self.driver.maximize_window()

    def openSaleActive(self):
        LoginPage(self.driver).login(rc.get_ngboss('username'), rc.get_ngboss('password'))  # 登录
        MainPage(self.driver).open_CataMenu('crm9000', 'crm9300', 'crmw902',menuPath='order.page.pc.saleActive.accept.SaleActiveAccept')  # 进入产品变更页面
        logger.info('进入营销活动受理(存送营销)菜单')

    def acceptAddSaleActive(self,accessNum,OfferCode):
        '''
        个人业务-新增预存营销活动办理
        :param accessNum:服务号码
        :param OfferCode:营销活动编码
        :return:
        '''
        title = '%s办理营销活动%s_测试记录%s' % (accessNum,OfferCode)
        self.add_dochead(title)
        self.openSaleActive()
        self.screen_step("进入营销活动受理(存送营销)菜单")
        DealUserCommon(self.driver).AuthUserInfo(accessNum) #用户鉴权
        # if not flag :
        #     logger.info('用户鉴权失败，终止测试')
        #     self.save_docreport(title)
        #     # self.driver.close()    #直接关闭浏览器
        SaleActivePart(self.driver).selActivePop()
        self.screen_step("点击营销包，选择营销营销活动")
        SaleActivePart(self.driver).searchSaleActive(OfferCode)
        self.screen_step("选择营销活动")
        SaleActivePart(self.driver).selectActive(OfferCode) #选择营销包
        # RuleCheckBefore(self.driver).checkRule()   #规则校验
        RuleCheckBefore(self.driver).checkRule()  #规则校验
        time.sleep(3)
        ####校验码的问题######
        PageCommonPart(self.driver).submit() #点击提交
        submitMsg = PageAssert(self.driver).assert_Submit()
        logger.info('业务受理信息：{}'.format(submitMsg))
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)



