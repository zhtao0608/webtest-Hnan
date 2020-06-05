import unittest,os
import time
from Base import HTMLTestRunnerCNNew
from PageObj.login_page import LoginPage
from selenium import webdriver
from Common.function import project_path
from Base import ReadConfig


os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")
base_url = rc.get_ngboss("url")
username = rc.get_ngboss("username")
password = rc.get_ngboss("password")
# print(base_url)

class LoginTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_login(self):
        '''登录测试'''
        driver = self.driver
        driver.get(base_url)
        login = LoginPage(self.driver)
        login.login(username,password)
        # login.login('testkm01', '123456')
        driver.switch_to.default_content()
        res=driver.page_source
        # print(res)
        self.assertIn('TESTKM06', res)
        self.driver.close()


if __name__ == '__main__':
    report_title = u'登录自动化测试报告'
    # 定义脚本内容，加u为了防止中文乱码
    desc = u'搜索测试详情：'
    # 定义date为日期，time为时间
    date = time.strftime("%Y%m%d")
    time = time.strftime("%Y%m%d%H%M%S")
    # 定义一个测试容器
    testsuite = unittest.TestSuite()
    # 将测试用例添加到容器
    testsuite.addTest(LoginTest("test_login"))
    print("++++开始执行测试++++")
    with open(project_path() + "/Reports/"  + time + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2,retry=1)
        runner.run(testsuite)
        fp.close()

    '''
    retry，用例执行失败后指定重试次数，
    如果save_last_try 为True ，一个用例仅显示最后一次测试的结果。
                     为Flase，则展示全部测试结果。
    verbosity=2 为信息输出控制台的展示方式
    retry，指定重试次数
    '''