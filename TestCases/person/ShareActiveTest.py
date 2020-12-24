import unittest,os
import time,ddt
from Base import HTMLTestRunnerCNNew
from PageObj.order.person.ShareActive import ShareActive
from selenium import webdriver
from selenium.webdriver.common.by import By
from Base import ReadConfig
from Base.OperExcel import get_exceldata,write_xlsBycolName_append
from Base.Mylog import LogManager
from Check.PageCheck import PageAssert
from TestCases.suite import mySuitePrefixAdd
from Data.DataMgnt.TestDataMgnt import TestDataExcel as TDE

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('ShareActiveTest').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

# file = ReadConfig.data_path + 'UITest_ShareActive.xls'
# paras = get_exceldata(file,0)
# logger.info('测试案例执行数据准备：{}'.format(paras))
file = TDE().get_testDataFile()
paras = TDE().get_TestData('ShareActiveTest')['params']
row = TDE().get_FuncRow('ShareActiveTest')

@ddt.ddt
class ShareActiveTest(unittest.TestCase):
    """家庭畅享活动办理"""
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(rc.get_ngboss('url'))     #这里可以切换环境，去ngboss_config.ini配置
        self.driver.maximize_window()
        # self.driver.implicitly_wait(20)    #暂时设置40s，隐式等待

    @ddt.data(*paras)
    def test_acceptShareActive(self,dic):
        """家庭畅享活动办理"""
        logger.info("开始参数化......")
        # row = int(dic.get('No'))   #标识行号，后续写入xls使用
        accessNum = str(dic.get('主号'))
        logger.info("主号:{}".format(accessNum))
        offerId = str(dic.get('活动ID'))
        logger.info("家庭活动编码:{}" .format(offerId))
        phoneNum = dic.get('副号')
        logger.info("副号码:{}" .format(phoneNum))
        Idencode = dic.get('副号密码')
        logger.info("副号密码:{}".format(Idencode))
        logger.info('开始执行第{}个用例,测试数据：{}'.format(row,dic))
        print('开始执行第{}个用例,测试数据：{}'.format(row,dic))
        test = ShareActive(self.driver)
        title = '家庭畅享活动受理测试记录'
        test.add_dochead(title)
        loc_commit = (By.CSS_SELECTOR, '#winInfoPop > div.c_popupBox > div > div > div > div.c_submit.e_center > button')
        test.Open_PersonMenu(accessNum=accessNum,password='123123',cataMenuId='crm9200',menuId='crmy198') #进入菜单
        time.sleep(5)
        test.open_ShareActiveFrame() #进入iframe
        logger.info('进入家庭畅享活动菜单时验证主号')
        logger.info('暂时屏蔽主号校验')
        # test.vaild_BusiRule() #业务检查点（进入菜单时校验）
        test.screen_step('进入家庭畅享活动CRM,选择活动')
        test.choose_ActiveOffer(offerId) #选择共享活动
        test.set_ShareActiveInfo(phoneNum,Idencode)
        logger.info('副号校验....')
        # vaildMsg = test.vaild_BusiRule()
        vaildMsg = PageAssert(self.driver).check_BusiRule(file,row)
        print('副号校验结果:{}'.format(vaildMsg))
        logger.info('副号校验结果:{}'.format(vaildMsg))
        test.screen_step('验证副号')
        self.assertNotIn('校验失败',vaildMsg)
        # if '校验失败' in vaildMsg:
        #     # PageAssert(self.driver).write_vaildErrResult(file=file,row=row)
        #     write_xlsBycolName_append(file=file,row=row,colName='RESULT_INFO',value=vaildMsg)
        #     logger.info('写入副号校验结果到xls成功.....')
        #     time.sleep(2)
        #     test.quit_browse()
        time.sleep(2)
        test.find_element_click(loc_commit) #点击办理
        time.sleep(15)
        submitMsg = PageAssert(self.driver).assert_submitAfter(file=file,row=row)
        logger.info('业务受理信息：{}'.format(submitMsg))
        test.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        test.save_docreport(title)
        time.sleep(3)
        self.assertIn('业务受理成功',submitMsg)
        test.driver.close()


if __name__ == '__main__':
    report_title = u'家庭畅享活动办理自动化测试报告'
    desc = u'家庭畅享活动办理测试详情：'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath() + report_title + nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2)
        runner.run(mySuitePrefixAdd(ShareActiveTest,"test_acceptShareActive"))

