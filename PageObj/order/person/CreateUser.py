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
from PageObj.order.BizCommon.ElementPartBase import SelectElements as SelEle
from PageObj.order.BizCommon.RealNamePart import RealNamePart as RN
from PageObj.order.BizCommon.ElementPartBase import PageCommonPart as PageCommon
from selenium import webdriver


rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('CrtUserPage').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

#================处理个人用户开户界面元素======================#

class CrtUserPage(Base):
    '''个人开户页面'''
    def openCrtUserPage(self):
        LoginPage(self.driver).login()  # 登录
        MainPage(self.driver).open_CataMenu('crm9000', 'crm9100', 'crmw908',menuPath='order.page.pc.person.createuser.CreateUser')  # 进入集团商品受理


    def accept_CreateUser(self,accessNum,simId,mainPlanId,elementList,scene=''):
        '''
        个人用户开户业务受理
        :param accessNum: 开户手机号码
        :param simId: 开户SIM卡号
        :param mainPlan: 主套餐
        :param elementList:
        :return:
        '''
        self.openCrtUserPage()  #打开开户菜单
        self.inputSerialNum(accessNum) #输入手机号并校验
        self.inputSim(simId) #输入SIM卡并校验
        RN(self.driver).openUserVerify(accessNum) #开户时按手机号码做实名制校验（在线验证）
        self.addMainPlan(mainPlanId=mainPlanId,elementList=elementList) #主套餐选择
        PageCommon(self.driver).submit()
        RuleCheckBefore(self.driver).checkRule(scene)
        submitMsg = PageAssert(self.driver).assert_Submit()
        logger.info('业务受理信息：{}'.format(submitMsg))
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))


    def inputSerialNum(self,serialNum):
        '''
        输入手机号码并校验
        :param serialNum: 开户手机号码
        :return:
        '''
        textSerialNum = (By.ID,'SERIAL_NUMBER')
        btn_VerifyNum = (By.ID,'SERIAL_NUM_BUTTON')
        self.sendkey(textSerialNum,serialNum)
        self.isElementDisplay(btn_VerifyNum,'click')
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
        self.sendkey(textSim,simId)
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


    def addMainPlan(self,mainPlanId,elementList=[]):
        '''
        新增主套餐
        :param mainPlanId: 主套餐编码
        :param elementList: 服务优惠等元素，默认不选择
        :return:
        '''
        li_productSelectBtn = (By.ID,'productSelectBtn')
        self.isElementDisplay(li_productSelectBtn,'click')#新增主套餐
        PageAssert(self.driver).pageLoading() #处理下页面加载
        MPS(self.driver).MainProductSel(productId=mainPlanId,elementList=elementList) #选择主套餐



if __name__ == '__main__':
    driver = webdriver.Chrome()
    test = CrtUserPage(driver)
    test.accept_CreateUser(scene='CrtPersonUser',accessNum='19509753849',simId='898600E9281891603748',mainPlanId='99110071',elementList=[])








