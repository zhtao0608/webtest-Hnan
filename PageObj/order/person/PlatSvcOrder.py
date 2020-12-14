import time
from Base.base import Base
from selenium.webdriver.common.by import By
from Base import ReadConfig
from selenium import webdriver
from PageObj.ngboss.login_page import LoginPage
from PageObj.ngboss.mainpage import MainPage
from PageObj.order.BizCommon.ElementPartBase import DealUserCommon
from PageObj.order.BizCommon.ElementPartBase import SelectElements
from Check.PageCheck import PageAssert
from Base.Mylog import LogManager

rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('PlatServiceOrder').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

class PlatServiceOrder(Base):
    '''平台业务受理'''
    def open_base(self):
        self.driver.get(rc.get_ngboss('url'))
        self.driver.maximize_window()
        #self.driver.implicitly_wait(30)

    def openPlatServiceOrder(self):
        LoginPage(self.driver).login()  # 登录
        MainPage(self.driver).open_CataMenu('crm9000', 'IBS1000', 'IBS9271',menuPath='page/order.page.pc.person.plat.PlatOrder')  # 进入产品变更页面
        logger.info('进入平台业务办理页面')

    def backPlatOrderPage(self):
        '''点击回到平台业务受理页面'''
        loc_backPopup = (By.XPATH,'//*[@id="platOrderAddItem"]/div[1]/div[1]')
        self.isElementDisplay(loc_backPopup,'click')

    def searchPlatSvcByOfferCode(self,OfferCode):
        '''
        通过OfferCode查询平台服务
        :param OfferCode:平台服务编码OfferCode
        :return:
        '''
        btn_PlatOrderAdd = (By.XPATH,"//li[contains(@ontap,'platOrderAddItem')]")
        self.isElementDisplay(btn_PlatOrderAdd,'click')
        self.isElementDisplay((By.ID,'myplatform_tab_li_2'),'click') #点击全部
        self.sendkey((By.ID,'COND'),OfferCode) #输入平台服务编码
        btn_platSvcSearch = (By.XPATH,"//span[contains(@ontap,'platOrderAdd.searchOffer')]")
        self.isElementDisplay(btn_platSvcSearch,'click')
        btn_subPlatOffer = (By.XPATH,"//span[contains(@ontap,'platOrderAdd.do_subPlatOffer')]")
        self.isElementDisplay(btn_subPlatOffer,'click') #点击订购按钮
        SelectElements(self.driver).backAcceptPage() #点击回到受理主页面
        return self.checkPlatOrderShow(OfferCode) #返回True或者False  ,

    def acceptSubPlatSvcByOfferCode(self,accessNum,OfferCode):
        '''
        订购OfferCode平台服务
        :param OfferCode:平台服务编码OfferCode
        :return:
        '''
        title = '测试号码_%s订购平台服务测试记录%s' % (accessNum,OfferCode)
        self.add_dochead(title)
        self.openPlatServiceOrder()
        self.screen_step("进入平台业务办理菜单")
        DealUserCommon(self.driver).AuthUserInfo(accessNum) #用户鉴权
        self.screen_step("查看平台服务订购列表")
        isSuc = self.searchPlatSvcByOfferCode(OfferCode)
        if not isSuc:
            logger.info('平台服务%s未订购成功'.format(OfferCode))
        PageCommonPart(self.driver).submit() #点击提交
        submitMsg = PageAssert(self.driver).assert_Submit()
        logger.info('业务受理信息：{}'.format(submitMsg))
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)










    def checkPlatOrderShow(self,OfferCode):
        '''
        检查选择订购的平台服务是否展示在主页面
        :param OfferCode: 平台服务编码
        :return:返回True或者False，如果在订购列表则返回True,否则返回False
        '''
        platOrderShowStr = "//div[contains(@value,'%s') and contains(@ontap,'platOrderShow.unsubPlatform')]" %OfferCode
        flag = self.isElementDisplay(platOrderShowStr)
        return flag








