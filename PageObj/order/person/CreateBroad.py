import time
from Base.base import Base
from selenium.webdriver.common.by import By
from Base import ReadConfig
from Base.Mylog import LogManager
from Check.RuleCheck import RuleCheckBefore
from Check.PageCheck import PageAssert
from Common.TestAsserts import Assertion as Assert
from PageObj.ngboss.mainpage import MainPage
from PageObj.ngboss.login_page import LoginPage
from PageObj.order.BizCommon.BroadPart import BroadPart
from PageObj.order.BizCommon.ElementPartBase import PageCommonPart as PageCommon
from selenium import webdriver
from Check.DataCheck import DataCheck as Dc
from Common.SuiteExec import DealSuiteExec as Dse
from Common.function import getOrdIdFromStr
from PageObj.order.BizCommon.PayFeePart import PayFeePart as Pay


logger = LogManager('CrtBroadPage').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

#================处理个人宽带开户界面元素======================#

class CrtBroadPage(Base):
    '''个人宽带开户'''
    def openCrtBroadPage(self):
        LoginPage(self.driver).login()  # 登录
        MainPage(self.driver).open_CataMenuNew(funcId='crm9731')

    def input_custInfo(self,phone,authority,folk_code='汉'):
        '''完善客户资料'''
        self.input((By.ID,'PHONE'),phone)
        self.input((By.ID,'ISSUING_AUTHORITY'),authority)
        self.wadeSelectByTitle(id_locator='FOLK_CODE',title=folk_code)
        self.input((By.ID,'PSPT_END_DATE'),'2030-12-31')
        self.sleep(1)

    def sel_ModemType(self,typeCode='自动配发'):
        '''选择MODEM方式'''
        self.wadeSelectByTitle(id_locator='MODEM_SALE_TYPE',title=typeCode)
        self.sleep(1)
        return self.driver

    def set_BroadOtherInfo(self):
        '''设置宽带其他信息'''
        self.sel_ModemType()
        self.isElementDisplay((By.XPATH,'//*[@id="ADSL_TYPE_span"]/span[2]'),'click') #ADSL迁移 选择否
        self.isElementDisplay((By.XPATH,'//*[@id="BOOK_YES_span"]/span[2]'),'click') #是否预约装机 否


    def accept_CrtBroad(self,accessNum,sAddr,groupId,elementList,productId='99799889',scene='CrtBroad'):
        '''
        宽带开户受理
        :param accessNum:绑定手机号码
        :param sAddr:宽带安装地址
        :param productId:宽带主套餐
        :param elementList:宽带优惠列表
        :param productId:宽带主套餐
        :return:
        '''
        title = '宽带开户测试%s' % accessNum
        self.add_dochead(title)
        self.openCrtBroadPage()  #打开宽带开户菜单
        BroadPart(self.driver).authSerial(accessNum) #绑定手机号码做个鉴权
        self.input_custInfo(phone=accessNum,authority='长沙市公安局')
        BroadPart(self.driver).qryBroadAddr(sAddr)
        self.set_BroadOtherInfo()
        BroadPart(self.driver).selBroadPlan(elementList,groupId,productId=productId)
        # self.set_BroadOtherInfo() #设置宽带其他信息
        PageCommon(self.driver).submit()
        PageAssert(self.driver).assert_WadePage() #提交后先进行一次Page检查
        Pay(self.driver).confirmPayFee() #处理支付
        submitMsg = PageAssert(self.driver).assertSubmit()
        logger.info('业务受理信息：{}'.format(submitMsg))
        if Assert().verifyassertIn('业务受理成功',submitMsg):
            Dc().dealMainOrder(orderId=getOrdIdFromStr(submitMsg)) #处理主订单，如果状态是Y或者X 修改成0
        else:
            Dse().upd_RuleChkBySuiteCaseId(suite_case_id=scene, rule_chkmsg=submitMsg)
        self.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        self.save_docreport(title)
        return submitMsg



if __name__ == '__main__':
    driver = webdriver.Chrome()
    test = CrtBroadPage(driver)
    test.accept_CrtBroad(accessNum='13667312503',sAddr='长沙长沙县星沙街道办事处板仓路长沙县县政府第一宿舍小区7栋1单元3层301号',
                         groupId='99940450',elementList=[{"OFFER_CODE":"20151601","OFFER_TYPE":"D"},{"OFFER_CODE":"99003714","OFFER_TYPE":"D"}])




