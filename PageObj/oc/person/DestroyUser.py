import time,sys
from selenium.webdriver.common.by import By
from selenium import webdriver
from Common import ReadConfig
from PageObj.oc.person.PersonBase import PersonBase
from Common.Mylog import LogManager
from Common.Assert import PageAssert


# logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
logger = LogManager('DestroyUser').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
rc = ReadConfig.ReadConfig("ngboss_config.ini")

class DestroyUser(PersonBase):
    '''销户业务业务'''
    def open_base(self):
        self.driver.get(rc.get_ngboss('url'))
        self.driver.maximize_window()
        #self.driver.implicitly_wait(30)

    def open_DestroyUserFrame(self):
        self.driver.switch_to.default_content() #记得一定要回到主窗口后再找iframe
        loc_frame = (By.XPATH,"//iframe[contains(@src,'/ordercentre/ordercentre?service=page/oc.person.cs.DestroyUser')]")
        # 切换到销户主frame
        self.iframe(loc_frame)
        logger.info("进入销户frame:" + str(loc_frame))
        time.sleep(2)

    def set_destroyReason(self):
        loc_Reason = (By.ID,'DESTROY_REASON_VALUE')
        loc_reasonDetail = (By.XPATH,'//*[@id="DESTROY_REASON"]/div[2]/div[1]/ul/li[6]') #默认资费高
        # self.find_element_click(loc_Reason)
        self.isElementDisplay(loc_Reason,'click')
        time.sleep(3)
        self.screen_step('设置销户原因')
        self.isElementDisplay(loc_reasonDetail,'click')
        time.sleep(2)

    def accept_DestroyUser(self,accessNum,password='123123'):
        '''销户业务受理'''
        title = '个人销户受理测试记录'
        self.add_dochead(title)
        loc_vaild = (By.XPATH,'//*[@id="MYSELF_div"]/div[1]')
        loc_commit = (By.ID,'CSSUBMIT_BUTTON')
        self.Open_PersonMenu(accessNum,password,cataMenuId='crm9300',menuId='crm9311') #进入菜单
        time.sleep(5)
        self.open_DestroyUserFrame() #进入销户iframe
        errMsg = self.vaild_BusiRule() #业务检查点（进入菜单时校验）
        if errMsg:
            print('业务规则校验失败：{}'.format(errMsg))
        else:
            PageAssert(self.driver).assert_HelpPage()
            self.close_UIstep()
        self.find_element_click(loc_vaild) #移动到认证并点击
        time.sleep(2)
        self.set_destroyReason()
        self.find_element_click(loc_commit)  #点击提交
        time.sleep(10)  #销户业务提交比较慢
        submitMsg = PageAssert(self.driver).assert_Submit()  #提交后返回信息，flowId或者报错
        # print('===提交后页面返回信息：',submitMsg)
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)
        time.sleep(3)

if __name__ == '__main__':
    print("用例开始执行时间：" + time.strftime("%Y%m%d%H%M%S"))
    driver = webdriver.Chrome()
    test = DestroyUser(driver)
    # test.accept_DestroyUser('13608729157')
    # test.accept_DestroyUser('13988545265')
    test.accept_DestroyUser('18206720231')

    driver.close()
    print("用例执行结束时间：" + time.strftime("%Y%m%d%H%M%S"))


