import time
from Base.base import Base
from selenium.webdriver.common.by import By
from Base import ReadConfig
from Base.Mylog import LogManager
from Check.RuleCheck import RuleCheckBefore

rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('DealMebElements').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )


class DealMebElements(Base):
    '''处理成员商品受理页面元素'''

    def QryMebInfo(self,mebSerialNum):
        '''
        传入成员服务号码，查询成员用户信息
        :param mebSerialNum:成员服务号码
        :return:
        '''
        text_MebAccessNum = (By.ID,'cond_SERIAL_NUMBER_INPUT')
        self.element_sendkey_enter(text_MebAccessNum,mebSerialNum)
        time.sleep(1)


    def selMebPayPlan(self,planType='P',itemId='42701'):
        '''
        选择成员付费方式
        :param planType:传入G表示集团付费，传入P表示个人付费
        :return:
        '''
        MebPayPlanTypeStr = '//*[@id="PAY_PLAN_SEL_PLAN_TYPE_span"]/span[contains(@val,"%s")]' % planType
        btn_SelMebPayPlanType = (By.XPATH,MebPayPlanTypeStr)
        if planType == 'G':    #如果选择的是集团付费才进入，否则不进入
            self.isElementDisplay(btn_SelMebPayPlanType,'click')
            time.sleep(1)
            self.setMebGrpPayItem(itemId)
            time.sleep(1)

    def setGrpMebPayRela(self,planType='G',itemId='42701'):
        '''
        选择集团付费
        :param planType:传入G表示集团付费，
        :return:
        '''
        if planType == 'G':    #如果选择的是集团付费才进入，否则不进入
            self.setMebGrpPayItem(itemId)
            time.sleep(1)

    def setMebGrpPayItem(self,itemId):
        '''
        设置集团代付付费关系
        :param itemId: 帐务代付帐目,默认42701套餐及固定费
            42701	套餐及固定费
            42702	套餐外语音费
            42703	套餐外上网费
            42704	套餐外短彩信费
            42705	增值业务费
            42706	代收费
            42707	代他人付费,承诺消费补差,多业务组合优惠
        :return:
        '''
        loc_PayPlanAcctInfo = (By.XPATH,'//*[contains(@ontap,"selectPayPlanAcctInfo")]')
        self.isElementDisplay(loc_PayPlanAcctInfo,'click') #点击付费账目
        time.sleep(2)
        PayItemStr = "//input[contains(@id,'noteItems') and contains(@value,'%s')]" % itemId
        loc_PayItem = (By.XPATH,PayItemStr)
        self.isElementDisplay(loc_PayItem,'click')
        btn_confirmPayItem = (By.XPATH,"//button[contains(@ontap,'validateAccount')]")
        self.isElementDisplay(btn_confirmPayItem,'click')


    def OpenSubmitGrpMebOffer(self):
        '''成员商品受理-订购提交'''
        btn_commitGrpMebOffer = (By.XPATH,'//*[@id="OpenSubmit"]/button[contains(@ontap,"submitAll")]')
        self.isElementDisplay(btn_commitGrpMebOffer,'click')


    def ChgSubmitGrpMebOffer(self):
        '''成员商品受理-变更提交'''
        btn_commitGrpMebOffer = (By.XPATH,'//*[@id="ChgSubmit"]/button[contains(@ontap,"submitAll")]')
        self.isElementDisplay(btn_commitGrpMebOffer,'click')


    def DelSubmitGrpMebOffer(self):
        '''成员商品受理-变更提交'''
        btn_commitGrpMebOffer = (By.XPATH,'//*[@id="DelSubmit"]/button[contains(@ontap,"submitAll")]')
        self.isElementDisplay(btn_commitGrpMebOffer,'click')


    def InputDstMbRemark(self):
        '''成员注销时填写备注'''
        text_DstMbRemark = (By.ID,'cond_REMARK')
        self.sendkey(text_DstMbRemark,'自动化测试')
        return self.driver

    def CrtMebshortNum(self,serialNum):
        '''
        根据传入的手机号码生成短号
        :param serialNum:手机号码
        :return:
        '''
        return '61' + serialNum[-4:]  #手机号码截取后四位

    def verifyShortNum(self):
        '''校验短号'''
        btn_vaildShortNum = (By.XPATH,'//button[contains(@onclick,"validateShortNum") and contains(@id,"validButton")]')
        self.isElementDisplay(btn_vaildShortNum,'click')
        RuleCheckBefore(self.driver).checkRule()

    def submitMebOfferAttr(self,offerCode):
        '''商品特征设置页面点击确认'''
        loc_confirmGroupAttr = (By.XPATH,"//button[contains(@ontap,'checkSub')]")
        loc_submitGroupDeskTelAttr = (By.XPATH,"//button[contains(@ontap,'validateParamPage')]") #桌面电话特殊
        loc_submitCntxVpmnAttr = (By.ID,'sumbitTrue') #融合VPMN
        if '8001' == offerCode:
            self.isElementDisplay(loc_submitCntxVpmnAttr,'click')
        else:
            self.isElementDisplay(loc_confirmGroupAttr,'click')



