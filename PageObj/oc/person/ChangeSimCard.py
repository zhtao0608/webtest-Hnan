import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from Base import ReadConfig
from PageObj.oc.person.PersonBase import PersonBase
from Base.Mylog import LogManager
from Common.Assert import PageAssert
from Base.GenTestData import GenTestData


logger = LogManager('ChangeSimCard').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
rc = ReadConfig.ReadConfig("ngboss_config.ini")

class ChangeSimCard(PersonBase):
    '''换卡业务'''
    def open_base(self):
        self.driver.get(rc.get_ngboss('url'))
        self.driver.maximize_window()
        #self.driver.implicitly_wait(20)

    def open_ChangSimCardFrame(self):
        self.driver.switch_to.default_content() #记得一定要回到主窗口后再找iframe
        loc_frame = (By.XPATH,"//iframe[contains(@src,'/ordercentre/ordercentre?service=page/oc.person.cs.ChangeSimCard')]")
        # 切换到销户主frame
        self.iframe(loc_frame)
        logger.info("进入换卡frame:" + str(loc_frame))
        time.sleep(2)

    def Input_NewSimId(self,simId):
        '''
        输入新sim卡并验证
        :param simId: 副号
        '''
        loc_newSim = (By.ID,'newSimcardNo')
        self.screen_step('输入SIM新卡')
        self.sendkey(loc_newSim,simId)
        time.sleep(2)

    def check_CustInfoBypwd(self,userPwd='108109'):
        '''选择服务密码验证，输入客户名称和服务密码，点击确定
        :param custName:客户名称
        :param userPwd:服务密码
        :return:
        '''
        sel_loc = (By.ID,'LEVEL_TYPE_CODE_span') #点击
        li_pwd = (By.CSS_SELECTOR,'#LEVEL_TYPE_CODE_float > div.content > div > div > ul > li:nth-child(3)') #选择服务密码
        # li_iden = (By.XPATH,'//*[@id="LEVEL_TYPE_CODE_list_ul"]/li[2]')
        # li_iden = (By.CSS_SELECTOR, '#LEVEL_TYPE_CODE_float > div.content > div > div > ul > li:nth-child(2)') #选择证件
        text_custName = (By.ID,'LOGIN_NAME') #客户姓名
        text_pwd = (By.ID,'LOGIN_VAL') #服务密码
        Btn_confirm = (By.ID,'BSL_SUBMIT_BTN') #确定按钮
        self.find_element_click(sel_loc)
        time.sleep(2)
        self.find_element_click(li_pwd)
        time.sleep(1)
        custName = GenTestData().create_CustName()
        self.sendkey(text_custName,custName) #输入客户姓名
        self.sendkey(text_pwd,userPwd) #输入密码
        self.screen_step('输入客户名称和服务密码，点击提交')
        self.find_element_click(Btn_confirm) #点击确定
        time.sleep(2)

    def check_CustInfoByIdcard(self):
        '''选择服务密码验证，输入客户名称和服务密码，点击确定
        :param custName:客户名称
        :param userPwd:服务密码
        :return:
        '''
        sel_loc = (By.ID,'LEVEL_TYPE_CODE_span') #点击
        # li_pwd = (By.CSS_SELECTOR,'#LEVEL_TYPE_CODE_float > div.content > div > div > ul > li:nth-child(3)') #选择服务密码
        li_iden = (By.CSS_SELECTOR, '#LEVEL_TYPE_CODE_float > div.content > div > div > ul > li:nth-child(2)') #选择证件
        text_custName = (By.ID,'LOGIN_NAME') #客户姓名
        text_pwd = (By.ID,'LOGIN_VAL') #服务密码
        Btn_confirm = (By.ID,'BSL_SUBMIT_BTN') #确定按钮
        self.find_element_click(sel_loc)
        time.sleep(2)
        self.find_element_click(li_iden)
        time.sleep(1)
        custName = GenTestData().create_CustName()
        idCard = GenTestData().Create_Idcard()
        self.sendkey(text_custName,custName) #输入客户姓名
        self.sendkey(text_pwd,idCard) #输入密码
        self.screen_step('输入客户名称和服务密码，点击提交')
        self.find_element_click(Btn_confirm) #点击确定
        time.sleep(2)


    def vaild_Customer(self):
        '''校验客户信息'''
        Loc_msg = (By.XPATH,"//div[@class='c_msg c_msg-h c_msg-phone-v c_msg-full' and not(contains(@style,'display: none'))]/div/div[2]/div[1]/div[2]")
        try :
            Vaildmsg = self.isElementDisplay(Loc_msg, 'text')
            time.sleep(3)
            logger.info('提示信息：' + Vaildmsg)
            print('提示信息：' + Vaildmsg)
            self.screen_step('验证信息：{}'.format(Vaildmsg))
            self.sendEnter()   #按回车键（继续办理）
            return Vaildmsg
        except Exception as e:
            print(e)
            logger.info('出现异常:{}'.format(e))

    def accept_ChangeSimCard(self,AccessNum,simId,userPwd,password='123123'):
        '''
        受理换卡业务
        :param accessNum: 手机号码
        :param simId: 新SIM卡号
        :param custName: 客户姓名
        :param userPwd: 服务密码
        :param password: 用户登录密码
        '''
        title = '换卡业务受理测试记录'
        self.add_dochead(title)
        text_remark = (By.ID,'REMARKS')  #备注
        loc_commit = (By.ID, 'CSSUBMIT_BUTTON') #提交按钮
        self.Open_PersonMenu(AccessNum,password,cataMenuId='crm9400',menuId='crm9431') #登录并进入换卡菜单
        time.sleep(5)
        self.open_ChangSimCardFrame() #进入iframe
        RuleMsg = self.vaild_BusiRule() #业务检查点（进入菜单时校验）
        print('换卡业务提交前规则:{}'.format(RuleMsg))
        logger.info('换卡业务提交前规则:{}'.format(RuleMsg))
        if '业务校验失败' in RuleMsg:
            self.quit_browse() #业务规则校验失败，直接终止程序
        self.screen_step('进入换卡菜单')
        self.check_CustInfoBypwd(userPwd)
        Vaild_custMsg = self.vaild_Customer()
        print('客户验证信息:{}'.format(Vaild_custMsg))
        logger.info('客户验证信息:{}'.format(Vaild_custMsg))
        time.sleep(2)
        # Valid_simMsg = self.vaild_NewSimId(simId)
        # print('新SIM卡验证结果:{}'.format(Valid_simMsg))
        # logger.info('新SIM卡验证结果:{}'.format(Valid_simMsg))
        self.Input_NewSimId(simId)
        self.sendkey(text_remark,'AntoTest') #填写备注信息
        self.find_element_click(loc_commit) #点击提交
        time.sleep(10)
        submitMsg = PageAssert(self.driver).assert_SubmitPage()
        logger.info('业务受理信息：{}'.format(submitMsg))
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)

if __name__ == '__main__':
    print("用例开始执行时间：" + time.strftime("%Y%m%d%H%M%S"))
    driver = webdriver.Chrome()
    test = ChangeSimCard(driver)
    # test.accept_ChangeSimCard(AccessNum='18708720015',simId ='89860011241071801002',custName='测试',userPwd='108109')
    test.accept_ChangeSimCard(AccessNum='18708720057',simId ='89860001240642520092',userPwd='108109')

    driver.close()
    print("用例执行结束时间：" + time.strftime("%Y%m%d%H%M%S"))










