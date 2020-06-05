import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from Base import ReadConfig
from PageObj.oc.person.PersonBase import PersonBase
from Base.Mylog import LogManager
from Common.Assert import PageAssert
from Base.GenTestData import GenTestData


# logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
logger = LogManager('ChangeCustOwner').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
rc = ReadConfig.ReadConfig("ngboss_config.ini")

class ChangeCustOwner(PersonBase):
    '''过户业务'''
    def open_base(self):
        self.driver.get(rc.get_ngboss('url'))
        self.driver.maximize_window()
        #self.driver.implicitly_wait(5)

    def open_ChangeCustOwnerFrame(self):
        self.driver.switch_to.default_content() #记得一定要回到主窗口后再找iframe
        loc_frame = (By.XPATH,"//iframe[contains(@src,'/ordercentre/ordercentre?service=page/oc.person.cs.ChangeCustOwner')]")
        self.iframe(loc_frame)
        logger.info("进入过户页面:" + str(loc_frame))
        time.sleep(2)

    def check_CustInfo(self,oldcustName,oldIdcard):
        '''验证客户信息'''
        loc_select = (By.ID,'LEVEL_TYPE_CODE_span')
        li_loc = (By.XPATH,'//*[@id="LEVEL_TYPE_CODE_list_ul"]/li[2]') #二代身份证（过户手输）
        text_custName = (By.ID,'LOGIN_NAME')  #客户姓名
        text_IdenId = (By.ID,'LOGIN_VAL')  #证件号码
        Btn_confirm = (By.ID,'BSL_SUBMIT_BTN') #确定按钮
        self.find_element_click(loc_select)
        time.sleep(2)
        ele_link = self.find(li_loc)
        # self.find_element_click(li_loc)
        self.click_on_element(ele_link) # 点击二代身份证（过户手输）
        time.sleep(2)
        self.sendkey(text_custName,oldcustName)  # 输入客户名称
        self.sendkey(text_IdenId,oldIdcard)   #输入证件号码
        self.find_element_click(Btn_confirm) #点击确定
        time.sleep(2)

    def set_NewCustInfo(self,idenAddress,idenExpDate,postCode,emailAdd):
        '''设置过户后新客户信息'''
        loc_input = (By.ID,'editInfoButton')
        text_newCustName = (By.ID,'PARTY_NAME') #客户名称
        text_birthDay = (By.ID,'BIRTH_DATE') # 出生日期
        text_idenAddress = (By.ID,'IDEN_ADDRESS') #证件地址
        text_idenExpDate = (By.ID,'IDEN_EXP_DATE') #证件有效期
        text_conNum = (By.ID,'CONT_NUMBER') #联系电话
        text_postCode = (By.ID,'POSTAL_CODE') #通信邮编
        text_emailAdd = (By.ID,'EMAIL_ADDRESS') #通信地址
        # newIdcard = GenTestData().Create_Idcard() #自动创建身份证件号码
        newCustName = GenTestData().create_CustName() #自动创建一个客户名称
        conNum = GenTestData().create_phone() # 自动创建一个手机号码
        logger.info('新客户名称:{},联系人号码：{}'.format(newCustName,conNum))
        # self.valid_IdenNr(newIdcard) # 输入证件并校验
        self.find_element_click(loc_input) #点击手工输入
        self.Input_validIdenNrNew() # 输入证件并校验
        self.sendkey(text_newCustName,newCustName)
        # self.sendkey(text_birthDay,birthDay)  身份证验证通过后自动填写
        self.sendkey(text_idenAddress,idenAddress)
        self.sendkey(text_idenExpDate,idenExpDate)
        self.sendkey(text_conNum,conNum)
        self.sendkey(text_postCode,postCode)
        self.sendkey(text_emailAdd,emailAdd)
        time.sleep(2)
        self.screen_step('设置新客户信息')
        li_district = (By.ID,'DISTRICT_NAME')  #客户业务区
        li_districtName = (By.ID,'L099') #默认都设置为L099 测试业务区
        self.find_element_click(li_district) #选择业务区
        time.sleep(2)
        self.find_element_click(li_districtName) #默认测试业务区
        time.sleep(1)
        #####设置账户信息
        li_acctInfo = (By.XPATH,'//li[contains(@ontap,"acctInfoPopup")]')
        # li_acctInfo = (By.CSS_SELECTOR,'body > div.l_edit > div.l_editMain > div:nth-child(6) > ul > li')
        text_acctName = (By.ID,'acctinfo_PAY_NAME')
        Btn_confirm = (By.ID,'submitAcctInfoBut')
        self.find_element_click(li_acctInfo)
        time.sleep(1)
        self.sendkey(text_acctName,newCustName) #账户名称默认设置成新客户名称
        self.find_element_click(Btn_confirm) #账户信息确认

    def set_NewPwd(self,newPwd):
        '''变更新服务密码'''
        li_pwd = (By.ID,'changePw')
        text_newPwd = (By.ID,'NEW_PASSWORD')
        text_confirmNewpwd = (By.ID,'CONFIRM_NEW_PASSWORD')
        Btn_confirm = (By.CSS_SELECTOR,'#ChgPwInfoPart > div > div.c_submit.c_submit-full > button.e_button-blue.e_button-l.e_button-r')
        self.find_element_click(li_pwd) #点击密码变更
        time.sleep(2)
        self.sendkey(text_newPwd,newPwd)
        self.sendkey(text_confirmNewpwd,newPwd)
        self.find_element_click(Btn_confirm) #确认密码变更
        time.sleep(2)

    def accept_ChangeCustOwner(self,AccessNum,oldIdcard,oldcustName,idenAddress,idenExpDate,postCode,emailAdd,newPwd,password='123123'):
        '''
        :param AccessNum: 业务办理号码
        :param oldIdcard: 旧证件号码
        :param oldcustName: 旧客户名称
        :param newIdcard: 新证件号码
        :param newCustName: 新客户名称
        :param birthDay: 出生日期
        :param idenAddress: 证件地址
        :param idenExpDate: 证件有效期
        :param conNum: 联系人电话
        :param postCode: 通信邮编
        :param emailAdd: 通信地址
        :param newPwd: 新密码
        :param password: 老服务密码（登录时使用）
        :return:
        '''
        title = '过户业务受理测试记录'
        self.add_dochead(title)
        loc_commit = (By.ID, 'CSSUBMIT_BUTTON') #提交按钮
        self.Open_PersonMenu(AccessNum,password,cataMenuId='crm9200',menuId='crm9210') #登录并进入过户菜单
        time.sleep(5)
        self.open_ChangeCustOwnerFrame() #进入iframe
        RuleMsg = self.vaild_BusiRule() #验证过户号码
        logger.info('过户规则验证结果:{}'.format(RuleMsg))
        self.screen_step('验证老客户信息')
        self.check_CustInfo(oldcustName,oldIdcard)
        time.sleep(3)
        self.sendEnter() # 先简单处理，直接回车处理
        time.sleep(2)
        self.set_NewCustInfo(idenAddress,idenExpDate,postCode,emailAdd) # 设置新客户信息
        self.screen_step('设置新客户信息')
        self.set_NewPwd(newPwd)
        time.sleep(2)
        self.find_element_click(loc_commit) #点击提交
        time.sleep(10)
        submitMsg = PageAssert(self.driver).assert_SubmitPage()
        logger.info('业务受理信息：{}'.format(submitMsg))
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)

if __name__ == '__main__':
    print("用例开始执行时间：" + time.strftime("%Y%m%d%H%M%S"))
    driver = webdriver.Chrome()
    test = ChangeCustOwner(driver)
    # test.accept_ChangeSimCard(AccessNum='18708720015',simId ='89860011241071801002',custName='测试',userPwd='108109')
    test.accept_ChangeCustOwner(AccessNum ='18725337983',oldIdcard='110101199003076835',oldcustName='测试',
                               idenAddress='测试地址测试地址测试',idenExpDate='2030-12-31',
                               postCode='410000',emailAdd='18708720015@139.com',newPwd='108109')


    # driver.close()
    print("用例执行结束时间：" + time.strftime("%Y%m%d%H%M%S"))


























