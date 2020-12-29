import time
import requests
import json
from Base import ReadConfig
from Base.Mylog import LogManager
from Base.SysPara import SysPara

logger = LogManager('UserAuth').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

class UserAuth():
    '''登录用户鉴权'''
    def __init__(self):
        self.url = SysPara().get_IntfUrl('order')
        self.h = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "Connection": "keep - alive",
            "Origin":"http://10.230.81.26:10701",
            "Referer": "http://10.230.81.26:10701/swagger-ui.html"
        }

    def generateByName(self,userName):

        requestUrl = 'http://10.230.81.26:10701/svc/base/generateByName?username={}'.format(userName)
        intf_res = requests.get(url=requestUrl,headers =self.h)
        logger.info("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        return intf_res.content.decode(encoding='utf-8')


if __name__ == '__main__':
    Auth = UserAuth()
    result = Auth.generateByName(userName='HNTEST02')
    print(result)