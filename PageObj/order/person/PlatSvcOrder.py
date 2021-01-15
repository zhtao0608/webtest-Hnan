import time
from Base.base import Base
from selenium.webdriver.common.by import By
from Base import ReadConfig
from selenium import webdriver
from PageObj.ngboss.login_page import LoginPage
from PageObj.ngboss.mainpage import MainPage
from PageObj.order.BizCommon.ElementPartBase import DealUserCommon,PageCommonPart
from Check.PageCheck import PageAssert
from Base.Mylog import LogManager
from Common.TestAsserts import Assertion as alert
from Check.DataCheck import DataCheck as dc
from Check.RuleCheck import RuleCheckBefore
from Common.function import getDigitFromStr


logger = LogManager('PlatServiceOrder').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

class PlatServiceOrder(Base):
    '''平台业务受理'''
    def open_base(self):
        self.driver.maximize_window()
        #self.driver.implicitly_wait(30)

    def openPlatServiceOrder(self):
        LoginPage(self.driver).login()  # 登录
        # MainPage(self.driver).open_CataMenu('crm9000', 'IBS1000', 'IBS9271',menuPath='page/order.page.pc.person.plat.PlatOrder')  # 进入产品变更页面
        MainPage(self.driver).open_CataMenuNew(funcId='crm9431')
        logger.info('进入平台业务办理页面')

    def backPlatOrderPage(self):
        '''点击回到平台业务受理页面'''
        # loc_backPopup = (By.XPATH,'//*[@id="platOrderAddItem"]/div[1]/div[1]')
        loc_backPopup = (By.XPATH,'//*[@id="CondPart"]/div[1]')
        self.isElementDisplay(loc_backPopup,'click')

    def operPlatOffer(self,offerCode,dealType):
        '''
        平台服务操作(暂停：04，恢复：05，退订：07)
        :param offerCode:
        :param dealType:
        :return:
        '''
        alert().assertTrue(dealType in ['04','05','07'],msg='dealType只能传入04，05和07')
        if '04' == dealType:
            print('{}平台业务暂停操作'.format(offerCode))
        elif '05' ==dealType:
            print('{}平台业务恢复操作'.format(offerCode))
        elif '07' ==dealType:
            print('{}平台业务退订操作'.format(offerCode))
        platOperStr = "//*[contains(@offerid,'%s') and contains(@dealtype,'%s')]" %(offerCode,dealType)
        li_offerOper = (By.XPATH,platOperStr)
        self.isElementDisplay(li_offerOper,'click',delay=1)


    def searchPlatSvcByOfferCode(self,OfferCode):
        '''
        通过OfferCode查询平台服务
        :param OfferCode:平台服务编码OfferCode
        :return:
        '''
        btn_PlatOrderAdd = (By.XPATH,"//li[contains(@ontap,'platOrderAddItem')]")
        self.isElementDisplay(btn_PlatOrderAdd,'click')
        PageAssert(self.driver).wait_for_load()
        self.sleep(1)
        self.isElementDisplay((By.ID,'myplatform_tab_li_2'),'click') #点击全部
        self.isElementDisplay((By.ID,'oper0'),'click') #点击下不限TAB
        self.input((By.ID,'COND'),OfferCode) #输入平台服务编码
        btn_platSvcSearch = (By.XPATH,"//span[contains(@ontap,'platOrderAdd.searchOffer')]")
        self.isElementDisplay(btn_platSvcSearch,'click')
        PageAssert(self.driver).wait_for_load() #加入一个页面等待加载
        btn_subPlatOffer = (By.XPATH,"//*[contains(@ontap,'platOrderAdd.do_subPlatOffer')]")
        self.isElementDisplay(btn_subPlatOffer,'click',delay=2) #点击订购按钮
        self.backPlatOrderPage()#点击回到受理主页面
        PageAssert(self.driver).assert_WadePage()
        return self.checkPlatOrderShow(OfferCode) #返回True或者False  ,

    def acceptSubPlatSvcByOfferCode(self,accessNum,offerCode,scene='AddPlatSvc'):
        '''
        订购OfferCode平台服务
        :param OfferCode:平台服务编码OfferCode
        :return:
        '''
        title = '测试号码_%s订购平台服务测试记录%s' % (accessNum,offerCode)
        self.add_dochead(title)
        self.openPlatServiceOrder()
        self.screen_step("进入平台业务办理菜单")
        DealUserCommon(self.driver).AuthUserInfo(accessNum) #用户鉴权
        self.screen_step("查看平台服务订购列表")
        isSuc = self.searchPlatSvcByOfferCode(offerCode)
        if not isSuc:
            logger.info('平台服务{}未订购成功'.format(offerCode))
        PageCommonPart(self.driver).submit() #点击提交
        submitMsg = PageAssert(self.driver).assertSubmit()
        RuleCheckBefore(self.driver).checkRule(scene) #规则校验
        logger.info('业务受理信息：{}'.format(submitMsg))
        if '业务受理成功' in submitMsg:
            dc().dealMainOrder(getDigitFromStr(submitMsg))
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)
        return submitMsg


    def acceptModPlatSvc(self,accessNum,offerCode,dealType,scene='ModPlatSvc'):
        '''
        OfferCode平台服务相关操作：暂停、恢复、退订
        :param OfferCode:平台服务编码OfferCode
        :param dealType:操作类型
        :return:
        '''
        title = '测试号码_%s平台服务_%s变更测试记录%s' % (accessNum,offerCode,time.strftime('%Y%m%d%H%M%S'))
        self.add_dochead(title)
        self.openPlatServiceOrder()
        self.screen_step("进入平台业务办理菜单")
        DealUserCommon(self.driver).AuthUserInfo(accessNum) #用户鉴权
        self.operPlatOffer(offerCode=offerCode,dealType=dealType) #根据掺入的服务编码和操作类型并点击
        self.screen_step("点击操作类型")
        PageCommonPart(self.driver).submit() #点击提交
        submitMsg = PageAssert(self.driver).assertSubmit()
        RuleCheckBefore(self.driver).checkRule(scene) #规则校验
        logger.info('业务受理信息：{}'.format(submitMsg))
        if '业务受理成功' in submitMsg:
            dc().dealMainOrder(getDigitFromStr(submitMsg))
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)
        return submitMsg



    def checkPlatOrderShow(self,OfferCode):
        '''
        检查选择订购的平台服务是否展示在主页面
        :param OfferCode: 平台服务编码
        :return:返回True或者False，如果在订购列表则返回True,否则返回False
        '''
        platOrderShowStr = "//div[contains(@value,'%s') and contains(@ontap,'platOrderShow.unsubPlatform')]" %OfferCode
        loc_platOrderShowStr = (By.XPATH,platOrderShowStr)
        flag = self.isElementDisplay(loc_platOrderShowStr)
        return flag


if __name__ == '__main__':
    driver = webdriver.Chrome()
    test = PlatServiceOrder(driver)
    # test.acceptSubPlatSvcByOfferCode(accessNum='13787173972',offerCode='99073092')
    test.acceptModPlatSvc(accessNum='13787173972',offerCode='99081371',dealType='07')








