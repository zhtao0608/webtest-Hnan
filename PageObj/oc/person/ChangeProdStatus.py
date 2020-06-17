import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from Base import ReadConfig
from PageObj.oc.person.PersonBase import PersonBase
from Base.Mylog import LogManager
from Common.Assert import PageAssert


logger = LogManager('ChangeProdStatus').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
rc = ReadConfig.ReadConfig("ngboss_config.ini")

class ChangeProdStatus(PersonBase):
    '''换卡业务'''
    def open_base(self):
        self.driver.get(rc.get_ngboss('url'))
        self.driver.maximize_window()
        #self.driver.implicitly_wait(20)

    def open_ChangeProdStatusFrame(self):
        self.driver.switch_to.default_content() #记得一定要回到主窗口后再找iframe
        loc_frame = (By.XPATH,"//iframe[contains(@src,'/ordercentre/ordercentre?service=page/oc.person.cs.ChangeProdStatus')]")
        # 切换到销户主frame
        self.iframe(loc_frame)
        logger.info("进入停开机受理frame:" + str(loc_frame))
        time.sleep(2)

    def select_BusiType(self,busiCode):
        '''
        选择停开机业务办理类型
        :param busiCode: 传入停开机业务受理类型
        126 局方开机,136 局方停机
        132 挂失
        131 报停,133 报开
        138 特殊停机
        496 担保开机 497 紧急开机
        '''
        loc_stop = (By.ID,'stopMobile')  #停机
        loc_open = (By.ID,'openMobile')  #开机
        loc_lost = (By.ID,'lostMobile') #挂失
        loc_emergencyopen = (By.ID,'emergencyOpen') #紧急开机
        loc_officeStopMobile = (By.ID,'officeStopMobile') #局方停机
        loc_officeOpenMobile = (By.ID,'officeOpenMobile') #局方开机
        loc_guaranteeOpen = (By.ID,'guaranteeOpen') #担保开机
        if busiCode == '131':   #报停
            self.find_element_click(loc_stop)
            time.sleep(2)
        elif busiCode == '133':  # 报开
            self.find_element_click(loc_open)
            time.sleep(2)
        elif busiCode == '132':  #挂失
            self.find_element_click(loc_lost)
            time.sleep(2)
        elif busiCode == '496':  #紧急开机
            self.find_element_click(loc_emergencyopen)
            time.sleep(2)
        elif busiCode == '136': #局方停机
            self.find_element_click(loc_officeStopMobile)
            time.sleep(2)
        elif busiCode == '126': #局方开机
            self.find_element_click(loc_officeOpenMobile)
            time.sleep(2)
        elif busiCode == '496': #担保开机
            self.find_element_click(loc_guaranteeOpen)
            time.sleep(2)
        else:
            logger.info('传入的busiCode不对，退出操作')
            # self.quit_browse()

    def accept_stopOrOpen(self,AccessNum,busiCode,password='123123'):
        '''停开机业务受理'''
        title = '停开机业务受理测试记录'
        self.add_dochead(title)
        self.Open_PersonMenu(AccessNum,password,cataMenuId='crm9200',menuId='crm9247') #登录并进入停开机业务受理菜单
        self.open_ChangeProdStatusFrame()
        self.screen_step('进入菜单，选择停开机业务类型')
        self.select_BusiType(busiCode) # 选择停开机业务受理类型
        loc_submit = (By.ID,'CSSUBMIT_BUTTON')
        # RuleMsg = PageAssert(self.driver).assert_error() #校验号码是否满足停机受理规则
        RuleMsg = self.vaild_BusiRule() #校验号码是否满足停机受理规则
        if '业务校验失败' in RuleMsg:
            print('业务规则校验结果：{}'.format(RuleMsg))
            logger.info('业务规则校验结果：{}'.format(RuleMsg))
            self.screen_step('业务规则校验')
            self.quit_browse()
        else:
            print('业务规则校验通过')
            self.find_element_click(loc_submit)
            submitMsg = PageAssert(self.driver).assert_SubmitPage()
            logger.info('业务受理信息：{}'.format(submitMsg))
            self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
            self.save_docreport(title)

if __name__ == '__main__':
    print("用例开始执行时间：" + time.strftime("%Y%m%d%H%M%S"))
    driver = webdriver.Chrome()
    test = ChangeProdStatus(driver)
    # test.accept_DelMember(AccessNum='18887251971',serialNum='18313160723')
    test.accept_stopOrOpen(AccessNum='18887251971',busiCode='133')
    # test.accept_stopOrOpen(AccessNum='18887251971',busiCode='131')

    driver.close()
    print("用例执行结束时间：" + time.strftime("%Y%m%d%H%M%S"))