import unittest,os
import time,ddt
from Base import HTMLTestRunnerCNNew
from PageObj.oc.person.SubscriberOpen import SubscriberOpen
from selenium import webdriver
from selenium.webdriver.common.by import By
from Base import ReadConfig
from Base.OperExcel import write_xlsBycolName_append
from Base.Mylog import LogManager
from Common.Assert import PageAssert
from TestCases.suite import mySuitePrefixAdd
from Common.TestDataMgnt import create_testDataFile
from Common.TestDataMgnt import get_TestData,get_FuncRow,get_testDataFile

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('SubscriberOpenTest').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

paras = get_TestData('SubscriberOpenTest')['params']
file = get_TestData('SubscriberOpenTest')['filename']
row = get_FuncRow('SubscriberOpenTest')
logger.info('测试案例执行数据准备：{}'.format(paras))
# create_testDataFile(paras=paras,filename=file)

@ddt.ddt
class SubscriberOpenTest(unittest.TestCase):
    """个人业务-商品订购测试"""
    @classmethod
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(rc.get_ngboss('url'))     #这里可以切换环境，去ngboss_config.ini配置
        self.driver.maximize_window()
        #self.driver.implicitly_wait(40)    #暂时设置40s，隐式等待

    @ddt.data(*paras)
    def test_acceptSubscriberOpen(self,dic):
        """个人用户开户"""
        logger.info("开始参数化......")
        # row = int(dic.get('NO'))   #标识行号，后续写入xls使用
        accessNum = str(dic.get('ACCESS_NUMBER'))
        simId = dic.get('ICC_ID')
        offerId = str(dic.get('OFFER_ID'))
        logger.info("开户号码:{},SIM卡号：{},主套餐：{}".format(accessNum,simId,offerId))
        print("开户号码:{},SIM卡号：{},主套餐：{}".format(accessNum,simId,offerId))
        logger.info('开始执行第{}个用例,测试数据：{}'.format(row,dic))
        test = SubscriberOpen(self.driver)
        title = '个人用户开户受理测试记录'
        test.add_dochead(title)
        loc_commitAll = (By.XPATH, '//*[@id="CSSUBMIT_BUTTON"]')
        test.Open_subscriberOpen()  # 进入开户页面
        test.set_customerInfo(accessNum)  # 设置客户信息
        # test.set_BusiAcceptInfo(simId, offerId, acctName, password)  # 设置业务受理信息
        validMsg = test.Input_validSim(simId) #输入SIMID并校验
        logger.info('SIM卡校验结果:{}'.format(validMsg))
        if '业务校验失败' in validMsg:
            write_xlsBycolName_append(file = file, row=row, colName='RESULT_INFO', value=validMsg,index=0)  #向xls模板指定行列写入结果
            test.quit_browse()
        test.set_personMainOffer(offerId) #设置个人主套餐
        test.set_Acctinfo()  #设置账户信息
        test.set_personPwd() #设置用户服务新密码
        test.find_element_click(loc_commitAll)# 点击提交时校验服务密码
        test.find_element_click(loc_commitAll)# 再次点击提交
        time.sleep(10)
        #提交时如果发生异常，则将结果写入到xls
        vaildMsg = PageAssert(self.driver).write_vaildErrResult(file=file,row=row,index=0) #如果有错误就写入结果到xls
        if '校验通过' in vaildMsg:
            test.confirm_Payinfo() #校验通过后再支付确认
            time.sleep(5)
        submitMsg = PageAssert(self.driver).assert_Submit()  # 提交后返回信息，flowId或者报错
        print('===提交后页面返回信息：', submitMsg)
        test.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        # 点击确认支付后，页面返回的信息写入xls
        PageAssert(self.driver).write_testResult(file=file,row=row,index=0) #写入结果到xls
        logger.info('写入测试结果到xls成功.....')
        test.save_docreport(title)
        self.driver.close()

    def tearDown(self):
        print('测试结束，关闭浏览器器!')
        self.driver.close()

if __name__ == '__main__':
    report_title = u'[个人开户]自动化测试报告'
    desc = u'个人开户测试详情：'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath()  + report_title + nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2)
        runner.run(mySuitePrefixAdd(SubscriberOpenTest,"test_acceptSubscriberOpen"))

