import unittest,ddt
import time
import requests
import json
from Base import HTMLTestRunnerCNNew
from Base import ReadConfig
from Base.Mylog import LogManager
from Common.function import dict_get
from Base.OracleOper import MyOracle
from Base.OperExcel import write_dict_xls,write_xlsBycolName_append
from TestCases.suite import mySuitePrefixAdd

logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

rc = ReadConfig.ReadConfig("ngboss_config.ini")
h = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36',
    "Connection": "keep - alive",
    "Referer": rc.get_ngboss('url')
}
lo_param = {"LOGIN_MODE": "BOSS", "STAFF_ID": "TESTKM06", "IS_XACTIVE": "false", "BROWSER_VERSION": "IE-11",
        "PASSWORD": "e3937dc80f9bb5ab17cc016cdc612b7d", "LOGIN_FLAG": "1"}

now = time.strftime("%Y%m%d%H%M%S")
file = ReadConfig.get_data_path() + 'ApiTest_ChgProdstatus_%s.xls' % now
ora = MyOracle()
#取10个测试号码停机操作：busicode =131表示停机操作
'''busiCode: 传入停开机业务受理类型
        126 局方开机,136 局方停机
        132 挂失
        131 报停,133 报开
        138 特殊停机
        496 担保开机 497 紧急开机
'''
sql = "select rownum No ,'' flowid , '' result_info ,t.access_num , '133' busicode \
    from  uop_file4.um_subscriber t \
    where t.access_num in ('18887253716','18887269718','18887269711','18887267264') and t.remove_tag = '0' and rownum <=10"
paras = ora.select(sql)
#生成xls表,方便后续写入测试结果
write_dict_xls(inputData=paras, sheetName='停开机业务受理', outPutFile=file)
logger.info('写入测试数据到xls.....')

##数据驱动paramunittest：
# interfaceList_xls = get_exceldata(ReadConfig.data_path+ 'testdata.xls',0)
# print(interfaceList_xls)
# @paramunittest.parametrized(*interfaceList_xls)


@ddt.ddt
class TestIntf(unittest.TestCase):
    def setUp(self):
        self.file = file
        self.headers = h
        self.session = requests.session()
        logger.info("构建登录请求.....")
        logger.info("登录地址："+rc.get_interface_url("url_login"))
        self.session.post(url=rc.get_interface_url("url_login"), headers=h, data=lo_param)
        logger.info("初始化主页，url地址："+rc.get_interface_url("url_login"))
        self.session.get(url=rc.get_interface_url("url_init"), headers=h)

    @ddt.data(*paras)
    def test_IntfChgprodstatus(self,dic):
        '''【接口】停开机业务受理测试'''
        logger.info("开始参数化......")
        index = int(dic.get('NO'))
        accessNum = str(dic.get('ACCESS_NUM'))
        logger.info("测试号码:"+accessNum)
        busicode = dic.get('BUSICODE')
        logger.info("停开机业务类型:"+ busicode)
        params = {"svcName": 'OrderCentre.person.IChangeProdStaOperateSV.changeProdStatus', "ACCESS_NUM": accessNum, "BUSI_ITEM_CODE": busicode}
        logger.info("params参数化以后的接口入参:"+json.dumps(params))
        print("params参数化以后的接口入参:"+json.dumps(params))
        # logger.info("开始接口测试开始，接口名为"+svcname +" 接口参数是：" + json.dumps(params))
        logger.info('开始执行第{}个用例,接口入参:{}'.format(index,dic))

        logger.info("开始构建请求......"+"\n")
        intf_url = rc.get_interface_url("url_interface")
        logger.info("接口测试地址：" + intf_url )
        intf_res = self.session.post(url=intf_url,headers = h,data = params)
        logger.info("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        d_intf_res = json.loads(intf_res.content.decode(encoding='utf-8'))
        x_resultcode = dict_get(d_intf_res, 'x_resultcode', None)
        if x_resultcode == '0':
            flowid = dict_get(d_intf_res, 'flowId', None)
            access_num = dict_get(d_intf_res, 'ACCESS_NUM', None)
            x_resultinfo = dict_get(d_intf_res, 'X_RESULTINFO', None)
            logger.info("接口处理成功，受理号码为："+ access_num +"  订单交互流水号："+flowid)
            print("接口处理成功，受理号码为："+ access_num +"  订单交互流水号："+flowid)
            logger.info("开始写入xls数据......")
            write_xlsBycolName_append(file=self.file,row=index,colName='RESULT_INFO',value=x_resultinfo)
            write_xlsBycolName_append(file=self.file,row=index,colName='FLOWID',value=flowid)
            logger.info("测试结果写入xls成功......")
        else:
            x_resultinfo = dict_get(d_intf_res, 'x_resultinfo', None)
            logger.info("接口调用失败，错误信息："+x_resultinfo)
            print("接口处理错误信息：" + x_resultinfo)
            logger.info("开始写入xls数据......")
            write_xlsBycolName_append(file=self.file,row=index,colName='RESULT_INFO',value=x_resultinfo)
            logger.info("测试结果写入xls成功......")
        self.assertEqual(x_resultcode,'0')

if __name__ == '__main__':
    report_title = u'停开机受理接口自动化测试报告'
    desc = u'停开机受理接口测试详情'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath()  + report_title + nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2)
        runner.run(mySuitePrefixAdd(TestIntf,"test_IntfChgprodstatus"))
