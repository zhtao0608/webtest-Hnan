import unittest,ddt
import time
import requests
import json
from Base import HTMLTestRunnerCNNew
from Base import ReadConfig
from Base.Mylog import LogManager
from Base.OperExcel import get_exceldata,write_xlsBycolName_append,write_dict_xls
from Base.OracleOper import MyOracle
from Common.function import dict_get
from TestCases.suite import mySuitePrefixAdd

logger = LogManager('ChgUserPwd').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
ora = MyOracle()
#取10个测试号码修改密码为108109：
sql = "select rownum No ,'' flowid , '' result_info ,t.access_num , \
    t.password Old_pwd,uop_file4.f_csb_encrypt('108109',t.subscriber_ins_id) new_pwd ,t.subscriber_ins_id \
    from  uop_file4.um_subscriber t \
    where t.access_num like '139%' \
    and t.remove_tag = '0' and rownum <=3"

paras = ora.select(sql)
logger.info('测试准备数据:{}'.format(paras))
now = time.strftime("%Y%m%d%H%M%S")
file = ReadConfig.get_data_path() + 'ApiTest_ChgUserPwd_%s.xlsx' % now
#生成xls表,方便后续写入测试结果
write_dict_xls(inputData=paras, sheetName='用户密码修改', outPutFile=file)
logger.info('写入测试数据到xls.....')

rc = ReadConfig.ReadConfig("ngboss_config.ini")
h = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36',
    "Connection": "keep - alive",
    "Referer": rc.get_ngboss('url')
}

lo_param = {"LOGIN_MODE": "BOSS", "STAFF_ID": "TESTKM06", "IS_XACTIVE": "false", "BROWSER_VERSION": "IE-11",
        "PASSWORD": "e3937dc80f9bb5ab17cc016cdc612b7d", "LOGIN_FLAG": "1"}



@ddt.ddt
class ChgUserPwd(unittest.TestCase):
    '''修改用户服务密码'''
    def setUp(self):
        self.file = file
        self.headers = h
        self.session = requests.session()
        self.session.post(url=rc.get_interface_url("url_login"), headers=h, data=lo_param)
        self.session.get(url=rc.get_interface_url("url_init"), headers=h)
        print("\n")

    @ddt.data(*paras)
    def test_ChgUserPwd(self,dic):
        logger.info("开始参数化......")
        index = int(dic.get('NO'))
        logger.info('开始执行第{}个用例,接口入参:{}'.format(index,dic))
        accessNum = str(dic.get('ACCESS_NUM'))
        logger.info("测试号码:"+accessNum)
        newPassword = dic.get('NEW_PWD')

        params =  {
                "IS_INTERFACE" : "1" ,
                "CHANGE_TYPE" : "1" ,
                "ACCESS_NUM" : accessNum,
                "NEW_PASSWORD" : newPassword,
                "svcName" : "OrderCentre.person.ISubscriberOperateSV.changeSubscriberPassword"
        }
        logger.info("开始构建请求......"+"\n")
        intf_url = rc.get_interface_url("url_interface")
        logger.info("接口测试地址：" + intf_url )
        intf_res = self.session.post(url=intf_url,headers = h, data = params)
        logger.info("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        logger.info("处理接口返回数据....")
        d_intf_res = json.loads(intf_res.content.decode(encoding='utf-8'))
        x_resultcode = dict_get(d_intf_res, 'X_RESULTCODE', None)
        if x_resultcode == '0':
            flowid = dict_get(d_intf_res, 'flowId', None)
            logger.info("接口处理成功，受理号码为：{},订单交互流水号：{}".format(accessNum,flowid))
            print("接口处理成功，受理号码为：{},订单交互流水号：{}".format(accessNum,flowid))
            logger.info("开始写入结果xls数据......")
            write_xlsBycolName_append(file=self.file, row=index,colName='FLOWID', value=flowid)
            logger.info("测试结果写入xls成功......")
        else:
            x_resultinfo = dict_get(d_intf_res, 'x_resultinfo', None)
            logger.info("接口处理失败，错误信息：{}".format(x_resultinfo))
            print("接口处理错误信息：" + x_resultinfo)
            logger.info("开始写入xls数据......")
            write_xlsBycolName_append(file=self.file, row=index,colName='RESULT_INFO', value=x_resultinfo)
            logger.info("测试结果写入xls成功......")

if __name__ == '__main__':
    report_title = u'接口自动化测试报告'
    desc = u'接口测试详情：'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath() + report_title + nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2)
        runner.run(mySuitePrefixAdd(ChgUserPwd,"test_ChgUserPwd"))
