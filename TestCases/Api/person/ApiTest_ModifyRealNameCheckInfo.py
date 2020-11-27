import unittest,ddt
import time
import requests
import json
from Base import HTMLTestRunnerCNNew
from Base import ReadConfig
from Base.Mylog import LogManager
from Base.OperExcel import write_xlsBycolName_append,write_dict_xls
from Base.OracleOper import MyOracle
from Common.function import dict_get
from Data.DataMgnt.GenTestData import GenTestData
from TestCases.suite import mySuitePrefixAdd

logger = LogManager('test').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
ora = MyOracle()
#取20个未实名制的测试号码客户信息：
sql = "SELECT rownum No ,t.access_num ,to_char(t.subscriber_ins_id) subscriber_ins_id , \
      to_char(a.iden_id) iden_id,'' NEW_IDENID ,a.iden_type_id,a.iden_nr,b.party_name,\
      to_char(t.cust_id) cust_id ,'' flowid , '' result_info  ,'' NEWCUSTNAME \
     FROM  uop_file4.um_subscriber T ,uop_cp.cb_identification a,uop_cp.cb_party b  \
      where t.remove_tag = '0' and t.access_num LIKE '1880872%' and t.mgmt_district = '0872'\
     and a.party_id = t.cust_id \
     and a.party_id = b.party_id \
     and rownum <=100"

paras = ora.select(sql)
logger.info('测试准备数据:{}'.format(paras))
now = time.strftime("%Y%m%d%H%M%S")
file = ReadConfig.get_data_path() + 'ApiTest_ModfiyRealChkInfo_%s.xls' % now
#生成xls表,方便后续写入测试结果
write_dict_xls(inputData=paras, sheetName='实名制登记', outPutFile=file)
logger.info('写入测试数据到xls.....')

rc = ReadConfig.ReadConfig("ngboss_config.ini")
h = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36',
    "Connection": "keep - alive",
    "Referer": rc.get_ngboss('url')
}

lo_param = {"LOGIN_MODE": "BOSS", "STAFF_ID": "TESTKM13", "IS_XACTIVE": "false", "BROWSER_VERSION": "IE-11",
        "PASSWORD": "e3937dc80f9bb5ab17cc016cdc612b7d", "LOGIN_FLAG": "1"}

@ddt.ddt
class ModfiyRealChkInfo(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.file = file
        self.headers = h
        self.session = requests.session()
        self.session.post(url=rc.get_interface_url("url_login"), headers=h, data=lo_param)
        self.session.get(url=rc.get_interface_url("url_init"), headers=h)
        print("\n")

    @ddt.data(*paras)
    def test_modifyRealChkInfo(self,dic):
        logger.info("开始参数化......")
        index = int(dic.get('NO'))
        logger.info('开始执行第{}个用例,接口入参:{}'.format(index,dic))
        accessNum = str(dic.get('ACCESS_NUM'))
        logger.info("测试号码:"+accessNum)
        custId = str(dic.get('CUST_ID'))
        IdenId= str(dic.get('IDEN_ID'))
        custName = GenTestData().create_CustName() #随机生成姓名
        psptId = GenTestData().Create_Idcard() #随机身份证号码
        # logger.info('证件号码:{}'.format(psptId))
        write_xlsBycolName_append(file=file,row=index,colName='NEWCUSTNAME',value=custName)
        write_xlsBycolName_append(file=file,row=index,colName='NEW_IDENID',value=psptId)

        params = {
            "CUSTINFO_PSPT_ID": psptId, # 证件号先写死这个
            "SERIAL_NUMBER": accessNum,
            "PARTY_ID": custId,
            "CUSTINFO_PSPT_ADDRESS": "测试地址测试地址11",
            "ACCESS_NUM": accessNum,
            "CUSTINFO_PSPT_TYPE_CODE": "10000000", #10000000表示身份证
            "svcName": "CustomerCentre.custmgr.IPersonOperateSV.modifyRealNameCheckInInfo",
            "IDEN_ID": IdenId,
            "CUST_ID": accessNum,
            "CUSTINFO_CUST_NAME": custName
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
            flowid = dict_get(d_intf_res, 'INTACT_ID', None)
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
    report_title = u'实名制登记接口自动化测试报告'
    desc = u'接口测试详情：'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath() + report_title + nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2)
        runner.run(mySuitePrefixAdd(ModfiyRealChkInfo,"test_modifyRealChkInfo"))
