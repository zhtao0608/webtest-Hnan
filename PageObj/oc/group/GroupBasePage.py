import time
from Base.base import Base
from selenium.webdriver.common.by import By
from Base import ReadConfig
from PageObj.mainpage import MainPage
from PageObj.login_page import LoginPage
from PageObj.loginPart import LoginPart
from Base.Mylog import LogManager
from Common.Assert import PageAssert

# logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
logger = LogManager('test').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

rc = ReadConfig.ReadConfig("ngboss_config.ini")

class BasePage(Base):
    '''公共方法'''
    def open_base(self):
        self.driver.get(rc.get_ngboss('url'))
        self.driver.maximize_window()
        #self.driver.implicitly_wait(30)

    def Open_groupMenu(self,groupId,parentMenuId,MenuId):
        '''选择集团菜单，点击进入'''
        self.open_base()
        LoginPage(self.driver).login(rc.get_ngboss('username'), rc.get_ngboss('password'))  # 登录
        LoginPart(self.driver).login_by_groupId(groupId)
        main = MainPage(self.driver)
        main.open_OcCataMenu('crm8000', parentMenuId)
        # self.screen_step('选择对应集团菜单')
        main.Open_menu(MenuId)

    def vaild_GroupBusiRule(self):
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

    def Open_GrpBusiOrd(self,groupId):
        self.open_base()
        LoginPage(self.driver).login(rc.get_ngboss('username'), rc.get_ngboss('password'))  # 登录
        LoginPart(self.driver).login_by_groupId(groupId)
        main = MainPage(self.driver)
        main.open_OcCataMenu('crm8000','crm8100')
        self.screen_step('选择集团商品受理菜单，点击打开')
        main.Open_menu('crm8109')
        self.Open_Grpsubframe()  # 进入集团订购iframe
        self.screen_step('进入集团商品业务受理菜单')

    def Open_GrpMebBusiOrd(self,groupId):
        self.open_base()
        LoginPage(self.driver).login(rc.get_ngboss('username'), rc.get_ngboss('password'))  # 登录
        LoginPart(self.driver).login_by_groupId(groupId)
        main = MainPage(self.driver)
        main.open_OcCataMenu('crm8000','crm8100')
        main.Open_menu('crm8108')
        self.Open_GrpMebBusiframe()  # 进入集团成员业务受理iframe
        self.screen_step("打开成员商品业务受理菜单")


    def Open_Grpsubframe(self):
        '''进入集团商品订购iFrame处理'''
        self.driver.switch_to.default_content()
        loc_frame = self.find((By.XPATH,"//iframe[contains(@src,'/ordercentre/ordercentre?service=page/oc.enterprise.cs.OperGroupUser')]"))
        self.driver.switch_to.frame(loc_frame)
        logger.info("OperGroupUser:" + str(loc_frame))
        print("OperGroupUser:" + str(loc_frame))
        self.iframe(0)
        time.sleep(2)
        Btn_msg = self.find((By.CSS_SELECTOR,'#UI-step1 > div > div.fn > button:nth-child(1)'))
        Btn_msg.click()
        self.driver.switch_to.parent_frame()  # 切换到父iframe 回到集团商品订购iframe
        time.sleep(5)
        return self.driver

    def click_SelGrpOffer(self):
        '''集团商品受理页面点击选择按钮'''
        li_sel = (By.XPATH,'//li[contains(@ontap,"initOfferPopupItem")]')
        self.screen_step('点击选择按钮')
        self.find(li_sel).click()
        time.sleep(2)
        return self.driver

    def Choose_mainOfferandSub(self,offerId):
        '''选择主商品，点击订购'''
        #暂时还有点问题，目前用搜索商品代替更简单
        str_xpath = '//*[@id="cata_%s_null"]/div[2]/button' %str(offerId)
        print(str_xpath)
        Loc_subBtn = self.find((By.XPATH,str_xpath ))
        print("Loc_subBtn元素:" + str(Loc_subBtn))
        Loc_subBtn.click()
        return self.driver

    def click_BtnGrpOrded(self):
        '''点击集团已订购按钮'''
        li_Orded = (By.ID,'10012')
        if self.isElementExist(li_Orded):
            self.find(li_Orded).click()
            time.sleep(10)
        return self.driver

    def deal_GrpPriEYE(self):
        '''公共方法：处理集团智慧眼，如果显示在页面上则直接关闭，否则跳过'''
        self.driver.switch_to.default_content()
        loc_PRI_EYE = (By.XPATH, '//*[@id="PRI_EYE"]')
        flag = 'block' in self.get(loc_PRI_EYE,Type='attribute',name='style')
        print("=======展示style属性是否展示：" ,flag)
        if flag:
            btn_PRI_EYE = (By.XPATH, '//button[contains(@onclick,"closePRI_EYE")]')
            logger.info('====集团认证时弹出了智慧眼弹窗====')
            self.isElementDisplay(btn_PRI_EYE,'click')
            time.sleep(1)
        else:
            print("=========跳过=============")
            pass

    def click_BtnMebSub(self):
        '''点击可订购按钮'''
        li_subOrder = (By.ID,'10013')
        try :
            self.isElementExist(li_subOrder,'click')
            self.screen_step("点击订购按钮")
            time.sleep(10)
        except:
            self.screen_step("执行失败")
            self.save_docreport()
            self.close()
        return self.driver

    def click_BtnMebOrded(self):
        '''点击成员已订购按钮'''
        li_Orded = (By.ID,'10014')
        if self.isElementExist(li_Orded):
            self.find(li_Orded).click()
            time.sleep(10)
        return self.driver

    def choose_grpOfferandsub(self,grpofferid,offerinsid):
        '''在可订购商品列表中选择集团商品点击订购
        :param grpofferid: 集团已订购商品OfferId
        :param offerinsid: 集团已订购商品OfferInstid
        :return:
        '''
        strsub = grpofferid + '_' + offerinsid
        print("拼接的集团已订购商品：" + strsub)
        str_xpth = '//*[@id="cata_%s"]/div[2]/button/span[2]' % strsub   #构造已订购集团商品
        loc_sub = (By.XPATH,str_xpth)
        if self.isElementExist(loc_sub):
            self.find(loc_sub).click()   #点击订购按钮
            time.sleep(10)
        else:
            print('没找到集团已订购商品，无法成员商品订购')

    def search_grpOffer(self,mainOffer):
        '''搜索商品，mainOffer可以是商品ID也可以是商品名称'''
        # self.find((By.ID,'searchkeyWord')).send_keys(mainOffer)
        self.sendkey((By.ID,'searchkeyWord'),mainOffer)
        self.screen_step("搜索集团商品")
        self.find_element_click((By.ID,'searchsearchButton'))
        time.sleep(2)
        self.find((By.XPATH,'//*[@id="searchOfferResultsearchResult"]/li')).click()
        time.sleep(3)

    def set_mainOffer(self,offerId):
        '''主商品点击设置'''
        str_xpath = '//*[@id="li_%s"]/div/div[2]/span' %str(offerId)
        self.find((By.XPATH,str_xpath)).click()
        time.sleep(5)
        return self.driver

    def choose_grpOfferandCancel(self,grpofferid,offerinsid):
        '''在可订购商品列表中选择集团商品点击注销按钮
        :param grpofferid: 集团已订购商品OfferId
        :param offerinsid: 集团已订购商品OfferInstid
        :return:
        '''
        strsub = grpofferid + '_' + offerinsid
        logger.info("拼接的集团已订购商品：" + strsub)
        str_xpth = '//*[@id="cata_%s"]/div[2]/button[2]/span[2]' % strsub   #构造已订购集团商品
        loc_cancel = (By.XPATH,str_xpth)
        if self.isElementExist(loc_cancel):
            self.find_element_click(loc_cancel) #点击注销按钮
            time.sleep(3)
            vaildMsg = PageAssert(self.driver).assert_error() #校验下是否出现错误
            if '业务校验失败' in vaildMsg:
                logger.info('注销时报错:{}'.format(vaildMsg))
                self.quit_browse()
        else:
            logger.info('没找到集团已订购商品，无法成员商品注销')
            self.quit_browse()
        return self.driver

    def choose_OptionalOffer(self,subofferId):
        '''页面checkBox，传入subofferId，如果可选则选择'''
        check_box_offer = (By.ID,subofferId)
        try :
            if not self.isSelected(check_box_offer):
                self.find_element_click(check_box_offer)
        except:
            print('没有可以选择的子商品')
            pass
        return self.driver

    def set_subOffer(self,subOffer):
        '''ADC等子商品待设置按钮'''
        str_xpth = '//*[@id="div_%s"]/div[1]/div[2]/span' %subOffer
        loc_setsubOffer = (By.XPATH,str_xpth)
        flag = self.isElementExist(loc_setsubOffer)
        print("是否显示子商品待设置",flag)
        if not flag:
            pass # 不用设置，直接跳过
        else:
            self.isElementDisplay(loc_setsubOffer,'click')
            time.sleep(2)
        return self.driver

    """=====================集团成员操作====================="""
    def Open_GrpMebBusiframe(self):
        '''进入集团商品订购iFrame处理'''
        self.driver.switch_to.default_content()
        loc_frame = self.find((By.XPATH,"//iframe[contains(@src,'/ordercentre/ordercentre?service=page/oc.enterprise.cs.OperGroupMember')]"))
        self.driver.switch_to.frame(loc_frame) #进入集团成员商品业务
        logger.info("OperGroupMeb:" + str(loc_frame))
        print("OperGroupMeb:" + str(loc_frame))
        time.sleep(3)
        return self.driver

    def set_MebsubOffer(self,subOffer):
        '''成员子商品待设置按钮'''
        str_css1 = '#li_%s > div > div.side > span' %subOffer
        str_css2 = '#div_%s > div.group.link > div.side > span' %subOffer
        loc_css1 = (By.CSS_SELECTOR,str_css1)
        loc_css2 = (By.CSS_SELECTOR,str_css2)
        try:
            if self.is_element_located(loc_css1):
                logger.info('找到元素，元素为：' + str_css1)
                self.find_element_click(loc_css1)
            elif self.is_element_located(loc_css2):
                logger.info('找到元素，元素为：' + str_css2)
                self.find_element_click(loc_css2)
        except:
            logger.info('没有找到待设置元素！成员子商品待设置失败')
            raise


    """=====================集团成员操作====================="""
    def submit_prodSpec(self):
        '''产品规格特征设置点击完成'''
        loc_submit = (By.ID, 'pam_Button_submit')
        try:
            flag = self.isElementDisplay(loc_submit)
            print("是否显示子商品待设置完成按钮：", flag)
            if not flag:
                # self.find_element_click((By.ID,'Button'))
                self.isElementDisplay((By.ID,'Button'),'click')
            else:
                self.find_element_click(loc_submit)
                time.sleep(2)
        except:
            raise

    def submit_offerSpec(self,subOfferList):
        loc_submit = (By.ID ,'pam_Button_submit')
        loc_Btn = (By.ID, 'Button')
        if self.isElementExist(loc_submit):
            inner_submit = self.find(loc_submit)
            print("找到了submit" + str(inner_submit))
            time.sleep(3)
            inner_submit.click()
            time.sleep(2)
            for i in range(len(subOfferList)):
                self.choose_OptionalOffer(subOfferList[i])  #商品设置确认提交前，判断是否有可选商品，有则选中checkbox
            out_submit = self.find((By.XPATH,'//*[@id="productPopupItem"]/div[3]/button[2]'))
            out_submit.click()
        elif self.isElementExist(loc_Btn):   #这里主要是考虑多媒体桌面电话
            self.find_element_click(loc_Btn)
            time.sleep(2)
            self.sendEnter()
            self.find_element_click((By.XPATH,'//*[@id="productPopupItem"]/div[3]/button[2]'))
        else:
            self.find_element_click((By.XPATH,'//*[@id="productPopupItem"]/div[3]/button[2]'))
            self.find_element_click((By.XPATH,'//*[@id="productPopupItem"]/div[3]/button[2]'))
        return self.driver

    def set_OfferSpec(self,subOfferList):
        '''设置商品规格特征'''
        #先点击是商品设置->产品规格->待设置：先判断是否要进行商品规格设置，如果不显示待设置则不需要设置，否则进入待设置页面
        loc_offerspec = (By.XPATH,'//*[@id="prodSpecUL"]/li/div[2]/span')
        if self.find(loc_offerspec).is_displayed(): #待设置是否显示
            print("进入商品规格设置......")
            self.find((By.XPATH,'//*[@id="prodSpecUL"]/li/div[2]/span')).click() #进入商品规格设置
            ##ADC商品规格没有需要操作的步骤，直接提交，后续根据实际情况添加
            self.submit_offerSpec(subOfferList)
            time.sleep(5)
        else:   #没有商品待设置，直接点击确定
            print("不需要设置商品规格特征")
            self.submit_offerSpec(subOfferList)

    def confirm_OfferSpec(self):
        '''商品设置下点击确定'''
        loc_confirm = (By.XPATH,'//*[@id="productPopupItem"]/div[3]/button[2]')
        flag = self.isElementDisplay(loc_confirm)
        print("是否显示确认完成按钮：", flag)
        if not flag:
            pass  # 不用设置，直接跳过
        else:
            self.isElementDisplay(loc_confirm, 'click')
            time.sleep(2)
        return self.driver

    def set_prodSpec(self):
        '''主服务设置后点击完成'''
        Btn_prodSpec = (By.CSS_SELECTOR,'#prodSpecUL > li > div.side > span')
        self.find_element_click(Btn_prodSpec)
        time.sleep(3)
        return self.driver

    def submit_prodSpec(self):
        '''商品设置点击完成'''
        loc_submit = (By.ID, 'pam_Button_submit')
        flag = self.isElementDisplay(loc_submit)
        print("是否显示确认完成按钮：", flag)
        if not flag:
            pass  # 不用设置，直接跳过
        else:
            self.isElementDisplay(loc_submit, 'click')
            time.sleep(2)
        return self.driver

    def Open_SubmitAll(self):
        submit = self.find((By.XPATH,'//*[@id="OpenSubmit"]/button[2]'))
        self.js_scrollIntoView(submit)
        submit.click()
        time.sleep(10)
        return self.driver

    def Del_SubmitAll(self):
        submit = self.find((By.XPATH,'//*[@id="DelSubmit"]/button[1]'))
        self.js_scrollIntoView(submit)
        submit.click()
        time.sleep(10)
        return self.driver


    def close(self):
        self.driver.quit()


