import time
from Base.base import Base
from selenium.webdriver.common.by import By
from Base import ReadConfig
from PageObj.order.BizCommon.DealGroupMebElements import DealMebElements
from Base.Mylog import LogManager
from Check.PageCheck import PageAssert

rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('DealElements').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )


class DealElements(Base):
    '''处理页面元素'''
    def initGroupOffer(self):
        '''点击新增子商品按钮'''
        loc_prodAdd = (By.XPATH,"//button[contains(@ontap,'enterpriseGroupOffers.initGroupOffersNew')]")
        self.isElementDisplay(loc_prodAdd,'click')
        return self.driver


    def initOfferAttrInfo(self):
        '''初始化商品设置按钮'''
        loc_initOfferAttr = (By.XPATH,"//button[contains(@ontap,'EnterpriseOfferObj.initOfferAttrInfo')]")
        self.isElementDisplay(loc_initOfferAttr,'click')
        time.sleep(1)   #初始化页面属性
        PageAssert(self.driver).pageLoading()
        return self.driver


    def selectElements(self,elementAttrBizList=[]):
        '''
        页面上选择可订购的资费和服务
        :param elementAttrBizList: 传入要订购的优惠和服务列表，注意这里为OfferId,是长码以及参数
        eg :[{"ELEMENT_ID":"120010122813","OFFER_TYPE":"S","AttrBizList": [],
            {"ELEMENT_ID":"120000008174","OFFER_TYPE":"S","AttrBizList": [{ATTR_VALUE": "IMS融合通信-@ims.qh.chinamobile.com","ATTR_CODE": "IMPU_TYPE" }],
            {"ELEMENT_ID":"120000008172","OFFER_TYPE":"S","AttrBizList": []]
        :return:
        '''
        for i in range(len(elementAttrBizList)):
            logger.info("受理页面要订购资费或服务如下：")
            logger.info(elementAttrBizList[i])
            elementId = elementAttrBizList[i]['ELEMENT_ID']
            offerType = elementAttrBizList[i]['OFFER_TYPE']
            AttrBizList = elementAttrBizList[i]['AttrBizList']
            if isinstance(elementId,int):
                elementId = str(elementId)
            self.selectOfferSingle(elementId) #统一写法
            self.setPriceOfferChaNew(elementAttrBizList[i]) #传入字典设置元素属性
        self.submitOffers() #提交商品


    def selectDisSvcElements(self,ElementsList=[]):
        '''
        页面上选择资费或者服务列表
        :param ElementsList 元素列表
        :return:
        '''
        for  i in range(len(ElementsList)):
            elementId = ElementsList[i]['ELEMENT_ID']
            offerType = ElementsList[i]['OFFER_TYPE']
            if offerType in ['D','S','P','Z','K']:
                logger.info("受理页面要订购资费或服务：{}".format(elementId))
                logger.info("受理页面要订购商品类型：{}".format(offerType))
                self.selectOfferSingle(elementId)

    def selectOfferSingle(self,elementId):
        '''
        根据传入的offerId直接选择资费或者服务,适用于订购单个资费或者服务
        :param elementId: 传入资费或者服务的OFFERID，长编码
        :return:
        '''
        # selGroupOffereleStr = "//*[contains(@name,'selGroupOffer') and contains(@offer_id,'%s')]" % elementId #传入集团商品编码并通过Xpath定位
        selGroupOffereleStr = 'grpOffer_' + elementId
        loc_selGroupOffer = (By.ID,selGroupOffereleStr)
        logger.info("受理页面要订购资费或服务：" + elementId)
        self.isElementDisplay(loc_selGroupOffer,'click')
        # self.isSelected(loc_selGroupOffer, 'click')  # 是否选中元素，如果没有则选中订购


    def filerElementsByOfferType(self,offerType,elementAttrBizList=[]):
        '''
        根据传入的元素类型OFFER_TYPE过滤出元素订购列表
        :param offerType:
        :param elementAttrBizList: 元素列表,包含P、D、S、Z、K 等不同类型
        :return:OfferList 根据条件过滤后返回的列表
        '''
        OfferList = []
        if not isinstance(elementAttrBizList,list) :
            logger.info('传入的不是List类型')
            return
        for i in range(len(elementAttrBizList)):
            print(elementAttrBizList[i])
            offer_type = elementAttrBizList[i]['OFFER_TYPE']
            if offer_type == offerType:
                OfferList.append(elementAttrBizList[i])
        return OfferList

    def submitOffers(self):
        '''页面选择完资费和服务后点击确定'''
        loc_confirmGroupOffers = (By.XPATH,"//button[contains(@ontap,'enterpriseGroupOffers.submitGroupOffers')]")
        self.isElementDisplay(loc_confirmGroupOffers,'click')


    def submitOfferAttr(self,offerCode):
        '''商品特征设置页面点击确认'''
        loc_confirmGroupAttr = (By.XPATH,"//button[contains(@ontap,'checkSub')]")
        loc_submitGroupDeskTelAttr = (By.XPATH,"//button[contains(@ontap,'validateParamPage')]") #桌面电话特殊
        loc_submitCntxVpmnAttr = (By.ID,'sumbitTrue') #融合VPMN
        if '8001' == offerCode:
            self.isElementDisplay(loc_submitCntxVpmnAttr,'click')
        elif '2222' ==offerCode:
            self.isElementDisplay(loc_submitGroupDeskTelAttr,'click')
        else:
            self.isElementDisplay(loc_confirmGroupAttr,'click')

    def setOfferAttr(self,AttrBizList=[]):
        '''
        处理集团商品/成员商品 业务受理参数，传入AttrBizList字典列表包含Attr_Code和Attr_Value两个Key
        先找到对应的Key对应的元素位置，然后输入对应的AttrValue
        该方法只针对需要手工输入的text类型和select下拉枚举类型
        :param AttrBizList: eg :ATTR_CODE 和 ATTR_VALUE 两个Key不变，ATTR_CODE的Key值要以pam开头
        [{"ATTR_VALUE": "710000000011","ATTR_CODE": "pam_MAX_INNER_NUM"  },{"ATTR_VALUE": "710000000012","ATTR_CODE": "pam_MAX_OUTNUM"}]
        :return:
        '''
        for i in range(len(AttrBizList)):
            logger.info('需要设置的页面属性:{}'.format(AttrBizList[i]))
            AttrCode = AttrBizList[i]['ATTR_CODE']
            AttrValue = AttrBizList[i]['ATTR_VALUE']
            logger.info("设置的业务参数名：" + AttrCode)
            logger.info("设置的业务参数值：" + AttrValue)
            try:
                eletype = self.getAttrElementType(AttrCode)
                if ('textfield' == eletype ):    #如果是textfiled类型，则直接输入
                    self.inputOfferAttrTextfiled(AttrBizList[i])
                elif('select' == eletype):     #如果是select下拉选择类型，则传入的value选择对应值
                    self.selOfferAttrByValue(AttrBizList[i])
            except:
                logger.info('根据传入的AttrCode无法定位到页面元素')

    def setOfferAttrNew(self,ElementAttrBizList=[]):
        '''
        处理集团商品/成员商品 业务受理参数，传入AttrBizList字典列表包含Attr_Code和Attr_Value两个Key
        先找到对应的Key对应的元素位置，然后输入对应的AttrValue
        该方法只针对需要手工输入的text类型和select下拉枚举类型
        :param AttrBizList:
                eg :[{"ELEMENT_ID":"120010122813","OFFER_TYPE":"S","AttrBizList": []},
                     {"ELEMENT_ID":"120000008174","OFFER_TYPE":"P","AttrBizList": [{ATTR_VALUE": "IMS融合通信-@ims.qh.chinamobile.com","ATTR_CODE": "IMPU_TYPE"]},
                     {"ELEMENT_ID":"120000008172","OFFER_TYPE":"S","AttrBizList": []}]
        :return:
        '''
        for i in range(len(ElementAttrBizList)):
            logger.info('需要设置的页面属性:{}'.format(ElementAttrBizList[i]))
            print('需要设置的页面属性:{}'.format(ElementAttrBizList[i]))
            # print(type(ElementAttrBizList[i]))
            elementId = ElementAttrBizList[i]['ELEMENT_ID'] #获取元素编码
            OfferType = ElementAttrBizList[i]['OFFER_TYPE']  #获取元素类型
            AttrBizList = ElementAttrBizList[i]['AttrBizList'] #获取属性列表
            logger.info("要设置属性的元素编码：" + elementId)
            logger.info(AttrBizList)
            if OfferType == 'P' :
                self.setOfferAttr(AttrBizList)   #注意是商品类型才进入商品特征设置页面

    def setPriceOfferCha(self,elementAttrBizList=[]):
        '''
        处理集团商品/成员商品 资费或者服务参数，传入AttrBizList字典列表包含ElementId ，OFFER_TYPE，AttrBizList三个Key
        :param elementAttrBizList: eg :ATTR_CODE 和 ATTR_VALUE 两个Key不变，ATTR_CODE的Key值要以pam开头,ELEMENT_ID是资费或者服务的OFFERID长码
        eg :[{"ELEMENT_ID":"120010122813","OFFER_TYPE":"S","AttrBizList": []},
            {"ELEMENT_ID":"120000008174","OFFER_TYPE":"P","AttrBizList": [{ATTR_VALUE": "IMS融合通信-@ims.qh.chinamobile.com","ATTR_CODE": "IMPU_TYPE"]},
            {"ELEMENT_ID":"120000008172","OFFER_TYPE":"S","AttrBizList": []}]
        :return:
        '''
        for i in range(len(elementAttrBizList)):
            elementId = elementAttrBizList[i]['ELEMENT_ID']   #获取要设置的elementId
            offerType = elementAttrBizList[i]['OFFER_TYPE']
            AttrBizList = elementAttrBizList[i]['AttrBizList']  #获取当前元素要设置的属性列表
            if isinstance(elementId,int):
                elementId = str(elementId)
            if offerType == 'S' or offerType == 'D': #如果是资费或者服务才进入设置属性
                self.initPriceOfferCha(elementId)  #先点击待设置按钮进入设置页面
                self.setOfferAttr(AttrBizList)
                self.submitPriceOfferCha()  #商品资费服务属性设置完成


    def setPriceOfferChaNew(self,elementAttrBizDic={}):
        '''
        处理集团商品/成员商品 资费或者服务参数，传入AttrBizList字典列表包含ElementId ，OFFER_TYPE，AttrBizList三个Key
        :param elementAttrBizDic: eg :ATTR_CODE 和 ATTR_VALUE 两个Key不变，ATTR_CODE的Key值要以pam开头,ELEMENT_ID是资费或者服务的OFFERID长码
        eg :{"ELEMENT_ID":"120010122813","OFFER_TYPE":"S","AttrBizList": []}
        :return:
        '''
        elementId = elementAttrBizDic['ELEMENT_ID']   #获取要设置的elementId
        offerType = elementAttrBizDic['OFFER_TYPE']
        AttrBizList = elementAttrBizDic['AttrBizList']  #获取当前元素要设置的属性列表
        if isinstance(elementId,int):
            elementId = str(elementId)
        if offerType == 'S' or offerType == 'D': #如果是资费或者服务才进入设置属性
            self.initPriceOfferCha(elementId)  #先点击待设置按钮进入设置页面
            self.setOfferAttr(AttrBizList)
            self.submitPriceOfferCha()  #商品资费服务属性设置完成

    def inputOfferAttrTextfiled(self,attrbiz={}):
        '''
        处理集团商品/成员商品 业务受理参数，传入AttrBiz字典包含Attr_Code和Attr_Value两个Key
        先找到对应的Key对应的元素位置，然后输入对应的AttrValue
        该方法只针对需要手工输入的类型
        :param AttrBizList: eg :ATTR_CODE 和 ATTR_VALUE 两个Key不变，ATTR_CODE的Key值要以pam开头
        [{"ATTR_VALUE": "710000000011","ATTR_CODE": "pam_MAX_INNER_NUM"  },{"ATTR_VALUE": "710000000012","ATTR_CODE": "pam_MAX_OUTNUM"}]
        :return:
        '''
        AttrCode = attrbiz['ATTR_CODE']
        AttrValue = attrbiz['ATTR_VALUE']
        logger.info("设置的业务参数名：" + AttrCode)
        logger.info("设置的业务参数值：" + AttrValue)
        loc_AttrCode = (By.ID,AttrCode)
        if ('textfield'==self.getAttrElementType(AttrCode)):
            self.sendkey(loc_AttrCode,AttrValue)
            if AttrCode == 'pam_SHORT_CODE':
                DealMebElements(self.driver).verifyShortNum()   #如果是短号属性，加个校验

    def selOfferAttrByValue(self,attrbiz={}):
        '''
        处理集团商品/成员商品 业务受理参数，传入AttrBizList字典列表包含Attr_Code和Attr_Value两个Key
        先找到对应的Key对应的元素位置，然后输入对应的AttrValue
        该方法只针对select的类型
        :param AttrBizList: eg :ATTR_CODE 和 ATTR_VALUE 两个Key不变，ATTR_CODE的Key值要以pam开头
        [{"ATTR_VALUE": "710000000011","ATTR_CODE": "pam_MAX_INNER_NUM"  },{"ATTR_VALUE": "710000000012","ATTR_CODE": "pam_MAX_OUTNUM"}]
        :return:
        '''
        AttrCode = attrbiz['ATTR_CODE']
        AttrValue = attrbiz['ATTR_VALUE']
        logger.info("设置的业务参数名：" + AttrCode)
        logger.info("设置的业务参数值：" + AttrValue)
        eleType = self.getAttrElementType(AttrCode)
        if (eleType== 'select'):   #只针对可以编辑输入的select类型属性
            selAttrCodeStr = AttrCode + '_span'
            loc_selAttrCode = (By.ID,selAttrCodeStr)
            self.isElementDisplay(loc_selAttrCode,'click')
            time.sleep(1)
            selAttrFloatStr = AttrCode + '_float'  #pam_DIVIDE_DEPART_float
            ele_selAttrFloat = self.find((By.ID,selAttrFloatStr))
            floatStr = "./div[2]/div/div/ul/li[contains(@title,'%s')]" % AttrValue   #用AttrValue匹配元素title的属性值
            ele_AttrFloat = ele_selAttrFloat.find_element_by_xpath(floatStr)
            self.click_on_element(ele_AttrFloat)
            time.sleep(1)


    def getAttrElementType(self,attrcode):
        '''
        传入属性编码判断该元素的Type类型
        :return:页面元素类型
        '''
        eleType = 'textfield'   #默认text类型
        loc_attrCode = (By.ID,attrcode)
        eleType = self.get_attribute(loc_attrCode, name='x-wade-uicomponent')
        logger.info('传入属性编码：'.format(attrcode))
        logger.info( attrcode + '元素对应的类型是:{}'.format(eleType))
        return eleType

    def selectGroupContract(self,contractId):
        '''
        传入集团合同编码，选择集团对应合同
        :param contractId:合同编码,提前准备的合同必须包含商品受理时选择集团商品编码
        :return:
        '''
        span_QryContract = (By.XPATH,"//*[contains(@ontap,'queryContractInfo')]")
        selcontractStr = "//button[contains(@contractid,'%s')]" %contractId
        loc_selcontract = (By.XPATH,selcontractStr)
        self.isElementDisplay(span_QryContract,'click')
        time.sleep(2)
        self.isElementDisplay(loc_selcontract,'click')

    def submitAccept(self):
        '''集团商品受理提交'''
        btn_Offersubmit = (By.ID,'submitButton')
        self.isElementDisplay(btn_Offersubmit,'click')


    def selectRemoveReason(self,reason='不必要使用该产品'):
        '''
        集团商品受理时选择注销原因
        :param reason: 传入注销原因
        :return:
        '''
        loc_selRemoveReason = (By.ID,'REMOVE_REASON_span')
        self.isElementDisplay(loc_selRemoveReason,'click')
        time.sleep(1)
        reasonfloatStr = '//*[@id="REMOVE_REASON_float"]/div[2]/div/div/ul/li[contains(@title,"%s")]' % reason  # 用reason匹配元素title的属性值
        loc_reasonfloat = (By.XPATH,reasonfloatStr)
        self.isElementDisplay(loc_reasonfloat,'click')

    def initPriceOfferCha(self,elementId):
        '''
        初始化集团资费或者服务参数设置页面
        :param elementId: 元素ID，可能是资费也可能是服务
        :return:
        '''
        PriceOfferChaStr = "//button[contains(@id,'%s') and contains(@ontap,'priceOfferCha.initPriceOfferChaNew')]" % elementId
        loc_PriceOfferCha = (By.XPATH,PriceOfferChaStr)
        self.isElementDisplay(loc_PriceOfferCha,'click') #点击待设置

    def submitPriceOfferCha(self):
        '''资费或者服务参数设置完成后点击提交'''
        btn_submitPriceOfferCha = (By.XPATH,"//button[contains(@ontap,'priceOfferCha.submitPriceOfferCha')]")
        self.isElementDisplay(btn_submitPriceOfferCha,'click')


    def setApprovalInfo(self,staffId):
        '''
        省内审批信息处理，如2222桌面电话商品受理
        :param staffId: 传入审核人工号
        :return:
        '''
        btn_QryStaffInfo = (By.XPATH,"//*[contains(@popid,'cond_AUDIT_STAFF_NAME')]")
        self.isElementDisplay(btn_QryStaffInfo,'click')
        self.iframe('staffSelFrame')  #切换到工号选择Iframe
        self.element_sendkey_enter((By.ID,'STAFF_SEARCH_TEXT'),staffId)
        loc_staffListUI = (By.XPATH,'//*[@id="StaffListUl"]/li')
        self.isElementDisplay(loc_staffListUI,'click')
        self.driver.switch_to.parent_frame() #退出staffSelFrame ,回到受理页面？？