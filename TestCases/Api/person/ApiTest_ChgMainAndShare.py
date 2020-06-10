import unittest,ddt
import time
import requests
import json
from Base import HTMLTestRunnerCNNew
from Base import ReadConfig
from Base.Mylog import LogManager
from Base.OperExcel import get_exceldata,write_xlsBycolName_append,write_dict_xls
from Base.OracleOper import MyOracle
from Common.function import dict_get,join_dictlists
from TestCases.suite import mySuitePrefixAdd


logger = LogManager('ChgMainAndShare').get_logger_and_add_handlers(1, is_add_stream_handler= True,log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
ora = MyOracle()
#分别取5个主卡号码和副卡号码：
'''主卡号码'''
sql_accessNum = "select rownum No ,'' flowid , '' result_info ,t.access_num , to_char(t.subscriber_ins_id) subscriber_ins_id \
    from  uop_file4.um_subscriber t \
    where t.access_num like '1380872%' and t.mgmt_district = '0872' \
    and t.remove_tag = '0' and rownum <=5"

'''副卡号码'''
sql_ViceaccessNum = "select t.access_num VICE_ACCESS_NUM , to_char(t.subscriber_ins_id) rel_subscriber_insid \
    from  uop_file4.um_subscriber t \
    where t.access_num like '183%' and t.mgmt_district = '0872' \
    and t.remove_tag = '0' and rownum <=5"

AccessNumList = ora.select(sql_accessNum)
ViceNumList = ora.select(sql_ViceaccessNum)
paras = join_dictlists(AccessNumList,ViceNumList)
# paras = [{'NO':'1','FLOWID':'','RESULT_INFO':'','ACCESS_NUM':'13908720067','VICE_ACCESS_NUM':'13908720080'}]
logger.info('测试准备数据:{}'.format(paras))
now = time.strftime("%Y%m%d%H%M%S")
file = ReadConfig.get_data_path() + 'ApiTest_ChgMainAndShare_%s.xlsx' % now
#生成xls表,方便后续写入测试结果
write_dict_xls(inputData=paras, sheetName='主套餐共享受理', outPutFile=file)
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
class ChgMainAndShare(unittest.TestCase):
    '''主套餐共享受理'''
    def setUp(self):
        self.file = file
        self.headers = h
        self.session = requests.session()
        self.session.post(url=rc.get_interface_url("url_login"), headers=h, data=lo_param)
        self.session.get(url=rc.get_interface_url("url_init"), headers=h)
        print("\n")

    @ddt.data(*paras)
    def test_ChgMainAndShare(self,dic):
        '''主套餐共享受理'''
        logger.info("开始参数化......")
        index = int(dic.get('NO'))
        logger.info('开始执行第{}个用例,接口入参:{}'.format(index,dic))
        accessNum = str(dic.get('ACCESS_NUM'))
        logger.info("主卡:"+accessNum)
        VICE_ACCESS_NUM = dic.get('VICE_ACCESS_NUM')
        logger.info("副卡:"+VICE_ACCESS_NUM)


        body ={
            "OFFERS": json.dumps([
                {
                    "ENABLE_MODE": "4",
                    "OFFER_ID": "99091283",
                    "OFFER_LIST": [
                        {
                            "OFFER_ID": "199999999",
                            "ACTION": "0",
                            "ROLE_ID": "999999999"
                        },
                        {
                            "OFFER_ID": "100000000",
                            "ACTION": "0",
                            "ROLE_ID": "999999999"
                        },
                        {
                            "OFFER_ID": "100000023",
                            "ACTION": "0",
                            "ROLE_ID": "999999999"
                        }
                    ],
                    "ACTION": "0",
                    "OFFER_TYPE": "00"
                },
                {
                    "OFFER_ID": "100000001",
                    "ACTION": "0"
                },
                {
                    "OFFER_ID": "100000200",
                    "ACTION": "0"
                }
            ]),
            "SELECTED_OFFER_VALUE":json.dumps( [
                {
                    "OFFER_ID": "99091283",
                    "ACTION": "0",
                    "ENABLE_MODE": "4",
                    "OFFER_TYPE": "00",
                    "OFFER_LIST": [
                        {
                            "OFFER_ID": "199999999",
                            "ROLE_ID": "999999999",
                            "ACTION": "0"
                        },
                        {
                            "OFFER_ID": "100000000",
                            "ROLE_ID": "999999999",
                            "ACTION": "0"
                        },
                        {
                            "OFFER_ID": "100000023",
                            "ROLE_ID": "999999999",
                            "ACTION": "0"
                        }
                    ]
                },
                {
                    "OFFER_ID": "100000001",
                    "ACTION": "0"
                },
                {
                    "OFFER_ID": "100000200",
                    "ACTION": "0"}
            ]),
            "ACCESS_NUM": accessNum,
            "SELECTED_OFFER_NAME": "4G飞享138元全国套餐",
            "MENU_ID": "crm4G12",
            "LOGIN_TYPE_CODE": "|P",
            "SELECTED_ACTIVE_NAME": "",
            "SUBMIT_TYPE": "0",
            # "page": "oc.person.cs.ChangeMainAndShare",
            "VICE_ACCESS_NUM":VICE_ACCESS_NUM ,
            # "IDENTITYAUTH_LOG_ID": "",
            # "service": "ajax",
            # "listener": "onTradeSubmit",
            "BILLING_CODES": "99091283",
            "CHANGE_MAIN_AND_SHARE": "TRUE"
        }

        params = {
                "svcName" : "OrderCentre.person.IChangeMainAndShareSV.changeMainAndShare"
        }
        params.update(body)
        print('请求参数:{}'.format(params))
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
    report_title = u'主套餐共享套餐受理接口自动化测试报告'
    desc = u'主套餐共享套餐受理接口测试详情：'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath() + report_title + nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2)
        runner.run(mySuitePrefixAdd(ChgMainAndShare,"test_ChgMainAndShare"))
