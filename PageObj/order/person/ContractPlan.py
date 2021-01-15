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
from PageObj.order.BizCommon.ElementPartBase import DealUserCommon
from PageObj.order.BizCommon.ElementPartBase import PageCommonPart as PageCommon
from selenium import webdriver
from Check.DataCheck import DataCheck as Dc
from Common.SuiteExec import DealSuiteExec as Dse
from Common.function import getDigitFromStr
from PageObj.order.BizCommon.PayFeePart import PayFeePart as Pay


logger = LogManager('ContractPlanPage').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

#================处理合约计划受理业务组件======================#

class ContractPlanPage(Base):
    '''合约计划受理'''
    def openContractPlanPage(self):
        LoginPage(self.driver).login()  # 登录
        # MainPage(self.driver).open_CataMenu('crm9000', 'crm9100', 'crmw908',menuPath='order.page.pc.person.createuser.CreateUser')  # 进入集团商品受理
        MainPage(self.driver).open_CataMenuNew(funcId='crm933I')


    def accept_ContractPlan(self,accessNum,IMEI,elementId,contractId='3000元档(比例50%)',contractType='合约计划受理',productType='购机送费',scene='ContractPlanAccept'):
        '''
        个人用户开户业务受理
        :param accessNum: 手机号码
        :param IMEI: IMEI号
        :param contractId: 合约方案
        :param contractType:合约模块
        :param productType:资费方案
        :param elementId:语音产品套餐
                :return:
        '''
        title = '合约计划受理%s' % accessNum
        self.add_dochead(title)
        self.openContractPlanPage()  #打开开户菜单
        authUser = DealUserCommon(self.driver).AuthUserInfo(accessNum) #用户鉴权,包含了用户鉴权都结果和规则校验信息
        # TR().updateRuleCheckInfo(sceneCode=scene,msg=authUser['msg'])
        if not authUser['IsAuthSuc']:
            Dse().upd_RuleChkBySuiteCaseId(suite_case_id=scene,rule_chkmsg=authUser['msg'])
        Assert().assertTrue(authUser['IsAuthSuc'],msg='用户鉴权失败')   #做个鉴权认证
        #选择合约操作
        self.setContractPlan(IMEI=IMEI,contractId=contractId,contractType=contractType,productType=productType)
        #选择语音套餐
        self.VoiceProdSel(elementId)
        self.screen_step('选择合约和语音产品')
        self.sleep(1)
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


    def setContractPlan(self,IMEI,contractId='3000元档(比例50%)',contractType='合约计划受理',productType='购机送费'):
        '''

        :param IMEI:IMei号
        :param contractID:合约方案
        :param contractType:合约模块
        :param productType:资费方案
        :return:
        '''
        self.wadeSelectByTitle(id_locator='CONTRACT_TYPE_SELECT',title=contractType)
        self.sleep(1)
        self.wadeSelectByTitle(id_locator='PRODUCT_TYPE_CODE',title=productType)
        self.sleep(1)
        self.wadeSelectByTitle(id_locator='CONTRACT_ID',title=contractId)
        self.sleep(1)
        self.input((By.ID,'goods_RES_CODE'),IMEI)
        self.vaildImei() #校验IMEI

    def vaildImei(self):
        '''校验IMEI'''
        self.isElementDisplay((By.ID,'checkResButtonName'),'click',delay=1)
        vaildMsg = PageAssert(self.driver).assert_WadePage()
        Assert().assertIn('通过',vaildMsg,msg='终端校验失败，测试终止!')

    def VoiceProdSel(self,elementId):
        '''
        选择语音产品
        :param elementId: 套餐编码
        :return:
        '''
        loc_selectVoice = (By.XPATH,'//*[@id="ContractDetailPart"]//li[contains(@ontap,"VoiceProdSelectPopup")]')
        self.isElementDisplay(loc_selectVoice,'click',delay=2)
        elementSelStr = '//*[@elementid="%s" and contains(@onclick,"elementOnClick(this)") and contains(@id,"%s")]' %(elementId,elementId)
        loc_elementSel= (By.XPATH,elementSelStr)
        self.isElementDisplay(loc_elementSel,'click',delay=1) #选择套餐
        btn_confirm = (By.XPATH,'//*[@id="voiceProdProgram"]//*[contains(@ontap,"pickProducts")]')
        self.isElementDisplay(btn_confirm,'click',delay=2) #点击确认
        PageAssert(self.driver).wait_for_load()
        PageAssert(self.driver).assert_WadePage()


if __name__ == '__main__':
    driver = webdriver.Chrome()
    test = ContractPlanPage(driver)
    # test.acceptChgMainProduct(accessNum='15874139293',productId='99913849',elementList=[{"OFFER_CODE":"99650338","OFFER_TYPE":"D"}]) #必选优惠列表
    # test.acceptAddElements(accessNum='18229967646',elementList=[{"OFFER_CODE":"18013676","OFFER_TYPE":"S"},{"OFFER_CODE":"18009531","OFFER_TYPE":"D"}],scene='AddElements')
    test.accept_ContractPlan(accessNum='15111048902',IMEI='864752031434419',elementId='31535732')

