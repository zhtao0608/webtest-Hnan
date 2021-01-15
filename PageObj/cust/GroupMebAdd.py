import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from Base import ReadConfig
from Base.Mylog import LogManager
from PageObj.ngboss.login_page import LoginPage
from PageObj.ngboss.mainpage import MainPage
from PageObj.cust.CustomerBase import CustBasePage
from Check.PageCheck import PageAssert

# logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
logger = LogManager('GroupMebAdd').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log')
rc = ReadConfig.ReadConfig("ngboss_config.ini")

class GroupMebAdd(CustBasePage):
    def open_base(self):
        self.driver.get(rc.get_ngboss('url'))
        self.driver.maximize_window()

    def Open_GroupMebAddFrame(self):
        self.driver.switch_to.default_content()
        loc_frame = self.find((By.XPATH,"//iframe[contains(@src,'/customercentre/customercentre?service=page/customer.cs.entmembermgr.addmember.AddEnterpriseMember')]"))
        self.driver.switch_to.frame(loc_frame)
        logger.info("GrpMebAdd:" + str(loc_frame))
        print("GrpMebAdd:" + str(loc_frame))

    def qry_GroupMebInfoByAccessNum(self,AccessNum):
        '''根据服务号码查询集团成员'''
        text_accessNum = (By.ID,'cond_ACCESS_NUM')
        self.input(text_accessNum,AccessNum)
        Btn_qry = (By.CSS_SELECTOR,'#QryPart > div > div > div.info > div > div:nth-child(3) > span > button')
        self.find_element_click(Btn_qry)
        self.sleep(2)
        vaildMsg = PageAssert(self.driver).assert_WadePage() #校验
        logger.info('集团成员校验信息:{}'.format(vaildMsg))
        return vaildMsg

    def qry_GroupInfo(self,groupId):
        '''查询集团客户信息'''
        Btn_qry = (By.CSS_SELECTOR,'#QryGroupInfoPart > div.l_queryFn > div > div.right > div > button')
        input_groupID = (By.ID,'cond_GROUP_ID2')
        Btn_query = (By.CSS_SELECTOR,'#popupt > div.c_scroll.c_scroll-float.c_scroll-header > div > div.c_submit.c_submit-full > button')
        self.find_element_click(Btn_qry)
        self.sleep(1)
        self.input(input_groupID,groupId)
        self.sleep(1)
        self.find_element_click(Btn_query)
        self.sleep(5)
        qryVaildMsg = PageAssert(self.driver).assert_WadePage()
        logger.info('查询校验信息:{}'.format(qryVaildMsg))
        loc_groupInfo= (By.XPATH,'//*[@id="groupinfosTable"]/div[1]/div/table/tbody/tr/td[2]/a') #找到集团编码
        try :
            GroupId = self.get_attribute(loc_groupInfo,name='groupid')
            logger.info('===页面显示的GroupId:{}'.format(GroupId))
            if GroupId == groupId :
                self.find_element_click(loc_groupInfo)
            else:
                logger.info('查询失败!')
        except:
            print('根据集团编码未获取集团信息，测试失败!')
            logger.info('根据集团编码未获取集团信息，测试失败!')

    def set_groupMebRela(self,groupId):
        '''设置集团成员关系'''
        li_setRela = (By.XPATH,'//*[@id="EditPart"]/div/div[17]/ul/li')
        # text_groupId = (By.ID,'GROUP_ID')
        btn_check = (By.XPATH,'//*[@id="groupRel"]/div[2]/div/div[2]/ul/li[1]/div[2]/span/span')
        self.find_element_click(li_setRela)
        self.sleep(1)
        self.find_element_click(btn_check)
        self.sleep(2)
        self.qry_GroupInfo(groupId)  #查询集团
        self.find((By.ID,'MEMBER_BELONG_span')).click()#点击成员归属
        self.sleep(1)
        self.find((By.XPATH,'//*[@id="MEMBER_BELONG_float"]/div[2]/div/div/ul/li[2]')).click() #网内成员
        self.sleep(1)
        self.find((By.ID,'MEMBER_KIND_span')).click()  #点击成员类型
        self.sleep(1)
        self.find((By.XPATH,'//*[@id="MEMBER_KIND_float"]/div[2]/div/div/ul/li[2]')).click() #一般成员
        self.find((By.ID,'MEMBER_RELA_span')).click()
        self.sleep(1)
        self.find((By.XPATH,'//*[@id="MEMBER_RELA_float"]/div[2]/div/div/ul/li[2]')).click() #成员关系->雇佣关系
        self.find((By.ID,'MEMBER_PROPERTY_span')).click()
        self.sleep(1)
        self.find((By.XPATH,'//*[@id="MEMBER_PROPERTY_float"]/div[2]/div/div/ul/li[2]')).click()
        Btn_confirm = (By.CSS_SELECTOR,'#groupRel > div.c_scroll.c_scroll-float.c_scroll-header > div > div.c_submit.c_submit-full > button')
        self.find(Btn_confirm).click() #点击确认

    def submiyAll(self):
        self.find_element_click((By.ID,'submitButton'))


if __name__ == '__main__':
    print("用例开始执行时间：" + time.strftime("%Y%m%d%H%M%S"))
    driver = webdriver.Chrome()
    test =GroupMebAdd(driver)
    test.open_base()
    MainPage(driver).open_CataMenu(0,'crm5000','crm5300','crm5217')
    test.Open_GroupMebAddFrame()
    test.qry_GroupMebInfoByAccessNum('18808723367')
    test.set_groupMebRela('8723403452')
    test.submiyAll()
    PageAssert(self.driver).assert_WadePage()

