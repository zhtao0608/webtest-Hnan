# -*- coding:utf-8 -*-
# __author:Administrator
# date: 2017/12/28
import requests
import json
from Common import ReadConfig
from Common.Mylog import LogManager
from Base.OracleOper import MyOracle
# from sePublic.GetData import get_cookie
from Common.function import ret_dic,dict_get
import sys ,io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

# co = "WADE_SID=FDDF943B62874A6A954D1F205C149BA7; STAFF_ID=TESTKM06; DEPART_ID=55913; STAFF_EPARCHY_CODE=0872; NGBOSS_NAVHELP_COOKIE=AokBKhs3DpmzVbmKdWoLGQ%3D%3D; NGBOSS_LOGIN_COOKIE=i3EErF5sis0ZG1b6ye11mF%2BPHO%2BP3yU8bAT%2BSGPZugMSwl7TMruwcg%3D%3D"
# cookie = ret_dic(co)
# print(cookie)

svcname = "OrderCentre.person.IChangeProdStaOperateSV.changeProdStatus"
access_number = "18760919710"

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

    def set_url(self, url):
        """
        接口路径
        :param url:
        :return:
        """
        self.url = "%s://%s:%s%s" % (self.scheme, self.ip, self.port, url)
        # print(self.url)

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
            # loggerger.error(e)
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

    def session_get(self):
        '''session发送get请求'''
        session = requests.session()
        try:
            # 当headers传的cookies时，要把键值对id改成cookies
            # response = requests.post(self.url, headers=self.headers, data=self.data, cooikes=self.cookie,timeout=float(self.timeout))
            response = session.get(self.url, headers=self.headers)
            return response
        except TimeoutError as e:
            logger.error(e)
            return None

    def session_post(self):
        """
        session发送post请求
        :return:
        """
        session = requests.session()
        try:
            # 当headers传的cookies时，要把键值对id改成cookies
            # response = requests.post(self.url, headers=self.headers, data=self.data, cooikes=self.cookie,timeout=float(self.timeout))
            response = session.post(self.url, headers=self.headers, data=self.data)
            return response
        except TimeoutError as e:
            logger.error(e)
            return None



if __name__ == '__main__':
    ht = Http()
    ht.set_url(rc.get_interface_url("url_login"))
    print(ht.url)
    ht.set_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36",
     "Connection": "keep-alive",
    "Referer": "http://10.174.43.39:9090/ngboss?service=page/Home" })
    print(ht.headers)

    ht.set_data({"LOGIN_MODE":"BOSS","STAFF_ID":"TESTKM06","IS_XACTIVE":"false","BROWSER_VERSION":"IE-11",
            "PASSWORD":"e3937dc80f9bb5ab17cc016cdc612b7d","LOGIN_FLAG":"1"})
    print(ht.data)

    # # 获取结果的json(),可以像字典一样取值
    ht.post()
    c = ht.post().cookies
    print(c)
    ##发送接口测试请求
    ht2 = Http()
    ht2.set_url(rc.get_interface_url("url_interface"))
    print(ht2.url)
    ht2.set_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36",
     "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
     "Connection": "keep-alive"})
    print(ht2.headers)
    ht2.set_data({"svcName":svcname,"REMARKS":"test_by_api_zhout","BUSI_ITEM_CODE":"131" , "ACCESS_NUM":access_number })
    # print(ht2.data)
    #
    # # 获取结果的json(),可以像字典一样取值
    d_res = ht2.post().text
    print(d_res)
    print(type(d_res))
    x_resultcode = dict_get(json.loads(d_res),'x_resultcode',None)
    if x_resultcode=='ok':
        flowid = dict_get(json.loads(d_res),'flowId',None)
        print("订单交互流水号：" + flowid)
    else:
        print("错误信息："+dict_get(json.loads(d_res),'x_errorinfo',None))


# print("接口处理情况：" + x_resultcode)
    # print(d_res["status"])
    # # 再把status传到另一个接口中获取数据
    # print(d_res["text"])


    # ht = Http()
    #     # ht.set_url(rc.get_interface_url("url_interface"))
    #     #
    #     # ht.set_headers({"ocde": "0", "username": "system", "password": "system%40123", "orgCode": "B"
    #     #                 , "JSESSIONID": "LrKMJ9rCUZZPYt0Mp4veUaKvRYRcWqQqwWVlvAVsQlJ0vyYFiPIv!-1564142059", "TOPMENU": "%2Fhome.do"})
    #     #
    #     # ht.set_data({"vehicleIds": "52100001", "cmdCode": "1", "cmdVal": "1", "sendTitle": "点名", "paramCode": "param",
    #     #              "paramName": "", "id": "Z1000101"})
    #     # # res = ht.post()
    #     # # status = res.status_code
    #     # # print(type(status))
    #     #
    #     # res = ht.post().json()
    #     # print(res)