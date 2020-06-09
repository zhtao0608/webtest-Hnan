import unittest,os
import time,HTMLTestRunnerCN
from PageObj.login_page import LoginPage
from PageObj.loginPart import LoginPart
from selenium import webdriver
from Common.function import project_path
from Base import ReadConfig

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")
base_url = rc.get_ngboss("url")
username = rc.get_ngboss("username")
password = rc.get_ngboss("password")

class LoginTest(unittest.TestCase):
    """登录鉴权测试"""
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_loginpart(self):
        """服务号码登录，验证用户信息"""
        driver = self.driver
        driver.get(base_url)
        login = LoginPage(self.driver)
        login.login(username,password)
        # self.assertIn('ngboss.frame.pc.common', res)
        loginpart = LoginPart(self.driver)
        loginpart.login_by_pwd("13808710001","123123")
        import time
        time.sleep(3)
        hander = self.driver.current_window_handle
        self.driver.switch_to.window(hander)
        res = self.driver.page_source
        # print(res)
        self.assertIn('用户信息不存在', res)
        self.driver.close()

    def test_loginpart_grp(self):
        """集团编号登录，验证用户信息"""
        driver = self.driver
        driver.get(base_url)
        login = LoginPage(self.driver)
        login.login(username,password)
        loginpart = LoginPart(self.driver)
        loginpart.login_by_groupId("8721420859")
        import time
        time.sleep(5)
        hander = self.driver.current_window_handle
        self.driver.switch_to.window(hander)
        res = self.driver.page_source
        # print(res)
        self.assertIn("8721420859", res)
        self.driver.close()

    def tearDown(self):
        print('测试结束，关闭浏览器器!')
        self.driver.close()

if __name__ == '__main__':
    report_title = u'号码登录自动化测试报告'
    # 定义脚本内容，加u为了防止中文乱码
    desc = u'搜索测试详情：'
    # 定义date为日期，time为时间
    date = time.strftime("%Y%m%d")
    time = time.strftime("%Y%m%d%H%M%S")
    # 定义一个测试容器
    testsuite = unittest.TestSuite()
    # 将测试用例添加到容器
    testsuite.addTest(LoginTest("test_loginpart"))
    testsuite.addTest(LoginTest("test_loginpart_grp"))
    print("++++开始执行测试++++")
    with open(project_path() + "/Reports/"  + time + ".html", 'wb') as fp:
        #runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=report_title, description=desc)
        runner = HTMLTestRunnerCN.HTMLTestReportCN(stream=fp, title=report_title, description=desc)
        runner.run(testsuite)

