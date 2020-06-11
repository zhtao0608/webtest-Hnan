# -*- coding:utf-8 -*-
# __author:Administrator
# date: 2017/12/28
import requests
import json
from Base import ReadConfig
from Base.Mylog import LogManager
from Base.OracleOper import MyOracle
# from sePublic.GetData import get_cookie
from Common.function import ret_dic,dict_get
import sys ,io,time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('HttpRequest').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

h = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36',
    "Connection": "keep - alive",
    "Referer": rc.get_ngboss('url')
}

lo_param = {'LOGIN_MODE': 'BOSS', 'STAFF_ID': 'TESTKM06', 'IS_XACTIVE': 'false', 'IP_DATA': '', 'MAC_DATA': '', 'BROWSER_VERSION': '', 'PASSWORD': 'e3937dc80f9bb5ab17cc016cdc612b7d', 'FOURA_CODE': '', 'UNIFIED_CODE': '', 'LOGIN_FLAG': '1'}

# co = "WADE_SID=FDDF943B62874A6A954D1F205C149BA7; STAFF_ID=TESTKM06; DEPART_ID=55913; STAFF_EPARCHY_CODE=0872; NGBOSS_NAVHELP_COOKIE=AokBKhs3DpmzVbmKdWoLGQ%3D%3D; NGBOSS_LOGIN_COOKIE=i3EErF5sis0ZG1b6ye11mF%2BPHO%2BP3yU8bAT%2BSGPZugMSwl7TMruwcg%3D%3D"
# cookie = ret_dic(co)
# print(cookie)

class Http:

    def __init__(self):
        # logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
        self.resultPath = ReadConfig.get_reportPath()
        self.scheme = rc.get_ngboss("SCHEME")
        self.ip = rc.get_ngboss("IP")
        self.port = rc.get_ngboss("PORT")
        self.timeout = rc.get_ngboss("timeout")
        self.headers = {}
        self.data = {}
        self.cookie = {}
        self.url = None
        self.session = requests.session()
        self.files = {}
        self.state = 0

    def set_headers(self, header):
        """
        cookies为header中的一个键值对，所以可以在header中添加
        :param header:
        """
        self.headers = header

    def set_data(self, data):
        """
        传的参数json\params等
        :param data:
        :return:
        """
        self.data = data

    def set_url(self,url):
        """
        接口路径
        :param url:
        :return:
        """
        # self.url = "%s://%s:%s%s" % (self.scheme, self.ip, self.port, url)
        self.url = url
        print(self.url)

    def get(self):
        """
        get请求
        :return:
        """
        try:
            # 当headers传的cookies时，要把键值对id改成cookies
            response = requests.get(self.url, cookies=self.headers, timeout=float(self.timeout))
            return response
        except TimeoutError as e:
            logger.error(e)
            return None

    def post(self):
        """
        post请求
        :return:
        """
        try:
            # 当headers传的cookies时，要把键值对id改成cookies
            # response = requests.post(self.url, headers=self.headers, data=self.data, cooikes=self.cookie,timeout=float(self.timeout))
            response = requests.post(self.url,headers=self.headers, data=self.data,cookies=self.cookie,timeout=float(self.timeout))
            return response
        except TimeoutError as e:
            logger.error(e)
            return None

    def IntfSessionPost(self,params={}):
        '''初始化登录，保持登录'''
        lo_url = rc.get_interface_url("url_login")
        init_url = rc.get_interface_url("url_init")
        intf_url = rc.get_interface_url("url_interface")
        self.session.post(url=lo_url,headers=h,data=lo_param)
        self.session.post(url=init_url,headers=h)
        d_intf_res=self.session.post(url=intf_url,headers=h,data=params)
        return d_intf_res.content.decode(encoding='utf-8')


if __name__ == '__main__':
    http = Http()
    para = {"svcName": "OrderCentre.person.IChangeProdStaOperateSV.changeProdStatus", "ACCESS_NUM": "18887269711", "BUSI_ITEM_CODE": "133"}
    d_intf_res = http.IntfSessionPost(para)
    print(d_intf_res)

    # http.session_post()

