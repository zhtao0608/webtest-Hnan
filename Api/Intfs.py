import unittest,ddt,HTMLTestRunnerCN
import time
from Common.OperExcel import get_exceldata
import requests
import json
from Common import ReadConfig
from Common.Mylog import LogManager
from Common.function import dict_get

logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
rc = ReadConfig.ReadConfig("ngboss_config.ini")
h = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36',
    "Connection": "keep - alive",
    "Referer": "http://10.174.43.39:9090/ngboss"
}

lo_param = {"LOGIN_MODE": "BOSS", "STAFF_ID": "TESTKM06", "IS_XACTIVE": "false", "BROWSER_VERSION": "IE-11",
        "PASSWORD": "e3937dc80f9bb5ab17cc016cdc612b7d", "LOGIN_FLAG": "1"}




##数据驱动paramunittest：
# interfaceList_xls = get_exceldata(ReadConfig.data_path+ 'testdata.xls',0)
# print(interfaceList_xls)
# @paramunittest.parametrized(*interfaceList_xls)
paras = get_exceldata(ReadConfig.data_path+ 'IntfTest.xls',0)
# print(paras)

@ddt.ddt
class TestInter(unittest.TestCase):
    def setUp(self):
        self.headers = h
        self.session = requests.session()

    def setParameters(self,CaseNo,svcName,accessNum,busicode,para,x_resultinfo,Expect_result,flow_id ):
        self.CaseNo = str(CaseNo)
        self.svcName = str(svcName)
        self.params = str(para)
        self.accessNum = str(accessNum)
        self.busicode = str(busicode)
        self.x_resultinfo = str(x_resultinfo)
        self.Expect_result = str(Expect_result )
        self.flowId = str(flow_id )

    def main_login(self):
        # session发送登录请求
        lo_url = rc.get_interface_url("url_login")
        print("url_login:" + lo_url)
        resp = self.session.post(url=lo_url,headers=h,data=lo_param)
        print(resp.content.decode(encoding='utf-8'))
        init_resp = self.session.get(url =rc.get_interface_url("url_init"),headers= h)
        print(init_resp.content.decode(encoding='utf-8'))
        return init_resp

    def intf_subscriberstop(self,svcname,accessnum):
        '''用户停机接口测试方法'''
        ##构建intfTest请求
        intf_url = rc.get_interface_url("url_interface")
        print("url_interface:"+intf_url)
        #停机参数
        params = {  "svcName":svcname,
                    "REMARKS":"test_by_api",
                    "BUSI_ITEM_CODE":"131",
                    "SUBMIT_TYPE":"0",
                    "ACCESS_NUM":accessnum,
                    "LOGIN_TYPE_CODE":"|P"
                }
        intf_res = self.session.post(url=intf_url,headers = h,data = params)
        d_intf_res = json.loads(intf_res.content.decode(encoding='utf-8'))
        print(d_intf_res)
        x_resultcode = dict_get(d_intf_res, 'x_resultcode', None)
        if x_resultcode == '0':
            flowid = dict_get(d_intf_res, 'flowId', None)
            access_num = dict_get(d_intf_res, 'ACCESS_NUM', None)
            logger.info("接口处理成功，受理号码为："+ access_num +"  订单交互流水号："+flowid)
            print("接口处理成功，受理号码为："+ access_num +"  订单交互流水号："+flowid)
        else:
            # FrameLog.log().info("接口调用失败")
            x_resultinfo = dict_get(d_intf_res, 'x_resultinfo', None)
            logger.info("接口调用失败，错误信息："+x_resultinfo)
            print("接口处理错误信息：" + x_resultinfo)
        # print("接口处理情况："+intf_res.content.decode(encoding='utf-8'))

    def intf_subscriberOpen(self,svcname,accessnum):
        '''用户开机测试方法'''
        ##构建intfTest请求
        intf_url = rc.get_interface_url("url_interface")
        print("url_interface:"+intf_url)
        #停机参数
        params = {  "svcName":svcname,
                    "REMARKS":"test_by_api",
                    "BUSI_ITEM_CODE":"133",
                    "SUBMIT_TYPE":"0",
                    "ACCESS_NUM":accessnum,
                    "LOGIN_TYPE_CODE":"|P"
                }
        intf_res = self.session.post(url=intf_url,headers = h,data = params)
        d_intf_res = json.loads(intf_res.content.decode(encoding='utf-8'))
        print(d_intf_res)
        x_resultcode = dict_get(d_intf_res, 'x_resultcode', None)
        if x_resultcode == '0':
            flowid = dict_get(d_intf_res, 'flowId', None)
            access_num = dict_get(d_intf_res, 'ACCESS_NUM', None)
            logger.info("接口处理成功，受理号码为：" + access_num + "  订单交互流水号："+ flowid)
            print("接口处理成功，受理号码为：" + access_num + "  订单交互流水号：" + flowid)
        else:
            x_resultinfo = dict_get(d_intf_res, 'x_resultinfo', None)
            logger.info("接口调用失败，错误信息：" + x_resultinfo)
            print("接口处理错误信息：" + x_resultinfo)

    def intf_StopOrOpen(self,svcname,accessnum,busi_code):
        '''
        用户停开机业务受理接口测试类封装
        @param busi_code 131 Stop
        @param busi_code 133 Open
        '''
        ##构建intfTest请求
        intf_url = rc.get_interface_url("url_interface")
        print("url_interface:"+intf_url)
        #停机参数
        params = {  "svcName":svcname,
                    "REMARKS":"test_by_api",
                    "BUSI_ITEM_CODE":busi_code,
                    "SUBMIT_TYPE":"0",
                    "ACCESS_NUM":accessnum,
                    "LOGIN_TYPE_CODE":"|P"
                }
        intf_res = self.session.post(url=intf_url,headers = h,data = params)
        d_intf_res = json.loads(intf_res.content.decode(encoding='utf-8'))
        print(d_intf_res)
        x_resultcode = dict_get(d_intf_res, 'x_resultcode', None)
        if x_resultcode == '0':
            flowid = dict_get(d_intf_res, 'flowId', None)
            access_num = dict_get(d_intf_res, 'ACCESS_NUM', None)
            logger.info("接口处理成功，受理号码为：" + access_num + "  订单交互流水号：" + flowid)
            print("接口处理成功，受理号码为：" + access_num + "  订单交互流水号：" + flowid)
        else:
            # FrameLog.log().info("接口调用失败")
            x_resultinfo = dict_get(d_intf_res, 'x_resultinfo', None)
            logger.info("接口调用失败，错误信息：" + x_resultinfo)
            print("接口处理错误信息：" + x_resultinfo)
        # print("接口处理情况："+intf_res.content.decode(encoding='utf-8'))

    @ddt.data(*paras)
    def test_intf(self,dic):
        '''
        用户停开机业务受理接口测试类封装并参数化，参数包括：
        svcname, accessNum, busicode, para
        参数化后的接口入参 params 参数保存为接口类的参数，以字典格式传入
        构建intfTest请求并判断返回
        后续缺失内容：将测试结果自动写入xls
        '''
        ####每次都先登录一下
        logger.info("构建登录请求.....")
        lo_url = rc.get_interface_url("url_login")
        print("url_login:" + lo_url)
        self.session.post(url=lo_url, headers=h, data=lo_param)
        self.session.get(url=rc.get_interface_url("url_init"), headers=h)
        logger.info("开始参数化......")
        svcname = dic.get('svcName')
        logger.info("测试接口名:"+svcname)
        # print(svcname)
        accessNum = dic.get('accessNum')
        logger.info("测试号码:"+accessNum)
        busicode = dic.get('busicode')
        # print(busicode)
        logger.info("停开机业务类型:"+busicode)
        para = dic.get('para')
        dic_para = json.loads(para)
        print(json.dumps(dic_para))
        params = {"svcName": svcname, "ACCESS_NUM": accessNum, "BUSI_ITEM_CODE": busicode}
        params.update(dic_para)
        logger.info("params参数化以后的接口入参:"+json.dumps(params))
        print("params参数化以后的接口入参:"+json.dumps(params))
        logger.info("开始接口测试开始，接口名为"+svcname +" 接口参数是：" + json.dumps(params))

        logger.info("开始构建请求......"+"\n")
        intf_url = rc.get_interface_url("url_interface")
        logger.info("接口测试地址：" + intf_url )
        intf_res = self.session.post(url=intf_url,headers = h,data = params)
        d_intf_res = json.loads(intf_res.content.decode(encoding='utf-8'))
        x_resultcode = dict_get(d_intf_res, 'x_resultcode', None)
        logger.info("开始处理接口返回参数......")
        if x_resultcode == '0':
            flowid = dict_get(d_intf_res, 'flowId', None)
            access_num = dict_get(d_intf_res, 'ACCESS_NUM', None)
            logger.info("接口处理成功，受理号码为："+ access_num +"  订单交互流水号："+flowid)
            print("接口处理成功，受理号码为："+ access_num +"  订单交互流水号："+flowid)
        else:
            x_resultinfo = dict_get(d_intf_res, 'x_resultinfo', None)
            logger.info("接口调用失败，错误信息："+x_resultinfo)
            print("接口处理错误信息：" + x_resultinfo)

if __name__ == '__main__':
    #先调用一下main_login，初始化session
    test = TestInter()
    test.main_login()
    report_title = u'接口自动化测试报告'
    desc = u'接口测试详情：'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    # 定义一个测试容器
    suite = unittest.TestSuite()
    # 将测试用例添加到容器
    suite.addTest(TestInter("test_intf"))
    print("++++开始执行测试++++")
    with open(ReadConfig.get_reportPath() + report_title + nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCN.HTMLTestReportCN(stream=fp, title=report_title, description=desc,verbosity=2)
        runner.run(suite)








