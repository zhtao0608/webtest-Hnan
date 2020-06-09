import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from Base import ReadConfig
from Base.Mylog import LogManager
from PageObj.oc.group.GroupBasePage import BasePage
from Common.Assert import PageAssert
from Base.GenTestData import GenTestData

logger = LogManager('test').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

rc = ReadConfig.ReadConfig("ngboss_config.ini")

class GroupMebBusiOper(BasePage):
    def open_base(self):
        self.driver.get(rc.get_ngboss('url'))
        self.driver.maximize_window()
        #self.driver.implicitly_wait(30)

    def initPage(self):
        '''初始化页面，主要是查找是否存在StepUI，如果存在，则直接关闭'''
        loc_UIiframe = (By.XPATH,"//iframe[contains(@src,'service=page/enterprise.vc.navi.MemberOfferNav')]")
        if self.isElementExist(loc_UIiframe):
            self.iframe(loc_UIiframe)
            loc_UIStep = (By.XPATH,'//*[@id="UI-step1"]/div/div[2]/button[1]')
            print("是否显示提示：" + str(self.isElementExist(loc_UIStep)))
            if self.isElementExist(loc_UIStep):
                self.find(loc_UIStep).click()
                time.sleep(1)
                self.driver.switch_to.parent_frame()
        return self.driver

    def input_GrpMebNum(self,accessNum):
        self.find((By.ID,'cond_ACCESS_NUM')).send_keys(accessNum)   #输入成员服务号码
        self.find((By.XPATH,'//*[@id="snInfo"]/ul/li/div[2]/div/button')).click() #点击查询
        time.sleep(5)
        return self.driver

    def submit_cancel(self):
        loc_submit = (By.XPATH,'//*[@id="DelSubmit"]/button')
        # if self.isElementExist(loc_submit):  #是否存在注销按钮
            # submit = self.find((loc_submit))  #先找到submit按钮
            # self.js_scrollIntoView(submit)    #鼠标移动到该元素
        self.find_element_click(loc_submit)
        time.sleep(5)

    def confirm_vaildTips(self):
        '''在点击集团已订购列表下的注销按钮后，会弹出集团认证信息重新认证的页面'''
        loc_tipsbtn = (By.XPATH,"//*[starts-with(@id,'wade_messagebox') and contains(@class,'fn')]/button")
        try:
            flag = self.is_element_located(loc_tipsbtn)  #判断是否能定位到
            self.screen_step("判断是否出现集团鉴权认证提示")
            print("====是否出现鉴权认证提示信息=====：",flag)
            logger.info('是否出现鉴权认证提示信息' + str(flag))
            if not flag:
                logger.info('不用再次集团鉴权认证')
                pass
            else:
                print("========出现鉴权认证提示=======")
                logger.info('========出现鉴权认证提示=======')
                # 点击确定，重新鉴权集团
                self.find(loc_tipsbtn).click()
                time.sleep(3)
                # 跳回到主页iframe判断是否存在智慧眼
                # 集团认证时可能会弹出智慧眼
                try:
                    self.deal_GrpPriEYE() #处理集团智慧眼
                except:
                    print("没有出现智慧眼,直接跳过")
                    logger.info('没有出现智慧眼,直接跳过')
                    pass
                finally:
                    print("最后都跳转到集团成员受理主frame")
                    self.Open_GrpMebBusiframe()
        except:
            pass
        return self.driver

    def set_VpmnMebSpec(self,subofferList):
        '''设置VPMN成员主产品规格特征'''
        #先点击是商品设置->产品规格->待设置：先判断是否要进行商品规格设置，如果不显示待设置则不需要设置，否则进入待设置页面
        loc_offerspec = (By.XPATH,'//*[@id="prodSpecUL"]/li/div[2]/span')
        if self.find(loc_offerspec).is_displayed(): #待设置是否显示
            print("进入商品规格设置......")
            self.find((By.XPATH,'//*[@id="prodSpecUL"]/li/div[2]/span')).click() #进入商品规格设置
            ##ADC商品规格没有需要操作的步骤，直接提交，后续根据实际情况添加
            self.submit_offerSpec(subofferList)
            time.sleep(5)
        else:   #没有商品待设置，直接点击确定
            print("不需要设置商品规格特征")
            self.submit_offerSpec(subofferList)

    def assert_VPMNshortCode(self):
        '''处理下短号验证提示信息'''
        try :
            msg = PageAssert(self.driver).assert_error()
            if '校验通过' in msg:
                msg = PageAssert(self.driver).assert_SucPage()
        except:
            logger.info('短号校验发生异常!关闭')
            msg  = '校验失败，发生异常!'
        return msg

            # print("短号验证结果：",msg)
            # if 'ok' == self.get(btn_msg,Type='attribute',name = 'tag'):
            #     self.screen_step("短号验证")
            #     return True
            # if 'cancel' == self.get(btn_msg,Type='attribute',name = 'tag'):
            #     print("短号验证失败，直接关闭浏览器")
            #     # self.screen_step('短号验证失败')
            #     self.screenshot_SaveAsDoc('短号验证失败')
            #     return False
        # except:
        #     pass #没有找到直接跳过

    def set_vpmnMebshortCode(self):
        '''设置VPMN成员短号'''
        loc_shortCode = (By.ID,'pam_SHORT_CODE')
        loc_pam_CHECK = (By.XPATH,'//*[@id="pam_CHECK"]')
        loc_yanzheng = (By.ID,'pam_YANZHENG')
        shortCode = GenTestData().create_shortCode() #随机生成一个短号
        logger.info('自动生成的短号:{}'.format(shortCode))
        self.sendkey(loc_shortCode,shortCode)
        flag = self.isElementDisplay(loc_pam_CHECK)
        if flag :
            self.find_element_click(loc_pam_CHECK)
            time.sleep(2)
        else:
            self.find_element_click(loc_yanzheng)
            time.sleep(2)
        validshortCodeMsg = self.assert_VPMNshortCode()
        logger.info('短号校验结果:{}'.format(validshortCodeMsg))

    def set_DispMode(self):
        '''设置主叫号码显示，如80001短号集群网成员产品'''
        li_DispMode = (By.ID,'pam_CALL_DISP_MODE_span')
        li_DispMode_float = (By.CSS_SELECTOR,'#pam_CALL_DISP_MODE_float > div.content > div > div > ul > li:nth-child(2)')
        try:
            self.isElementExist(li_DispMode,'click')
            self.isElementExist(li_DispMode_float, 'click') #默认：选择显示短号
        except:
            print("没有找到主叫号码显示元素，测试失败")
            self.close()
        return self.driver

    def confirm_MebsubMainOfferSpec(self):
        '''成员主商品设置完成'''
        confirm_btn = (By.ID,'pam_Button')
        confirm_btn2 = (By.ID,'pam_COMMITID')
        try:
            flag = self.isElementDisplay(confirm_btn)
            if flag:
                self.find_element_click(confirm_btn)
                time.sleep(2)
            else:
                self.find_element_click(confirm_btn2)
                time.sleep(2)
        except:
            logger.info('Vpmn成员规格特征发生异常')

    def confirm_AdcMebsubOfferSpec(self):
        '''ADC子商品点击确认按钮'''
        confirm_btn = (By.ID, 'pam_BUTTON_SRV_PLAT')
        self.find_element_click(confirm_btn)
        time.sleep(1)


    def Oper_grpMemDel(self,groupId,accessNum,mainOffer,OfferInstId):
        '''
        :param groupId: 集团编码
        :param accessNum: 成员服务号码
        :param mainOffer: 要注销的集团主商品OFFER_ID
        :param OfferInstId: 要注销的集团主商品实例Offer_inst_id
        :return:
        '''
        title = u'成员商品业务注销'
        self.add_dochead(title)
        self.Open_GrpMebBusiOrd(groupId)
        self.initPage()   #初始化
        self.screen_step("输入成员服务号码")
        self.input_GrpMebNum(accessNum)
        self.screen_step("选择要注销的集团产品订购实例，点击注销")
        self.choose_grpOfferandCancel(mainOffer,OfferInstId)
        self.confirm_vaildTips()  #有可能重新进行集团认证鉴权
        # time.sleep(5)
        self.screen_step("点击注销按钮")
        self.submit_cancel()
        print("处理页面返回信息.....")
        logger.info("处理页面返回信息......")
        submitMsg = PageAssert(self.driver).assert_Submit()
        logger.info('业务受理信息：{}'.format(submitMsg))
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        time.sleep(5)
        self.save_docreport(title)

    def sub_VpmnMeb(self,groupId,accessNum,mainOffer,subOfferList,OfferInstId):
        '''
        :param groupId: 集团编码
        :param accessNum: 成员服务号码
        :param mainOffer: 要注销的集团主商品OFFER_ID
        :param subOfferList: 需要设置的子商品列表[]
        :param OfferInstId: 要注销的集团主商品实例Offer_inst_id
        :param shortcode: 短号 自动生成
        :return:
        '''
        title = u'VPMN成员商品订购测试记录'
        self.add_dochead(title)
        self.Open_GrpMebBusiOrd(groupId)
        self.screen_step('步骤1：打开成员商品受理菜单')
        self.initPage()   #初始化
        self.input_GrpMebNum(accessNum)
        self.screen_step("步骤2：输入成员服务号码")
        self.click_BtnMebSub() #点击可订购按钮
        self.screen_step("步骤3:选择集团商品并点击订购按钮")
        self.choose_grpOfferandsub(mainOffer,OfferInstId) #选择集团商品并点击订购按钮
        print("直接进入子商品设置页面")
        logger.info("开始设置VPMN成员子商品......")
        for i in range(len(subOfferList)):
            print("子商品编码subofferId=" + subOfferList[i])
            print("设置子商品......")
            logger.info("开始设置子商品产品规格特征" + subOfferList[i])
            self.set_MebsubOffer(subOfferList[i]) #子商品点击待设置(注意这里与集团商品有点区别)
            self.screen_step("步骤4：产品规格特征设置页面，点击待设置")
            time.sleep(8)
            self.set_prodSpec() #产品规格特征设置页面，点击待设置
            if (subOfferList[i] =='222201'):
                # 如果成员商品offerid = 222201 多媒体桌面电话成员产品或者短号集群网则要设置短号
                self.set_vpmnMebshortCode()
            if (subOfferList[i] =='800001'):
                self.set_vpmnMebshortCode()
                self.screen_step("步骤5：设置成员短号")
                self.set_DispMode()
            self.confirm_MebsubMainOfferSpec()#确认VPMN子商品规格设置
            self.confirm_OfferSpec() #最后确认商品设置
        self.screen_step("步骤6：确认商品配置，点击提交")
        self.Open_SubmitAll()  #订购主页，点击提交
        submitMsg = PageAssert(self.driver).assert_SubmitPage()
        logger.info('业务受理信息：{}'.format(submitMsg))
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)

if __name__ == '__main__':
    print("用例开始执行时间：" + time.strftime("%Y%m%d%H%M%S"))
    driver = webdriver.Chrome()
    test = GroupMebBusiOper(driver)
    # test.Oper_grpMemDel('8763809379','13988130181','6415','9193010829233773')
    # test.Oper_grpMemDel('8763809379','13988130181','2222','7695073028397821')
    # groupId,accessNum,mainOffer,subOfferList,OfferInstId,shortcode
    # test.sub_VpmnMeb('8763809379','13908880079','2222',['222201','100008172'],'7695073028397821','65790')
    # test.sub_VpmnMeb('8763809379','13908720051','2222',['222201','100008172'],'7695073028397821','61790')
    # test.Oper_grpMemDel('8763809379','13908720051','2222','7695073028397821')
    # test.sub_VpmnMeb('8763809379','13887027547','2222',['222201','100008172'],'7695073028397821','62790')
    # test.Oper_grpMemDel('8763809379','13887027547','2222','7695073028397821')
    # test.Oper_grpMemDel('8711402148','13987262203','6415','7290122853398928')
    # test.Oper_grpMemDel('8711402148','13908813755','6480','9195042906984912')
    # test.Oper_grpMemDel('8711402148','13708612623','6480','9195042906984912')
    # test.Oper_grpMemDel('8711200069','13578137966','6480','9195042906984912')
    # test.sub_VpmnMeb('8711200069','13887269940','8000',['800001'],'7220051300188173','63792')
    # test.sub_VpmnMeb('8763809379','13608722158','2222',['222201','100008172'],'7695073028397821','62190')
    # test.sub_VpmnMeb('8763809379','13908720051','2222',['222201','100008172'],'7695073028397821','62290')
    # test.sub_VpmnMeb('8763809379','13887224496','2222',['222201','100008172'],'7695073028397821','62290')
    # test.sub_VpmnMeb('8763809379','13887238883','2222',['222201','100008172'],'7695073028397821','67193')
    # test.sub_VpmnMeb('8763809379', '18787291199', '2222', ['222201', '100008172'], '7695073028397821', '67210')
    # test.Oper_grpMemDel('8711400327', '08723076037', '2222', '7294081355895754')
    # test.sub_VpmnMeb('8711400810','18787291810','8000',['800001'],'7292062121402886')
    test.sub_VpmnMeb('8711421911', '18787291898', '2222', ['222201', '100008172'], '7294120180010135')
    # test.sub_VpmnMeb('8711400810','18787291039','8000',['800001'],'7292062121402886')

    print("用例执行结束时间：" + time.strftime("%Y%m%d%H%M%S"))
    driver.close()






