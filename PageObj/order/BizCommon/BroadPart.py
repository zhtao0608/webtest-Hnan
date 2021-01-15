import time
from Base.base import Base
from selenium.webdriver.common.by import By
from Base import ReadConfig
from Base.Mylog import LogManager
from Check.RuleCheck import RuleCheckBefore
from Check.PageCheck import PageAssert
from Common.TestAsserts import Assertion as alert
from PageObj.order.BizCommon.ElementPartBase import MainPlanSelectPart as mps


logger = LogManager('MainPlanSelectPart').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

#================宽带业务组件======================#

class BroadPart(Base):
    """宽带业务组件"""
    def authSerial(self,serialNum):
        '''绑定手机号鉴权'''
        text_SerialNum = (By.ID,'AUTH_SERIAL_NUMBER')
        self.element_sendkey_enter(text_SerialNum,serialNum)
        PageAssert(self.driver).wait_for_load() #页面加载
        verifyMsg = PageAssert(self.driver).assert_WadePage() #这里做个规则校验
        logger.info('业务校验检查结果：'.format(verifyMsg))
        alert().assertIn('校验通过',verifyMsg,msg='鉴权失败')

    def Open_QryAddrFrame(self):
        '''
        传入菜单路径，进入对应菜单的Iframe页面
        :param menuPath: 菜单路径
        :return:
        '''
        src = '/presmanm/presserv?service=page/otherinfo.QueryAddress'
        QryAddrFrameStr =  "//iframe[contains(@src,'%s')]" %src   #传入对应的菜单路径
        loc_QryAddrFrame= self.find((By.XPATH,QryAddrFrameStr))
        self.driver.switch_to.frame(loc_QryAddrFrame)
        logger.info("进入菜单Iframe:" + str(loc_QryAddrFrame))
        self.sleep(1)   #暂定进入菜单时间1s
        return self.driver

    def qryBroadAddr(self,sAddr):
        '''
        宽带地址模糊查询,传入精确地址
        :param sAddr: 精确地址
        :return:
        '''
        loc_showAdd = (By.XPATH,'//*[contains(@onclick,"BroadbandCreate.showAddrPopup")]')
        btn_QryRes = (By.XPATH,'//*[contains(@onclick,"queryAddressBtn")]')
        self.isElementDisplay(loc_showAdd,'click',delay=2)
        PageAssert(self.driver).wait_for_load()
        self.Open_QryAddrFrame() #进入地址查询Frame
        self.input((By.ID,'address'),sAddr)
        self.isElementDisplay(btn_QryRes,'click',delay=1)
        loc_AddrTable = (By.XPATH,'//*[@id="addrtable3"]/div[1]/div/table/tbody/tr/td/span')
        addr = self.get(loc_AddrTable)
        alert().assertIn(sAddr,addr,msg='查询的地址与传入地址不匹配，返回False')
        self.isElementDisplay(loc_AddrTable,'click',delay=1)
        selAddrStr = '//*[@id="select" and contains(@onclick,"subMitAddr") and contains(@regionname,"%s")]' %sAddr
        li_selectAddr = (By.XPATH,selAddrStr)
        self.isElementDisplay(li_selectAddr,'click',delay=2)
        PageAssert(self.driver).wait_for_load()
        self.switchToParFrame() #返回上级Frame


    def selBroadPlan(self,element_list,groupId,productId='99799889'):
        '''
        选择宽带主套餐以及优惠列表
        :param productId: 主套餐编码,默认99799889
        :param groupId: 可选组编码
        :param element_list: 资费列表
          eg :elementList =  [{"OFFER_TYPE":"D","OFFER_CODE":"99410190"},{"OFFER_TYPE":"D","OFFER_CODE":"2285"}]
        :return:
        '''
        btn_SelBroad = (By.XPATH,'//*[contains(@ontap,"showProductSelect")]')
        self.isElementDisplay(btn_SelBroad,'click',delay=2)
        #点击宽带主产品订购
        self.sleep(2)
        PageAssert(self.driver).wait_for_load()
        mps(self.driver).searchMainPlan(productId)
        #按组点击展开
        div_groupStr = '//*[@id="productSelectproductItemListArea"]/div[contains(@ontap,"%s")]/div/div[2]/ul/li/span'  % groupId
        loc_productMore = (By.XPATH,div_groupStr)
        self.isElementDisplay(loc_productMore,'click',delay=2)
        self.screen_step('选择宽带套餐和优惠')
        mps(self.driver).selectProductItem(element_list)








