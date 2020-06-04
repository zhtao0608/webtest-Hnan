import time,sys
from Base.base import Base
from selenium.webdriver.common.by import By
from selenium import webdriver
from Common import ReadConfig
from PageObj.mainpage import MainPage
from PageObj.login_page import LoginPage
from PageObj.loginPart import LoginPart
from Common.Mylog import LogManager
from Common.Assert import PageAssert
from Base.GenTestData import GenTestData
# logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
logger = LogManager('PersonBase').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
rc = ReadConfig.ReadConfig("ngboss_config.ini")

class PersonBase(Base):
    '''公共方法'''
    def open_base(self):
        self.driver.get(rc.get_ngboss('url'))
        self.driver.maximize_window()
        #self.driver.implicitly_wait(30)

    def Open_PersonMenu(self,accessNum,password,cataMenuId,menuId):
        '''
        :param accessNum: 认证号码
        :param password: 号码服务密码
        :param cataMenuId: 菜单目录Id
        :param menuId: 个人业务菜单
        :return:
        '''
        self.open_base()
        LoginPage(self.driver).login(rc.get_ngboss('username'), rc.get_ngboss('password'))  # 登录
        LoginPart(self.driver).login_by_pwd(accessNum,password) #号码登录
        main = MainPage(self.driver)
        main.open_OcCataMenu('crm9000',cataMenuId)
        self.screen_step('打开菜单')
        main.Open_menu(menuId)
        print('进入菜单ID：{}'.format(menuId))
        time.sleep(5)


    def valid_IdenNr(self,idennr):
        '''输入证件号，点击校验按钮'''
        loc_IDENNR = (By.ID,'IDEN_NR') #证件号
        btn_check = (By.ID,'checkIsOneCardManyNumsButton')
        self.sendkey(loc_IDENNR,idennr)
        time.sleep(2)
        ele_btnCheck = self.find(btn_check)
        ele_btnCheck.click()
        ele_btnCheck.click()
        time.sleep(3)
        #判断是否校验通过
        validMsg = PageAssert(self.driver).assert_WarnPage() #不管校验是否通过都点击了确认按钮
        logger.info('一证五号校验结果:' + validMsg)

    def Input_validIdenNrNew(self):
        '''输入证件号，点击校验按钮,直到校验通过'''
        while True:
            loc_IDENNR = (By.ID, 'IDEN_NR')  # 证件号
            idennr = GenTestData().Create_Idcard()  # 自动生成一个证件号码
            logger.info('证件号码:{}'.format(idennr))
            print('证件号码:{}'.format(idennr))
            self.sendkey(loc_IDENNR, idennr)
            self.move_element_enter(loc_IDENNR)
            time.sleep(3)
            # 判断是否校验通过
            validMsg = PageAssert(self.driver).assert_WarnPage()  # 不管校验是否通过都点击了确认按钮
            logger.info('证件号：{}校验结果:{}'.format(idennr, validMsg))
            if '校验通过' in validMsg:
                break

    def vaild_BusiRule(self):
        '''业务规则校验,进入菜单时'''
        Msg = PageAssert(self.driver).assert_error()
        if '业务校验失败' in Msg:
            print('业务规则校验结果：{}'.format(Msg))
            logger.info('业务规则校验结果：{}'.format(Msg))
            self.screen_step('业务校验')
        elif '校验通过' in Msg:
            Msg = PageAssert(self.driver).assert_SucPage()  # 校验通过要确认后才能继续办理
            if '没有弹出成功提示' in Msg:
                Msg = PageAssert(self.driver).assert_WarnPage() #警告信息
                if '警告校验通过' in Msg:
                    Msg = PageAssert(self.driver).assert_HelpPage() #帮助信息
        return Msg

    def close_UIstep(self):
        '''关闭操作导航'''
        Btn_msg = (By.CSS_SELECTOR,'#UI-step1 > div > div.fn > button:nth-child(1)')
        self.isElementDisplay(Btn_msg,'click') #出现步骤引导弹窗，直接关闭
        return self.driver