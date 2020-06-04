import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from Common import ReadConfig
from Common.Mylog import LogManager
from PageObj.oc.group.GroupBasePage import BasePage
from Common.Assert import PageAssert
from Common.OperExcel import write_excel_append

# logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
rc = ReadConfig.ReadConfig("ngboss_config.ini")

class GrouprelaAdv(BasePage):
    def open_base(self):
        self.driver.get(rc.get_ngboss('url'))
        self.driver.maximize_window()
        #self.driver.implicitly_wait(30)

    def Open_GrprelaAdvframe(self):
        '''进入集团商品订购iFrame处理'''
        self.driver.switch_to.default_content()
        loc_frame = self.find((By.XPATH,"//iframe[contains(@src,'/ordercentre/ordercentre?service=page/oc.cs.PayrelaAdvChg')]"))
        self.driver.switch_to.frame(loc_frame)
        logger.info("进入GrprelaAdv:" + str(loc_frame))
        Btn_msg = self.find((By.CSS_SELECTOR,'#UI-step1 > div > div.fn > button:nth-child(1)'))
        Btn_msg.click()
        time.sleep(5)
        return self.driver

    def Open_GrprelaAdv(self, groupId):
        '''进入集团高级付费关系受理界面'''
        self.Open_groupMenu(groupId,'crm8400','crm8093') #点击进入菜单 ,父菜单>子菜单
        self.Open_GrprelaAdvframe()  # 进入集团订购iframe
        self.screen_step('进入集团高级付费关系管理菜单')
        time.sleep(2)

    def choose_grpAcct(self,acctId):
        loc_choose = (By.CSS_SELECTOR,'#QryCondPart > div:nth-child(1) > div.fn > ul > li') #选择按钮
        # str_xpath = '//li[@acct_id="%s" and contains(@ontap,"chooseAccount")]' % acctId  #传入集团账户ID
        str_xpath = '//li[@acct_id="%s"]' % acctId  #传入集团账户ID
        loc_acct = (By.XPATH,str_xpath)
        self.isElementDisplay(loc_choose,'click') #点击选择按钮
        self.screen_step('选择集团付费账户')
        self.find(loc_acct).click() #选择集团付费账户
        time.sleep(2)

    def set_PayCustInfo(self,payAcessNum):
        '''设置付费客户信息'''
        loc_payAccess = (By.ID,'cond_ACCESS_NUM')
        loc_startDate = (By.ID,'cond_START_TIME')
        btn_check = (By.CSS_SELECTOR,'#snPart > span')
        self.sendkey(loc_payAccess,payAcessNum)
        self.isElementDisplay(btn_check,'click') #点击check
        time.sleep(2)
        self.screen_step('设置付费客户信息')
        # valid_accessMsg = PageAssert(self.driver).assert_ErrPage() #校验号码是否异常
        # if valid_accessMsg:
        #     print('付费号码校验未通过：', valid_accessMsg)
        #     logger.info('付费号码校验未通过:{}'.format(valid_accessMsg))
        # else:
        #     logger.info('付费号码校验通过')
        start_date = time.strftime("%Y-%m-%d")
        self.sendkey(loc_startDate,start_date)

    def choose_operAction(self,operCode):
        '''选择操作类型, 根据operCode判断操作类型
        @operCode = 0 新增
        @operCode = 1 删除
        @operCode = 2 修改
        '''
        loc_select = (By.CSS_SELECTOR,'#operActionPart > span') #选择按钮
        li_add = (By.XPATH,'//*[@id="cond_ACTION_float"]/div[2]/div/div/ul/li[2]') #选择新增link
        li_modify = (By.CSS_SELECTOR,'#cond_ACTION_float > div.content > div > div > ul > li:nth-child(4)') #修改
        li_del = (By.CSS_SELECTOR,'#cond_ACTION_float > div.content > div > div > ul > li:nth-child(3)')
        try:
            if operCode == '0':
                self.isElementDisplay(loc_select, 'click')  # 点击选择
                time.sleep(2)
                # self.isElementDisplay(li_add, 'click')  # 新增操作
                self.find_element_click(li_add)
            elif operCode == '1':
                self.isElementDisplay(loc_select, 'click')  # 点击选择
                time.sleep(2)
                self.find_element_click(li_del)  # 删除操作
            elif operCode == '2':
                self.isElementDisplay(loc_select, 'click')  # 点击选择
                time.sleep(2)
                self.find_element_click(li_modify)  # 修改操作
        except:
            logger.info('传入的operCode参数{}错误，只能传入0,1,2'.format(operCode))

    def set_Payitem(self,itemName):
        '''设置付费帐目'''
        loc_choose = (By.CSS_SELECTOR, '#payItemDiv > div.c_title > div.fn > ul > li')  # 选择按钮
        loc_itemName = (By.ID,'NOTE_ITEM')
        btn_qry = (By.CSS_SELECTOR, '#qryAcctDiv > button')  # 过滤按钮
        # str_xpath = '//*[contains(@item_id,"%s") and contains(@ontap,"chooseNoteItem"]' % itemId  # 传入科目ID
        liItem_loc = (By.CSS_SELECTOR,'#noteItemListPart > ul > li') #根据账目查询结果列表，选择第一个
        self.isElementDisplay(loc_choose, 'click') #点击选择
        logger.info('选择的付费帐务科目：{}'.format(itemName))
        self.sendkey(loc_itemName,itemName)
        self.isElementDisplay(btn_qry, 'click') #点击过滤
        self.screen_step('付费账目信息')
        time.sleep(2)
        self.isElementDisplay(liItem_loc, 'click')  # 选择付费科目，点击确定

    def accept_AddGrprelaAdv(self,groupId,acctId,payAcessNum,itemName='所有费用',operCode='0'):
        '''受理新增集团高级付费关系'''
        title = '新增集团高级付费关系测试记录'
        self.add_dochead(title)
        self.Open_GrprelaAdv(groupId)
        self.choose_grpAcct(acctId) #选择付费账户
        self.set_PayCustInfo(payAcessNum)
        self.choose_operAction(operCode)
        self.set_Payitem(itemName)
        self.isElementDisplay((By.ID,'submitButton'),'click') #点击提交
        submitMsg = PageAssert(self.driver).assert_Submit()  #提交后返回信息，flowId或者报错
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)
        time.sleep(3)

if  __name__ == '__main__':
    print("用例开始执行时间：" + time.strftime("%Y%m%d%H%M%S"))
    driver = webdriver.Chrome()
    test = GrouprelaAdv(driver)
    test.accept_AddGrprelaAdv(groupId='8723410368',acctId='7294060300545854',payAcessNum='13987288386',operCode='0')

    print("用例执行结束时间：" + time.strftime("%Y%m%d%H%M%S"))





