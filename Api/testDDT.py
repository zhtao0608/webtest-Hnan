import ddt
import unittest,time
from Common.OperExcel import get_exceldata,write_excel_append
import json
from Common import ReadConfig
import HTMLTestRunnerCN
from Common.function import project_path

from Common.function import dict_get

rc = ReadConfig.ReadConfig("ngboss_config.ini")
file = ReadConfig.data_path + 'IntfTest.xls'
paras = get_exceldata(ReadConfig.data_path+ 'IntfTest.xls',0)
# print(paras)
# print("\n")

@ddt.ddt
class TestInter(unittest.TestCase):

    @ddt.data(*paras)
    def test_intf(self,dic):
        '''
        用户停开机业务受理接口测试类封装
        @param params 参数保存为接口类的参数，以字典格式传入
        svcname, accessNum, busicode, para
        ##构建intfTest请求
        '''
        # print(type(dic))
        print(json.dumps(dic))
        index = dic.get('No')
        print(type(index))
        print(index)

        svcname = dic.get('svcName')
        accessNum = dic.get('accessNum')
        busicode = dic.get('busicode')
        para = dic.get('para')
        # print("para参数化以后："+para)
        dic_para = json.loads(para)
        print(json.dumps(dic_para))
        params = {"svcName": svcname, "ACCESS_NUM": accessNum, "BUSI_ITEM_CODE": busicode}
        params.update(dic_para)
        print("params参数化以后的接口入参:"+json.dumps(params))
        write_excel_append(file,int(index),7,'x_result_info')

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
    # test = TestInter()
    # test.test_intf()
    report_title = u'接口自动化测试报告'
    desc = u'接口测试详情：'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath() + report_title + nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCN.HTMLTestReportCN(stream=fp, title=report_title, description=desc)
        runner.run(mySuitePrefixAdd(TestInter,"test_intf"))





