# -*- coding:utf-8 -*-
#__author:Administrator
#date: 2018/1/3

import os,time
import unittest
from Base import ReadConfig
from Base.Mylog import LogManager
from Base import HTMLTestRunnerCNNew
from Common.SuiteExec import DealSuiteExec as se

logger = LogManager('RunTest').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

class RunSuiteTest:
    def __init__(self):
        """
        初始化需要的参数
        :return:
        """
        global log, resultPath
        # log初始化
        log = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
        # 定义结果保存路径
        self.resultPath = ReadConfig.log_path
        print("log  ****"+self.resultPath)
        # 取得config\caselist.txt文件路径
        self.caseListFile = os.path.join(ReadConfig.conf_path, "caselist.txt")
        # 取得test_case文件目录
        # self.caseFile = os.path.join(ReadConfig.proDir, "../TestCases")
        self.caseDir = ReadConfig.case_path
        logger.info('用例目录:{}'.format(self.caseDir))

        # 定义一个空列表，用于保存类名
        self.caseList = []


    def get_caselist(self,suiteCode):
        """
        从本地mysql数据库中根据suiteCode获取用例执行到路径
        :return: self.caseList
        """
        # f = open(self.caseListFile)
        # for value in f.readlines():
        #     if value != '' and not value.startswith("#"):
        #         self.caseList.append(value.replace("\n", ""))
        # f.close()
        return se().get_execPathBySuiteCode(suiteCode=suiteCode) #返回一个用例执行到python文件列表


    def get_case_suite(self,suiteCode):
        """
        获取测试集
        :return:
        """
        # 获取config\caselist.txt中的每一行
        caseList=self.get_caselist(suiteCode)
        logger.info('从数据库中获取到用例文件路径列表:{}'.format(self.get_caselist(suiteCode)))
        # 定义测试集对象
        test_suite = unittest.TestSuite()
        # 初始化一个列表，存在所有的测试模块
        suite_module = []
        # 获取className ,把所有case中测试集添加到suite_module列表中
        for i in range(0,len(caseList)):
            case_name = caseList[i].split("/")[-1]
            print('****用例名称****{}'.format(case_name))
            discover = unittest.defaultTestLoader.discover(self.caseDir, pattern=case_name + ".py", top_level_dir=None)
            suite_module.append(discover)
        # print('*****suite_module********',suite_module)
        # print('*****suite_module的长度********',len(suite_module))


        # for case in caseList:
        #     case_name = case.split("/")[-1]
        #     discover = unittest.defaultTestLoader.discover(self.caseDir, pattern=case_name + ".py", top_level_dir=None)
        #     suite_module.append(discover)
        # 获取列表中所有的测试模块，添加到测试集test_suite中
        if len(suite_module) > 0:
            for suite in suite_module:
                for test_name in suite:
                    test_suite.addTest(test_name)
        else:
            return None
        return test_suite

    def run(self,suite_code):
        try:
            # 每次执行套件前将上次执行执行结果全部清空
            se().initSuiteExecData(suite_code)
            # 获取测试集
            suite = self.get_case_suite(suite_code)
            print("suite:", suite)
            # 判断测试集是否为None
            if suite is not None:
                log.info("********TEST START********")
                now = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime(time.time()))
                filepath = ReadConfig.proDir + "/Reports/" + now + '.html'
                print(filepath)
                fp = open(filepath, 'wb')
                # runner = HTMLTestRunner_PY3.HTMLTestRunner(stream=fp, title='WEB-UI自动化测试报告', description="测试报告")
                # f = open(self.resultPath, 'wb')
                # 使用HTMLTestRunner输出html报告
                # runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title='Test Report',
                #                 #                           description='Test Description', verbosity=2,retry=1,save_last_try=False)
                # 运行测试用例
                runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title='WEB-UI自动化测试报告',description='测试报告',verbosity=2,retry=0)
                runner.run(suite)
            else:
                log.info("Have no case to test.")
        except Exception as e:
            log.error(str(e))
        finally:
            log.info("*********TEST END*********")
            fp.close()


if __name__ == '__main__':
    testRun = RunSuiteTest()
    # suite = testRun.get_case_suite(suiteCode='SvcStateChgTest')
    suite = testRun.get_case_suite(suiteCode='SaleActive')
    print(suite)
    # print(type(suite))
    # testRun.run(suite_code='SvcStateChgTest')
    # testRun.run(suite_code='ProdChgTest')
    # testRun.run(suite_code='PlatSvcTest')
    # testRun.run(suite_code='SaleActive')



