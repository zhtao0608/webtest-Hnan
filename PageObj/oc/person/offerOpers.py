import time
from Base.OperExcel import write_xlsBycolName_append
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait  # 用于处理元素等待
from Base import ReadConfig
from PageObj.ngboss.mainpage import MainPage
from PageObj.ngboss.login_page import LoginPage
from PageObj.ngboss.loginPart import LoginPart
from PageObj.oc.person.PersonBase import PersonBase
from Base.Mylog import LogManager
from Common.Assert import PageAssert


# logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
logger = LogManager('test').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

rc = ReadConfig.ReadConfig("ngboss_config.ini")

class OfferOperPage(PersonBase):
    def open_base(self):
        self.driver.get(rc.get_ngboss('url'))
        self.driver.maximize_window()
        #self.driver.implicitly_wait(30)

    def Loc_Tab(self):
        #套餐
        self.li_MainOffer = self.findele(By.ID,"CategoryPart_tab_li_0")
        self.li_yxhd = self.findele(By.ID,"CategoryPart_tab_li_1")
        self.li_jtsp = self.findele(By.ID,"CategoryPart_tab_li_2")
        self.li_jcfw = self.findele(By.ID,"CategoryPart_tab_li_3")
        self.li_zzfw = self.findele(By.ID,"CategoryPart_tab_li_4")
        self.li_rhsp = self.findele(By.ID,"CategoryPart_tab_li_5")
        self.li_qita = self.findele(By.ID,"CategoryPart_tab_li_6")

    def Open_Offerframe(self):
        '''进入商品订购页面'''
        self.driver.switch_to.default_content()
        loc_frame = self.findele(By.XPATH,"//iframe[contains(@src,'service=page/oc.person.cs.OfferDetail&listener=init')]")
        self.driver.switch_to.frame(loc_frame)
        logger.info("OfferDetail:" + str(loc_frame))
        print("OfferDetail:" + str(loc_frame))
        # time.sleep(12)  #进入商品订购页面非常慢
        self.screen_step('进入商品订购页面')

    def Open_SubOffer(self,accessNum,offerId):
        '''进入商品订购Iframe'''
        self.open_base()
        LoginPage(self.driver).login(rc.get_ngboss('username'), rc.get_ngboss('password'))  # 登录
        loginPart = LoginPart(self.driver)
        loginPart.login_by_pwd(accessNum,'123123') #号码登录
        self.screen_step('搜索商品')
        MainPage(self.driver).search_offerNew(offerId) #根据OfferId搜索并回车进入商品订购Iframe
        self.Open_Offerframe() #进入商品订购Iframe

    def Btn_sub(self):
        '''用显式等待处理，最少时间90s'''
        loc_submit = (By.ID, "CSSUBMIT_BUTTON")
        try:
            ele = WebDriverWait(self.driver, 120, 3).until(EC.presence_of_element_located(loc_submit))
            if self.is_element_displayed(ele):
                ele.click()
        except :
            logger.info('商品详情页面90s没加载成功，直接退出!')
            raise

    def Btn_shoppingCar(self):
        return self.findele(By.ID,"ADD_SHOPPING_CART")

    def input_remark(self,remark):
        """商品订购备注信息"""
        self.findele(By.ID,"REMARKS").send_keys(remark)

    def choose_subOffer(self,subofferList):
        '''可选子商品，如服务等'''
        if subofferList :
            for i in range(len(subofferList)):
                checkbox_offer = 'checkbox_' + subofferList[i]
                logger.info("你选择订购的子商品ID：" , subofferList[i])
                if (checkbox_offer.is_selected()):
                    checkbox_offer.click()
                    continue
        else:
            print('没有传入可选子商品列表')
        return self.driver

    def close(self):
        self.driver.quit()

    def Sub_personOffer(self,accessNum,OfferId,subOfferList=[]):
        '''订购个人商品'''
        title = '个人商品订购测试记录'
        self.add_dochead(title)
        self.Open_SubOffer(accessNum,OfferId) #直接进入商品订购界面
        time.sleep(5)
        self.choose_subOffer(subOfferList)  #可选商品列表
        Loc_submit = ('id', 'CSSUBMIT_BUTTON')
        self.screen_step('点击订购')
        self.isElementDisplay(Loc_submit,'click')
        time.sleep(5)
        logger.info("处理页面返回信息.....")
        submitMsg = PageAssert(self.driver).assert_Submit()  #提交后返回信息，flowId或者报错
        logger.info('===提交后页面返回信息：{}'.format(submitMsg))
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)
        time.sleep(3)

    def assert_OfferOperSubmit(self):
        """针对商品订购订购页面特殊处理，显式等待时间90s"""
        loc_flow = (By.ID, 'flowId')
        Loc_msg = (By.XPATH,"//*[@class='c_msg c_msg-h c_msg-phone-v c_msg-full c_msg-error' and not(contains(@style,'display: none'))]/div/div[2]/div[1]/div[2]")
        try:
            ele = WebDriverWait(self.driver, 90, 1).until(EC.presence_of_element_located(Loc_msg))
            flag = self.is_element_displayed(ele)
            if flag:
                errmsg = self.get(Loc_msg)
                logger.info('提交失败，错误信息：' + errmsg)
                print('提交失败，错误信息：' + errmsg)
                self.screen_step('业务受理失败：{}'.format(errmsg))
                submitMsg = '业务受理失败：' + errmsg
            else:
                ele_flowId = WebDriverWait(self.driver, 90, 2).until(EC.presence_of_element_located(loc_flow))
                flowId = ele_flowId.text
                logger.info("业务受理成功，交互流水：" + flowId)
                print("业务受理成功，交互流水：" + flowId)
                self.screen_step('业务受理成功，交互流水：{}'.format(flowId))
                submitMsg = '业务受理成功：' + flowId
        except :
            logger.info('业务提交异常!')
            submitMsg = '业务提交异常'
        return submitMsg

    def assert_OfferOpersubmitAfter(self,file,row,index=0):
        '''
        测试结果写入xls，按xls模板已将flowId 和errmsg列指定了
        :param file: xls完整路径
        :param row: xls行号
        :param index: xls的sheet页index
        :return:
        '''
        try:
            Msg = self.assert_OfferOperSubmit()
            if '业务受理成功' in Msg:
                logger.info("业务受理成功，交互流水号写入xls中FLOWID列")
                write_xlsBycolName_append(file, row, 'FLOWID', Msg,index)  #向xls模板指定行列写入结果
            elif '业务受理失败' in Msg:
                logger.info("业务受理失败，错误信息写入xls中RESULT_INFO列")
                write_xlsBycolName_append(file, row, 'RESULT_INFO', Msg,index)  #向xls模板指定行列写入结果
        except :
            logger.info("测试结果写入xls发生异常！")
            Msg = '测试异常'
            write_xlsBycolName_append(file, row, 'RESULT_INFO', '测试异常', index)  # 向xls模板指定行列写入结果
        return Msg

if __name__ == '__main__':
    driver = webdriver.Chrome()
    test = OfferOperPage(driver)
    # test.Sub_personOffer('13887258227','99091283')
    test.Sub_personOffer('13887027547','99091283')



    # try:
    # loc_flow = (By.XPATH,'/html/body/div[3]/div[2]/div[2]/div[1]/div[2]/span')
    # err = (By.CSS_SELECTOR,'#wade_messagebox-2_ct > a')
    # if (OfferOperPage(driver).isElementExist(loc_flow)):
    #     FlowId = OfferOperPage(driver).get(loc_flow)
    #     print("业务受理成功，交互流水号：" + FlowId)
    # else:
    #     msg = OfferOperPage(driver).get(err)
    #     print("提交失败，错误信息：：" + msg)
    driver.close()













