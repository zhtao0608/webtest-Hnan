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

class GroupBusiAcceptTestOper():
    def __init__(self):
        # self.file = file
        self.headers = h
        self.session = requests.session()
        self.session.post(url=rc.get_interface_url("url_login"), headers=h, data=lo_param)
        self.session.get(url=rc.get_interface_url("url_init"), headers=h)
        print("\n")

    def queryEnterpriseByGroupId(self,groupId):
        '''根据集团编码查询集团信息'''
        params = {
                    "GROUP_ID": groupId, #需要参数化 accessNum
                    "svcName": "CustomerCentre.custmgr.IEntQuerySV.queryEnterpriseByGroupId"
                }

        logger.info("接口名：" + params['svcName'])
        logger.info("拼装商品订购入参完成，接口完整入参：" + json.dumps(params))
        print("拼装入参完成，接口完整入参：" + json.dumps(params))
        logger.info("接口名：" + params['svcName'])
        logger.info("开始构建请求......"+"\n")
        intf_res = self.session.post(url=rc.get_interface_url("url_interface"),headers = h, data = params)
        print("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        d_intf_res = json.loads(intf_res.content.decode(encoding='utf-8'))
        x_resultcode = dict_get(d_intf_res, 'X_RESULTCODE', None)
        if x_resultcode == '0':
            result = dict_get(d_intf_res, 'DATAS', None)
            logger.info("查询成功，处理结果result：" + json.dumps(result, ensure_ascii=False))
            cust_id = result[0]['ORGA_ENTERPRISE_ID']
            group_id = result[0]['GROUP_ID']
            groupName = result[0]['GROUP_NAME']
            print("查询成功，集团编码为：" + group_id + "  集团名称：" + groupName + ", cust_id =" + cust_id )
            return cust_id

    def queryOfferInstByCustId(self,custId):
        '''根据集团客户标识查询已订购商品'''
        #先查询集团客户信息获取custId
        # custId = self.queryEnterpriseByGroupId('8743603478')  #返回custId
        params = {
                    "CUST_ID": custId,
                    "svcName": "OrderCentre.enterprise.IUmOfferQuerySV.queryOfferInstanceByCustIdAndOfferId"
                }

        logger.info("接口名：" + params['svcName'])
        logger.info("拼装商品订购入参完成，接口完整入参：" + json.dumps(params))
        print("拼装入参完成，接口完整入参：" + json.dumps(params))
        logger.info("接口名：" + params['svcName'])
        logger.info("开始构建请求......"+"\n")
        intf_res = self.session.post(url=rc.get_interface_url("url_interface"),headers = h, data = params)
        print("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
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
                print("订购的集团商品ID:" + offerId)
                print("订购的集团商品名称:" + offername)
                print("订购的集团用户ID:" + grp_inst_id)
                print("订购的集团商品实例ID:" + offerInstId)
                # return json.dumps(result, ensure_ascii=False)
        else:
            x_resultInfo = dict_get(d_intf_res, 'x_resultinfo', None)
            return x_resultInfo


    def queryOfferInstByCustIdAndOfferId(self,custId,offerId):
        '''根据集团客户标识和主商品OFFERID查询已订购商品'''
        #先查询集团客户信息获取custId
        # custId = self.queryEnterpriseByGroupId('8743603478')  #返回custId
        params = {
                    "CUST_ID": custId, #参数化 custId 由上个接口返回
                    "OFFER_ID":int(offerId),
                    "svcName": "OrderCentre.enterprise.IUmOfferQuerySV.queryOfferInstanceByCustIdAndOfferId"
                }

        logger.info("接口名：" + params['svcName'])
        logger.info("拼装商品订购入参完成，接口完整入参：" + json.dumps(params))
        print("拼装入参完成，接口完整入参：" + json.dumps(params))
        logger.info("接口名：" + params['svcName'])
        logger.info("开始构建请求......"+"\n")
        intf_res = self.session.post(url=rc.get_interface_url("url_interface"),headers = h, data = params)
        print("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        logger.info("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
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
                return json.dumps(result, ensure_ascii=False)
        else:
            x_resultInfo = dict_get(d_intf_res, 'x_resultinfo', None)
            return x_resultInfo



if __name__ == '__main__':
    test = GroupBusiAcceptTestOper()
    cust_id = test.queryEnterpriseByGroupId('8713164024')
    test.queryOfferInstByCustIdAndOfferId(cust_id,100000950)
    print("开始执行第2个接口 \n")
    test.queryOfferInstByCustId(cust_id)

