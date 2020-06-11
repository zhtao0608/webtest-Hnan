import time
from Base.base import Base
from selenium.webdriver.common.by import By
from selenium import webdriver
from Base import ReadConfig
from PageObj.ngboss.login_page import LoginPage
from Base.Mylog import LogManager
from Common.Assert import PageAssert
from Base.OperExcel import write_xlsBycolName_append

logger = LogManager('login').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
rc = ReadConfig.ReadConfig("ngboss_config.ini")

class LoginPart(Base):
    def open_base(self):
        self.driver.get(rc.get_ngboss('url'))
        self.driver.maximize_window()
        #self.driver.implicitly_wait(30)

    def input_accessnum(self,number):
        input_accessNum = (By.ID,"LOGIN_NUM")
        self.sendkey(input_accessNum,number)
        return self.driver

    def input_pwd(self,password):
        input_password = (By.ID,"LOGIN_VAL")
        self.sendkey(input_password,password)
        return self.driver

    def button_login(self):
        loc_btn = (By.ID,"LOGIN_BTN")
        self.isElementExist(loc_btn,'click')
        return self.driver

    def close_MyMobile(self):
        loc_ele = (By.XPATH, "/html/body/div[2]/div[4]/ul/li/div[2]/div[2]")
        self.isElementExist(loc_ele,'click')
        return self.driver

    def login_by_pwd(self,number,password):
        self.driver.switch_to.default_content()
        self.input_accessnum(number)
        self.input_pwd(password)
        self.button_login()
        time.sleep(3)
        self.close_MyMobile()  # 关闭我的移动
        ##先屏蔽这段，加快调试！
        # try :
        #     assertMsg = PageAssert(self.driver).assert_ErrPage() #登录的时候校验下是否错误
        #     if not assertMsg:
        #         self.close_MyMobile() #如果正常直接关闭我的移动
        #     else:
        #         self.screenshot_SaveAsDoc('号码登录时校验失败')
        #         logger.info('号码登录校验失败：{}'.format(assertMsg))
        #         time.sleep(1)
        #         # data_file = ReadConfig.find_Newfile(dir=ReadConfig.get_data_path())
        #         # PageAssert(self.driver).write_vaildErrPageResult(file=data_file,row=0)
        #         # write_xlsBycolName_append(file=data_file, row=0, colName='RESULT_INFO', value=assertMsg, index=0)
        #         self.quit_browse()
        # except:
        #     logger.info('校验异常失败')
        # return self.driver

    def deal_PRIEYE(self):
        loc_PRI_EYE = (By.XPATH, '//*[@id="PRI_EYE"]')
        flag = 'block' in self.get(loc_PRI_EYE,Type='attribute',name='style')
        print("=======js展示style属性是否展示：" + str(flag))
        if flag:
            btn_PRI_EYE = (By.XPATH, '//button[contains(@onclick,"closePRI_EYE")]')
            self.find(btn_PRI_EYE).click()  # 如果有直接关闭页面再操作
            time.sleep(1)
        else:
            print("=========跳过=============")
            pass

    def login_by_groupId(self,groupid):
        self.isElementExist((By.ID,"groupFn"),'click')
        time.sleep(2)
        self.sendkey((By.ID,"groupQueryTypeValueInput"),groupid)
        Btn_qry = (By.CSS_SELECTOR,"#groupLogin > div.submit > button:nth-child(2)")
        self.isElementExist(Btn_qry,'click')
        time.sleep(3)
        self.isElementExist((By.XPATH,'//*[@id="groupList"]/div[1]/div[2]/ul/li'),'click')
        time.sleep(5)
        assertMsg = PageAssert(self.driver).assert_ErrPage() #登录的时候校验下是否错误
        if not assertMsg:
            self.deal_PRIEYE() #如果正常直接关闭我的移动
        else:
            logger.info('集团登录校验失败：{}'.format(assertMsg))
        return self.driver

if __name__ == '__main__':
    driver = webdriver.Chrome()
    test = LoginPart(driver)
    test.open_base()
    LoginPage(driver).login(rc.get_ngboss('username'),rc.get_ngboss('password'))  #登录
    test.login_by_groupId('8711200069') #有智慧眼的测试集团
    # test.login_by_pwd('8711200069','111314') #有智慧眼的测试集团

    # driver.close()
    # test.login_by_groupId('8763808741')


