import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from Common import ReadConfig
from PageObj.oc.person.PersonBase import PersonBase
from Common.Mylog import LogManager
from Common.Assert import PageAssert


# logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
logger = LogManager('ShareActive').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
rc = ReadConfig.ReadConfig("ngboss_config.ini")

class ShareActive(PersonBase):
    '''销户业务业务'''
    def open_base(self):
        self.driver.get(rc.get_ngboss('url'))
        self.driver.maximize_window()
        #self.driver.implicitly_wait(5)

    def open_ShareActiveFrame(self):
        self.driver.switch_to.default_content() #记得一定要回到主窗口后再找iframe
        loc_frame = (By.XPATH,"//iframe[contains(@src,'/ordercentre/ordercentre?service=page/oc.person.cs.ShareActive')]")
        # 切换到销户主frame
        self.iframe(loc_frame)
        logger.info("进入家庭畅享活动frame:" + str(loc_frame))
        time.sleep(2)

    def choose_ActiveOffer(self,offerId):
        '''选择共享活动商品'''
        #offerid="1000295520"
        xpath_str = "//li[@offerid='%s' and contains(@ontap,'Share.showInfo')]" % offerId
        logger.info('定位的活动：{}'.format(xpath_str))
        loc_Offer = (By.XPATH,xpath_str)
        self.find_element_click(loc_Offer) #点击进入办理界面
        time.sleep(2)

    def set_ShareActiveInfo(self,phoneNum,Idencode):
        '''
        :param phoneNum: 副号
        :param Idencode: 验证码
        '''
        sel_pwdLoc = (By.ID,'IS_NEW')
        loc_AccessNum1 = (By.ID,'CHECK_ACCESS_NUM1') #副号1
        loc_Accesspwd1 = (By.ID,'ACCESS_PASS1') #副号1密码
        btn_checkButNum1 = (By.ID,'checkButNum1') #副号1验证按钮
        loc_AccessNum2 = (By.ID,'CHECK_ACCESS_NUM2') #副号2
        loc_Accesspwd2 = (By.ID,'ACCESS_PASS2')#副号2密码
        btn_checkButNum2 = (By.ID,'checkButNum2')#副号2验证按钮
        self.find_element_click(sel_pwdLoc) #认证方式选择用户密码
        self.sendkey(loc_AccessNum1,phoneNum) #输入副号1
        self.sendkey(loc_Accesspwd1,Idencode) #输入服务密码
        self.screen_step('设置共享副号并验证')
        self.find_element_click(btn_checkButNum1) #点击验证

        time.sleep(2)
        # msg = self.vaild_BusiRule()

    def accept_ShareActive(self,AccessNum,offerId,phoneNum,Idencode,password='123123'):
        '''
        受理
        :param offerId: 共享活动OFFER_ID
        :param phoneNum: 副号
        :param Idencode: 副号密码
        '''
        title = '家庭畅享活动受理测试记录'
        self.add_dochead(title)
        loc_commit = (By.CSS_SELECTOR, '#winInfoPop > div.c_popupBox > div > div > div > div.c_submit.e_center > button')
        self.Open_PersonMenu(AccessNum,password,cataMenuId='crm9200',menuId='crmy198') #进入菜单
        time.sleep(5)
        self.open_ShareActiveFrame() #进入iframe
        logger.info('进入家庭畅享活动菜单时验证主号')
        logger.info('暂时屏蔽主号校验')
        # self.vaild_BusiRule() #业务检查点（进入菜单时校验）
        self.screen_step('进入家庭畅享活动CRM,选择活动')
        self.choose_ActiveOffer(offerId) #选择共享活动
        self.set_ShareActiveInfo(phoneNum,Idencode)
        logger.info('副号校验....')
        vaildMsg = self.vaild_BusiRule()
        self.screen_step('验证副号')
        if '出现警告信息' in vaildMsg:
            self.quit_browse()
            time.sleep(2)
        time.sleep(2)
        self.find_element_click(loc_commit) #点击办理
        time.sleep(10)
        submitMsg = PageAssert(self.driver).assert_SubmitPage()
        logger.info('业务受理信息：{}'.format(submitMsg))
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)
        time.sleep(3)

if __name__ == '__main__':
    print("用例开始执行时间：" + time.strftime("%Y%m%d%H%M%S"))
    driver = webdriver.Chrome()
    test = ShareActive(driver)
    test.accept_ShareActive(AccessNum='18887251971',offerId='1000295516',phoneNum='15808720624',Idencode='102103')

    # driver.close()
    print("用例执行结束时间：" + time.strftime("%Y%m%d%H%M%S"))










