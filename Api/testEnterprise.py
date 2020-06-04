# -*- coding:utf-8 -*-
from __future__ import unicode_literals
import unittest,HTMLTestRunnerCN,ddt
import time,sys,io
import requests
import json
from Common import ReadConfig
from Common.Mylog import LogManager
from Common.OperExcel import get_exceldata,write_excel_append
from Common.function import dict_get

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
rc = ReadConfig.ReadConfig("ngboss_config.ini")
h = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36',
    "Connection": "keep - alive",
    "Referer": rc.get_ngboss('url')
}

lo_param = {"LOGIN_MODE": "BOSS", "STAFF_ID": "TESTKM06", "IS_XACTIVE": "false", "BROWSER_VERSION": "IE-11",
        "PASSWORD": "e3937dc80f9bb5ab17cc016cdc612b7d", "LOGIN_FLAG": "1"}

# file = ReadConfig.data_path + 'IntfTest_Enterprise.xls'
# paras = get_exceldata(file,0)
logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
# print(type(paras))
# print(paras)

class TestEnterprise(unittest.TestCase):
    def setUp(self):
        # self.file = file
        self.headers = h
        self.session = requests.session()
        self.session.post(url=rc.get_interface_url("url_login"), headers=h, data=lo_param)
        self.session.get(url=rc.get_interface_url("url_init"), headers=h)
        print("\n")

    def test_queryEnterpriseByGroupId(self,groupId):
        '''根据集团编码查询集团信息'''
        logger.info("开始参数化......")

        params = {
                    "GROUP_ID": groupId, #需要参数化 accessNum
                    "svcName": "CustomerCentre.custmgr.IEntQuerySV.queryEnterpriseByGroupId"
                }

        logger.info("接口名：" + params['svcName'])
        logger.info("拼装商品订购入参完成，接口完整入参：" + json.dumps(params))
        print("拼装入参完成，接口完整入参：" + json.dumps(params))
        logger.info("接口名：" + params['svcName'])
        logger.info("开始构建请求......"+"\n")
        intf_url = rc.get_interface_url("url_interface")
        logger.info("接口测试地址：" + intf_url )
        intf_res = self.session.post(url=intf_url,headers = h, data = params)
        print("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        logger.info("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        # print(intf_res.content.decode(encoding='utf-8'))
        logger.info("处理接口返回数据....")
        d_intf_res = json.loads(intf_res.content.decode(encoding='utf-8'))
        x_resultcode = dict_get(d_intf_res, 'X_RESULTCODE', None)
        if x_resultcode == '0':
            result = dict_get(d_intf_res, 'DATAS', None)
            logger.info("查询成功，处理结果result：" + json.dumps(result, ensure_ascii=False))
            cust_id = result[0]['ORGA_ENTERPRISE_ID']
            group_id = result[0]['GROUP_ID']
            groupName = result[0]['GROUP_NAME']
            # print(type(subscriber_inst_id))
            print("查询成功，集团编码为：" + group_id + "  集团名称：" + groupName + "cust_id =" + cust_id )
            # return json.dumps(result, ensure_ascii=False)
            return cust_id


    def test_queryOfferInstanceByCustIdAndOfferId(self):
        '''根据集团客户标识查询已订购商品'''
        #先查询集团客户信息获取custId
        custId = self.test_queryEnterpriseByGroupId('8743603478')  #返回custId
        # logger.info("开始参数化......")
        # index = int(dic.get('No'))
        # accessNum = str(dic.get('accessNum'))
        # logger.info("测试号码:"+accessNum)
        params = {
                    "CUST_ID": custId, #参数化 custId 由上个接口返回
                    "svcName": "OrderCentre.enterprise.IUmOfferQuerySV.queryOfferInstanceByCustIdAndOfferId"
                }

        logger.info("接口名：" + params['svcName'])
        logger.info("拼装商品订购入参完成，接口完整入参：" + json.dumps(params))
        print("拼装入参完成，接口完整入参：" + json.dumps(params))
        logger.info("接口名：" + params['svcName'])
        logger.info("开始构建请求......"+"\n")
        intf_url = rc.get_interface_url("url_interface")
        logger.info("接口测试地址：" + intf_url )
        intf_res = self.session.post(url=intf_url,headers = h, data = params)
        print("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        logger.info("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        logger.info("处理接口返回数据....")
        d_intf_res = json.loads(intf_res.content.decode(encoding='utf-8'))
        x_resultcode = dict_get(d_intf_res, 'X_RESULTCODE', None)
        if x_resultcode == '0':
            result = dict_get(d_intf_res, 'DATAS', None)
            logger.info("查询成功，处理结果result：" + json.dumps(result, ensure_ascii=False))
            for i in range(len(result)):
                print("已订购的集团商品列表" + str(i) + ":\n" + json.dumps(result[i], ensure_ascii=False))
                offerId = result[i]['OFFER_ID']
                offername = result[i]['OFFER_NAME']
                grp_inst_id = result[i]['SUBSCRIBER_INS_ID']
                offerInstId = result[i]['OFFER_INS_ID']
                logger.info("订购的集团商品ID:" + offerId)
                logger.info("订购的集团商品名称:" + offername)
                logger.info("订购的集团用户ID:" + grp_inst_id)
                logger.info("订购的集团商品实例ID:" + offerInstId)
                print("订购的集团商品ID:" + offerId)
                print("订购的集团商品名称:" + offername)
                print("订购的集团用户ID:" + grp_inst_id)
                print("订购的集团商品实例ID:" + offerInstId)
                # return json.dumps(result, ensure_ascii=False)
        else:
            x_resultInfo = dict_get(d_intf_res, 'x_resultinfo', None)
            return x_resultInfo

    # @ddt.data(*paras)
    def test_queryInfoByAccessNumber(self,accessNum):
        '''根据号码查询用户信息'''
        logger.info("开始参数化......")
        params = {
                    "ACCESS_NUM": accessNum, #需要参数化 accessNum
                    "svcName": "OrderCentre.enterprise.IMemberUserInfoQuerySV.queryInfoByAccessNumber"
                }

        logger.info("接口名：" + params['svcName'])
        logger.info("拼装商品订购入参完成，接口完整入参：" + json.dumps(params))
        print("拼装入参完成，接口完整入参：" + json.dumps(params))
        logger.info("接口名：" + params['svcName'])
        logger.info("开始构建请求......"+"\n")
        intf_url = rc.get_interface_url("url_interface")
        logger.info("接口测试地址：" + intf_url )
        intf_res = self.session.post(url=intf_url,headers = h, data = params)
        print("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        logger.info("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        # print(intf_res.content.decode(encoding='utf-8'))
        logger.info("处理接口返回数据....")
        d_intf_res = json.loads(intf_res.content.decode(encoding='utf-8'))
        x_resultcode = dict_get(d_intf_res, 'X_RESULTCODE', None)
        # x_resultinfo = dict_get(d_intf_res, 'X_RESULTINFO', None)
        if x_resultcode == '0':
            result = dict_get(d_intf_res, 'DATAS', None)
            access_num = result[0]['ACCESS_NUM']
            subscriber_inst_id = result[0]['SUBSCRIBER_INS_ID']
            # print(type(subscriber_inst_id))
            print("接口处理成功，受理号码为：" + access_num + "  用户实例号：" + subscriber_inst_id)
            return subscriber_inst_id
            # logger.info("开始写入xls数据......")
            # write_excel_append(self.file, index, 3, x_resultinfo)
            # write_excel_append(self.file, index, 2, flowid)
            # logger.info("测试结果写入xls成功......")

    def test_queryOfferInstByMebSubscriberInsId(self):
        '''根据用户实例查询订购的集团商品'''
        subscriberId = self.test_queryInfoByAccessNumber('13987267334')
        print(subscriberId)
        logger.info("用户实例subscriber_inst_id :" + str(subscriberId))
        params = {
                    "SUBSCRIBER_INS_ID":subscriberId , #需要参数化 accessNum
                    "svcName": "OrderCentre.enterprise.IUmOfferQuerySV.queryOfferInstanceByMebSubscriberInsId"
                }
        logger.info("接口名：" + params['svcName'])
        logger.info("拼装商品订购入参完成，接口完整入参：" + json.dumps(params))
        print("拼装入参完成，接口完整入参：" + json.dumps(params))
        logger.info("接口名：" + params['svcName'])
        logger.info("开始构建请求......"+"\n")
        intf_url = rc.get_interface_url("url_interface")
        logger.info("接口测试地址：" + intf_url )
        intf_res = self.session.post(url=intf_url,headers = h, data = params)
        print("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        logger.info("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        # print(intf_res.content.decode(encoding='utf-8'))
        logger.info("处理接口返回数据....")
        d_intf_res = json.loads(intf_res.content.decode(encoding='utf-8'))
        x_resultcode = dict_get(d_intf_res, 'X_RESULTCODE', None)
        # x_resultinfo = dict_get(d_intf_res, 'X_RESULTINFO', None)
        if x_resultcode == '0':
            result = dict_get(d_intf_res, 'DATAS', None)
            print("查询结果：" + json.dumps(result,ensure_ascii=False))
            logger.info("查询成功，处理结果result：" + json.dumps(result,ensure_ascii=False))
            for i in range(len(result)):
                print("已订购的集团商品列表" + str(i) + ":\n" + json.dumps(result[i],ensure_ascii=False))
                offername = result[i]['OFFER_NAME']
                grp_inst_id = result[i]['SUBSCRIBER_INS_ID']
                logger.info("订购的集团商品名称:" + offername)
                logger.info("订购的集团用户ID:" + grp_inst_id)
                print("订购的集团商品名称:" + offername)
                print("订购的集团用户ID:" + grp_inst_id)
            return json.dumps(result,ensure_ascii=False)  #把订购的集团商品实例列表返回
        else:
            x_resultInfo = dict_get(d_intf_res, 'x_resultinfo', None)
            return x_resultInfo


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
    # test = TestEnterprise()
    # test.test_queryInfoByAccessNumber()

    report_title = u'接口自动化测试报告'
    desc = u'接口测试详情：'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath() + report_title + nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCN.HTMLTestReportCN(stream=fp, title=report_title, description=desc,verbosity=2)
        runner.run(mySuitePrefixAdd(TestEnterprise,"queryOfferInstByMebSubscriberInsId"))
