# -*- coding:utf-8 -*-
from __future__ import unicode_literals
# import unittest,HTMLTestRunnerCN,ddt
import time,sys,io
import requests
import json
from Base import ReadConfig
from Base.Mylog import LogManager
from Base.OperExcel import get_exceldata,write_excel_append
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
logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

class GrpMebOpers():
    def __init__(self):
        self.headers = h
        self.session = requests.session()
        self.session.post(url=rc.get_interface_url("url_login"), headers=h, data=lo_param)
        self.session.get(url=rc.get_interface_url("url_init"), headers=h)
        print("\n")

    def queryInfoByAccessNumber(self,accessNum):
        '''根据号码查询用户信息'''
        logger.info("开始参数化......")
        params = {
                    "ACCESS_NUM": accessNum, #需要参数化 accessNum
                    "svcName": "OrderCentre.enterprise.IMemberUserInfoQuerySV.queryInfoByAccessNumber"
                }
        print("接口名：" + params['svcName'])
        print("拼装入参完成，接口完整入参：" + json.dumps(params))
        logger.info("接口名：" + params['svcName'])
        logger.info("拼装商品订购入参完成，接口完整入参：" + json.dumps(params))
        logger.info("接口名：" + params['svcName'])
        logger.info("开始构建请求......"+"\n")
        intf_res = self.session.post(url=rc.get_interface_url("url_interface"),headers = h, data = params)
        print("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        logger.info("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        logger.info("处理接口返回数据....")
        d_intf_res = json.loads(intf_res.content.decode(encoding='utf-8'))
        x_resultcode = dict_get(d_intf_res, 'X_RESULTCODE', None)
        if x_resultcode == '0':
            result = dict_get(d_intf_res, 'DATAS', None)
            access_num = result[0]['ACCESS_NUM']
            subscriber_inst_id = result[0]['SUBSCRIBER_INS_ID']
            print("接口处理成功，受理号码为：" + access_num + "  用户实例号：" + subscriber_inst_id)
            return subscriber_inst_id

    def queryOfferInstByAccessNumber(self,accessNum):
        '''根据手机号码查询订购的集团商品'''
        userId = self.queryInfoByAccessNumber(accessNum)
        params = {
                    "SUBSCRIBER_INS_ID":userId ,
                    "svcName": "OrderCentre.enterprise.IUmOfferQuerySV.queryOfferInstanceByMebSubscriberInsId"
                }
        logger.info("接口名：" + params['svcName'])
        logger.info("拼装商品订购入参完成，接口完整入参：" + json.dumps(params))
        print("拼装入参完成，接口完整入参：" + json.dumps(params))
        logger.info("接口名：" + params['svcName'])
        logger.info("开始构建请求......"+"\n")
        intf_res = self.session.post(url=rc.get_interface_url("url_interface"),headers = h, data = params)
        print("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        logger.info("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
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

    def querySubscriberRel(self,accessNum,rel_type):
        '''根据用户实例查询订购的集团商品'''
        userId = self.queryInfoByAccessNumber(accessNum)
        params = {
            "REL_SUBSCRIBER_INS_ID": userId,  # 需要参数化 userId
            "SUBSCRIBER_REL_TYPE": rel_type,  # 需要参数化
            "ACCESS_NUM":accessNum,
            "svcName": "OrderCentre.enterprise.IUmSubscriberRelQuerySV.querySubscriberRelByRelSubInsIdAndSubRelType"
        }
        logger.info("接口名：" + params['svcName'])
        logger.info("拼装商品订购入参完成，接口完整入参：" + json.dumps(params))
        print("拼装入参完成，接口完整入参：" + json.dumps(params))
        logger.info("接口名：" + params['svcName'])
        logger.info("开始构建请求......" + "\n")
        intf_res = self.session.post(url=rc.get_interface_url("url_interface"), headers=h, data=params)
        print("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        logger.info("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        logger.info("处理接口返回数据....")
        d_intf_res = json.loads(intf_res.content.decode(encoding='utf-8'))
        x_resultcode = dict_get(d_intf_res, 'X_RESULTCODE', None)
        if x_resultcode == '0':
            result = dict_get(d_intf_res, 'DATAS', None)
            print("查询结果：" + json.dumps(result, ensure_ascii=False))
            logger.info("查询成功，处理结果result：" + json.dumps(result, ensure_ascii=False))
            for i in range(len(result)):
                grp_inst_id = result[i]['SUBSCRIBER_INS_ID']
                accessnum = result[i]['REL_ACCESS_NUM']
                reltype = result[i]['SUBSCRIBER_REL_TYPE']
                logger.info("订购的集团用户ID:" + grp_inst_id)
                print("成员号码：" + accessnum +  " 订购的集团用户ID:" + grp_inst_id + " 关系类型：" + reltype )
            return json.dumps(result, ensure_ascii=False)  # 把订购关系返回
        else:
            x_resultInfo = dict_get(d_intf_res, 'x_resultinfo', None)
            return x_resultInfo

    def ImsMebStopOrOpen(self,imsNum,operCode):
        '''IMS号码停开机接口'''
        params = {
            "IMS_USER_STATE": operCode,  #02停机 01 开机
            "ACCESS_NUM": imsNum,  # 需要参数化
            "svcName": "OrderCentre.enterprise.IImsCloseGrpMainOperateSV.commitUserSvcOpen"
        }
        logger.info("接口名：" + params['svcName'])
        logger.info("拼装商品订购入参完成，接口完整入参：" + json.dumps(params))
        print("拼装入参完成，接口完整入参：" + json.dumps(params))
        logger.info("接口名：" + params['svcName'])
        logger.info("开始构建请求......" + "\n")
        intf_res = self.session.post(url=rc.get_interface_url("url_interface"), headers=h, data=params)
        print("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        logger.info("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        logger.info("处理接口返回数据....")
        d_intf_res = json.loads(intf_res.content.decode(encoding='utf-8'))
        x_resultcode = dict_get(d_intf_res, 'X_RESULTCODE', None)
        if x_resultcode == '0':
            flowid = dict_get(d_intf_res, 'DATAS', None)
            logger.info(" 受理成功,业务交互流水号：" + flowid)
            print(" 受理成功,业务交互流水号：" + flowid)
        else:
            x_resultInfo = dict_get(d_intf_res, 'x_resultinfo', None)
            print("受理异常，错误信息：" + x_resultInfo)
            logger.info("受理异常，错误信息：" + x_resultInfo)
            return x_resultInfo

if __name__ == '__main__':
    test = GrpMebOpers()
    # print("开始执行第1个接口 \n")
    # userId = test.queryInfoByAccessNumber('13987262203')
    # print("开始执行第2个接口 \n")
    # test.queryOfferInstByAccessNumber('13987262203')
    # print("开始执行第3个接口 \n")
    # test.querySubscriberRel('08753033636','E1')
    print("开始执行第4个接口 \n")
    test.ImsMebStopOrOpen('08753033500','02')
    self.sleep(10)
    test.ImsMebStopOrOpen('08753033500','01')




