import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from Base import ReadConfig
from PageObj.oc.person.PersonBase import PersonBase
from Base.Mylog import LogManager
from Common.Assert import PageAssert


logger = LogManager('ShareCluster').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
rc = ReadConfig.ReadConfig("ngboss_config.ini")

class ShareCluster(PersonBase):
    '''共享主卡操作'''
    def open_base(self):
        self.driver.get(rc.get_ngboss('url'))
        self.driver.maximize_window()
        #self.driver.implicitly_wait(5)

    def open_ShareClusterFrame(self):
        self.driver.switch_to.default_content() #记得一定要回到主窗口后再找iframe
        loc_frame = (By.XPATH,"//iframe[contains(@src,'/ordercentre/ordercentre?service=page/oc.person.cs.ShareCluster')]")
        # 切换到主frame
        self.iframe(loc_frame)
        logger.info("进入主卡操作:" + str(loc_frame))
        time.sleep(2)


    def add_MebAccessNum(self,serialNum):
        '''
        :param serialNum: 副卡手机号码
        '''
        # loc_add = (By.CSS_SELECTOR,'body > div.l_edit > div.l_editMain > div:nth-child(4) > div.fn > ul > li') #新增按钮
        loc_add = (By.XPATH,"//li[contains(@onclick,'newAcct')]") #新增按钮
        loc_serialNum = (By.ID,'new_serial_number') #副卡号码
        Btn_confirm = (By.CSS_SELECTOR,'#newAcct > div.c_scroll.c_scroll-float.c_scroll-header > div > div.c_submit.c_submit-full > button') #确定按钮
        self.find_element_click(loc_add)
        self.screen_step('输入副卡成员服务号码')
        time.sleep(1)
        self.sendkey(loc_serialNum,serialNum) #输入副卡号码
        time.sleep(2)
        self.find_element_click(Btn_confirm)

    def del_MebAccessNum(self,serialNum):
        '''
        删除成员
        :param serialNum: 成员手机号码
        '''
        xpath_str = '//div[contains(@member_sn,"%s")]' % serialNum
        print('删除成员按钮：{}'.format(xpath_str))
        loc_del = (By.XPATH,xpath_str)
        self.find_element_click(loc_del)
        time.sleep(2)

    def cancel_ShareCluster(self):
        '''取消家庭共享群组'''
        loc_cancel = (By.ID,'cancelBox')
        self.find_element_click(loc_cancel)
        time.sleep(2)

    def accept_addMember(self,AccessNum,serialNum,password='123123'):
        '''
        新增共享成员
        :param AccessNum: 手机号码（主卡）
        :param serialNum: 副卡手机号码
        :param password: 用户登录密码
        '''
        title = '4G家庭共享套餐业务新增成员'
        self.add_dochead(title)
        loc_commit = (By.ID, 'CSSUBMIT_BUTTON') #提交按钮
        self.Open_PersonMenu(AccessNum,password,cataMenuId='crm9400',menuId='crm4G10') #登录并进入主卡菜单
        time.sleep(5)
        self.open_ShareClusterFrame() #进入iframe
        RuleMsg = self.vaild_BusiRule() #业务检查点（进入菜单时校验）
        print('4G家庭共享套餐业务提交前规则:{}'.format(RuleMsg))
        logger.info('4G家庭共享套餐业务提交前规则:{}'.format(RuleMsg))
        if '业务校验失败' in RuleMsg:
            self.quit_browse() #业务规则校验失败，直接终止程序
        self.screen_step('进入主卡操作菜单')
        self.add_MebAccessNum(serialNum)
        time.sleep(2)
        self.find_element_click(loc_commit) #点击提交
        time.sleep(10)
        submitMsg = PageAssert(self.driver).assert_SubmitPage()
        logger.info('业务受理信息：{}'.format(submitMsg))
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)

    def accept_DelMember(self,AccessNum,serialNum,password='123123'):
        '''
        新增共享成员
        :param AccessNum: 手机号码（主卡）
        :param serialNum: 副卡手机号码
        :param password: 用户登录密码
        '''
        title = '4G家庭共享套餐业务删除成员'
        self.add_dochead(title)
        loc_commit = (By.ID, 'CSSUBMIT_BUTTON') #提交按钮
        self.Open_PersonMenu(AccessNum,password,cataMenuId='crm9400',menuId='crm4G10') #登录并进入主卡菜单
        time.sleep(5)
        self.open_ShareClusterFrame() #进入iframe
        RuleMsg = self.vaild_BusiRule() #业务检查点（进入菜单时校验）
        print('4G家庭共享套餐业务提交前规则:{}'.format(RuleMsg))
        logger.info('4G家庭共享套餐业务提交前规则:{}'.format(RuleMsg))
        if '业务校验失败' in RuleMsg:
            self.quit_browse() #业务规则校验失败，直接终止程序
        self.screen_step('进入主卡操作菜单')
        self.del_MebAccessNum(serialNum)
        time.sleep(2)
        self.find_element_click(loc_commit) #点击提交
        time.sleep(10)
        submitMsg = PageAssert(self.driver).assert_SubmitPage()
        logger.info('业务受理信息：{}'.format(submitMsg))
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)

    def accept_cancelShareCluster(self,AccessNum,password='123123'):
        '''
        新增共享成员
        :param AccessNum: 手机号码（主卡）
        :param password: 用户登录密码
        '''
        title = '4G家庭共享套餐业务取消群组'
        self.add_dochead(title)
        loc_commit = (By.ID, 'CSSUBMIT_BUTTON') #提交按钮
        self.Open_PersonMenu(AccessNum,password,cataMenuId='crm9400',menuId='crm4G10') #登录并进入主卡菜单
        time.sleep(5)
        self.open_ShareClusterFrame() #进入iframe
        RuleMsg = self.vaild_BusiRule() #业务检查点（进入菜单时校验）
        print('4G家庭共享套餐业务提交前规则:{}'.format(RuleMsg))
        logger.info('4G家庭共享套餐业务提交前规则:{}'.format(RuleMsg))
        if '业务校验失败' in RuleMsg:
            self.quit_browse() #业务规则校验失败，直接终止程序
        self.screen_step('进入主卡操作菜单')
        self.cancel_ShareCluster() #点击取消群组按钮
        Msg = PageAssert(self.driver).assert_WarnPage()
        print('取消共享群组时，提醒信息:{}'.format(Msg))
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
    test = ShareCluster(driver)
    # test.accept_DelMember(AccessNum='18887251971',serialNum='18313160723')
    # test.accept_addMember(AccessNum='18887251971',serialNum='18306900081')
    test.accept_cancelShareCluster(AccessNum='18887251971')


    driver.close()
    print("用例执行结束时间：" + time.strftime("%Y%m%d%H%M%S"))










