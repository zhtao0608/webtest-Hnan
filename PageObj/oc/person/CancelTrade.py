import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from Base import ReadConfig
from PageObj.oc.person.PersonBase import PersonBase
from Base.Mylog import LogManager
from Common.Assert import PageAssert


logger = LogManager('CancelTrade').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
rc = ReadConfig.ReadConfig("ngboss_config.ini")

class CancelTrade(PersonBase):
    '''业务返销'''
    def open_CancelTradeFrame(self):
        self.driver.switch_to.default_content() #记得一定要回到主窗口后再找iframe
        loc_frame = (By.XPATH,"//iframe[contains(@src,'/ordercentre/ordercentre?service=page/oc.person.cs.CancelTrade')]")
        self.iframe(loc_frame)
        logger.info("进入业务返销页面:" + str(loc_frame))
        time.sleep(2)

    def query_CancelTradeByAccessNum(self,AccessNum,Busi_item_code):
        '''
        根据手机号码和业务类型查询业务返销信息
        :param AccessNum: 手机号码
        :param BusiName: 业务类型名称
        :return:
        '''
        btn_qry = (By.ID,'qryBox')
        text_accessNum = (By.ID,'ACCESS_NUM')
        loc_selBusi = (By.ID,'BUSI_ITEM_CODE_span')
        xpath_str = '//*[@id="BUSI_ITEM_CODE_list_ul"]/li[contains(@val,"%s")]'  % Busi_item_code  #业务类型
        loc_busiName = (By.XPATH,xpath_str)
        loc_qryButton = (By.ID,'qryButton')
        btn_confirm = (By.ID,'sureBtn')
        self.find_element_click(btn_qry) #点击查询
        time.sleep(2)
        self.sendkey(text_accessNum,AccessNum)
        self.find_element_click(loc_selBusi) #点击业务类型
        time.sleep(1)
        self.find_element_click(loc_busiName) #选择一个业务类型
        time.sleep(1)
        self.find_element_click(loc_qryButton) #点击查询
        time.sleep(2)
        self.find_element_click(btn_confirm) #点击确定


    def accept_CancelTrade(self,AccessNum,Busi_item_code,password='123123'):
        '''受理亲情网省内版'''
        title = '业务返销测试记录'
        self.add_dochead(title)
        Btn_commit = (By.ID, 'CSSUBMIT_BUTTON') #提交按钮
        self.Open_PersonMenu(AccessNum,password,cataMenuId='crm9200',menuId='crm9456') #登录并进入业务返销菜单
        time.sleep(5)
        self.open_CancelTradeFrame() #进入iframe
        self.query_CancelTradeByAccessNum(AccessNum,Busi_item_code) #查询业务返销信息
        errMsg = PageAssert(self.driver).assert_error()
        if '业务校验失败' in errMsg:
            self.quit_browse() #查询返销信息失败，直接终止程序
        time.sleep(3)
        self.find_element_click(Btn_commit)
        helpMsg = PageAssert(self.driver).assert_HelpPage()
        if '校验通过' not in helpMsg:
            logger.info('弹出帮助提示信息:{}'.format(helpMsg))
        submitMsg = PageAssert(self.driver).assert_SubmitPage()
        logger.info('业务受理信息：{}'.format(submitMsg))
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)


if __name__ == '__main__':
    print("用例开始执行时间：" + time.strftime("%Y%m%d%H%M%S"))
    driver = webdriver.Chrome()
    test = CancelTrade(driver)
    test.accept_CancelTrade(AccessNum='15894390007',Busi_item_code='10')
    driver.close()
    print("用例执行结束时间：" + time.strftime("%Y%m%d%H%M%S"))
