# coding: utf-8
import time,datetime
from datetime import timedelta, date
import os,configparser
import hashlib
import types
from urllib import parse
from Base import ReadConfig
from Base.Mylog import LogManager
import json
import ast
import re
import inspect
from Base.SysPara import SysPara
from collections import defaultdict

logger = LogManager('DataCheck').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")


def project_path():
    return os.path.dirname(os.path.dirname(__file__))
    # print(os.path.dirname(os.path.dirname(__file__)))

#返回config_ini文件中的testUrl
def config_url():
    # config = configparser.ConfigParser()
    # config.read(project_path()+"/config.ini")
    # return config.get('NGBOSS','url')
	# return rc.get_ngboss('url')
	return SysPara().get_ngboss('url')

def date_n(n):
	'''返回当前日期后n天的日期'''
	return date.today()+timedelta(days=n)

def parseDate(date_str):
    try:
        if not date_str:
            return None
        if "-" in date_str:
            if date_str.count("-") == 1:
                date = datetime.datetime.strptime(date_str, "%Y-%m")
            elif date_str.count("-") == 2:
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        elif "年" in date_str:
            if "日" in date_str:
                date = datetime.datetime.strptime(date_str, "%Y年%m月%d日")
            elif "月" in date_str:
                date = datetime.datetime.strptime(date_str, "%Y年%m月")
            else:
                date = datetime.datetime.strptime(date_str, "%Y年")
        elif date_str.isdigit():
            if len(date_str) == 4:
                date = datetime.datetime.strptime(date_str, "%Y")
            elif len(date_str) > 6:
                date = datetime.datetime.strptime(date_str, "%Y%m%d")
            else:
                date = datetime.datetime.strptime(date_str, "%Y%m")
        else:
            date = None
    except:
        return None
    return date


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



def getDigitFromStr(String):
	'''从String字符串中提取数字部分'''
	return re.sub("\D","",String)

def retDigitListFromStr(String):
	'''从String字符串中提取数字部分,返回数组'''
	return re.findall(r"\d+\.?\d*",String)

def getCharacterfromStr(String):
	'''从String字符串中提取字母字符串'''
	return ''.join(re.findall(r'[A-Za-z]', String))

def getChsfromStr(String):
	'''从String字符串中提取中文字符串'''
	ste = re.sub("[A-Za-z0-9\!\%\[\]\,\。]", "", String)
	print('提取的中文字符串：' + ste)
	return ste

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

def get_listdictData(list_data):
	'''将字典列表合并为一个字典'''
	dict_data = {}
	for i in list_data:
		key, = i
		value, = i.values()
		dict_data[key] = value
	return dict_data

def mergeDictList(lst):
	'''
	合并字典列表
	合并key值相同的字典列表
	'''
	dic = {}
	for _ in lst:
		for k, v in _.items():
			dic.setdefault(k, []).append(v)
	return dic

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

def strAppend(s, n):
    output = ''
    i = 0
    while i < n:
        output += s
        i = i + 1
    return output


def sqlJoiningDic(sqlParams):
	'''
	SQL拼装
	:param sqlparams: 一个字段类型｛'COLNAME':'VALUE'｝
	:return:
	'''
	if not isinstance(sqlParams, dict):
		logger.info('sqlParams入参必须是dict类型')
	if len(sqlParams) == 0:
		logger.info('sqlParams入参为空')
	print (len(sqlParams))
	Sqlexpr = ''
	for colName,value in sqlParams.items():
		value = "'" + value + "'"
		string = colName +'='+ value + ','
		print(string)
		Sqlexpr = Sqlexpr + string
		# print(type(expr))
	return Sqlexpr[0:len(Sqlexpr)-1]   #注意删除最后一个字符‘,’

def retStackFunc():
	'''从堆栈信息中获取外层函数名'''
	t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
	execInfoList = inspect.stack()
	logger.info('完整堆栈信息:{}'.format(execInfoList))
	stackInfoList = []
	for i in range(0,len(execInfoList)):
		exec_info = execInfoList[i]
		logger.info('外层堆栈信息{}'.format(exec_info))
		_function = exec_info[3]
		# print('-----------------',_function)
		logger.info('调用的函数：{}'.format(_function))
		fn = exec_info[1].rsplit("/", 1)[1]
		logger.info('调用的外层函数文件名:{}'.format(fn))
		# 所在行
		_line = exec_info[2]
		# 调用的方法
		_function = exec_info[3]
		# 执行的命令
		_cmd = exec_info[4][0]
		# 执行的命令中参数的名称
		pattern = re.compile(
			retStackFunc.__name__ + '\((.*?)\)$',
			re.S
		)
		_cmd = _cmd.strip().replace('\r', '').replace('\n', '')
		# 变量名
		# 变量转字符串
		log_info = '[{time}] [{func}] [{line}] '.format(
			time=t,
			func=_function,
			line=_line

		)
		logger.info(log_info)
		dicStackInfo = {'time':t,'func':_function,'line':_line}
		logger.info(dicStackInfo)
		stackInfoList.append(dicStackInfo)

	return stackInfoList

# if __name__ == '__main__':
#     print("项目路径"+project_path())
#     print(project_path())
#
#     # print(project_path()+"/config.ini")
#     print("被测系统Url:"+config_url())

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

	# dic_1 = {"REMARKS":"test_by_api","BUSI_ITEM_CODE":"131","SUBMIT_TYPE":"0","ACCESS_NUM":"18213349760","LOGIN_TYPE_CODE":"|P"}
	# str = "LOGIN_MODE=BOSS&STAFF_ID=TESTKM06&IS_XACTIVE=false&IP_DATA=&MAC_DATA=&BROWSER_VERSION=&PASSWORD=e3937dc80f9bb5ab17cc016cdc612b7d&FOURA_CODE=&UNIFIED_CODE=&LOGIN_FLAG=1"
	# dict_enUrl = convert_enurlToDic(str)


	# frame = "[FrameInfo(frame=<frame at 0x0000028A88C757E8, file 'E:\\ProgramData\\PycharmProjects\\webtest-Qhai\\Common\\function.py', line 230, code retStackFunc>, filename='E:\\ProgramData\\PycharmProjects\\webtest-Qhai\\Common\\function.py', lineno=229, function='retStackFunc', code_context=['\texecInfoList = inspect.stack()\n'], index=0), FrameInfo(frame=<frame at 0x0000028A8A5B4C58, file 'E:\\ProgramData\\PycharmProjects\\webtest-Qhai\\Check\\RuleCheck.py', line 22, code checkRule>, filename='E:\\ProgramData\\PycharmProjects\\webtest-Qhai\\Check\\RuleCheck.py', lineno=22, function='checkRule', code_context=['        stackInfo = retStackFunc()\n'], index=0), FrameInfo(frame=<frame at 0x0000028A88C779E8, file 'E:\\ProgramData\\PycharmProjects\\webtest-Qhai\\PageObj\\order\\group\\BusiAccept\\GroupOfferAccept.py', line 46, code accept_CrtUs>, filename='E:\\ProgramData\\PycharmProjects\\webtest-Qhai\\PageObj\\order\\group\\BusiAccept\\GroupOfferAccept.py', lineno=46, function='accept_CrtUs', code_context=['        RuleCheckBefore(self.driver).checkRule(scene) #\n'], index=0), FrameInfo(frame=<frame at 0x0000028AFFC8D768, file 'E:/ProgramData/PycharmProjects/webtest-Qhai/TestCases/group/CrtUsVPMNTest.py', line 50, code testCrtUsVpmn>, filename='E:/ProgramData/PycharmProjects/webtest-Qhai/TestCases/group/CrtUsVPMNTest.py', lineno=50, function='testCrtUsVpmn', code_context=['                                                   contractId=contractId,elementAttrBizList=elementAttrBizList)\n'], index=0), FrameInfo(frame=<frame at 0x0000028A896D3220, file 'D:\\Program File\\python37\\lib\\site-packages\\ddt.py', line 151, code wrapper>, filename='D:\\Program File\\python37\\lib\\site-packages\\ddt.py', lineno=151, function='wrapper', code_context=['        return func(self, *args, **kwargs)\n'], index=0), FrameInfo(frame=<frame at 0x0000028A888F36B8, file 'D:\\Program File\\python37\\lib\\unittest\\case.py', line 615, code run>, filename='D:\\Program File\\python37\\lib\\unittest\\case.py', lineno=615, function='run', code_context=['                    testMethod()\n'], index=0), FrameInfo(frame=<frame at 0x0000028A8969B8E0, file 'D:\\Program File\\python37\\lib\\unittest\\case.py', line 663, code __call__>, filename='D:\\Program File\\python37\\lib\\unittest\\case.py', lineno=663, function='__call__', code_context=['        return self.run(*args, **kwds)\n'], index=0), FrameInfo(frame=<frame at 0x0000028A89628228, file 'D:\\Program File\\python37\\lib\\unittest\\suite.py', line 122, code run>, filename='D:\\Program File\\python37\\lib\\unittest\\suite.py', lineno=122, function='run', code_context=['                test(result)\n'], index=0), FrameInfo(frame=<frame at 0x0000028A8969B728, file 'D:\\Program File\\python37\\lib\\unittest\\suite.py', line 84, code __call__>, filename='D:\\Program File\\python37\\lib\\unittest\\suite.py', lineno=84, function='__call__', code_context=['        return self.run(*args, **kwds)\n'], index=0), FrameInfo(frame=<frame at 0x0000028A882383D8, file 'E:\\ProgramData\\PycharmProjects\\webtest-Qhai\\Base\\HTMLTestRunnerCNNew.py', line 971, code run>, filename='E:\\ProgramData\\PycharmProjects\\webtest-Qhai\\Base\\HTMLTestRunnerCNNew.py', lineno=971, function='run', code_context=['        test(result)\n'], index=0), FrameInfo(frame=<frame at 0x0000028AFF9FE9F8, file 'E:/ProgramData/PycharmProjects/webtest-Qhai/TestCases/group/CrtUsVPMNTest.py', line 66, code <module>>, filename='E:/ProgramData/PycharmProjects/webtest-Qhai/TestCases/group/CrtUsVPMNTest.py', lineno=66, function='<module>', code_context=['        runner.run(mySuitePrefixAdd(CrtUsVpmnTest,'test'))\n'], index=0)]"
	# print(type(frame))
	# # frame.replace('\\','/').replace(' ','').replace('\n','').replace('\\','\/')
	# frame=re.sub('[\r\n\t\"]', '', frame)
	# frame=re.sub('=', ':', frame)
	#
	# print(frame)

	# ret= retStackFunc()
	# print('==========',ret)

	# print('=====',dict_enUrl)
	# print('*****',config_url())
	# sqlparams ={'name':'xiaoming','age':'11','school':'tsinghua'}
	# expr = sqlJoiningDic(sqlparams)
	# print(type(expr))
	# print(expr)



	# print(get_enurl(dic_1))
	# enurl_str = get_enurl(dic_1).replace('=',":")
	# list_enurl = enurl_str.split('&')
	# print('list_enurl=',list_enurl)
	# dict_key = []
	# dict_value = []
	# for i in range(len(list_enurl)):
	# 	value = list_enurl[i]
	# 	list_value = value.split(':')
	# 	print(list_value)
	# 	print(type(list_value))
	# 	for j in range(1,len(list_value)):
	# 		dict_key.append(list_value[0])
	# 		dict_value.append(list_value[1])
	# print('dict_key=',dict_key)
	# print('dict_value',dict_value)
	# dict = convert_ListToDic(dict_key,dict_value)
	# print(dict)

	# print(convert_ListToDic(dict_key,dict_value))
	# print('转换后的dict====',dict)



		# dict_i = eval(list_enurl[i])
		# print(dict_i)

		# print(value.split(':'))
		# value_list = list(value)
		# print(value_list)

	# keylist = []
		# for j in range(len(value)):
		# 	# key = str(value).split(':')
		# 	# keylist.append(key)
		# 	print(keylist)
		# for j in range(len(value)):
		# 	dict_key = value[0]
		# 	dict_value = value[1]
		# 	print(dict_key,dict_value)

# 	daten = date_n(10)
# 	print('n天后的日期:' ,daten)
# 	datetimen = datetime_n(30)
# 	print('n天后的时间：',datetimen)
#     # co = "SUBSCRIBER_OPEN_COOKIE_10=3Rz6w1QsiDxyypM51REBbQ%3D%3D; CRM_ECNAVIGATION_COOKIE=bnLIzblE%2B3B1QqCj583MjVcmUOU4lV3JrAg8genK9jJABq1Y1q9XTClc7P7%2BYKsG6A3wS4NtCSKsrgayrQ7iAuNuOPtx%2Bxnrii2nv8m%2BzEAsv%2FRNXoFz5OJLs56Cxobb5a9EhkUVCmD9BDNUf0DlurzA0aMrDMrl; NGBOSS_NAVHELP_COOKIE=AokBKhs3DpmzVbmKdWoLGQ%3D%3D; STAFF_ID=TESTKM06; DEPART_ID=55913; STAFF_EPARCHY_CODE=0872; WADE_SID=2359B5A00E744C4B9B58D3EF2EBE1BE8; NGBOSS_LOGIN_COOKIE=X48c74%2FfJTxsBP5IY9m6A0%2FsS9SMWUNZtqUtYnG20bA30bCuF9z8Ow%3D%3D"
# 	dictest = {
# 	"context": {
# 		"provinceId": "",
# 		"contextRoot": "",
# 		"productMode": "true",
# 		"subSysCode": "",
# 		"x_resultinfo": "ok",
# 		"x_resultcode": "0",
# 		"contextName": "",
# 		"version": "0"
# 	},
# 	"data": {
# 		"X_RESULTINFO": "ok",
# 		"X_NODE_NAME": "app-node01-srv01",
# 		"DATAS": [{
# 			"EXPIRE_DATE": "2050-12-31 23:59:59.0",
# 			"DATA_STATUS": "1",
# 			"OP_ID": "CB201014",
# 			"IS_MAIN": "1",
# 			"OFFER_NAME": "移动人人通A(ADC)",
# 			"MGMT_COUNTY": "C0LB",
# 			"SUBSCRIBER_INS_ID": "7090120700227870",
# 			"OFFER_INS_ID": "7090120743986708",
# 			"ORG_ID": "41921",
# 			"CREATE_ORG_ID": "41921",
# 			"REGION_ID": "06",
# 			"CUST_ID": "7009120710016270",
# 			"CREATE_OP_ID": "CB201014",
# 			"VALID_DATE": "2014-09-29 16:48:14.0",
# 			"OFFER_ID": "6465",
# 			"DONE_DATE": "2010-12-07 17:42:11.0",
# 			"CREATE_DATE": "2010-12-07 17:42:11.0",
# 			"IS_BUNDLE": "1",
# 			"BRAND": "ADCG",
# 			"OFFER_TYPE": "10",
# 			"MGMT_DISTRICT": "0870"
# 		}, {
# 			"EXPIRE_DATE": "2050-12-31 23:59:59.0",
# 			"DATA_STATUS": "1",
# 			"OP_ID": "CJ001166",
# 			"IS_MAIN": "1",
# 			"OFFER_NAME": "企信通行业版",
# 			"MGMT_COUNTY": "C0LJ",
# 			"SUBSCRIBER_INS_ID": "7092112700395952",
# 			"OFFER_INS_ID": "7092112792176223",
# 			"ORG_ID": "41908",
# 			"CREATE_ORG_ID": "41908",
# 			"REGION_ID": "06",
# 			"CUST_ID": "7006052300124493",
# 			"CREATE_OP_ID": "CJ001166",
# 			"VALID_DATE": "2012-12-07 16:15:11.0",
# 			"OFFER_ID": "6415",
# 			"DONE_DATE": "2012-11-27 16:14:17.0",
# 			"CREATE_DATE": "2012-11-27 16:14:17.0",
# 			"IS_BUNDLE": "1",
# 			"BRAND": "ADCG",
# 			"OFFER_TYPE": "10",
# 			"MGMT_DISTRICT": "0870"
# 		}, {
# 			"EXPIRE_DATE": "2050-12-31 00:00:00.0",
# 			"DATA_STATUS": "1",
# 			"IS_MAIN": "1",
# 			"OFFER_NAME": "短号集群网",
# 			"REMARKS": "NG割接导入",
# 			"MGMT_COUNTY": "C0LJ",
# 			"SUBSCRIBER_INS_ID": "7008082116429310",
# 			"OFFER_INS_ID": "7009000416595229",
# 			"REGION_ID": "06",
# 			"CUST_ID": "7008082106837850",
# 			"VALID_DATE": "2015-03-09 16:10:12.0",
# 			"OFFER_ID": "8000",
# 			"CREATE_DATE": "2008-08-21 00:00:00.0",
# 			"IS_BUNDLE": "1",
# 			"BRAND": "VPMN",
# 			"OFFER_TYPE": "10",
# 			"MGMT_DISTRICT": "0870"
# 		}, {
# 			"EXPIRE_DATE": "2050-12-31 23:59:59.0",
# 			"DATA_STATUS": "1",
# 			"OP_ID": "CJ001065",
# 			"IS_MAIN": "1",
# 			"OFFER_NAME": "移动人人通A(ADC)",
# 			"MGMT_COUNTY": "C0LJ",
# 			"SUBSCRIBER_INS_ID": "7090120700227982",
# 			"OFFER_INS_ID": "7090120744024508",
# 			"ORG_ID": "41908",
# 			"CREATE_ORG_ID": "41908",
# 			"REGION_ID": "06",
# 			"CUST_ID": "7009120509988067",
# 			"CREATE_OP_ID": "CJ001065",
# 			"VALID_DATE": "2013-09-14 21:44:44.0",
# 			"OFFER_ID": "6465",
# 			"DONE_DATE": "2010-12-07 22:27:49.0",
# 			"CREATE_DATE": "2010-12-07 22:27:49.0",
# 			"IS_BUNDLE": "1",
# 			"BRAND": "ADCG",
# 			"OFFER_TYPE": "10",
# 			"MGMT_DISTRICT": "0870"
# 		}, {
# 			"EXPIRE_DATE": "2050-12-31 23:59:59.0",
# 			"DATA_STATUS": "1",
# 			"OP_ID": "IBOSS000",
# 			"IS_MAIN": "1",
# 			"OFFER_NAME": "中央ADC业务(商品)",
# 			"MGMT_COUNTY": "A0AL",
# 			"SUBSCRIBER_INS_ID": "7193090800490363",
# 			"OFFER_INS_ID": "7193090858365958",
# 			"ORG_ID": "00309",
# 			"CREATE_ORG_ID": "00309",
# 			"REGION_ID": "06",
# 			"CUST_ID": "7113090863032571",
# 			"CREATE_OP_ID": "IBOSS000",
# 			"VALID_DATE": "2014-01-20 15:41:16.0",
# 			"OFFER_ID": "9945",
# 			"DONE_DATE": "2013-09-08 00:09:40.0",
# 			"CREATE_DATE": "2013-09-08 00:09:40.0",
# 			"IS_BUNDLE": "1",
# 			"BRAND": "BOSG",
# 			"OFFER_TYPE": "10",
# 			"MGMT_DISTRICT": "0871"
# 		}, {
# 			"EXPIRE_DATE": "2050-12-31 23:59:59.0",
# 			"DATA_STATUS": "1",
# 			"OP_ID": "CA101028",
# 			"IS_MAIN": "1",
# 			"OFFER_NAME": "集团彩铃",
# 			"MGMT_COUNTY": "C0LA",
# 			"SUBSCRIBER_INS_ID": "7099062600011114",
# 			"OFFER_INS_ID": "7099062603769207",
# 			"ORG_ID": "41886",
# 			"CREATE_ORG_ID": "41886",
# 			"REGION_ID": "06",
# 			"CUST_ID": "7008082106837850",
# 			"CREATE_OP_ID": "CA101028",
# 			"VALID_DATE": "2009-06-27 18:12:05.0",
# 			"OFFER_ID": "6200",
# 			"DONE_DATE": "2009-06-26 11:52:10.0",
# 			"CREATE_DATE": "2009-06-26 11:52:10.0",
# 			"IS_BUNDLE": "1",
# 			"BRAND": "VPMR",
# 			"OFFER_TYPE": "10",
# 			"MGMT_DISTRICT": "0870"
# 		}, {
# 			"EXPIRE_DATE": "2050-12-31 23:59:59.0",
# 			"DATA_STATUS": "1",
# 			"OP_ID": "CJ001102",
# 			"IS_MAIN": "1",
# 			"OFFER_NAME": "企信通行业版",
# 			"MGMT_COUNTY": "C0LJ",
# 			"SUBSCRIBER_INS_ID": "7094031400600899",
# 			"OFFER_INS_ID": "7094031415595663",
# 			"ORG_ID": "41908",
# 			"CREATE_ORG_ID": "41908",
# 			"REGION_ID": "06",
# 			"CUST_ID": "7014031133431322",
# 			"CREATE_OP_ID": "CJ001102",
# 			"VALID_DATE": "2015-11-17 17:22:30.0",
# 			"OFFER_ID": "6415",
# 			"DONE_DATE": "2014-03-14 10:04:59.0",
# 			"CREATE_DATE": "2014-03-14 10:04:59.0",
# 			"IS_BUNDLE": "1",
# 			"BRAND": "ADCG",
# 			"OFFER_TYPE": "10",
# 			"MGMT_DISTRICT": "0870"
# 		}],
# 		"X_RESULTCODE": "0"
# 	}
# }
# 	ret1 = dict_get(dictest, 'DATAS', None)
#     # ret2 = dict_get(dictest, 'ACCESS_NUM', None)
#     # print(ret1)   #list
# 	print(ret1)
# 	print(type(ret1))
# 	for i in range(len(ret1)):
# 		print("订购的商品列表：" + json.dumps(ret1[i]))
# 		# offername = ret1[i]['OFFER_NAME']
# 		# grp_inst_id = ret1[i]['SUBSCRIBER_INS_ID']
# 		# print("订购的集团商品名称:" + offername)
# 		# print("订购的集团用户ID:" + grp_inst_id)
# 	lista = [{'serialNum':'15969006462','shortCode':'681618','userId':'7008080716050718'},
# 			 {'serialNum': '18787961713', 'shortCode': '681713', 'userId': '9110102326860610'},
# 			 {'serialNum': '15096963621', 'shortCode': '693621', 'userId': '7208102218270765'}
# 			]
# 	listb = [{'groupId':8723409920,'GroupName':'大理市海东镇上和完小（校讯通）','OfferInstId':'7295021394647174'},
# 			 {'groupId': 8723409625, 'GroupName': '祥云县银冠希望小学','OfferInstId': '7295012691118641'},
# 			 {'groupId': 8711437379, 'GroupName': '巍山红河源初级中学','OfferInstId': '7291092369525517'}
# 			]
# 	listc = [{'simId':89860001240642520092},{'simId':89860076240442072049},{'simId':89860057245448890016}]
# 	print(lista)
# 	print(listb)
# 	newlist = join_dictlists(lista,listb)
# 	newlist = join_dictlists(newlist,listc)
# 	print(newlist)
# 	subofferList = '800001,990013,990013445,99315 '.replace(' ','').split(',')
# 	print(subofferList)
#
# 	dic_1 = {'No': 1, 'CaseName': '集团商品订购，订购ADC集团管家商品', 'flowid': '7220052100507558', 'x_result_info': 'testtest', 'groupId': '8711400551', 'mainoffer': '6480', 'accessNum': '13887241120', 'subofferList': '100648000,  100648001  ', 'grp_offer_ins_id': '', 'Expect_result ': 'ok'}
# 	list_values = [i for i in dic_1.values()]
# 	print(list_values)
# 	list_keys= [ i for i in dic_1.keys()]
# 	print(list_keys)
#
# 	# dic_list=dict(zip(list_keys,list_values))
# 	# print('==========',dic_list)
#
#
# 	# print(lista + listb)
#
# 	paras = "[[1,2], [3,4], [5,6], [7,8], [9,0]]"
# 	# paras = "{'ACCESS_NUMBER':'18708720668','ICC_ID':'898600D0242447530068','OFFER_ID':'99091283'},{'ACCESS_NUMBER':'18708720668','ICC_ID':'898600D0242447530068','OFFER_ID':'99091283'},{'ACCESS_NUMBER':'18708720668','ICC_ID':'898600D0242447530068','OFFER_ID':'99091283'},{'ACCESS_NUMBER':'18708720668','ICC_ID':'898600D0242447530068','OFFER_ID':'99091283'}"
# 	params = convertParatoList(paras)
# 	print('转换后Params=',params)
# 	print('转换后Params类型:',type(params))
#
# 	listDatas = list_data = [{'ACCESS_NUMBER':'11122233333'},
# 							 {'ICC_ID2': '898600D0242447530068'},
# 							 {'ICC_ID3': '898600D0242447530068'}
# 							]
# 	print(get_listdictData(listDatas))
# 	String = '尊敬的全球通白金卡用户，您好！您将办理主产品变更业务，变更前产品:5G智享套餐（个人版）128.5档~~变更后产品:飞享套餐39.00元（达量不限速），您的短信验证码为：592902。 【中国移动】'
# 	print(String)
# 	print(getDigitFromStr(String))
# 	print(retDigitListFromStr(String))
# 	# print(getCharacterfromStr(String))
# 	# print(getChsfromStr(String))
# 	smsCode = '9999999'
# 	print(len(smsCode))
# 	attrBizList = [{"ELEMENT_ID":"120010122813","OFFER_TYPE":"P","AttrBizList":[{"ATTR_VALUE": "610530","ATTR_CODE": "pam_SHORT_CODE"}]},
#                   {"ELEMENT_ID": "120010122813", "OFFER_TYPE": "S", "AttrBizList": []},
#                   {"ELEMENT_ID": "120000008174", "OFFER_TYPE": "S","AttrBizList": [{"ATTR_VALUE": "IMS融合通信 - @ ims.qh.chinamobile.com","ATTR_CODE": "IMPU_TYPE"}]},
#                   {"ELEMENT_ID": "120000008172", "OFFER_TYPE": "S", "AttrBizList": []}]
# 	for i in range(len(attrBizList)):
# 		print('需要设置的页面属性:{}'.format(attrBizList[i]))
# 		elementId = attrBizList[i]['ELEMENT_ID']  # 获取元素编码
# 		OfferType = attrBizList[i]['OFFER_TYPE']  # 获取元素类型
# 		AttrBizList = attrBizList[i]['AttrBizList']  # 获取属性列表
# 		print("要设置属性的元素编码：" + elementId)
# 		print(AttrBizList)
# 	dicAttrBiz = {"ATTR_VALUE": "IMS融合通信 - @ ims.qh.chinamobile.com", "ATTR_CODE": "IMPU_TYPE"}
# 	print('========')
# 	print(dicAttrBiz['ATTR_VALUE'])
#
# 	ElementAttrBizList = [{"ELEMENT_ID":"120010122813","OFFER_TYPE":"P","AttrBizList":[{"ATTR_VALUE": "610530","ATTR_CODE": "pam_SHORT_CODE"}]},
#                   {"ELEMENT_ID": "120010122813", "OFFER_TYPE": "S", "AttrBizList": []},
#                   {"ELEMENT_ID": "120000008174", "OFFER_TYPE": "D","AttrBizList": [{"ATTR_VALUE": "IMS融合通信 - @ ims.qh.chinamobile.com","ATTR_CODE": "IMPU_TYPE"}]},
#                   {"ELEMENT_ID": "120000008172", "OFFER_TYPE": "S", "AttrBizList": []}]
# 	subOfferList = []
# 	for i in range(len(ElementAttrBizList)):
# 		print(ElementAttrBizList[i])
# 		offer_type = ElementAttrBizList[i]['OFFER_TYPE']
# 		if offer_type =='P':
# 			subOfferList.append(ElementAttrBizList[i])
#
# 	print('================过滤以后===============')
# 	print(subOfferList)

	# IdCard = '632124196502235348'
	# birthday = IdCard[6:10] + '_' + IdCard[10:12] + '_' + IdCard[12:14]
	# print(birthday)

	# dic = {'name':'xiaoming','age':'11','school':'tsinghua'}
	# if dic:
	# 	print('字典不是空的')
	# 	print(len(dic))
	# else:
	# 	print('字典是空的')

