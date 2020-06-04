import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from Common import ReadConfig
from Common.Mylog import LogManager
from PageObj.oc.group.GroupBasePage import BasePage
from Common.Assert import PageAssert
from Common.OperExcel import write_excel_append
# logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
rc = ReadConfig.ReadConfig("ngboss_config.ini")

class EcCampnOper(BasePage):
    def open_base(self):
        # self.driver = webdriver.Chrome()
        # self.driver.get(config_url())
        self.driver.get(rc.get_ngboss('url'))
        self.driver.maximize_window()
        #self.driver.implicitly_wait(30)

    def Open_GrpEcCampnOperframe(self):
        '''进入集团营销活动受理iFrame处理'''
        self.driver.switch_to.default_content()
        loc_frame = self.find((By.XPATH,"//iframe[contains(@src,'/ordercentre/ordercentre?service=page/oc.enterprise.cs.EcCampnOper')]"))
        self.driver.switch_to.frame(loc_frame)
        logger.info("进入集团营销活动受理:" + str(loc_frame))
        time.sleep(5)
        Btn_msg = self.find((By.CSS_SELECTOR,'#UI-step1 > div > div.fn > button:nth-child(1)'))
        Btn_msg.click()
        return self.driver

    def choose_EcCampnOffer(self,CampnOfferId,OfferKey,prePrice,AcctId,month):
        '''选择集团营销活动'''
        li_selectCampnOffer = (By.ID,'CAMPN_ID_span') #活动
        xpath_CampnOfferstr = '//*[@id="CAMPN_ID_list_ul"]/li[contains(@val,"%s")]' % CampnOfferId  #选择活动
        loc_CampnOffer = (By.XPATH,xpath_CampnOfferstr)
        '''选择集团营销活动'''
        self.find_element_click(li_selectCampnOffer)
        time.sleep(2)
        self.find_element_click(loc_CampnOffer)
        time.sleep(1)
        '''选择营销活动下对应的商品'''
        li_selectOfferKey = (By.ID,'OFFER_KEY_span') #商品
        xpath_OfferKeystr = '//*[@id="OFFER_KEY_list_ul"]/li[contains(@val,"%s")]' % OfferKey   #选择商品
        loc_OfferKey = (By.XPATH,xpath_OfferKeystr)
        self.find_element_click(li_selectOfferKey)
        time.sleep(1)
        self.find_element_click(loc_OfferKey)
        time.sleep(1)
        '''设置预存金额'''
        text_price = (By.ID,'PRICE_0')  #预存金额
        self.sendkey(text_price,prePrice) # 输入预存金额
        '''选择合约期'''
        li_selectValidPeriod = (By.ID,'VALID_PERIOD_span')  #合约期
        xpath_ValidPeriodStr = '//*[@id="VALID_PERIOD_list_ul"]/li[contains(@val,"%s")]' % month  #选择合约期
        loc_ValidPeriod = (By.XPATH,xpath_ValidPeriodStr)
        self.find_element_click(li_selectValidPeriod)
        time.sleep(1)
        self.find_element_click(loc_ValidPeriod)
        time.sleep(1)
        '''选择存入方式'''
        li_selectInfoWay = (By.ID,'INTO_WAY_span')  #话费存入方式
        loc_InfoWayAcct = (By.XPATH,'//*[@id="INTO_WAY_list_ul"]/li[contains(@val,"ACCT_ID")]') # 话费存入账户
        loc_InfoWayAccess = (By.XPATH,'//*[@id="INTO_WAY_list_ul"]/li[contains(@val,"ACCESS_NUM")]') # 话费存入计费号
        self.find_element_click(li_selectInfoWay)
        time.sleep(1)
        self.find_element_click(loc_InfoWayAcct)  #选择话费存入方式
        time.sleep(1)
        '''选择话费存入账户'''
        li_selectAcctId = (By.ID,'ACCT_ID_span')   #存入账户
        xpath_acctIdStr = '//*[@id="ACCT_ID_list_ul"]/li[contains(@val,"%s")]' % AcctId
        loc_AcctId = (By.XPATH,xpath_acctIdStr)
        self.find_element_click(li_selectAcctId)
        time.sleep(1)
        self.find_element_click(loc_AcctId)  #选择存入账户ID
        time.sleep(1)
        '''处理合同附件,直接通过js去除nullable 属性，提交时可以不用校验'''
        loc_contractId = (By.ID,'CONTRACT_ID_name') #合同附件
        loc_browseCampn_approver = (By.CSS_SELECTOR,'#commonPart > ul > li:nth-child(8) > div.value > span > span:nth-child(1) > span') #活动办理审批要件上传按钮
        loc_browseContractId = (By.CSS_SELECTOR,'#commonPart > ul > li:nth-child(9) > div.value > span > span:nth-child(1) > span') #合同附件上传
        # self.js_removeNullable(idElement ='CONTRACT_ID')  #删除合同附件必填属性
        # self.js_removeNullable(idElement ='CAMPN_APPROVER') #活动办理审批要件删除必填
        self.uploadFile(locator=loc_browseCampn_approver,filename=r"F:\Downloads\EC_GROUPVALUE_IMPORT.xls")
        self.uploadFile(locator=loc_browseContractId,filename=r"F:\Downloads\EC_GROUPVALUE_IMPORT.xls")

    def accept_SubEcCampn(self,groupId,CampnOfferId,OfferKey,prePrice,AcctId,month):
        '''订购集团营销活动'''
        title = '新增集团营销活动受理测试记录'
        self.add_dochead(title)
        self.Open_groupMenu(groupId,'crm8500','crm8097') #点击进入菜单 ,父菜单>子菜单
        self.Open_GrpEcCampnOperframe()  # 进入集团订购iframe
        self.screen_step('进入集团营销活动受理')
        self.choose_EcCampnOffer(CampnOfferId,OfferKey,prePrice,AcctId,month)
        self.screen_step('选择营销活动并设置')
        time.sleep(5)
        self.find_element_click((By.ID,'submitButton')) #点击提交
        time.sleep(2)
        self.sendEnter() #确认
        time.sleep(5)
        submitMsg = PageAssert(self.driver).assert_Submit()  #提交后返回信息，flowId或者报错
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)

if __name__ == '__main__':
    print("用例开始执行时间：" + time.strftime("%Y%m%d%H%M%S"))
    driver = webdriver.Chrome()
    test = EcCampnOper(driver)
    # test.accept_chgPayRela(AccessNum ='18725337983',operCode='1',SerialNum='18787295285')
    test.accept_SubEcCampn(groupId='8713160704',CampnOfferId='20170221',OfferKey='1000031238',prePrice='30000',
                           AcctId='7195110200755922',month='3')

    # driver.close()
    print("用例执行结束时间：" + time.strftime("%Y%m%d%H%M%S"))

