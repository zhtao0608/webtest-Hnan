# coding:utf-8
from __future__ import print_function
import json

def dict_get(dict, objkey, default):
    '''
    获取字典中的objkey对应的值，适用于字典嵌套
    dict:字典
    objkey:目标key
    default:找不到时返回的默认值
    '''
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



""" 
@author:Bingo.he 
@file: get_target_value.py 
@time: 2017/12/22 
"""
def get_target_value(key, dic, tmp_list = []):
    """
    :param key: 目标key值
    :param dic: JSON数据
    :param tmp_list: 用于存储获取的数据
    :return: list
    """
    if not isinstance(dic, dict) or not isinstance(tmp_list, list):  # 对传入数据进行格式校验
        return 'argv[1] not an dict or argv[-1] not an list '
    if key in dic.keys():
        tmp_list.append(dic[key])  # 传入数据存在则存入tmp_list
    for value in dic.values():  # 传入数据不符合则对其value值进行遍历
        if isinstance(value, dict):
            get_target_value(key, value, tmp_list)  # 传入数据的value值是字典，则直接调用自身
        elif isinstance(value, (list, tuple)):
            _get_value(key, value, tmp_list)  # 传入数据的value值是列表或者元组，则调用_get_value
    return tmp_list

def _get_value(key, val, tmp_list):
    for val_ in val:
        if isinstance(val_, dict):
            get_target_value(key, val_, tmp_list)  # 传入数据的value值是字典，则调用get_target_value
        elif isinstance(val_, (list, tuple)):
            _get_value(key, val_, tmp_list)   # 传入数据的value值是列表或者元组，则调用自身



def dict_generator(indict, pre=None):
    """python递归解析JSON（目前最好的方案）来源CSDN"""
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                if len(value) == 0:
                    yield pre+[key, '{}']
                else:
                    for d in dict_generator(value, pre + [key]):
                        yield d
            elif isinstance(value, list):
                if len(value) == 0:
                    yield pre+[key, '[]']
                else:
                    for v in value:
                        for d in dict_generator(v, pre + [key]):
                            yield d
            elif isinstance(value, tuple):
                if len(value) == 0:
                    yield pre+[key, '()']
                else:
                    for v in value:
                        for d in dict_generator(v, pre + [key]):
                            yield d
            else:
                yield pre + [key, value]
    else:
        yield indict


# 递归打印解析节点及路径
def recursion(node_dict, node):
    '''递归打印解析节点及路径'''
    tmp = []
    if len(node_dict) == 0:
        tmp.append(node)
    else:
        for i in node_dict:
            recursion(i.get('subNodes'), node+'-->'+i.get('node'))


def get_json_keys(json_str,json_keys = []):
    '''获取 json 数组或json 对象的 key 列表'''
    if isinstance(json_str,list):
        for json_obj in json_str:
            for key in json_obj.keys():
                if key not in json_keys:
                    json_keys.append(key)
    elif isinstance(json_str,dict):
        for key in json_str.keys():
                if key not in json_keys:
                    json_keys.append(key)
    return json_keys

def get_key_values(json_str,json_keys):
    '''将json 数组中相同的 key - value值进行合并'''
    target_json = {}
    for key in json_keys:
        key_values = []
        for json_obj in json_str:
            if isinstance(json_obj,dict):
                key_values.append(json_obj[key])
        target_json[key] = key_values
    return target_json

def analyse_json(json_str):
    '''解析json'''
    target_json = {}
    json_keys = []
    if isinstance(json_str,list):
        json_keys = get_json_keys(json_str,json_keys)
        target_json = get_key_values(json_str,json_keys)
    elif isinstance(json_str,dict):
        json_keys = get_json_keys(json_str,json_keys)
        for key in json_keys:
            if not isinstance(json_str[key],list) and not isinstance(json_str[key],dict):
                target_json[key] = json_str[key]
            else:
                target_json[key] = analyse_json(json_str[key])
    return target_json

if __name__ == "__main__":

    sJOSN = {
		"REQUEST_STRUCT" :  [
			{
				"COMMON_DATA" : {
					"REMARKS" : "" ,
					"ROLE_CODE_B" : "1"
				} ,
				"OFFERS" :  [
					{
						"OPER_CODE" : "0" ,
						"PRODS" :  [
							{
								"PROD_SPEC_ID" : "600648001" ,
								"OPER_CODE" : "0" ,
								"PROD_CHA_SPECS" :  [
									{
										"CHA_VALUE" : "64322" ,
										"CHA_SPEC_ID" : "8000010101" ,
										"CHA_SPEC_CODE" : "SHORT_CODE"
									} ,
									{
										"CHA_VALUE" : "1" ,
										"CHA_SPEC_ID" : "8000010103" ,
										"CHA_SPEC_CODE" : "SECOND_SMS"
									} ,
									{
										"CHA_VALUE" : "" ,
										"CHA_SPEC_ID" : "8000010201" ,
										"CHA_SPEC_CODE" : "VPN_CITY_CODE"
									} ,
									{
										"CHA_VALUE" : "" ,
										"CHA_SPEC_ID" : "8000010202" ,
										"CHA_SPEC_CODE" : "VPN_SMALL_TOWN"
									} ,
									{
										"CHA_VALUE" : "" ,
										"CHA_SPEC_ID" : "8000010203" ,
										"CHA_SPEC_CODE" : "VPN_VILLAGE"
									} ,
									{
										"CHA_VALUE" : "省内+省外" ,
										"CHA_SPEC_ID" : "8000010301" ,
										"CHA_SPEC_CODE" : "M_VPN109"
									} ,
									{
										"CHA_VALUE" : "省内+省外" ,
										"CHA_SPEC_ID" : "8000010302" ,
										"CHA_SPEC_CODE" : "M_VPN110"
									} ,
									{
										"CHA_VALUE" : "终止呼叫" ,
										"CHA_SPEC_ID" : "8000010303" ,
										"CHA_SPEC_CODE" : "M_VPN116"
									} ,
									{
										"CHA_VALUE" : "终止呼叫" ,
										"CHA_SPEC_ID" : "8000010304" ,
										"CHA_SPEC_CODE" : "M_VPN117"
									} ,
									{
										"CHA_VALUE" : "0" ,
										"CHA_SPEC_ID" : "8000010401" ,
										"CHA_SPEC_CODE" : "PERFEE_PLAY_BACK"
									} ,
									{
										"CHA_VALUE" : "1" ,
										"CHA_SPEC_ID" : "8000010402" ,
										"CHA_SPEC_CODE" : "M_SINWORD_TYPE_CODE"
									} ,
									{
										"CHA_VALUE" : "1" ,
										"CHA_SPEC_ID" : "8000010403" ,
										"CHA_SPEC_CODE" : "CALL_DISP_MODE"
									} ,
									{
										"CHA_VALUE" : "0" ,
										"CHA_SPEC_ID" : "8000010404" ,
										"CHA_SPEC_CODE" : "M_CALL_AREA_TYPE"
									} ,
									{
										"CHA_VALUE" : "1" ,
										"CHA_SPEC_ID" : "8000010601" ,
										"CHA_SPEC_CODE" : "M_CALL_NET_TYPE1"
									} ,
									{
										"CHA_VALUE" : "1" ,
										"CHA_SPEC_ID" : "8000010602" ,
										"CHA_SPEC_CODE" : "M_CALL_NET_TYPE2"
									} ,
									{
										"CHA_VALUE" : "1" ,
										"CHA_SPEC_ID" : "8000010603" ,
										"CHA_SPEC_CODE" : "M_CALL_NET_TYPE3"
									} ,
									{
										"CHA_VALUE" : "1" ,
										"CHA_SPEC_ID" : "8000010604" ,
										"CHA_SPEC_CODE" : "M_CALL_NET_TYPE4"
									} ,
									{
										"CHA_VALUE" : "0" ,
										"CHA_SPEC_ID" : "8000010801" ,
										"CHA_SPEC_CODE" : "ADMIN_FLAG"
									} ,
									{
										"CHA_VALUE" : "0" ,
										"CHA_SPEC_ID" : "8000010802" ,
										"CHA_SPEC_CODE" : "TELPHONIST_TAG"
									} ,
									{
										"CHA_VALUE" : "0" ,
										"CHA_SPEC_ID" : "8000010803" ,
										"CHA_SPEC_CODE" : "LOCK_TAG"
									} ,
									{
										"CHA_VALUE" : "0" ,
										"CHA_SPEC_ID" : "8000011001" ,
										"CHA_SPEC_CODE" : "LIMFEE_TYPE_CODE1"
									} ,
									{
										"CHA_VALUE" : "0" ,
										"CHA_SPEC_ID" : "8000011002" ,
										"CHA_SPEC_CODE" : "LIMFEE_TYPE_CODE2"
									} ,
									{
										"CHA_VALUE" : "0" ,
										"CHA_SPEC_ID" : "8000011003" ,
										"CHA_SPEC_CODE" : "LIMFEE_TYPE_CODE3"
									} ,
									{
										"CHA_VALUE" : "0" ,
										"CHA_SPEC_ID" : "8000011004" ,
										"CHA_SPEC_CODE" : "LIMFEE_TYPE_CODE4"
									} ,
									{
										"CHA_VALUE" : "0" ,
										"CHA_SPEC_ID" : "8000011102" ,
										"CHA_SPEC_CODE" : "MON_FEE_LIMIT"
									}
								] ,
								"PROD_SPEC_NAME" : "集团管家成员"
							}
						] ,
						"PRICE_PLANS" :  [
							{
								"EXPIRE_DATE" : "2050-12-31 00:00:00" ,
								"OPER_CODE" : "0" ,
								"PRICE_NAME" : "云南边防全省集群网包打15元资费套餐" ,
								"PRICES" :  [
									{
										"OPER_CODE" : "0" ,
										"PRICE_VAL" : "0" ,
										"PRICE_ID" : "99000906"
									}
								] ,
								"PRICE_VALID_TYPE" : "0" ,
								"PRICE_PLAN_ID" : "99000906" ,
								"VALID_DATE" : "2020-05-09 00:00:00"
							}
						] ,
						"OFFER_NAME" : "集团管家成员" ,
						"SUBOFFERS" :  [
							{
								"OPER_CODE" : "0" ,
								"PRODS" :  [
									{
										"PROD_SPEC_ID" : "648000" ,
										"OPER_CODE" : "0" ,
										"PROD_CHA_SPECS" :  [
											{
												"CHA_VALUE" : "P" ,
												"CHA_SPEC_ID" : "1418900052" ,
												"CHA_SPEC_CODE" : "MAS_OPER_TYPE"
											} ,
											{
												"CHA_VALUE" : "1" ,
												"CHA_SPEC_ID" : "1418900060" ,
												"CHA_SPEC_CODE" : "MEB_SERV_STATE"
											} ,
											{
												"CHA_VALUE" : "01" ,
												"CHA_SPEC_ID" : "1418900059" ,
												"CHA_SPEC_CODE" : "BIZ_IN_CODE_ATTR"
											} ,
											{
												"CHA_VALUE" : "10657087276563" ,
												"CHA_SPEC_ID" : "1418900063" ,
												"CHA_SPEC_CODE" : "BIZ_IN_CODE"
											} ,
											{
												"CHA_VALUE" : "TYN0015401" ,
												"CHA_SPEC_ID" : "1418900005" ,
												"CHA_SPEC_CODE" : "BIZ_CODE"
											} ,
											{
												"CHA_VALUE" : "集团短号通讯短信" ,
												"CHA_SPEC_ID" : "1418900006" ,
												"CHA_SPEC_CODE" : "BIZ_NAME"
											} ,
											{
												"CHA_VALUE" : "1" ,
												"CHA_SPEC_ID" : "1418900004" ,
												"CHA_SPEC_CODE" : "BIZ_ATTR"
											} ,
											{
												"CHA_VALUE" : "2020-5-8" ,
												"CHA_SPEC_ID" : "1418900040" ,
												"CHA_SPEC_CODE" : "WISH_EFF_DATA"
											} ,
											{
												"CHA_VALUE" : "true" ,
												"CHA_SPEC_ID" : "1418900072" ,
												"CHA_SPEC_CODE" : "BUTTON_SUBMIT_FLAG"
											} ,
											{
												"CHA_VALUE" : "" ,
												"CHA_SPEC_ID" : "1418900065" ,
												"CHA_SPEC_CODE" : "ADC_LOGIN_NAME"
											} ,
											{
												"CHA_VALUE" : "" ,
												"CHA_SPEC_ID" : "1418900066" ,
												"CHA_SPEC_CODE" : "ADC_SUBSCRIBER_NAME"
											} ,
											{
												"CHA_VALUE" : "" ,
												"CHA_SPEC_ID" : "1418900067" ,
												"CHA_SPEC_CODE" : "ADC_EMAIL"
											} ,
											{
												"CHA_VALUE" : "" ,
												"CHA_SPEC_ID" : "1418900068" ,
												"CHA_SPEC_CODE" : "ADC_IMEI"
											} ,
											{
												"CHA_VALUE" : "" ,
												"CHA_SPEC_ID" : "1418900069" ,
												"CHA_SPEC_CODE" : "ADC_TERMINAL_TYPE"
											} ,
											{
												"CHA_VALUE" : "" ,
												"CHA_SPEC_ID" : "1418900110" ,
												"CHA_SPEC_CODE" : "ROLE_TYPE"
											} ,
											{
												"CHA_VALUE" : "" ,
												"CHA_SPEC_ID" : "1418900119" ,
												"CHA_SPEC_CODE" : "OLD_ROLE_TYPE"
											}
										] ,
										"PROD_SPEC_NAME" : "集团管家短信"
									}
								] ,
								"OFFER_NAME" : "集团管家短信" ,
								"IS_SHOW_SET_TAG" : "true" ,
								"OFFER_ID" : "100648000" ,
								"OFFER_INDEX" : "0" ,
								"BRAND" : ""
							} ,
							{
								"OPER_CODE" : "0" ,
								"PRODS" :  [
									{
										"PROD_SPEC_ID" : "648001" ,
										"OPER_CODE" : "0" ,
										"PROD_CHA_SPECS" :  [
											{
												"CHA_VALUE" : "P" ,
												"CHA_SPEC_ID" : "1418900052" ,
												"CHA_SPEC_CODE" : "MAS_OPER_TYPE"
											} ,
											{
												"CHA_VALUE" : "1" ,
												"CHA_SPEC_ID" : "1418900060" ,
												"CHA_SPEC_CODE" : "MEB_SERV_STATE"
											} ,
											{
												"CHA_VALUE" : "02" ,
												"CHA_SPEC_ID" : "1418900059" ,
												"CHA_SPEC_CODE" : "BIZ_IN_CODE_ATTR"
											} ,
											{
												"CHA_VALUE" : "10657087276568" ,
												"CHA_SPEC_ID" : "1418900063" ,
												"CHA_SPEC_CODE" : "BIZ_IN_CODE"
											} ,
											{
												"CHA_VALUE" : "2270015401" ,
												"CHA_SPEC_ID" : "1418900005" ,
												"CHA_SPEC_CODE" : "BIZ_CODE"
											} ,
											{
												"CHA_VALUE" : "集团短号通讯录彩信" ,
												"CHA_SPEC_ID" : "1418900006" ,
												"CHA_SPEC_CODE" : "BIZ_NAME"
											} ,
											{
												"CHA_VALUE" : "1" ,
												"CHA_SPEC_ID" : "1418900004" ,
												"CHA_SPEC_CODE" : "BIZ_ATTR"
											} ,
											{
												"CHA_VALUE" : "2020-5-8" ,
												"CHA_SPEC_ID" : "1418900040" ,
												"CHA_SPEC_CODE" : "WISH_EFF_DATA"
											} ,
											{
												"CHA_VALUE" : "true" ,
												"CHA_SPEC_ID" : "1418900072" ,
												"CHA_SPEC_CODE" : "BUTTON_SUBMIT_FLAG"
											} ,
											{
												"CHA_VALUE" : "" ,
												"CHA_SPEC_ID" : "1418900065" ,
												"CHA_SPEC_CODE" : "ADC_LOGIN_NAME"
											} ,
											{
												"CHA_VALUE" : "" ,
												"CHA_SPEC_ID" : "1418900066" ,
												"CHA_SPEC_CODE" : "ADC_SUBSCRIBER_NAME"
											} ,
											{
												"CHA_VALUE" : "" ,
												"CHA_SPEC_ID" : "1418900067" ,
												"CHA_SPEC_CODE" : "ADC_EMAIL"
											} ,
											{
												"CHA_VALUE" : "" ,
												"CHA_SPEC_ID" : "1418900068" ,
												"CHA_SPEC_CODE" : "ADC_IMEI"
											} ,
											{
												"CHA_VALUE" : "" ,
												"CHA_SPEC_ID" : "1418900069" ,
												"CHA_SPEC_CODE" : "ADC_TERMINAL_TYPE"
											} ,
											{
												"CHA_VALUE" : "" ,
												"CHA_SPEC_ID" : "1418900110" ,
												"CHA_SPEC_CODE" : "ROLE_TYPE"
											} ,
											{
												"CHA_VALUE" : "" ,
												"CHA_SPEC_ID" : "1418900119" ,
												"CHA_SPEC_CODE" : "OLD_ROLE_TYPE"
											}
										] ,
										"PROD_SPEC_NAME" : "集团管家彩信"
									}
								] ,
								"OFFER_NAME" : "集团管家彩信" ,
								"IS_SHOW_SET_TAG" : "true" ,
								"OFFER_ID" : "100648001" ,
								"OFFER_INDEX" : "0" ,
								"BRAND" : ""
							} ,
							{
								"OPER_CODE" : "0" ,
								"PRODS" :  [
									{
										"PROD_SPEC_ID" : "860" ,
										"OPER_CODE" : "0" ,
										"PROD_SPEC_NAME" : "VPMN成员短号"
									}
								] ,
								"OFFER_NAME" : "VPMN成员短号" ,
								"IS_SHOW_SET_TAG" : "false" ,
								"OFFER_ID" : "100000860" ,
								"OFFER_INDEX" : "0" ,
								"BRAND" : ""
							}
						] ,
						"OFFER_ID" : "648001" ,
						"BRAND" : "VPMN" ,
						"ROLE_ID" : "5"
					}
				] ,
				"BUSI_TYPE" : "3744" ,
				"ORDER_OPER_CODE" : "memCrt" ,
				"EC_ACCESS_NUM" : "7164802115060" ,
				"EC_OFFER_ID" : "6480" ,
				"MEM_ACCESS_NUM" : "13908880079" ,
				"OTHER_DATA" : {
				}
			}
		] ,
		"REMARKS" : "" ,
		"ACCESS_NUM" : "13908880079" ,
		"IS_MAIN_OFFER_ID" : "648001" ,
		"IS_MAIN_OFFER_INS_ID" : "8820050800940110"
	}
    json_string = json.dumps(sJOSN)
    sValue = json.loads(json_string)
    print("***************我们采用第一种方式试试***************\n")
    for i in dict_generator(sValue):
        print('.'.join(i[0:-1]), ':', i[-1])

    print("***************我们采用第二种方式试试***************\n")
    # print(analyse_json(sJOSN))
    print(type(analyse_json(sJOSN)))
    print(json.dumps(analyse_json(sJOSN),ensure_ascii=False))

    print("***************我们采用第三种方式解析复杂嵌套json,找到对应的key值对应的Value***************\n")
    print(type(get_target_value('OFFER_NAME',sValue)))
    print(get_target_value('OFFER_NAME',sValue))

    print("***************我们采用第四种方式解析复杂嵌套json,找到对应的key值对应的Value***************\n")
    print(type(dict_get(sValue,'ACCESS_NUM',None)))
    print(dict_get(sValue,'ACCESS_NUM',None))
    # json_str_1 = {
    #     "node": "a",
    #     "subNodes": [{
    #         "node": "a1",
    #         "subNodes": [{
    #             "node": "a11",
    #             "subNodes": [{
    #                 "node": "a111",
    #                 "subNodes": []
    #             }, {
    #                 "node": "a112",
    #                 "subNodes": []
    #             }]
    #         }, {
    #             "node": "a12",
    #             "subNodes": []
    #         }]
    #     }, {
    #         "node": "a2",
    #         "subNodes": []
    #     }]
    # }

