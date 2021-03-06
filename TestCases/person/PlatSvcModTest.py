import unittest,os,time,ddt
from Base import HTMLTestRunnerCNNew
from Base import ReadConfig
from Base.Mylog import LogManager
from TestCases.suite import mySuitePrefixAdd
from selenium import webdriver
from Common.dealParas import convert_to_diclistUpper
from Common.SuiteExec import DealSuiteExec as dse
from Common.function import getDigitFromStr
from PageObj.order.person.PlatSvcOrder import PlatServiceOrder as Plat


os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
logger = LogManager('AddPlatSvcTest').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

params = convert_to_diclistUpper(dse().get_ParaBySuiteSceneCode(suiteCode='PlatSvcTest',sceneCode='ModPlatSvc')) #获取订购资费、服务测试套件参数
logger.info('测试套件执行参数列表:{}'.format(params))


@ddt.ddt
class ModPlatSvc(unittest.TestCase):
    """[个人业务]平台业务办理-暂停、恢复、退订"""

    def setUp(self):
        self.imgs = []
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def get_screenshot(self):
        self.imgs.append(self.driver.get_screenshot_as_base64())
        return True

    @ddt.data(*params)
    def test_PlatSvcMod(self,dic):
        """平台业务暂停、恢复、退订"""
        logger.info("开始参数化......{}".format(dic))
        print('开始执行用例,测试数据：{}'.format(dic))
        accessNum = str(dic.get('ACCESSNUM'))
        offerCode= dic.get('OFFERCODE')
        dealType = dic.get('DEALTYPE')
        suite_case_id = str(dic.get('SUITE_CASE_ID'))
        test = Plat(self.driver)
        msg = test.acceptModPlatSvc(accessNum=accessNum,offerCode=offerCode,dealType=dealType,scene=suite_case_id)
        print(msg)
        self.get_screenshot()
        dse().upd_resultBySuiteCaseId(suite_case_id=suite_case_id,actual_result=msg)
        self.assertIn('业务受理成功',msg)
        dse().upd_orderIdBySuiteCaseId(orderId=getDigitFromStr(msg),suite_case_id=suite_case_id)
        logger.info('执行完成')

    def tearDown(self):
        print('测试结束，关闭浏览器!')
        self.driver.close()


if __name__ == '__main__':
    # unittest.main()
    report_title = u'平台业务受理自动化测试报告'
    desc = u'平台业务受理测试详情：'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath() + report_title + nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2,retry=0)
        runner.run(mySuitePrefixAdd(ModPlatSvc,"test_PlatSvcMod"))