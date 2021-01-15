import time
from Base.base import Base
from selenium.webdriver.common.by import By
from Base import ReadConfig
from Base.Mylog import LogManager
from Check.RuleCheck import RuleCheckBefore
from Check.PageCheck import PageAssert
from Common.TestAsserts import Assertion as Assert
from PageObj.ngboss.mainpage import MainPage
from PageObj.ngboss.login_page import LoginPage
from PageObj.order.BizCommon.ElementPartBase import MainPlanSelectPart as MPS
from PageObj.order.BizCommon.RealNamePart import RealNamePart as RN
from PageObj.order.BizCommon.ElementPartBase import PageCommonPart as PageCommon
from selenium import webdriver
from Check.DataCheck import DataCheck as Dc
from Common.SuiteExec import DealSuiteExec as Dse
from Common.function import getDigitFromStr
from PageObj.order.BizCommon.PayFeePart import PayFeePart as Pay


logger = LogManager('CrtUserPage').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

#================处理个人用户开户界面元素======================#

class CrtUserPage(Base):
    '''个人开户页面'''
    def openCrtUserPage(self):
        LoginPage(self.driver).login()  # 登录
        # MainPage(self.driver).open_CataMenu('crm9000', 'crm9100', 'crmw908',menuPath='order.page.pc.person.createuser.CreateUser')  # 进入集团商品受理
        MainPage(self.driver).open_CataMenuNew(funcId='crm9112')

    def accept_CreateUser(self,accessNum,simId,mainPlanId,elementList,scene='CrtPersonUser'):
        '''
        个人用户开户业务受理
        :param accessNum: 开户手机号码
        :param simId: 开户SIM卡号
        :param mainPlan: 主套餐
        :param elementList:
        :return:
        '''
        title = '用户开户测试%s' % accessNum
        self.add_dochead(title)
        self.openCrtUserPage()  #打开开户菜单
        self.inputSerialNum(accessNum) #输入手机号并校验
        self.inputSim(simId) #输入SIM卡并校验
        self.selProdTypeCode(val='CG01') #默认选择全球通品牌
        RN(self.driver).openUserVerify(accessNum) #开户时按手机号码做实名制校验（在线验证）
        self.input_contactPhone(accessNum) #手工输入联系电话
        self.addMainPlan(mainPlanId=mainPlanId,elementList=elementList) #主套餐选择
        ##做下费用重算
        self.mputeFee() #点击费用重算
        ##设置用户服务密码
        self.addPasswd(password='108109')
        PageCommon(self.driver).submit()
        PageAssert(self.driver).assert_WadePage() #提交后先进行一次Page检查
        Pay(self.driver).confirmPayFee() #处理支付
        submitMsg = PageAssert(self.driver).assertSubmit()
        logger.info('业务受理信息：{}'.format(submitMsg))
        if Assert().verifyassertIn('业务受理成功',submitMsg):
            Dc().dealMainOrder(orderId=getDigitFromStr(submitMsg)) #处理主订单，如果状态是Y或者X 修改成0
        else:
            Dse().upd_RuleChkBySuiteCaseId(suite_case_id=scene, rule_chkmsg=submitMsg)
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)
        return submitMsg


    def inputSerialNum(self,serialNum):
        '''
        输入手机号码并校验
        :param serialNum: 开户手机号码
        :return:
        '''
        textSerialNum = (By.ID,'SERIAL_NUMBER')
        btn_VerifyNum = (By.ID,'SERIAL_NUM_BUTTON')
        self.input(textSerialNum,serialNum)
        self.isElementDisplay(btn_VerifyNum,'click',delay=1)
        PageAssert(self.driver).assert_WadePage()  #校验号码
        self.validSerialNum()  #校验手机号码是否成功

    def inputSim(self,simId):
        '''
        输入SIM卡并校验
        :param simId: 卡号
        :return:
        '''
        textSim = (By.ID,'SIM_CARD_NO')
        btn_VerifySim = (By.ID,'SIM_CHECK_BUTTON')
        self.input(textSim,simId)
        self.isElementDisplay(btn_VerifySim,'click')
        PageAssert(self.driver).assert_WadePage()  #校验号码
        self.validSim()  #校验SIM是否成功

    def validSerialNum(self):
        '''校验手机号码'''
        loc_validResut =(By.XPATH,'//*[@id="SERIAL_NUM_RESULT_BUTTON"]/span[2]')
        validResut = self.get(loc_validResut,Type='text')
        logger.info('校验结果:{}'.format(validResut))
        Assert().assertEqual(validResut,'校验成功',msg='手机号码校验不通过')

    def validSim(self):
        '''校验卡号'''
        loc_validResut =(By.XPATH,'//*[@id="SIM_CHECK_RESULT_BUTTON"]/span[2]')
        validResut = self.get(loc_validResut,Type='text')
        logger.info('校验结果:{}'.format(validResut))
        Assert().assertEqual(validResut,'校验成功',msg='SIM卡校验不通过')


    def selProdTypeCode(self,val='CG01'):
        '''
        选择产品类型
        :param val: 产品类型编码：IMSP-IMS固话,CG03-神州行,CG02-动感地带,CG01-全球通
        :return:
        '''
        list_val = ['IMSP','CG03','CG02','CG01']
        Assert().assertTrue(val in list_val,msg='选择的产品类型不存在，请确认')
        loc_ProdTypeCode = (By.ID,'PRODUCT_TYPE_CODE_span')
        ProdTypeCodeXpathStr = '//*[@id="PRODUCT_TYPE_CODE_float"]/div[2]/div/div/ul/li[contains(@val,"%s")]' % val
        loc_selProdTypeCode = (By.XPATH,ProdTypeCodeXpathStr)
        self.isElementDisplay(loc_ProdTypeCode,'click',delay=1)
        self.isElementDisplay(loc_selProdTypeCode,'click',delay=1)

    def addMainPlan(self,mainPlanId,elementList=[]):
        '''
        新增主套餐
        :param mainPlanId: 主套餐编码
        :param elementList: 服务优惠等元素，默认不选择
        :return:
        '''
        li_productSelectBtn = (By.ID,'productSelectBtn')
        self.isElementDisplay(li_productSelectBtn,'click')#新增主套餐
        PageAssert(self.driver).wait_for_load() #处理下页面加载
        MPS(self.driver).MainProductSel(productId=mainPlanId,elementList=elementList) #选择主套餐

    def mputeFee(self):
        '''费用重算'''
        btn_mputeButton = (By.XPATH,"//*[contains(@id,'mputeButton') and contains(@onclick,'createPersonUser.mputeFee')]")
        self.isElementDisplay(btn_mputeButton,'click')

    def addPasswd(self,password='108109'):
        '''
        新增用户服务密码
        :param password:
        :return:
        '''
        self.isElementDisplay((By.ID,'addNewPasswd'),'click') #点击密码设置按钮
        self.input((By.ID,'NEW_PASSWD'),password)
        self.input((By.ID,'NEW_PASSWD_AGAIN'),password)
        self.isElementDisplay((By.ID,'PassSubmitBtn'),'click',delay=2)
        PageAssert(self.driver).assert_WadePage() #这里暂时先加个校验

    def input_contactPhone(self,phone):
        '''输入联系人'''
        self.input((By.ID,'PHONE'),phone)

if __name__ == '__main__':
    driver = webdriver.Chrome()
    test = CrtUserPage(driver)
    test.accept_CreateUser(scene='CrtPersonUser',accessNum='15974109829',simId='898600071825F4108822',mainPlanId='99913849',elementList=[{"OFFER_CODE":"99650338","OFFER_TYPE":"D"}])








