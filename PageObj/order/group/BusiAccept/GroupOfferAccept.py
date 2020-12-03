import time
from Base import ReadConfig
from selenium import webdriver
from PageObj.ngboss.login_page import LoginPage
from PageObj.ngboss.mainpage import MainPage
from PageObj.order.group.BusiAccept.GroupBusiBase import GroupBusiBase
from PageObj.order.BizCommon.DealGroupEleBase import DealElements
from PageObj.order.BizCommon.DealGroupMebElements import DealMebElements
from Check.PageCheck import PageAssert
from Check.RuleCheck import RuleCheckBefore
from Base.Mylog import LogManager
from Common.function import getDigitFromStr
from Check.DataCheck import DataCheck

rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('GroupOfferAccept').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )


class GroupOfferAccept(GroupBusiBase):
    '''集团商品受理'''
    def open_base(self):
        self.driver = webdriver.Chrome()
        self.driver.get(rc.get_ngboss('url'))     #这里可以切换环境，去ngboss_config.ini配置
        self.driver.maximize_window()

    def accept_CrtUs(self,scene,groupId,brandCode,offerCode,elementAttrBizList=[],contractId=''):
        '''
        集团商品受理（开户）
        :param groupId: 场景编码
        :param groupId: 集团编码
        :param brandCode: 商品品牌
        :param offerCode: 商品编码
        :param AttrBizList:商品特征属性
        :param elementAttrBizList:资费或者服务包括属性列表
        :param contractId:
        :return:
        '''
        title = '集团商品受理测试记录%s' % offerCode
        self.add_dochead(title)
        LoginPage(self.driver).login(rc.get_ngboss('username'), rc.get_ngboss('password'))  # 登录
        MainPage(self.driver).open_CataMenu('crm8000', 'crm8200', 'crm8207',menuPath='order.page.pc.enterprise.operenterprisesubscriber.OperEnterpriseSubscriber')  # 进入集团商品受理
        self.GroupQryPart(groupId)  #按集团编码查询集团客户
        time.sleep(2)
        self.SelOfferTypePart(brandCode)# 选择商品目录
        self.SubGrpOffer(offerCode) #选择集团商品
        RuleCheckBefore(self.driver).checkRule(scene) #
        DealElements(self.driver).initOfferAttrInfo()  #点击商品待设置或者点击商品特征设置
        self.screen_step("进入集团商品设置页面")
        # DealElements(self.driver).setOfferAttr(AttrBizList) #传入需要设置属性列表并设置商品属性
        DealElements(self.driver).setOfferAttrNew(elementAttrBizList) #传入需设置属性列表并设置商品属性
        DealElements(self.driver).submitOfferAttr(offerCode) #设置商品属性完成
        DealElements(self.driver).initGroupOffer()  #点击新增子商品
        DealElements(self.driver).selectElements(elementAttrBizList) #选择要订购的资费和服务并且设置属性
        self.screen_step("进入子商品选择页面，选择资费和服务")
        # DealElements(self.driver).submitOffers() #页面选择完资费和服务后点击确定
        DealElements(self.driver).selectGroupContract(contractId) #选择集团对应合同
        time.sleep(2)
        if '2222' == offerCode :
            DealElements(self.driver).setApprovalInfo(staffId='AJF00189')
        DealElements(self.driver).submitAccept()
        submitMsg = PageAssert(self.driver).assert_Submit()
        logger.info('业务受理信息：{}'.format(submitMsg))
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        orderId = getDigitFromStr(submitMsg)
        time.sleep(2)
        orderTrace = DataCheck().retOrderTrace(orderId)
        logger.info(orderTrace)
        print(orderTrace) #输出到控制台。方便在测试报告html中查看订单轨迹
        self.save_docreport(title)


    def accept_DstUs(self,groupId,offerCode,reason='不必要使用该产品',scene='DstUs'):
        '''集团商品受理（销户）'''
        title = '集团商品退订测试记录%s' % offerCode
        self.add_dochead(title)
        LoginPage(self.driver).login(rc.get_ngboss('username'), rc.get_ngboss('password'))  # 登录
        MainPage(self.driver).open_CataMenu('crm8000', 'crm8200', 'crm8207',menuPath='order.page.pc.enterprise.operenterprisesubscriber.OperEnterpriseSubscriber')  # 进入集团商品受理
        self.screen_step("进入集团商品受理菜单")
        self.GroupQryPart(groupId)  #按集团编码查询集团客户
        time.sleep(2)
        self.selectGroupOffer()# 选择集团商品按钮
        self.OfferSubCata()  #点击已订购目录
        time.sleep(2)
        self.screen_step("选择要注销的集团商品")
        # self.DstGrpOfferCode(offerCode,userId) #传入要注销的集团商品编码和用户标识点击注销
        self.DstGrpOfferCodeNew(offerCode) #传入要注销的集团商品编码和用户标识点击注销
        RuleCheckBefore(self.driver).checkRule(scene)   #点击注销后判断规则
        DealElements(self.driver).selectRemoveReason(reason)  #选择注销原因
        DealElements(self.driver).submitAccept()
        submitMsg = PageAssert(self.driver).assert_Submit()
        logger.info('业务受理信息：{}'.format(submitMsg))
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        orderId = getDigitFromStr(submitMsg)
        time.sleep(2)
        orderTrace = DataCheck().retOrderTrace(orderId)
        logger.info(orderTrace)
        self.save_docreport(title)

    def accept_CrtMb(self,groupId,serialNum,offerCode,grpUserId,planType,itemId,elementAttrBizList=[]):
        '''
        成员商品受理-订购集团成员产品
        :param groupId: 集团编码
        :param serialNum: 成员服务号码
        :param grpUserId: 集团用户标识
        :param AttrBizList: 成员属性列表，需要页面设置
        :param elementList: 成员资费和服务
        :param planType: 成员付费关系
        :param itemId: 成员付费科目
        :return:
        '''
        title = '成员商品受理测试记录%s' % serialNum
        self.add_dochead(title)
        LoginPage(self.driver).login(rc.get_ngboss('username'), rc.get_ngboss('password'))  # 登录
        MainPage(self.driver).open_CataMenu('crm8000', 'crm8200', 'crm8206',menuPath='page/order.page.pc.enterprise.operenterprisemember')  # 进入成员商品受理
        self.screen_step("进入成员商品受理菜单")
        self.GroupQryPart(groupId)  #按集团编码查询集团客户
        time.sleep(1)
        DealMebElements(self.driver).QryMebInfo(serialNum) #查询成员用户信息
        time.sleep(2)
        self.selectGroupOffer()# 选择集团商品按钮
        self.screen_step("选择集团商品")
        time.sleep(3)
        self.SubMebOffer(grpUserId) #成员商品订购按钮
        DealElements(self.driver).initOfferAttrInfo()  #点击商品待设置或者点击商品特征设置
        DealElements(self.driver).setOfferAttrNew(elementAttrBizList) #传入需要设置属性列表并设置商品属性
        self.screen_step("设置成员商品规格特征")
        DealMebElements(self.driver).submitMebOfferAttr(offerCode)
        DealElements(self.driver).initGroupOffer()  #点击新增子商品
        DealElements(self.driver).selectElements(elementAttrBizList) #选择要订购的资费和服务以及属性
        # DealElements(self.driver).submitOffers() #页面选择完资费和服务后点击确定
        DealElements(self.driver).setPriceOfferCha(elementAttrBizList)  # 在受理主页面再设置一次资费服务属性
        self.screen_step("选择子商品成员资费和服务")
        if offerCode =='2222' :
            DealMebElements(self.driver).setGrpMebPayRela(planType,itemId) #桌面电话，只有集团付费，设置集团付费关系
        else:
            DealMebElements(self.driver).selMebPayPlan(planType,itemId) #【可以选择个人付费或集团付费的处理】设置成员付费关系
        DealMebElements(self.driver).OpenSubmitGrpMebOffer() #点击提交
        submitMsg = PageAssert(self.driver).assert_Submit()
        logger.info('业务受理信息：{}'.format(submitMsg))
        orderId = getDigitFromStr(submitMsg)
        time.sleep(2)
        orderTrace = DataCheck().retOrderTrace(orderId)
        logger.info(orderTrace)
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)

    def accept_DstMb(self,groupId,serialNum,grpUserId):
        '''
        成员商品受理-订购集团成员产品
        :param groupId: 集团编码
        :param serialNum: 成员服务号码
        :param grpUserId: 集团用户标识
        :return:
        '''
        LoginPage(self.driver).login(rc.get_ngboss('username'), rc.get_ngboss('password'))  # 登录
        MainPage(self.driver).open_CataMenu('crm8000', 'crm8200', 'crm8206',menuPath='page/order.page.pc.enterprise.operenterprisemember')  # 进入成员商品受理
        self.GroupQryPart(groupId)  #按集团编码查询集团客户
        time.sleep(1)
        DealMebElements(self.driver).QryMebInfo(serialNum) #查询成员用户信息
        self.OfferSubCata() #点击已订购目录
        time.sleep(3)
        self.DstMebOffer(grpUserId)
        ####这个还差一个重新认证集团客户的确认动作
        RuleCheckBefore(self.driver).checkRule() #业务规则判断
        DealMebElements(self.driver).InputDstMbRemark() #填写备注
        DealMebElements(self.driver).DelSubmitGrpMebOffer() #注销提交按钮
        submitMsg = PageAssert(self.driver).assert_Submit()
        logger.info('业务受理信息：{}'.format(submitMsg))
        orderId = getDigitFromStr(submitMsg)
        time.sleep(2)
        orderTrace = DataCheck().retOrderTrace(orderId)
        logger.info('=========订单轨迹检查结果========')
        logger.info(orderTrace)



if __name__ == '__main__':
    driver = webdriver.Chrome()
    test = GroupOfferAccept(driver)

    # test.accept_CrtUs(groupId='7100048602',brandCode='BZBG',offerCode='6200',
    #                   elementAttrBizList=[{'ELEMENT_ID':'3000030473','OFFER_TYPE':'D','AttrBizList':[]}],
    #                   contractId='7100048602')  # OK
    # test.accept_CrtUs(groupId='7100048602',brandCode='BZBG',offerCode='8000',
    #                   elementAttrBizList=[{'ELEMENT_ID':'110000008000','OFFER_TYPE':'P','AttrBizList':[{"ATTR_VALUE": "1-均显示短号","ATTR_CODE": "pam_CALL_DISP_MODE"}]},
    #                                       {'ELEMENT_ID': '130000060000', 'OFFER_TYPE': 'D', 'AttrBizList': []}
    #                                       ],
    #                   contractId='7100048602')  # VPMN集团商品受理

    test.accept_DstUs(groupId='7100048602',offerCode='8000',userId='7120112400099106')
    # test.accept_DstUs(groupId='7100048602',offerCode='8000',userId='7120111900088551')
    # test.accept_CrtMb(groupId='7100048602',serialNum='09717174690',offerCode='2222',grpUserId='7120112400099806',planType='G',itemId='42701',
    #                   elementAttrBizList=[{"ELEMENT_ID":"110000222201","OFFER_TYPE":"P","AttrBizList":[{"ATTR_VALUE": "610530","ATTR_CODE": "pam_SHORT_CODE"}]},
    #                                       {"ELEMENT_ID": "120010122813", "OFFER_TYPE": "S", "AttrBizList": []},
    #                                       {"ELEMENT_ID": "120000008174", "OFFER_TYPE": "S","AttrBizList": [{"ATTR_VALUE": "IMS融合通信-@ims.qh.chinamobile.com","ATTR_CODE":"IMPU_TYPE"}]},
    #                                       {"ELEMENT_ID": "120000008172", "OFFER_TYPE": "S", "AttrBizList": []}
    #                                       ])

    # test.accept_CrtMb(groupId='7100048602',serialNum='13897471185',offerCode='6200',grpUserId='7120112700109676',planType='G',itemId='90001',
    #                   elementAttrBizList=[{"ELEMENT_ID": "3000033664", "OFFER_TYPE": "D", "AttrBizList": []}])
    # #                                        #订购两条资费一个主产品，都没有属性  OK

    test.accept_CrtMb(groupId='7100048602',serialNum='18797098484',offerCode='8000',grpUserId='7120112700109681',planType='G',itemId='42701',
                      elementAttrBizList=[{"ELEMENT_ID": "110011003068", "OFFER_TYPE": "P", "AttrBizList": [{"ATTR_VALUE": "610530","ATTR_CODE": "pam_SHORT_CODE"},{"ATTR_VALUE": "1-均显示短号","ATTR_CODE": "pam_pam_CALL_DISP_MODE"}]},
                                         {"ELEMENT_ID": "3000033663", "OFFER_TYPE": "D", "AttrBizList": []},
                                         {"ELEMENT_ID": "120000008601", "OFFER_TYPE": "S", "AttrBizList": []}
                                          ])
    #                                        #订购两条资费一个主产品，都没有属性  OK


    # test.accept_DstMb(groupId='7100048602',serialNum='13897471185',grpUserId='7120112400099809')
    # test.accept_DstMb(groupId='7100048602',serialNum='15719780530',grpUserId='7120111900088551')
    # test.accept_DstUs(groupId='7100048602',offerCode='6200')
    # test.accept_DstUs(groupId='7100048602',offerCode='8000',userId='7120111900088551')
    # test.accept_CrtUs(groupId='7100048602',brandCode='TREX',offerCode='2222',contractId='7100048602',
    #     elementAttrBizList=[{"ELEMENT_ID": "110000222201", "OFFER_TYPE": "P",
    #     "AttrBizList": [{"ATTR_VALUE": "西宁","ATTR_CODE": "pam_DIVIDE_DEPART"},{"ATTR_VALUE": "5:5分成","ATTR_CODE": "pam_DIVIDE_BELIEL"}]}
    #     ])  --OK
