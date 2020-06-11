import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from Base import ReadConfig
from PageObj.oc.person.PersonBase import PersonBase
from Base.Mylog import LogManager
from Common.Assert import PageAssert


logger = LogManager('RestoreSubscriber').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
rc = ReadConfig.ReadConfig("ngboss_config.ini")

class RestoreSubscriber(PersonBase):
    '''个人业务-复机'''
    def open_base(self):
        self.driver.get(rc.get_ngboss('url'))
        self.driver.maximize_window()

    def open_RestoreSubscriberFrame(self):
        self.driver.switch_to.default_content() #记得一定要回到主窗口后再找iframe
        loc_frame = (By.XPATH,"//iframe[contains(@src,'/ordercentre/ordercentre?service=page/oc.person.cs.RestoreSubscriber')]")
        self.iframe(loc_frame)
        logger.info("进入复机页面:" + str(loc_frame))
        time.sleep(2)

    def InputSimAndVaild(self,SimId):
        '''输入SIM卡并校验SIM卡'''
        li_resCode = (By.XPATH,'//*[@id="userRes"]/ul/li[4]') #老SIM卡资源展示
        text_simId = (By.ID,'RES_CODE') #SIM卡输入框
        Btn_check = (By.ID,'checkResBtn') #校验按钮
        self.find_element_click(li_resCode)
        # ele_Res = self.find((By.ID,'userRes'))
        # ele_Res.find_element_by_class_name('group link checked').click() #SIM卡
        time.sleep(1)
        self.sendkey(text_simId,SimId) #输入SIM卡
        self.find_element_click(Btn_check) #点击校验
        checkMsg = self.check_ResCode() #校验卡号
        logger.info('资源SIM卡检查信息:{}'.format(checkMsg))

    def submit(self):
        Btn_submit = (By.ID,'CSSUBMIT_BUTTON')
        self.find_element_click(Btn_submit)

    def accept_RestoreSubscriber(self,AccessNum,simId):
        '''个人业务复机'''
        title = '个人业务复机测试记录'
        self.add_dochead(title)
        self.Open_PersonMenu(AccessNum,cataMenuId='crm9300',menuId='crm9313') #登录并进入普通付费关系变更菜单
        time.sleep(2)
        self.open_RestoreSubscriberFrame() #进入iframe
        RuleMsg = self.vaild_BusiRule() #验证号码办理规则
        logger.info('复机业务规则验证结果:{}'.format(RuleMsg))
        if '验证失败' in RuleMsg:
            self.driver.close()
        time.sleep(3)
        self.InputSimAndVaild(simId)
        self.screen_step('复机时输入SIM卡并校验')
        self.submit() #提交
        time.sleep(12)
        submitMsg = PageAssert(self.driver).assert_SubmitPage()
        logger.info('业务受理信息：{}'.format(submitMsg))
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)


if __name__ == '__main__':
    print("用例开始执行时间：" + time.strftime("%Y%m%d%H%M%S"))
    driver = webdriver.Chrome()
    test =RestoreSubscriber(driver)
    # test.accept_chgPayRela(AccessNum ='18725337983',operCode='1',SerialNum='18787295285')
    test.accept_RestoreSubscriber(AccessNum ='18724999835',simId='89860032241642474775')
    # driver.close()
    print("用例执行结束时间：" + time.strftime("%Y%m%d%H%M%S"))


