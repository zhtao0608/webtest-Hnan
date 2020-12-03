import time
from Base.base import Base
from selenium.webdriver.common.by import By
from Base import ReadConfig
from Base.Mylog import LogManager
from Check.RuleCheck import RuleCheckBefore
from Check.PageCheck import PageAssert
from Common.TestAsserts import Assertion


rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('MainPlanSelectPart').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

#================处理页面元素公共类，包含主套餐、服务、优惠、平台服务等======================#

class MainPlanSelectPart(Base):
    '''选择主套餐组件'''
    def searchMainPlan(self,productId):
        '''
        查询主套套餐
        :param productId: 主套餐编码
        :return:
        '''
        text_productSearch = (By.ID,'productSelectPRODUCT_SEARCH_TEXT')
        self.element_sendkey_enter(text_productSearch,productId) #输入产品编码按回车查询
        # time.sleep(2)
        PageAssert(self.driver).pageLoading()
        SubproductStr = "//button[contains(@productid,'%s') and contains(@ontap,'productSelect.selectProduct')]" %productId
        btn_Subproduct = (By.XPATH,SubproductStr)  #订购按钮
        self.isElementDisplay(btn_Subproduct,'click') #点击主套餐订购
        PageAssert(self.driver).pageLoading()


    def selectProductItem(self,elementList=[]):
        '''
        组选择
        :param elementList:可选组内元素 字典数组包含元素类型和元素编码
        eg :elementList =  [{"OFFER_TYPE":"D","OFFER_CODE":"99410190"},{"OFFER_TYPE":"D","OFFER_CODE":"2285"}]
        :return:
        '''
        for i in range(len(elementList)):
            elementId = elementList[i]['OFFER_CODE']
            elementType = elementList[i]['OFFER_TYPE']
            if not isinstance(elementId,str):
                elementId = str(elementId)
            selectElementStr = "//*[contains(@offercode,'%s') and contains(@offertype,'%s') and contains(@type,'checkbox')]" %(elementId,elementType)
            checkBox_selectElement = (By.XPATH,selectElementStr)
            self.isSelected(checkBox_selectElement,Type='click') # 选中要订购的元素（资费、服务）
        btn_confirmSelect = (By.XPATH,"//button[contains(@ontap,'productSelect.confirmAction')]")
        self.isElementDisplay(btn_confirmSelect,'click')
        PageAssert(self.driver).pageLoading()
        PageAssert(self.driver).assert_WadePage() #做个校验


    def MainProductSel(self,productId,elementList=[]):
        '''
        个人业务主产品选择
        :param productId: 主产品编码
        :param elementList: 可选组内选择的优惠或者服务列表
        :return:
        '''
        # btn_productSelect = (By.ID,'productSelectBtn')
        # self.isElementDisplay(btn_productSelect,'click') #点击选择套餐按钮
        self.searchMainPlan(productId)  #进入选择套餐界面搜索主产品
        self.selectProductItem(elementList) #进入组选择，选择可选资费或者服务
        return self.driver

class DealUserCommon(Base):
    '''用户信息处理类【公共】'''
    def AuthUserInfo(self,accessNum):
        '''用户鉴权'''
        text_SerialNum = (By.ID,'AUTH_SERIAL_NUMBER')
        self.element_sendkey_enter(text_SerialNum,accessNum)
        time.sleep(3)
        # busiVerify = RuleCheckBefore(self.driver).checkRule()
        busiVerify = RuleCheckBefore(self.driver).checkRule()
        print(type(busiVerify))
        # logger.info('业务校验检查结果：'.format(busiVerify))
        print('=============业务校验检查结果:' + busiVerify)
        PageAssert(self.driver).dealDialogPage() #关闭营销推荐
        loc_CustInfoViewPart = (By.ID,'CustInfoViewPart')
        flag = self.isElementDisplay(loc_CustInfoViewPart)
        print(flag)
        # Assertion().verifyassertTrue(flag,message='用户鉴权失败，终止测试')
        Assertion().assertTrue(flag,msg='用户鉴权失败，终止测试')


class SelectElements(Base):
    '''页面元素处理公共类'''
    def getElementListTab(self,idx='2'):
        '''
        点击页面元素大类页签
        :param idx: 0-推荐，1-服务，2-优惠 ，3-平台服务 4-收藏 （默认优惠）
        :return:
        '''
        inxStr = "elementListmyTab_tab_li_%s" %idx
        loc_ElementListTab = (By.ID,inxStr)
        self.isElementDisplay(loc_ElementListTab,'click')
        return self.driver

    def searchElementByCode(self,offerCode):
        '''
        根河Offer_code搜索元素
        :param offerCode: 元素编码 offer_code，资费/服务/平台服务等
        :return:
        '''
        text_elementSearch = (By.ID,'elementListELEM_SEARCH_TEXT')
        self.element_sendkey_enter(text_elementSearch,offerCode)
        return self.driver

    def backAcceptPage(self):
        loc_backPopup = (By.XPATH,"//*[contains(@ontap,'elementList.backPopup(this)')]")
        self.isElementDisplay(loc_backPopup,'click')


    def addElements(self,elementList=[]):
        '''
        传入elementList包含改笔订单要订购资费或者服务以及类型
        :param elementList: 字典数组，包含 OFFER_CODE 和 Offer_type 2个key
        eg :
        [{"OFFER_CODE":"120000008174","OFFER_TYPE":"S"},{"OFFER_CODE":"120010122813","OFFER_TYPE":"D"}]
        :return:
        '''
        for i in range(len(elementList)):
            offerCode = elementList[i]['OFFER_CODE']
            offerType = elementList[i]['OFFER_TYPE']
            if not isinstance(offerCode,str):
                offerType = str(offerCode)
            logger.info('要新增的元素类型：%s'.format(offerType))
            logger.info('要新增的元素编码：%s'.format(offerCode))
            self.searchElementByCode(offerCode)
            btnAddElementStr = "//button[contains(@onclick,'elementList.order') and contains(@offertype,'%s') and contains(@offercode,'%s')]" %(offerType,offerCode)
            Btn_AddElement = (By.XPATH,btnAddElementStr)
            self.isElementDisplay(Btn_AddElement,'click')
        self.backAcceptPage()  #回到受理主页面


    def delElements(self, elementList):
        '''
        传入elementList包含改笔订单要删除资费或者服务以及类型
        :param elementList:
        字典数组，包含 OFFER_CODE 和 Offer_type 2个key
        eg :        [{"OFFER_CODE":"120000008174","OFFER_TYPE":"S"},{"OFFER_CODE":"120010122813","OFFER_TYPE":"D"}]
        :return:
        '''
        for i in range(len(elementList)):
            offerCode = elementList[i]['OFFER_CODE']
            offerType = elementList[i]['OFFER_CODE']
            if not isinstance(offerCode,str):
                offerType = str(offerCode)
            logger.info('要新增的元素类型：%s'.format(offerType))
            logger.info('要新增的元素编码：%s'.format(offerCode))
            checkBoxDelElementStr = "//button[contains(@onclick,'selectedElements.checkBoxAction') and contains(@value,'%s')]" %offerCode
            checkBox_DelElement = (By.XPATH,checkBoxDelElementStr)
            self.isSelected(checkBox_DelElement,'click')

    # def chgMainProduct(self,productId,elementList):
    #     '''
    #     传入主产品和可选组元素列表，订购
    #     :param productId:主产品编码
    #     :param elementList:字典数组，包含 OFFER_CODE 和 Offer_type 2个key
    #     eg :[{"OFFER_CODE":"120000008174","OFFER_TYPE":"S"},{"OFFER_CODE":"120010122813","OFFER_TYPE":"D"}]
    #     :return:
    #     '''
    #     MainPlanSelectPart(self.driver).MainProductSel(productId,elementList)

class PageCommonPart(Base):
    '''页面公共组件'''
    def submit(self):
        '''公共提交按钮'''
        Btn_submit = (By.ID,'CSSUBMIT_BUTTON')
        if not PageAssert(self.driver).pageLoading():
            self.isElementDisplay(Btn_submit,'click')

class SaleActivePart(Base):
    '''营销活动办理组件'''
    def selActivePop(self):
        '''选择组件'''
        li_selActivePop =(By.XPATH,"//*[contains(@ontap,'SaleActiveMain.selectProductPopupAction')]")
        self.isElementDisplay(li_selActivePop,'click')
        time.sleep(1)

    def searchSaleActive(self,offerCode):
        '''
        通过OfferCode直接搜索营销活动
        :param offerCode: OfferType = 'K' 的营销活动包
        :return:
        '''
        text_searchContent = (By.ID,'searchContent')
        btn_search = (By.XPATH,"//*[contains(@ontap,'SaleActivePackageSelect.query')]")
        if (PageAssert(self.driver).pageLoading()):
            self.sendkey(text_searchContent,offerCode)
            self.isElementDisplay(btn_search,'click')
            time.sleep(1)

    def checkSaleActiveExists(self,OfferCode):
        '''检查是否传入的营销活动是否存在'''
        loc_PackageList = (By.XPATH,'//*[@id="PackageListPart"]/div/ul/li[1]/div/div')
        packgeId = self.get(loc_PackageList,Type='text')
        logger.info('查询结果列表展示的营销包:' + packgeId)
        Assertion().assertIsNotNone(packgeId,msg='营销包不存在，终止执行！')   #先断言一下，如果不存在则直接终止测试
        return self.is_value_in_text(loc_PackageList,OfferCode)

    def selectActive(self,OfferCode):
        '''
        检查是否传入的营销活动是否存在,存在则选择营销活动
        :param OfferCode: 营销活动编码
        :return:
        '''
        if self.checkSaleActiveExists(OfferCode):
            li_selectPackage = (By.XPATH,"//li[contains(@ontap,'SaleActivePackageSelect.selectPackageAction')]")
            self.isElementDisplay(li_selectPackage,'click')
        else:
            logger.info('营销包不存在或者选择异常，终止！')






