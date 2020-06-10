import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from Base import ReadConfig
from PageObj.oc.person.PersonBase import PersonBase
from Base.Mylog import LogManager
from Common.Assert import PageAssert
from Base.GenTestData import GenTestData


logger = LogManager('FamilyNetPage').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
rc = ReadConfig.ReadConfig("ngboss_config.ini")

class FamilyNetPage(PersonBase):
    '''亲情网（省内版）业务受理'''
    def open_base(self):
        self.driver.get(rc.get_ngboss('url'))
        self.driver.maximize_window()
        #self.driver.implicitly_wait(20)

    def open_MultiOfferFrame(self):
        self.driver.switch_to.default_content() #记得一定要回到主窗口后再找iframe
        loc_frame = (By.XPATH,"//iframe[contains(@src,'/ordercentre?service=page/oc.person.cs.MultiOfferDetail')]")
        # 切换到销户主frame
        self.iframe(loc_frame)
        logger.info("进入亲情网受理frame:" + str(loc_frame))
        time.sleep(2)

    def set_mainCard(self,mainPhoneNum):
        '''
        设置主卡家庭短号
        :param mainPhoneNum: 主卡号码
        :return:
        '''
        li_str = 'compOfferId_%s_100009901' % mainPhoneNum #家庭短号待设置
        loc_mainComp = (By.ID,li_str)
        li_shortCodeSpan_str = 'select_%s_390018000_span'  % mainPhoneNum # 请选择
        loc_shortCodeSpan = (By.ID,li_shortCodeSpan_str)
        li_shortCodeStr = '//*[@id="select_%s_390018000_list_ul"]/li[2]' % mainPhoneNum  #520短号
        loc_shortcode = (By.XPATH,li_shortCodeStr)
        li_open = (By.ID,'590020001')
        btn_confirm = (By.ID,'chaSpecPopOkButton_100009901')
        '''设置家庭主卡家庭短号'''
        self.find_element_click(loc_mainComp) #点击主卡家庭短号
        time.sleep(3)
        self.find_element_click(loc_shortCodeSpan) #点击选择
        time.sleep(1)
        self.find_element_click(loc_shortcode)  # 点击520
        self.find_element_click(li_open) #短号显示，点击开通
        self.screen_step('设置主卡家庭短号')
        self.find_element_click(btn_confirm)  #点击确认
        time.sleep(2)

    def set_mutiCard(self,mutiPhoneNumList = []):
        '''
        设置副卡家庭短号
        :param mutiPhoneNumList: 副卡号码列表
        :return:
        '''
        text_addMeb = (By.ID,'addMemberAccessNum')
        Btn_add = (By.XPATH,'//button[contains(@ontap,"MemberAction.addMember")]')
        logger.info('家庭成员号码列表:{}'.format(mutiPhoneNumList))
        logger.info('要设置{}个家庭成员：'.format(len(mutiPhoneNumList)+1))
        for i in range(len(mutiPhoneNumList)):
            self.sendkey(text_addMeb,mutiPhoneNumList[i]) #新增家庭成员
            self.find_element_click(Btn_add)
            alertmsg = self.alterMsg() #Alter处理
            logger.info('弹出的alert信息:{}'.format(alertmsg))
            '''设置副卡短号服务'''
            li_str = 'compOfferId_%s_100009901' % mutiPhoneNumList[i]  # 家庭短号待设置
            loc_mainComp = (By.ID, li_str)
            li_shortCodeSpan_str = 'select_%s_390018000_span' % mutiPhoneNumList[i]  # 请选择
            loc_shortCodeSpan = (By.ID, li_shortCodeSpan_str)
            li_shortCodeStr = '//*[@id="select_%s_390018000_list_ul"]/li[%d]' % (mutiPhoneNumList[i],i+3)  # 循环短号
            loc_shortcode = (By.XPATH, li_shortCodeStr)
            li_open = (By.ID, '590020001')
            btn_confirm = (By.ID, 'chaSpecPopOkButton_100009901')

            self.find_element_click(loc_mainComp) #点击家庭短号
            time.sleep(3)
            self.find_element_click(loc_shortCodeSpan) #点击选择
            time.sleep(1)
            self.find_element_click(loc_shortcode)  # 点击521
            self.find_element_click(li_open) #短号显示，点击开通
            self.screen_step('设置家庭成员短号')
            self.find_element_click(btn_confirm)  #点击确认
            time.sleep(2)

    def accept_MultiOffer(self,AccessNum,mutiAccessNumList=[],password='123123'):
        '''受理亲情网省内版'''
        title = '受理亲情网省内版测试记录'
        self.add_dochead(title)
        Btn_commit = (By.ID, 'CSSUBMIT_BUTTON') #提交按钮
        self.Open_PersonMenu(AccessNum,password,cataMenuId='crm9300',menuId='crmy165') #登录并进入菜单
        time.sleep(5)
        self.open_MultiOfferFrame() #进入iframe
        RuleMsg = self.vaild_BusiRule() #业务检查点（进入菜单时校验）
        print('受理亲情网省内版提交前规则:{}'.format(RuleMsg))
        logger.info('受理亲情网省内版提交前规则:{}'.format(RuleMsg))
        if '业务校验失败' in RuleMsg:
            self.quit_browse() #业务规则校验失败，直接终止程序
        logger.info('开始设置主号家庭短号服务')
        self.screen_step('进入亲情网办理菜单')
        self.set_mainCard(AccessNum)
        logger.info('新增家庭成员并设置家庭短号服务')
        self.set_mutiCard(mutiAccessNumList)
        time.sleep(2)
        self.find_element_click(Btn_commit)
        time.sleep(10)
        submitMsg = PageAssert(self.driver).assert_SubmitPage()
        logger.info('业务受理信息：{}'.format(submitMsg))
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)

if __name__ == '__main__':
    print("用例开始执行时间：" + time.strftime("%Y%m%d%H%M%S"))
    driver = webdriver.Chrome()
    test = FamilyNetPage(driver)
    # test.accept_MultiOffer(AccessNum='15808720006',mutiAccessNumList=['18787295285','18787289368'])
    test.accept_MultiOffer(AccessNum='13908720018',mutiAccessNumList=['13908720019','13908720043'])

    # driver.close()
    print("用例执行结束时间：" + time.strftime("%Y%m%d%H%M%S"))



