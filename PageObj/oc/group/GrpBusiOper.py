import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from Base import ReadConfig
from Base.Mylog import LogManager
from PageObj.oc.group.GroupBasePage import BasePage
from Common.Assert import PageAssert
from Base.OperExcel import write_excel_append
# logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
rc = ReadConfig.ReadConfig("ngboss_config.ini")

class GroupBusiOper(BasePage):
    def open_base(self):
        # self.driver = webdriver.Chrome()
        # self.driver.get(config_url())
        self.driver.get(rc.get_ngboss('url'))
        self.driver.maximize_window()
        #self.driver.implicitly_wait(30)

    def input_ADC_ECGN_ZH(self,signName):
        '''设置中文签名'''
        loc_ECGN_ZH = self.find((By.ID,'pam_TEXT_ECGN_ZH'))
        print("找到中文签名：" + str(loc_ECGN_ZH))
        self.js_scrollIntoView(loc_ECGN_ZH)
        loc_ECGN_ZH.send_keys(signName)
        return self.driver

    def input_ADC_ManagePhoneNum(self,accessNum):
        '''设置管理员手机号'''
        loc_phone = self.find((By.ID,'pam_MANAGER_PHONE_NUM'))
        time.sleep(2)
        self.js_scrollIntoView(loc_phone) #拖动到页面底部
        loc_phone.click()
        loc_phone.send_keys(accessNum)
        return self.driver

    def submit_subOfferProdSpec(self):
        '''子商品规格特征设置完成（ADC）'''
        self.find((By.ID,'pam_BUTTON_SRV_PLAT')).click()
        time.sleep(2)
        return self.driver

    def sel_GrpRemoveReason(self):
        '''集团商品销户元素'''
        loc_reason = (By.CSS_SELECTOR,'#cond_REMOVE_REASON_span > span')
        self.find(loc_reason).click()
        loc_idx5 = (By.CSS_SELECTOR,'#cond_REMOVE_REASON_float > div.content > div > div > ul > li:nth-child(6)')
        self.find(loc_idx5).click() #选择不必要使用该产品
        return self.driver

    def input_CancelRemark(self,remark):
        '''输入集团商品注销备注'''
        loc_remark = (By.ID,'cond_REMARK')
        self.find(loc_remark).send_keys(remark)
        return self.driver

    def Cancel_GrpOrder(self,groupId,offerid,offerInsId,remark):
        '''
        :param groupId:
        :param offerid:
        :param subOfferList:
        :return:
        '''
        title = '集团商品业务注销测试记录'
        self.add_dochead(title)
        self.Open_GrpBusiOrd(groupId)
        self.click_SelGrpOffer()
        self.screen_step('选择要注销的集团商品实例')
        self.choose_grpOfferandCancel(offerid,offerInsId)
        self.screen_step('录入商品注销原因和备注')
        self.sel_GrpRemoveReason()
        time.sleep(2)
        self.input_CancelRemark(remark)
        self.screen_step('点击注销提交')
        self.Del_SubmitAll()
        submitMsg = PageAssert(self.driver).assert_Submit()
        logger.info('业务受理信息：{}'.format(submitMsg))
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)

    def Open_GrpADC(self,groupId,offerid,subOfferList,accessNum,singname):
        '''
        :param groupId: 集团编码
        :param offerid: 集团主商品Offer_id
        :param subOfferList: 订购的子商品列表 subOffers
        :param accessNum: ADC平台属性中设置的管理员手机号属性值
        :param singname: ADC平台属性中设置的中文签名属性值
        :return: 成功返回交互流水号，失败返回错误信息
        '''
        title = '集团商品业务订购测试记录'
        # self.doc.add_heading(u'集团商品业务订购测试记录', level=1)
        self.add_dochead(title)
        self.Open_GrpBusiOrd(groupId)
        self.search_grpOffer(offerid)
        self.screen_step("点击集团商品待设置按钮")
        self.set_mainOffer(offerid) #商品订购主页点击待设置
        print("商品设置开始......")
        logger.info("商品设置开始")
        self.screen_step("设置集团商品规格特征")
        self.set_OfferSpec(subOfferList) #商品设置下点击确定,判断是否需要点击商品待设置
        print("商品设置完成......")
        logger.info("商品设置完成")
        for i in range(len(subOfferList)):
            logger.info("子商品编码subofferId=" + subOfferList[i])
            logger.info("设置子商品......")
            logger.info("开始设置子商品产品规格特征" + subOfferList[i])
            self.screen_step("点击集团子商品_%s待设置按钮" % subOfferList[i])
            self.set_subOffer(subOfferList[i]) #子商品点击设置
            self.screen_step("进入子商品_%s产品规格特征设置页面" % subOfferList[i])
            self.set_prodSpec()  #产品规格点击待设置
            self.input_ADC_ECGN_ZH(singname)
            self.input_ADC_ManagePhoneNum(accessNum)
            self.screen_step("ADC平台产品属性设置完成，点击确认")
            self.submit_subOfferProdSpec() #点击确认
            self.submit_subOfferProdSpec() #不知道是否再次提交一次
            logger.info("子商品产品规格特征设置结束" + subOfferList[i])
            self.screen_step("点击确认，完成集团商品订购设置")
            self.confirm_OfferSpec() #商品设置再确认
        self.screen_step("点击商品提交按钮")
        self.Open_SubmitAll()#商品订购提交
        print("处理页面返回信息.....")
        submitMsg = PageAssert(self.driver).assert_Submit()
        logger.info('业务受理信息：{}'.format(submitMsg))
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)

    def Open_GrpVpmn(self,groupId,offerid,subOfferList):
        '''
        :param groupId: 集团编码
        :param offerid: 集团主商品Offer_id
        :param subOfferList: 订购的子商品列表 subOffers
        :param accessNum: ADC平台属性中设置的管理员手机号属性值
        :param singname: ADC平台属性中设置的中文签名属性值
        :return: 成功返回交互流水号，失败返回错误信息
        '''
        title = 'VPMN集团商品订购'
        self.add_dochead(title)
        self.Open_GrpBusiOrd(groupId)
        self.search_grpOffer(offerid)
        self.set_mainOffer(offerid) #商品订购主页点击待设置
        self.screen_step('设置集团VPMN商品')
        logger.info("商品设置开始")
        self.set_OfferSpec(subOfferList) #商品设置下点击确定,判断是否需要点击商品待设置
        print("设置子商品......")
        logger.info("设置子商品")
        for i in range(len(subOfferList)):
            print("子商品编码subofferId=" + subOfferList[i])
            print("先选择子商品，再设置子商品......")
            logger.info("开始设置子商品产品规格特征" + subOfferList[i])
            self.screen_step('设置子商品产品规格特征_%s' %subOfferList[i])
            self.set_subOffer(subOfferList[i]) #子商品点击设置
            self.set_prodSpec()  #产品规格点击待设置
            self.submit_prodSpec()
            logger.info("子商品产品规格特征设置结束" + subOfferList[i])
            self.screen_step('商品设置完成')
            self.confirm_OfferSpec() #商品设置再确认
        self.screen_step('点击提交按钮')
        self.Open_SubmitAll()#商品订购提交
        print("处理页面返回信息.....")
        logger.info("处理页面返回信息......")
        submitMsg = PageAssert(self.driver).assert_Submit()
        logger.info('业务受理信息：{}'.format(submitMsg))
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)


if __name__ == '__main__':
    print("用例开始执行时间：" + time.strftime("%Y%m%d%H%M%S"))
    driver = webdriver.Chrome()
    test = GroupBusiOper(driver)

    # test.Open_GrpADC('8763809359','6480',['100648000','100648001'],'13908880079','中文签名')
    # test.Cancel_GrpOrder('8713161291','6480','7220051300188177','自动化测试')
    test.Open_GrpVpmn('8763809359','2222',[])

    driver.close()
    print("用例执行结束时间：" + time.strftime("%Y%m%d%H%M%S"))















