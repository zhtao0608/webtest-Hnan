import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from Base import ReadConfig
from PageObj.ngboss.mainpage import MainPage
from PageObj.ngboss.login_page import LoginPage
from Base.Mylog import LogManager
from Common.Assert import PageAssert
from PageObj.oc.person.PersonBase import PersonBase
from Base.GenTestData import GenTestData

logger = LogManager('test').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
rc = ReadConfig.ReadConfig("ngboss_config.ini")

class SubscriberOpen(PersonBase):
    '''个人用户开户'''
    def open_base(self):
        self.driver.get(rc.get_ngboss('url'))
        self.driver.maximize_window()

    def Open_subscriberOpen(self):
        self.open_base()
        LoginPage(self.driver).login(rc.get_ngboss('username'), rc.get_ngboss('password'))  # 登录
        main = MainPage(self.driver)
        main.open_OcCataMenu('crm9000','crm9100')
        self.screen_step('打开个人业务-开户业务')
        main.Open_menu('crm9130')
        time.sleep(10)
        self.open_SubscriberOpenFrame()  # 进入个人用户开户iframe
        self.screen_step('进入个人用户开户菜单')

    def open_SubscriberOpenFrame(self):
        self.driver.switch_to.default_content() #记得一定要回到主窗口后再找iframe
        loc_frame = (By.XPATH,"//iframe[contains(@src,'/ordercentre/ordercentre?service=page/oc.person.cs.SubscriberOpen')]")
        # 切换到个人用户开户主frame
        self.iframe(loc_frame)
        logger.info("进入个人用户开户frame:" + str(loc_frame))
        print("个人用户开户:" + str(loc_frame))
        Btn_msg = (By.CSS_SELECTOR,'#UI-step1 > div > div.fn > button:nth-child(1)')
        self.isElementDisplay(Btn_msg,'click') #出现步骤引导弹窗，直接关闭
        time.sleep(5)
        return self.driver

    def set_customerInfo(self,accessNum):
        '''新增客户信息，手工输入'''
        loc_edit = (By.ID,'editInfoButton') #手工输入按钮
        loc_PARTYNAME = (By.ID,'PARTY_NAME') #客户名称
        # loc_birthdate = (By.ID,'BIRTH_DATE') # 出生日期
        loc_IDENADDRESS = (By.ID,'IDEN_ADDRESS') #证件地址
        loc_CONTNUMBER = (By.ID,'CONT_NUMBER') #联系电话
        loc_ACCESSNUM = (By.ID,'ACCESS_NUM') #服务号码
        self.isElementDisplay(loc_edit,'click')
        # self.sendkey(loc_IDENNR,idennr)
        idennr = GenTestData().Create_Idcard() #自动生成一个证件号码
        logger.info('个人开户证件号码:{}'.format(idennr))
        self.Input_validIdenNrNew() # 输入证件并校验
        partyname = GenTestData().create_CustName() #自动生成一个客户名称
        logger.info('个人开户客户姓名:{}'.format(partyname))
        self.sendkey(loc_PARTYNAME,partyname)
        # self.sendkey(loc_birthdate,birthdate) #证件校验通过后自动填写
        idenaddress = '云南昆明开户自动化测试地址'
        self.sendkey(loc_IDENADDRESS,idenaddress)
        contnumber = GenTestData().create_phone() #自动生成一个联系人电话
        self.sendkey(loc_CONTNUMBER,contnumber)
        self.sendkey(loc_ACCESSNUM,accessNum)
        self.move_element_enter(loc_ACCESSNUM)  #移动到该元素按Enter键校验
        time.sleep(5)
        self.screen_step('设置个人客户信息')
        valid_accessMsg = PageAssert(self.driver).assert_error() #校验号码是否异常
        if '业务校验失败' in valid_accessMsg:
            print('号码校验提示：', valid_accessMsg)
            logger.info('开户号码校验:{}'.format(valid_accessMsg))
            self.quit_browse()
        else:
            logger.info('号码校验通过')
            logger.info('客户信息设置完成')
            time.sleep(2)

    def Input_validSim(self,simId):
        '''输入sim卡号，按Enter回车校验'''
        loc_simId = (By.ID,'ICC_ID')
        self.sendkey(loc_simId,simId)
        time.sleep(2)
        self.move_element_enter(loc_simId)  #移动到该元素按Enter键校验
        time.sleep(5)
        #判断是否校验通过
        validMsg = PageAssert(self.driver).assert_WadeMsg() #不管校验是否通过都点击了确认按钮
        logger.info('SIM卡校验结果:' + validMsg)
        return validMsg

    def set_personMainOffer(self,offerId):
        '''进入主套餐选择iframe，订购主套餐'''
        loc_selectOffer = (By.ID,'SELECTED_OFFER_NAME')
        self.find_element_click(loc_selectOffer)
        time.sleep(3)
        offerFrame = (By.XPATH,"//iframe[contains(@src,'service=page/oc.person.cs.OfferList')]")
        self.iframe(offerFrame)
        # self.iframe('offerFrame') #先进入主套餐订购frame
        print('进入商品订购offerFrame======')
        time.sleep(5)
        self.screen_step('进入主套餐订购页面，选择主套餐')
        xpath_str = "//li[contains(@ontap,'%s')]" %offerId
        loc_OfferName = (By.XPATH,xpath_str)
        self.js_focus_element(loc_OfferName)
        self.isElementDisplay(loc_OfferName,'click')  #聚焦到该套餐，点击进入套餐订购
        ##这里开可以写个方法选择可选子商品
        iframe_offerId = "//iframe[@id='iframe_%s']"  %offerId #Iframe是动态的
        print('iframe_offerId:',iframe_offerId)
        loc_offerId = (By.XPATH,iframe_offerId)
        self.iframe(loc_offerId) #进入到iframe_offerId
        time.sleep(2)
        print('======进入到iframe_offerId======',loc_offerId)
        self.screen_step('进入订购Iframe,点击确认')
        btn_confirm = (By.XPATH,'//*[@id="SubmitPart"]/button[1]')
        self.isElementDisplay(btn_confirm,'click') #点击确认按钮
        time.sleep(2)
        self.driver.switch_to.parent_frame()  # 回到Offerframe
        self.driver.switch_to.parent_frame()  # 回到个人用户开户主frame

    def set_Acctinfo(self):
        '''设置账户信息'''
        self.screen_step('设置账户信息')
        loc_acct = (By.ID,'ACCT_NAME')
        loc_acctinfoName= (By.ID,'acctinfo_PAY_NAME')
        loc_confirm = (By.ID,'submitAcctInfoBut')
        self.isElementDisplay(loc_acct,'click') #点击账户信息
        time.sleep(2)
        acctName = GenTestData().create_CustName() + '测试账户'
        self.sendkey(loc_acctinfoName,acctName) #输入账户名称
        self.isElementDisplay(loc_confirm,'click') #点击确定
        time.sleep(1)

    def set_personPwd(self):
        '''设置用户服务密码'''
        self.screen_step('设置用户服务密码')
        loc_pwd = (By.ID,'NEW_PASSWORD')  #新密码
        loc_confirmpwd = (By.ID,'CONFIRM_NEW_PASSWORD')  #确认新密码
        passwd = '108109'  #默认开户密码都设置为108109
        logger.info('开户默认密码:{}'.format(passwd))
        self.sendkey(loc_pwd,passwd)
        self.sendkey(loc_confirmpwd,passwd)
        time.sleep(1)

    def set_BusiAcceptInfo(self,simId,offerId):
        '''
        设置业务受理信息
        :param simId: sim卡号
        :param offerId: 个人主套餐ID
        :param acctName: 账户名称
        :param passwd: 服务密码
        :return:
        '''
        self.Input_validSim(simId) #输入SIMID并校验
        self.set_personMainOffer(offerId) #设置个人主套餐
        self.set_Acctinfo()  #设置账户信息
        self.set_personPwd() #设置用户服务新密码

    def confirm_Payinfo(self):
        '''提交后确认支付'''
        loc_UIstep = (By.CSS_SELECTOR,'#UI-step > div > div.fn > button')
        Btn_Pay = (By.CSS_SELECTOR,'#PayPart > div.l_editMain > div.c_submit.c_submit-full > button')
        self.isElementDisplay(loc_UIstep,'click')
        time.sleep(1)
        self.screen_step('进入支付页面，点击确认支付')
        self.isElementDisplay(Btn_Pay,'click')
        time.sleep(5)

    def accept_PersonOpen(self,accessNum,simId,offerId):
        '''受理个人用户开户'''
        title = '个人用户开户受理测试记录'
        self.add_dochead(title)
        loc_commitAll = (By.XPATH,'//*[@id="CSSUBMIT_BUTTON"]')
        self.Open_subscriberOpen() #进入开户页面
        self.set_customerInfo(accessNum) #设置客户信息
        self.set_BusiAcceptInfo(simId,offerId)   #设置业务受理信息
        self.find_element_click(loc_commitAll)
        self.find_element_click(loc_commitAll)
        time.sleep(10)
        msg = PageAssert(self.driver).assert_error() #提交后校验异常
        print('业务受理信息:',msg)
        self.confirm_Payinfo()
        submitMsg = PageAssert(self.driver).assert_Submit()  #提交后返回信息，flowId或者报错
        print('===提交后页面返回信息：',submitMsg)
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)
        time.sleep(3)

if __name__ == '__main__':
    print("用例开始执行时间：" + time.strftime("%Y%m%d%H%M%S"))
    driver = webdriver.Chrome()
    test = SubscriberOpen(driver)
    test.accept_PersonOpen(accessNum='18708728339',simId='89860057245448890016',offerId='99091283')
    driver.close()
    print("用例执行结束时间：" + time.strftime("%Y%m%d%H%M%S"))



