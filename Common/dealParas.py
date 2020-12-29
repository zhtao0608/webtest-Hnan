# coding: utf-8


from Common.TestAsserts import Assertion as alert
import time,datetime,os
from Base import ReadConfig
from Base.Mylog import LogManager
import json
from Base.SysPara import SysPara
from collections import defaultdict

# 获取logger实例
logger = LogManager('dealParas').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


def ConvertParas(paras):
    '''转换入参'''
    alert().assertIsNotNone(paras, msg='paras不允许为空！')
    logger.info('传入的Paras参数:{}'.format(paras))
    logger.info('传入的Paras的参数类型:{}'.format(type(paras)))
    if isinstance(paras,str):
        return json.loads(paras) #如果返回的是json,转换成字典返回
    if isinstance(paras, dict):
        logger.info('字典类型直接返回:{}'.format(paras))
        return paras
    elif isinstance(paras, list):
        listpara = []
        for i in range(0, len(paras)):
            # 因为读取出来的参数list数组里的元素都是Str先转换成字典后再讲参数部分组装到list返回
            param = {key: value for key, value in paras[i].items() if not key == 'PARAMS'}
            if isinstance(paras[i]['PARAMS'], str):
                paras[i]['PARAMS'].replace('\r', '').replace('\n', '')
                logger.info('PARAMS数据库读取出来都类型是Str,需要转换成Dict')
                inputPara = eval(paras[i]['PARAMS'])
                print('==============', inputPara)
                print('==============', type(inputPara))
                if isinstance(inputPara, dict):
                    inputPara.update(param)
                    logger.info('转换后都Dict参数:{}'.format(inputPara))
                    listpara.append(inputPara)
                if isinstance(inputPara, tuple):
                    print('转换都InPutPara都数据类型是tuple')
                    inputPara = list(inputPara)
                    for i in range(len(inputPara)):
                        Para = inputPara[i]
                        Para.update(param)
                        print('******再次转换成dict后{}'.format(inputPara))
                        listpara.append(inputPara)
        logger.info('读取出来的原始参数:{}'.format(listpara))
        return listpara

def capital_to_lower(dict_info):
	'''
	传入字典，将字典key转换成小写
	:param dict_info:
	:return:
	'''
	new_dict = {}
	for i, j in dict_info.items():
		new_dict[i.lower()] = j
	return new_dict


def capital_to_upper(dict_info):
	'''
	传入字典，将字典key转换成大写
	:param dict_info:
	:return:
	'''
	new_dict = {}
	for i, j in dict_info.items():
		new_dict[i.upper()] = j
	return new_dict

def convert_to_diclistLower(oldlist):
	'''
	传入一个字典列表，将所有的key都转换成小写
	:param oldlist: 字典列表
	:return: newlist
	'''
	new_list = []
	for i in range(0,len(oldlist)):
		new_list.append(capital_to_lower(oldlist[i]))
	return new_list

def convert_to_diclistUpper(oldlist):
	'''
	传入一个字典列表，将所有的key都转换成大写
	:param oldlist: 字典列表
	:return: newlist
	'''
	new_list = []
	for i in range(0,len(oldlist)):
		new_list.append(capital_to_upper(oldlist[i]))
	return new_list


def convert_dicValueToList(dic):
	'''传入字典，将字典value转换成List'''
	if isinstance(dic,dict):
		list_values = list(dic.values())
		print('字典中的value列表:',list_values)
		list_keys = list(dic.keys())
		print('字典中的key列表:',list_keys)
		return list_values
	else:
		print('传入的不是dict类型，不能转换！')


def convertDicList(oldDataList):
	'''
	转换字典列表：将字典列表转换成如下list格式
	eg :[{'TRADE_ID': 3120082587858316, 'ACCEPT_MONTH': 8, 'USER_ID': 3120082500014516},
		{'TRADE_ID': 3120082587858316, 'ACCEPT_MONTH': 8, 'USER_ID': 3120082500014516}
		]
    转换成
	[["TRADE_ID", "ACCEPT_MONTH", "USER_ID"], ##对应的key
    ["3120082587858316", "8", "3120082500014516"], ##对应value
    ["3120082587858316", "8", "3120082500014516"]]##value也有可能是个列表
	:param dataList: 字典列表
	:return:
	'''
	if not isinstance(oldDataList,list):
		print('必须传入list结构')
	newValueList = [] #转换后的列表
	item_0 = oldDataList[0]   # 先获取字典列表的key
	newValueList.append(list(item_0.keys()))  #先把key全部放到list
	for i in range(0,len(oldDataList)):
		logger.info('处理的字典：{}'.format(oldDataList[i]))
		itemlist = []
		for value in oldDataList[i].values():   #在字典中循环提取vaule
			if isinstance(value, datetime.datetime):  ##如果是时间格式要转换成字符
				value = value.strftime("%Y-%m-%d %H:%M:%S")
			if isinstance(value, int):
				value = str(value)
			itemlist.append(value)
		logger.info('====字典对应的valuelist：{}'.format(itemlist))
		newValueList.append(itemlist)
	return newValueList


def convert_ListToDic(Keylist,Valuelist):
	'''传入字典，将字典value转换成List'''
	if isinstance(Keylist,list):
		if isinstance(Valuelist,list):
			dic = dict(zip(Keylist,Valuelist))
	else:
		print('传入的不是list类型，不能转换！')
	return dic

def convert_enurlToDic(enurl_str):
	'''enUrl转换成Dict字典类型'''
	print('传入的enUrl:',enurl_str)
	enurl_str = enurl_str.replace('=', ":")
	list_enurl = enurl_str.split('&')
	# print('list_enurl=',list_enurl)
	dict_key = []
	dict_value = []
	for i in range(len(list_enurl)):
		value = list_enurl[i]
		list_value = value.split(':')
		# print(list_value)
		# print(type(list_value))
		for j in range(1,len(list_value)):
			dict_key.append(list_value[0])
			dict_value.append(list_value[1])
	# print('dict_key=',dict_key)
	# print('dict_value',dict_value)
	return convert_ListToDic(dict_key,dict_value)

def convertParatoList(paras):
	'''
	:param paras: 传入的参数值，可能是list、tuple、Str、Dict等各种数据类型
	:return: Paras转换成List数据类型返回
	'''
	paras.replace("\n","").replace("\r","").replace(" ","") #把空格和换行去掉
	logger.info('传入的Paras的参数类型:{}'.format(type(paras)))
	logger.info('原始参数:{}'.format(paras))
	paras = eval(paras)  #用eval函数处理转换
	# params = json.loads(paras)
	# print('=================')
	# print(params)
	# paras = ast.literal_eval(paras)  # 用eval函数处理转换
	if isinstance(paras, tuple):
		print('eval(paras) 转换后是tuple类型')
		params = list(paras)
	elif isinstance(paras, dict):
		print('eval(paras) 转换后是dict类型')
		dicList = []
		dicList.append(paras)
		params = dicList
	elif isinstance(paras, list):
		print('eval(paras) 转换后是list类型')
		params = paras
	return params  # 转换成字典返回


if __name__ == '__main__':
	oldDict = {'FUNC_ID': 'crm3480',
			   'MENU_CATA': 'crm991A',
			   'PARENT_FUNC_ID': 'crm9700',
			   'MENU_PATH': '家庭业务->宽带业务->宽带开户->新宽带一单清-重复保留',
			   'dll_path': '/web-order/order?service=page/order.page.pc.broadband.NewFusionBroadBand&listener=onInitBusi',
			   'module': '家庭业务', 'iscore': '1'}
	newDict = capital_to_lower(dict_info=oldDict)
	print(newDict)

	oldList = [{'func_id': 'crm3480', 'menu_cata': 'crm991A', 'parent_func_id': 'crm9700', 'menu_path': '家庭业务->宽带业务->宽带开户->新宽带一单清-重复保留', 'dll_path': '/web-order/order?service=page/order.page.pc.broadband.NewFusionBroadBand&listener=onInitBusi', 'module': '家庭业务', 'iscore': '1', 'test_result': ''}, {'func_id': 'crm9731', 'menu_cata': 'crm991A', 'parent_func_id': 'crm9700', 'menu_path': '家庭业务->宽带业务->宽带开户->宽带开户', 'dll_path': '/web-order/order?service=page/order.page.pc.broadband.BroadbandCreate&listener=onInitBusi&cond_CREATE_TYPE=PERSONSERV', 'module': '家庭业务', 'iscore': '1', 'test_result': ''}, {'func_id': 'crm97A0', 'menu_cata': 'crm991A', 'parent_func_id': 'crm9700', 'menu_path': '家庭业务->宽带业务->宽带开户->IMS单用户开户', 'dll_path': '/web-order/order?service=page/broadband.PersonIMSCreate&listener=onInitTrade', 'module': '家庭业务', 'iscore': '1', 'test_result': ''}, {'func_id': 'crm972E', 'menu_cata': 'crm991A', 'parent_func_id': 'crm9700', 'menu_path': '家庭业务->宽带业务->宽带业务变更->互联网电视', 'dll_path': '/web-order/order?service=page/broadband.InteractiveTV&listener=getProductList&TYPE_TAG=3', 'module': '家庭业务', 'iscore': '1', 'test_result': ''}, {'func_id': 'crm9750', 'menu_cata': 'crm991A', 'parent_func_id': 'crm9700', 'menu_path': '家庭业务->宽带业务->宽带业务变更->宽带提速', 'dll_path': '/web-order/order?service=page/order.page.pc.broadband.BroadbandChangeSpeed', 'module': '家庭业务', 'iscore': '1', 'test_result': ''}, {'func_id': 'crm972F', 'menu_cata': 'crm991A', 'parent_func_id': 'crm9700', 'menu_path': '家庭业务->宽带业务->宽带续费->互联网电视续费', 'dll_path': '/web-order/order?service=page/broadband.InteractiveTVContinuePay', 'module': '家庭业务', 'iscore': '1', 'test_result': ''}, {'func_id': 'crm975D', 'menu_cata': 'crm991A', 'parent_func_id': 'crm9700', 'menu_path': '家庭业务->宽带业务->宽带续费->家宽续费', 'dll_path': '/web-order/order?service=page/order.page.pc.broadband.NewBroadBandContinuePay', 'module': '家庭业务', 'iscore': '1', 'test_result': ''}, {'func_id': 'crm94BE', 'menu_cata': 'crm991A', 'parent_func_id': 'crm9700', 'menu_path': '家庭业务->宽带业务->宽带状态变更->废电视客服界面', 'dll_path': '/web-order/order?service=page/broadband.BroadBandTvInfoQuery', 'module': '家庭业务', 'iscore': '1', 'test_result': ''}, {'func_id': 'crm9723', 'menu_cata': 'crm991A', 'parent_func_id': 'crm9700', 'menu_path': '家庭业务->宽带业务->宽带状态变更->宽带移机', 'dll_path': '/web-order/order?service=page/broadband.MoveBroadBand', 'module': '家庭业务', 'iscore': '1', 'test_result': ''}, {'func_id': 'crm97B6', 'menu_cata': 'crm991A', 'parent_func_id': 'crm9700', 'menu_path': '家庭业务->宽带业务->宽带状态变更->家宽拆机', 'dll_path': '/web-order/order?service=page/order.page.pc.broadband.BroadBandDestroyNew', 'module': '家庭业务', 'iscore': '1', 'test_result': ''}, {'func_id': 'crm97B7', 'menu_cata': 'crm991A', 'parent_func_id': 'crm9700', 'menu_path': '家庭业务->宽带业务->宽带状态变更->家宽产品增值业务变更', 'dll_path': '/web-order/order?service=page/plat.BroadBandBusiAddNew', 'module': '家庭业务', 'iscore': '1', 'test_result': ''}, {'func_id': 'crm9728', 'menu_cata': 'crm991A', 'parent_func_id': 'crm9700', 'menu_path': '家庭业务->宽带业务->资料变更类->宽带密码变更-重复保留', 'dll_path': '/web-order/order?service=page/order.page.pc.person.broadband.passwdchg.BroadBandPassWDCHG&listener=initPage', 'module': '家庭业务', 'iscore': '1', 'test_result': ''}, {'func_id': 'crm9730', 'menu_cata': 'crm991A', 'parent_func_id': 'crm9700', 'menu_path': '家庭业务->宽带业务->宽带客服类->宽带移机(客服)', 'dll_path': '/web-order/order?service=page/broadband.MoveBroadBand&listener=initPage', 'module': '家庭业务', 'iscore': '1', 'test_result': ''}, {'func_id': 'crm9748', 'menu_cata': 'crm991A', 'parent_func_id': 'crm9700', 'menu_path': '家庭业务->宽带业务->宽带客服类->10086宽带开户-重复保留', 'dll_path': '/web-order/order?service=page/order.page.pc.broadband.BroadbandCreate&listener=onInitBusi&cond_CREATE_TYPE=PERSONSERV&strtest=testa', 'module': '家庭业务', 'iscore': '1', 'test_result': ''}, {'func_id': 'crm9768', 'menu_cata': 'crm991A', 'parent_func_id': 'crm9700', 'menu_path': '家庭业务->宽带业务->宽带客服类->宽带密码变更(客服)-重复保留', 'dll_path': '/web-order/order?service=page/order.page.pc.person.broadband.passwdchg.BroadBandPassWDCHG&listener=initPage&REAL_TAG=true', 'module': '家庭业务', 'iscore': '1', 'test_result': ''}, {'func_id': 'crm972H', 'menu_cata': 'crm991A', 'parent_func_id': 'crm9700', 'menu_path': '家庭业务->宽带业务->后台管理->互联网电视变更牌照', 'dll_path': '/web-order/order?service=page/order.page.pc.person.broadband.InteractiveTVChange&listener=init&FLAG=0', 'module': '家庭业务', 'iscore': '1', 'test_result': ''}, {'func_id': 'crm9734', 'menu_cata': 'crm991A', 'parent_func_id': 'crm9700', 'menu_path': '家庭业务->宽带业务->后台管理->宽带端口解绑', 'dll_path': '/web-order/order?service=page/order.page.pc.person.broadband.BroadBandUnBind', 'module': '家庭业务', 'iscore': '1', 'test_result': ''}, {'func_id': 'crm9772', 'menu_cata': 'crm991A', 'parent_func_id': 'crm9700', 'menu_path': '家庭业务->宽带业务->后台管理->宽带业务返销', 'dll_path': '/web-order/order?service=page/order.page.pc.broadband.CancelTrades&listener=onInitTrade', 'module': '家庭业务', 'iscore': '1', 'test_result': ''}, {'func_id': 'crm9775', 'menu_cata': 'crm991A', 'parent_func_id': 'crm9700', 'menu_path': '家庭业务->宽带业务->后台管理->宽带卡单重新派单', 'dll_path': '/web-order/order?service=page/order.page.pc.person.broadband.BroadBandReSend&listener=initPage', 'module': '家庭业务', 'iscore': '1', 'test_result': ''}, {'func_id': 'crm939F', 'menu_cata': 'crm991A', 'parent_func_id': 'crm9700', 'menu_path': '家庭业务->宽带业务->其它类->全业务捆绑营销注销(新)', 'dll_path': '/web-order/order?service=page/broadband.BundleChargesDestroy', 'module': '家庭业务', 'iscore': '1', 'test_result': ''}, {'func_id': 'crm9941', 'menu_cata': 'crm991A', 'parent_func_id': 'crm992B', 'menu_path': '家庭业务->家庭通信->共享业务->4G套餐共享->4G流量共享主卡业务办理', 'dll_path': '/web-order/order?service=page/order.page.pc.shareClusterFlow.ShareClusterFlow', 'module': '家庭业务', 'iscore': '1', 'test_result': ''}, {'func_id': 'crm9942', 'menu_cata': 'crm991A', 'parent_func_id': 'crm992B', 'menu_path': '家庭业务->家庭通信->共享业务->4G套餐共享->4G流量共享副卡业务办理', 'dll_path': '/web-order/order?service=page/order.page.pc.shareClusterFlow.MemberShareCluster', 'module': '家庭业务', 'iscore': '1', 'test_result': ''}, {'func_id': 'crm9948', 'menu_cata': 'crm991A', 'parent_func_id': 'crm992B', 'menu_path': '家庭业务->家庭通信->共享业务->4G套餐共享->共享类业务', 'dll_path': '/web-order/order?service=page/order.page.pc.tariffshare.TariffShare', 'module': '家庭业务', 'iscore': '1', 'test_result': ''}, {'func_id': 'crm9275', 'menu_cata': 'crm991A', 'parent_func_id': 'crm992D', 'menu_path': '家庭业务->智慧家庭->智慧家庭->腕表付费关系变更', 'dll_path': '/web-order/order?service=page/order.page.pc.person.changepayrelation.PayRelaNorChg&listener=init&PAYTYPE=KIDSWATCH', 'module': '家庭业务', 'iscore': '1', 'test_result': ''}]
	print(convert_to_diclistLower(oldList))

	# oldValue = [{'TRADE_ID': 3120082587858316, 'ACCEPT_MONTH': 8, 'USER_ID': 3120082500014516, 'USER_ID_A': -1, 'PACKAGE_ID': 32953733, 'PRODUCT_ID': 32811359, 'OFFER_TYPE': 'D', 'OFFER_ID': 130032532282, 'DISCNT_CODE': 32532282, 'SPEC_TAG': '0', 'RELATION_TYPE_CODE': None, 'INST_ID': 3120082500029184, 'CAMPN_ID': None, 'OLD_PRODUCT_ID': None, 'OLD_PACKAGE_ID': None, 'START_DATE': datetime.datetime(2020, 8, 25, 20, 0, 4), 'END_DATE': datetime.datetime(2050, 12, 31, 0, 0), 'MODIFY_TAG': '0', 'UPDATE_TIME': datetime.datetime(2020, 8, 25, 20, 0, 4), 'UPDATE_STAFF_ID': 'ITFTA114', 'UPDATE_DEPART_ID': '17EFF', 'OPER_CODE': None, 'IS_NEED_PF': None, 'CREATE_DATE': datetime.datetime(2020, 8, 25, 20, 0, 4), 'CREATE_STAFF_ID': 'ITFTA114', 'CREATE_DEPART_ID': '17EFF', 'DONE_CODE': 3120082587858316, 'REMARK': None, 'RSRV_DATE1': None, 'RSRV_DATE2': None, 'RSRV_DATE3': None, 'RSRV_NUM1': None, 'RSRV_NUM2': None, 'RSRV_NUM3': None, 'RSRV_NUM4': None, 'RSRV_NUM5': None, 'RSRV_STR1': None, 'RSRV_STR2': None, 'RSRV_STR3': None, 'RSRV_STR4': None, 'RSRV_STR5': None, 'RSRV_TAG1': None, 'RSRV_TAG2': None, 'RSRV_TAG3': None}, {'TRADE_ID': 3120082587858316, 'ACCEPT_MONTH': 8, 'USER_ID': 3120082500014516, 'USER_ID_A': -1, 'PACKAGE_ID': 99966954, 'PRODUCT_ID': 32811359, 'OFFER_TYPE': 'D', 'OFFER_ID': 130099665664, 'DISCNT_CODE': 99665664, 'SPEC_TAG': '0', 'RELATION_TYPE_CODE': None, 'INST_ID': 3120082500029185, 'CAMPN_ID': None, 'OLD_PRODUCT_ID': None, 'OLD_PACKAGE_ID': None, 'START_DATE': datetime.datetime(2020, 8, 25, 20, 0, 4), 'END_DATE': datetime.datetime(2022, 7, 31, 23, 59, 59), 'MODIFY_TAG': '0', 'UPDATE_TIME': datetime.datetime(2020, 8, 25, 20, 0, 4), 'UPDATE_STAFF_ID': 'ITFTA114', 'UPDATE_DEPART_ID': '17EFF', 'OPER_CODE': None, 'IS_NEED_PF': None, 'CREATE_DATE': datetime.datetime(2020, 8, 25, 20, 0, 4), 'CREATE_STAFF_ID': 'ITFTA114', 'CREATE_DEPART_ID': '17EFF', 'DONE_CODE': 3120082587858316, 'REMARK': None, 'RSRV_DATE1': None, 'RSRV_DATE2': None, 'RSRV_DATE3': None, 'RSRV_NUM1': None, 'RSRV_NUM2': None, 'RSRV_NUM3': None, 'RSRV_NUM4': None, 'RSRV_NUM5': None, 'RSRV_STR1': None, 'RSRV_STR2': None, 'RSRV_STR3': None, 'RSRV_STR4': None, 'RSRV_STR5': None, 'RSRV_TAG1': None, 'RSRV_TAG2': None, 'RSRV_TAG3': None}]
	# newValue = convertDicList(oldValue)
	# print(newValue)
	# oldlst = [{'INTF_ID': 'TF_B_TRADE,TF_B_TRADEFEE_SUB,TF_B_TRADE_PLATSVC,TF_B_TRADE_DISCNT,TF_B_TRADE_RES,TF_B_TRADE_OTHER', 'TRADE_ID': 3120121487954301, 'TRADE_TYPE_CODE': 1041}, {'INTF_ID': 'TF_B_TRADE', 'TRADE_ID': 3120121487954302, 'TRADE_TYPE_CODE': 996}]
	# dic = mergeDictList(oldValue)
	# print(dic)

	dic_1 = {"REMARKS":"test_by_api","BUSI_ITEM_CODE":"131","SUBMIT_TYPE":"0","ACCESS_NUM":"18213349760","LOGIN_TYPE_CODE":"|P"}
	str = "LOGIN_MODE=BOSS&STAFF_ID=TESTKM06&IS_XACTIVE=false&IP_DATA=&MAC_DATA=&BROWSER_VERSION=&PASSWORD=e3937dc80f9bb5ab17cc016cdc612b7d&FOURA_CODE=&UNIFIED_CODE=&LOGIN_FLAG=1"
	# dict_enUrl = convert_enurlToDic(str)
