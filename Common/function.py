# coding: utf-8
import time,datetime
from datetime import timedelta, date
import os,configparser
import hashlib
import types
from urllib import parse
import json

def project_path():
    return os.path.dirname(os.path.dirname(__file__))
    # print(os.path.dirname(os.path.dirname(__file__)))

#返回config_ini文件中的testUrl
def config_url():
    config = configparser.ConfigParser()
    config.read(project_path()+"/config.ini")
    return config.get('NGBOSS','url')

def date_n(n):
	'''返回当前日期后n天的日期'''
	return date.today()+timedelta(days=n)

def datetime_n(n):
	'''返回当前时间n天后的时间'''
	nowtime = time.strftime("%Y-%m-%d %H:%M:%S")
	start_time = datetime.datetime.strptime(nowtime,'%Y-%m-%d %H:%M:%S')
	return start_time + timedelta(days=n)

# 等式转换成字典格式
def ret_dic(str_Val):
    co = {}
    for line in str_Val.split(';'):
        key, value = line.split('=', 1)
        co[key] = value
    return co

# 获取字典中的objkey对应的值，适用于字典嵌套
# dict:字典
# objkey:目标key
# default:找不到时返回的默认值
def dict_get(dict, objkey, default):
    tmp = dict
    for k, v in tmp.items():
        if k == objkey:
            return v
        else:
            # if type(v) is types.DictType.:
            if type(v).__name__ == 'dict':
                ret = dict_get(v, objkey, default)
                if ret is not default:
                    return ret
    return default

# #如
# dicttest={"result":{"code":"110002","msg":"设备设备序列号或验证码错误"}}
# dicttest2={'context': {'provinceId': '', 'contextRoot': '', 'productMode': 'true', 'subSysCode': '', 'x_resultinfo': 'ok', 'x_resultcode': '0', 'contextName': '', 'version': '0'}, 'data': {}}
# dictest3= {'context': {'provinceId': '', 'contextRoot': '', 'productMode': 'true', 'subSysCode': '', 'x_resultinfo': 'ok', 'x_resultcode': '0', 'contextName': '', 'version': '0'}, 'data': {'ROUTE_CODE': '0872', 'X_RESULTINFO': 'ok', 'X_NODE_NAME': 'app-node01-srv01', 'ACCESS_NUM': '13988508496', 'flowId': '7220042400498435', 'X_RESULTCODE': '0'}}
# ret=dict_get(dicttest2, 'x_resultinfo', None)
# ret3 = dict_get(dictest3, 'flowId', None)
# print(ret)
# print(ret3)
def md5(arg):
    '''
    用于把用户的密码加密
    '''
    md5 = hashlib.md5()
    md5.update(bytes(arg, encoding='utf-8'))

    return md5.hexdigest()

def get_enurl(*args):
    return parse.urlencode(*args)

def join_dictlists(list1,list2):
	'''
	合并两个字典数组 ，两个数组的len一致
	:param list1:
	:param list2:
	:return:
	'''
	if not len(list1) == len(list2):
		print('两个list的长度不一致，不能合并！')
	else:
		newlist = []
		for i in range(len(list1)):
			list1[i].update(list2[i])
			print(list1[i])
			newlist.append(list1[i])
		print('合并后的list:',newlist)
		return newlist


# dic_1 = {"REMARKS":"test_by_api","BUSI_ITEM_CODE":"131","SUBMIT_TYPE":"0","ACCESS_NUM":"18213349760","LOGIN_TYPE_CODE":"|P"}
# print(get_enurl(dic_1))

# if __name__ == '__main__':
#     print("项目路径"+project_path())
#     print(project_path())
#
#     # print(project_path()+"/config.ini")
#     print("被测系统Url:"+config_url())

if __name__ == '__main__':
	daten = date_n(10)
	print('n天后的日期:' ,daten)
	datetimen = datetime_n(30)
	print('n天后的时间：',datetimen)
    # co = "SUBSCRIBER_OPEN_COOKIE_10=3Rz6w1QsiDxyypM51REBbQ%3D%3D; CRM_ECNAVIGATION_COOKIE=bnLIzblE%2B3B1QqCj583MjVcmUOU4lV3JrAg8genK9jJABq1Y1q9XTClc7P7%2BYKsG6A3wS4NtCSKsrgayrQ7iAuNuOPtx%2Bxnrii2nv8m%2BzEAsv%2FRNXoFz5OJLs56Cxobb5a9EhkUVCmD9BDNUf0DlurzA0aMrDMrl; NGBOSS_NAVHELP_COOKIE=AokBKhs3DpmzVbmKdWoLGQ%3D%3D; STAFF_ID=TESTKM06; DEPART_ID=55913; STAFF_EPARCHY_CODE=0872; WADE_SID=2359B5A00E744C4B9B58D3EF2EBE1BE8; NGBOSS_LOGIN_COOKIE=X48c74%2FfJTxsBP5IY9m6A0%2FsS9SMWUNZtqUtYnG20bA30bCuF9z8Ow%3D%3D"
	dictest = {
	"context": {
		"provinceId": "",
		"contextRoot": "",
		"productMode": "true",
		"subSysCode": "",
		"x_resultinfo": "ok",
		"x_resultcode": "0",
		"contextName": "",
		"version": "0"
	},
	"data": {
		"X_RESULTINFO": "ok",
		"X_NODE_NAME": "app-node01-srv01",
		"DATAS": [{
			"EXPIRE_DATE": "2050-12-31 23:59:59.0",
			"DATA_STATUS": "1",
			"OP_ID": "CB201014",
			"IS_MAIN": "1",
			"OFFER_NAME": "移动人人通A(ADC)",
			"MGMT_COUNTY": "C0LB",
			"SUBSCRIBER_INS_ID": "7090120700227870",
			"OFFER_INS_ID": "7090120743986708",
			"ORG_ID": "41921",
			"CREATE_ORG_ID": "41921",
			"REGION_ID": "06",
			"CUST_ID": "7009120710016270",
			"CREATE_OP_ID": "CB201014",
			"VALID_DATE": "2014-09-29 16:48:14.0",
			"OFFER_ID": "6465",
			"DONE_DATE": "2010-12-07 17:42:11.0",
			"CREATE_DATE": "2010-12-07 17:42:11.0",
			"IS_BUNDLE": "1",
			"BRAND": "ADCG",
			"OFFER_TYPE": "10",
			"MGMT_DISTRICT": "0870"
		}, {
			"EXPIRE_DATE": "2050-12-31 23:59:59.0",
			"DATA_STATUS": "1",
			"OP_ID": "CJ001166",
			"IS_MAIN": "1",
			"OFFER_NAME": "企信通行业版",
			"MGMT_COUNTY": "C0LJ",
			"SUBSCRIBER_INS_ID": "7092112700395952",
			"OFFER_INS_ID": "7092112792176223",
			"ORG_ID": "41908",
			"CREATE_ORG_ID": "41908",
			"REGION_ID": "06",
			"CUST_ID": "7006052300124493",
			"CREATE_OP_ID": "CJ001166",
			"VALID_DATE": "2012-12-07 16:15:11.0",
			"OFFER_ID": "6415",
			"DONE_DATE": "2012-11-27 16:14:17.0",
			"CREATE_DATE": "2012-11-27 16:14:17.0",
			"IS_BUNDLE": "1",
			"BRAND": "ADCG",
			"OFFER_TYPE": "10",
			"MGMT_DISTRICT": "0870"
		}, {
			"EXPIRE_DATE": "2050-12-31 00:00:00.0",
			"DATA_STATUS": "1",
			"IS_MAIN": "1",
			"OFFER_NAME": "短号集群网",
			"REMARKS": "NG割接导入",
			"MGMT_COUNTY": "C0LJ",
			"SUBSCRIBER_INS_ID": "7008082116429310",
			"OFFER_INS_ID": "7009000416595229",
			"REGION_ID": "06",
			"CUST_ID": "7008082106837850",
			"VALID_DATE": "2015-03-09 16:10:12.0",
			"OFFER_ID": "8000",
			"CREATE_DATE": "2008-08-21 00:00:00.0",
			"IS_BUNDLE": "1",
			"BRAND": "VPMN",
			"OFFER_TYPE": "10",
			"MGMT_DISTRICT": "0870"
		}, {
			"EXPIRE_DATE": "2050-12-31 23:59:59.0",
			"DATA_STATUS": "1",
			"OP_ID": "CJ001065",
			"IS_MAIN": "1",
			"OFFER_NAME": "移动人人通A(ADC)",
			"MGMT_COUNTY": "C0LJ",
			"SUBSCRIBER_INS_ID": "7090120700227982",
			"OFFER_INS_ID": "7090120744024508",
			"ORG_ID": "41908",
			"CREATE_ORG_ID": "41908",
			"REGION_ID": "06",
			"CUST_ID": "7009120509988067",
			"CREATE_OP_ID": "CJ001065",
			"VALID_DATE": "2013-09-14 21:44:44.0",
			"OFFER_ID": "6465",
			"DONE_DATE": "2010-12-07 22:27:49.0",
			"CREATE_DATE": "2010-12-07 22:27:49.0",
			"IS_BUNDLE": "1",
			"BRAND": "ADCG",
			"OFFER_TYPE": "10",
			"MGMT_DISTRICT": "0870"
		}, {
			"EXPIRE_DATE": "2050-12-31 23:59:59.0",
			"DATA_STATUS": "1",
			"OP_ID": "IBOSS000",
			"IS_MAIN": "1",
			"OFFER_NAME": "中央ADC业务(商品)",
			"MGMT_COUNTY": "A0AL",
			"SUBSCRIBER_INS_ID": "7193090800490363",
			"OFFER_INS_ID": "7193090858365958",
			"ORG_ID": "00309",
			"CREATE_ORG_ID": "00309",
			"REGION_ID": "06",
			"CUST_ID": "7113090863032571",
			"CREATE_OP_ID": "IBOSS000",
			"VALID_DATE": "2014-01-20 15:41:16.0",
			"OFFER_ID": "9945",
			"DONE_DATE": "2013-09-08 00:09:40.0",
			"CREATE_DATE": "2013-09-08 00:09:40.0",
			"IS_BUNDLE": "1",
			"BRAND": "BOSG",
			"OFFER_TYPE": "10",
			"MGMT_DISTRICT": "0871"
		}, {
			"EXPIRE_DATE": "2050-12-31 23:59:59.0",
			"DATA_STATUS": "1",
			"OP_ID": "CA101028",
			"IS_MAIN": "1",
			"OFFER_NAME": "集团彩铃",
			"MGMT_COUNTY": "C0LA",
			"SUBSCRIBER_INS_ID": "7099062600011114",
			"OFFER_INS_ID": "7099062603769207",
			"ORG_ID": "41886",
			"CREATE_ORG_ID": "41886",
			"REGION_ID": "06",
			"CUST_ID": "7008082106837850",
			"CREATE_OP_ID": "CA101028",
			"VALID_DATE": "2009-06-27 18:12:05.0",
			"OFFER_ID": "6200",
			"DONE_DATE": "2009-06-26 11:52:10.0",
			"CREATE_DATE": "2009-06-26 11:52:10.0",
			"IS_BUNDLE": "1",
			"BRAND": "VPMR",
			"OFFER_TYPE": "10",
			"MGMT_DISTRICT": "0870"
		}, {
			"EXPIRE_DATE": "2050-12-31 23:59:59.0",
			"DATA_STATUS": "1",
			"OP_ID": "CJ001102",
			"IS_MAIN": "1",
			"OFFER_NAME": "企信通行业版",
			"MGMT_COUNTY": "C0LJ",
			"SUBSCRIBER_INS_ID": "7094031400600899",
			"OFFER_INS_ID": "7094031415595663",
			"ORG_ID": "41908",
			"CREATE_ORG_ID": "41908",
			"REGION_ID": "06",
			"CUST_ID": "7014031133431322",
			"CREATE_OP_ID": "CJ001102",
			"VALID_DATE": "2015-11-17 17:22:30.0",
			"OFFER_ID": "6415",
			"DONE_DATE": "2014-03-14 10:04:59.0",
			"CREATE_DATE": "2014-03-14 10:04:59.0",
			"IS_BUNDLE": "1",
			"BRAND": "ADCG",
			"OFFER_TYPE": "10",
			"MGMT_DISTRICT": "0870"
		}],
		"X_RESULTCODE": "0"
	}
}
	ret1 = dict_get(dictest, 'DATAS', None)
    # ret2 = dict_get(dictest, 'ACCESS_NUM', None)
    # print(ret1)   #list
	print(ret1)
	print(type(ret1))
	for i in range(len(ret1)):
		print("订购的商品列表：" + json.dumps(ret1[i]))
		# offername = ret1[i]['OFFER_NAME']
		# grp_inst_id = ret1[i]['SUBSCRIBER_INS_ID']
		# print("订购的集团商品名称:" + offername)
		# print("订购的集团用户ID:" + grp_inst_id)
	lista = [{'serialNum':'15969006462','shortCode':'681618','userId':'7008080716050718'},
			 {'serialNum': '18787961713', 'shortCode': '681713', 'userId': '9110102326860610'},
			 {'serialNum': '15096963621', 'shortCode': '693621', 'userId': '7208102218270765'}
			]
	listb = [{'groupId':8723409920,'GroupName':'大理市海东镇上和完小（校讯通）','OfferInstId':'7295021394647174'},
			 {'groupId': 8723409625, 'GroupName': '祥云县银冠希望小学','OfferInstId': '7295012691118641'},
			 {'groupId': 8711437379, 'GroupName': '巍山红河源初级中学','OfferInstId': '7291092369525517'}
			]
	listc = [{'simId':89860001240642520092},{'simId':89860076240442072049},{'simId':89860057245448890016}]
	print(lista)
	print(listb)
	newlist = join_dictlists(lista,listb)
	newlist = join_dictlists(newlist,listc)
	print(newlist)
	subofferList = '800001,990013,990013445,99315 '.replace(' ','').split(',')
	print(subofferList)


	# print(lista + listb)

