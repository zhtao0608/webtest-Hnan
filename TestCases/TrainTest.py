import os,sys
import ddt
# sys.path.append(os.path.split(os.getcwd()))
import time,unittest,HTMLTestRunner,HTMLTestRunnerCN
from Common.excel_data import get_exceldata,read_xls_by_row

from PageObj.ngboss.search_page import SearchPage
from selenium import webdriver
from Common.function import project_path


class seachtrainTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
    #数据驱动测试
    def test_01(self):
        self.data = get_exceldata(project_path()+"/Data/testdata2.xls",0)
        for i in range(len(self.data)):
            self.driver.get("https://trains.ctrip.com/TrainBooking/SearchTrain.aspx")
            print(self.data[i]['leave'],self.data[i]['arrive'],self.data[i]['leave_date'])
            # self.driver.get("https://trains.ctrip.com/TrainBooking/SearchTrain.aspx")
            search = SearchPage(self.driver)
            res = search.search_train(self.data[i]['leave'],self.data[i]['arrive'],self.data[i]['leave_date'])
            ##新增断言
            self.assertIn('booking',res)
            # self.driver.quit()

    def test_search(self):
        self.driver.get("https://trains.ctrip.com/TrainBooking/SearchTrain.aspx")
        self.data = read_xls_by_row(project_path() + "/Data/testdata2.xls", 0)
        search = SearchPage(self.driver)
        res = search.search_train(self.data.get(1)[0], self.data.get(1)[1], self.data.get(1)[2])
        ##新增断言
        self.assertIn('booking', res)
        # self.driver.quit()

    def tearDown(self):
        self.driver.quit()


# if __name__ == '__main__':
#     suiteTest = unittest.TestSuite()
#     suiteTest.addTest(seachtrainTest("test_01"))
#     now = time.strftime("%Y-%m-%d_%H_%M_%S",time.localtime(time.time()))
#     filepath = project_path() + "/Reports/" + now + '.html'
#     fp = open(filepath, 'wb')
#     runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='WEB-UI自动化测试报告', description="测试报告")
#     runner.run(suiteTest)
#     fp.close()




if __name__ == "__main__":
    report_title = u'规则自动化测试报告'
    # 定义脚本内容，加u为了防止中文乱码
    desc = u'搜索测试详情：'
    # 定义date为日期，time为时间
    date = time.strftime("%Y%m%d")
    time = time.strftime("%Y%m%d%H%M%S")
    # 定义一个测试容器
    testsuite = unittest.TestSuite()
    # 将测试用例添加到容器
    testsuite.addTest(seachtrainTest("test_search"))
    print("++++开始执行测试++++")
    with open(project_path() + "/Reports/"  + time + ".html", 'wb') as fp:
        #runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=report_title, description=desc)
        runner = HTMLTestRunnerCN.HTMLTestReportCN(stream=fp, title=report_title, description=desc)
        runner.run(testsuite)


