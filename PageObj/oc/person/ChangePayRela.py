import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from Common import ReadConfig
from PageObj.oc.person.PersonBase import PersonBase
from Common.Mylog import LogManager
from Common.Assert import PageAssert


logger = LogManager('ChangePayRelaNor').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
rc = ReadConfig.ReadConfig("ngboss_config.ini")

class ChangePayRelaNor(PersonBase):
    '''普通付费关系变更业务'''
    def open_base(self):
        self.driver.get(rc.get_ngboss('url'))
        self.driver.maximize_window()

    def open_ChangePayRelaNorFrame(self):
        self.driver.switch_to.default_content() #记得一定要回到主窗口后再找iframe
        loc_frame = (By.XPATH,"//iframe[contains(@src,'/ordercentre/ordercentre?service=page/person.cs.changepayrelation.ChangePayRelaNor')]")
        self.iframe(loc_frame)
        logger.info("进入普通付费关系变更页面:" + str(loc_frame))
        time.sleep(2)

    def set_mergeSerialNum(self,SerialNum):
        '''合账时设置付费号码'''
        loc_merge = (By.XPATH,'//*[@id="change_account_type_span"]/span[2]')  #合账
        btn_qry = (By.ID,'check_serial_number') #查询校验按钮
        self.find_element_click(loc_merge)
        li_newSerialNum = (By.ID, 'new_serial_number')
        self.find_element_click(li_newSerialNum)
        time.sleep(2)
        text_newSerialNum = (By.ID, 'new_serial_number_1')
        self.sendkey(text_newSerialNum, SerialNum)
        time.sleep(2)
        self.find_element_click(btn_qry)


    def accept_chgPayRela(self,AccessNum,operCode,SerialNum='',password='123123'):
        '''
        普通付费关系变更，包括分账和合账两种操作
        :param AccessNum: 业务办理号码
        :param password: 老服务密码（登录时使用）
        :param operCode: 操作类型 1-分账，2-合账
        :param SerialNum: 付费号码(选择合帐操作时需要输入付费号码并校验)
        '''
        title = '普通付费关系变更测试记录'
        loc_separater = (By.XPATH,'//*[@id="change_account_type_span"]/span[1]') #分账
        loc_remark = (By.ID,'remarks') #备注
        loc_commit = (By.ID, 'CSSUBMIT_BUTTON') #提交按钮
        self.add_dochead(title)
        self.Open_PersonMenu(AccessNum,password,cataMenuId='crm9200',menuId='crm9257') #登录并进入普通付费关系变更菜单
        time.sleep(2)
        self.open_ChangePayRelaNorFrame() #进入iframe
        RuleMsg = self.vaild_BusiRule() #验证号码办理规则
        logger.info('普通付费关系变更规则验证结果:{}'.format(RuleMsg))
        time.sleep(3)
        #业务办理
        if operCode == '1' :  #分账
            logger.info('选择的是分账操作')
            self.find_element_click(loc_separater)
        elif operCode == '2': #合账
            logger.info('选择的是合帐操作')
            self.set_mergeSerialNum(SerialNum)
            vaildMsg = PageAssert(self.driver).assert_error()
            logger.info('付费号码校验结果：{}'.format(vaildMsg))
            if '业务校验失败' in vaildMsg:
                self.quit_browse()  # 如果校验失败，直接跳出
        else:
            print('OperCode只能传入1或者2，当前传入：{}'.format(operCode))
            self.quit_browse()
        self.sendkey(loc_remark,'AutoTest')
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
    test = ChangePayRelaNor(driver)
    # test.accept_chgPayRela(AccessNum ='18725337983',operCode='1',SerialNum='18787295285')
    test.accept_chgPayRela(AccessNum ='18787289368',operCode='2',SerialNum='18787295285')

    # driver.close()
    print("用例执行结束时间：" + time.strftime("%Y%m%d%H%M%S"))


























