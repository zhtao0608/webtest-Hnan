import time
import requests
import json
from Base import ReadConfig
from Base.Mylog import LogManager
from Api.ApiDef import ApiDefine as Api
from Base.OperExcel import write_xlsBycolName_append,write_dict_xls
from Base.OracleOper import MyOracle
from Common.function import dict_get
from Data.DataMgnt.GenTestData import GenTestData

logger = LogManager('OrderService').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )


class OrderService(Api):
    '''查询用户相关信息'''


