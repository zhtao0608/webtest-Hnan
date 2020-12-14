import time
from Base.base import Base
from selenium.webdriver.common.by import By
from Base import ReadConfig
from selenium import webdriver
from PageObj.ngboss.login_page import LoginPage
from PageObj.ngboss.mainpage import MainPage
from Base.Mylog import LogManager
from Check.PageCheck import PageAssert
from Check.RuleCheck import RuleCheckBefore

rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('MainPage').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )


class GroupBusiBase(Base):
    '''
    该类主要处理集团业务的6大类操作方式
    集团产品订购 CrtUs
    集团产品变更 ChgUs
    集团产品注销 DstUs
    集团成员订购 CrtMb
    集团成员变更 ChgMb
    集团成员注销 DstMb
    '''

    def GroupQryPart(self,groupId):
        ''' 集团查询组件-根据集团编码查询按Enter进入'''
        loc_GroupId = (By.ID,'cond_GROUP_ID_INPUT')
        self.element_sendkey_enter(loc_GroupId,groupId)

    def Qry_GroupCustInfoBySerialNum(self,accessNum):
        '''按集团服务号码查询集团客户信息
        :param SerialNum: 集团服务号码
        '''
        Btn_showCustInfo = (By.XPATH,"//button[contains(@ontap,'showGrpCustDialog')]")
        self.isElementDisplay(Btn_showCustInfo,'click')
        loc_selMode = (By.ID,'cond_GROUP_MODE_span') #选择查询方式
        self.isElementDisplay(loc_selMode,'click') #点击
        Loc_selByNumber = (By.XPATH,'//*[@id="cond_GROUP_MODE_float"]/div[2]/div/div/ul/li[3]') #按服务号码
        self.isElementDisplay(Loc_selByNumber,'click')
        self.sendkey((By.ID,'cond_GROUP_ID_INPUT'),accessNum) #输入集团服务服务号码
        Btn_showGroupUser = (By.XPATH,"//button[contains(@ontap,'queryGroupUserInfo')]")
        self.isElementDisplay(Btn_showGroupUser,'click')
        loc_TabGroupUserInfo = (By.XPATH,'//*[@id="groupUserTable"]/div[1]/div/table/tbody/tr')
        self.isElementDisplay(loc_TabGroupUserInfo,'click') #选择集团用户信息，点击选中
        time.sleep(2)

    '''集团商品选择组件'''
    def SelOfferTypePart(self,brandCode):
        # loc_offerSelectBox = (By.XPATH,'//*[@id="offerSelectBox"]/button')
        # self.isElementDisplay(loc_offerSelectBox,'click')
        self.selectGroupOffer()
        time.sleep(2)
        self.OfferCata()
        self.OfferTypePart(brandCode)
        return self.driver

    '''选择商品'''
    def initOfferCategoryPopup(self):
        loc_initOfferCata = (By.XPATH,"//li[contains(@ontap,'initOfferCategoryPopup')]")
        self.isElementDisplay(loc_initOfferCata,'click')
        return self.driver

    def selectGroupOffer(self):
        loc_offerSelectBox = (By.XPATH,'//*[@id="offerSelectBox"]/button')
        self.isElementDisplay(loc_offerSelectBox,'click')
        return self.driver

    '''搜索集团商品组件'''
    def searchGroupOffer(self,offerId):
        '''
        集团商品受理主页面按传入的商品编码搜索集团商品信息
        :param offerId:集团商品编码
        :return:
        '''
        text_searchOffer = (By.ID,'mainProductSearch_searchText')
        li_searchOfferResult = (By.XPATH,'//*[@id="mainProductSearch_searchResult"]/li')
        self.element_sendkey_click(text_searchOffer,offerId)
        self.isElementDisplay(li_searchOfferResult,'click')
        time.sleep(3)


    '''目录-可订购'''
    def OfferCata(self):
        loc_OfferCata = (By.ID,'myTab_tab_li_0')
        self.isElementDisplay(loc_OfferCata,'click')
        return self.driver

    '''目录-已订购商品'''
    def OfferSubCata(self):
        loc_OfferSub = (By.ID,'myTab_tab_li_1')
        self.isElementDisplay(loc_OfferSub,'click')
        return self.driver

    def OfferTypePart(self,brandCode):
        '''
        根据商品品牌选择商品大类
        :param brandCode:
        :return:
        '''
        link_OfferType = (By.ID,brandCode)
        self.isElementDisplay(link_OfferType,'click')
        time.sleep(2)
        return self.driver

    '''集团商品订购按钮'''
    def SubGrpOffer(self,offerCode):
        '''
        :param offerCode: 集团商品编码
        :return:
        '''
        OfferCodeStr =  "//button[contains(@offer_code,'%s') and contains(@ontap,'CrtUs')]" %offerCode   #传入集团编码并通过Xpath定位
        loc_subOfferCode = (By.XPATH,OfferCodeStr)
        self.isElementDisplay(loc_subOfferCode,'click')
        PageAssert(self.driver).pageLoading()

    '''集团商品变更按钮'''
    def ChgGrpOfferCode(self,offerCode,userId):
        '''
        :param userId: 传入集团用户标识，查询已订购商品
        offerCode:集团产品编码
        :return:
        '''
        ChgOfferCodeStr =  "//button[contains(@offer_code,'%s') and contains(@user_id,'%s') contains(@ontap,'ChgUs')]" %(offerCode,userId) #传入集团编码并通过Xpath定位
        loc_chgOfferCode = (By.XPATH,ChgOfferCodeStr)
        self.isElementDisplay(loc_chgOfferCode,'click')
        PageAssert(self.driver).pageLoading()
        return self.driver

    '''集团商品注销按钮'''
    def DstGrpOfferCode(self,offerCode,userId):
        '''
        :param offerCode:
        :param userId:
        :return:
        '''
        DstOfferCodeStr =  "//button[contains(@offer_code,'%s') and contains(@user_id,'%s') and contains(@ontap,'DstUs')]" %(offerCode,userId) #传入集团编码并通过Xpath定位
        loc_dstOfferCode = (By.XPATH,DstOfferCodeStr)
        self.isElementDisplay(loc_dstOfferCode,'click')
        PageAssert(self.driver).pageLoading()
        RuleCheckBefore(self.driver).checkRule()
        return self.driver

    def DstGrpOfferCodeNew(self,offerCode):
        '''
        只传入Offercode去找对应的集团已订购商品
        :param offerCode:
        :return:
        '''
        DstOfferCodeStr =  "//button[contains(@offer_code,'%s')  and contains(@ontap,'DstUs')]" %(offerCode) #传入集团编码并通过Xpath定位
        loc_dstOfferCode = (By.XPATH,DstOfferCodeStr)
        self.isElementDisplay(loc_dstOfferCode,'click')
        PageAssert(self.driver).pageLoading()
        RuleCheckBefore(self.driver).checkRule()
        return self.driver

    '''成员商品订购按钮'''
    def SubMebOffer(self,grpUserId):
        '''根据集团用户标识获取成员可订购产品
        :param grpUserId: 传入集团用户标识
        :return:
        '''
        # self.subOfferCata() #先点击可订购商品
        self.OfferCata()
        subMebOfferCodeStr =  "//button[contains(@value,'%s') and contains(@ontap,'CrtMb')]" %grpUserId #传入集团编码并通过Xpath定位
        loc_subMebOfferCode = (By.XPATH,subMebOfferCodeStr)
        self.isElementDisplay(loc_subMebOfferCode,'click')
        PageAssert(self.driver).pageLoading()
        return self.driver

    '''成员商品变更按钮'''
    def ChgMebOffer(self,grpUserId):
        chgMebOfferCodeStr =  "//button[contains(@value,'%s') and contains(@ontap,'ChgMb')]" %grpUserId #传入集团编码并通过Xpath定位
        loc_chgMebOfferCode = (By.XPATH,chgMebOfferCodeStr)
        self.isElementDisplay(loc_chgMebOfferCode,'click')
        RuleCheckBefore(self.driver).checkRule()
        return self.driver

    '''成员商品注销按钮'''
    def DstMebOffer(self,grpUserId):
        '''
        :param grpUserId: 传入集团用户标识
        :return:
        '''
        dstMebOfferCodeStr = "//button[contains(@value,'%s') and contains(@ontap,'DstMb')]" % grpUserId  # 传入集团编码并通过Xpath定位
        loc_dstMebOfferCode = (By.XPATH,dstMebOfferCodeStr)
        self.isElementDisplay(loc_dstMebOfferCode, 'click')
        RuleCheckBefore(self.driver).checkRule()
        return self.driver


if __name__ == '__main__':
    driver = webdriver.Chrome()
    test = MainPage(driver)
    test.open_base()
    LoginPage(driver).login(rc.get_ngboss('username'),rc.get_ngboss('password'))  #登录
    test.open_CataMenu('crm8000','crm8200','crm8207',menuPath='order.page.pc.enterprise.operenterprisesubscriber.OperEnterpriseSubscriber') #集团商品受理
    # test.open_CataMenu('crm8000','crm8200','crm8206',menuPath='order.page.pc.enterprise.operenterprisemember')#成员商品受理


    # GroupBusiAcceptTestBase(driver).OfferCata()
    # driver.close()