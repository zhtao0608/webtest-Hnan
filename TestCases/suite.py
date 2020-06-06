import unittest
from Base import HTMLTestRunnerCNNew
import time
from Common.function import project_path

def mySuitePrefixAdd(MyClass,cases):
    '''
    根据前缀添加测试用例-可用于ddt数据用例
    :param MyClass:
    :param cases:
    :return:
    '''
    test_list = []
    testdict = MyClass.__dict__
    if isinstance(cases,str):
        cases = [cases]
    for case in cases:
        tmp_cases = filter(lambda cs:cs.startswith(case) and callable(getattr(MyClass,cs)),testdict)
        for tmp_case in tmp_cases:
            test_list.append(MyClass(tmp_case))
    suite = unittest.TestSuite()
    suite.addTests(test_list)
    return suite


if __name__ == '__main__':
    test_dir = project_path()+"/TestCases"
    tests = unittest.defaultTestLoader.discover(test_dir,
                                                pattern="Case*.py",
                                                top_level_dir=None)
    now = time.strftime("%Y-%m-%d_%H_%M_%S",time.localtime(time.time()))
    filepath = project_path() + "/Reports" + now +'.html'
    fp = open(filepath,'wb')
    runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp,title='WEB-UI自动化测试报告',description="测试报告")
    runner.run(tests)
    fp.close()

