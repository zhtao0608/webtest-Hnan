import unittest,HTMLTestRunnerCN,ddt
import time
import requests
import json
from Common import ReadConfig
from Common.Mylog import LogManager
from Common.OperExcel import get_exceldata,write_excel_append
from Common.function import dict_get

rc = ReadConfig.ReadConfig("ngboss_config.ini")
h = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36',
    "Connection": "keep - alive",
    "Referer": rc.get_ngboss('url')
}

lo_param = {"LOGIN_MODE": "BOSS", "STAFF_ID": "TESTKM06", "IS_XACTIVE": "false", "BROWSER_VERSION": "IE-11",
        "PASSWORD": "e3937dc80f9bb5ab17cc016cdc612b7d", "LOGIN_FLAG": "1"}

file = ReadConfig.data_path + 'IntfTest_OfferOper.xls'
paras = get_exceldata(file,0)
logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
print(type(paras))
print(paras)

@ddt.ddt
class TestofferOper(unittest.TestCase):
    def setUp(self):
        self.file = file
        self.headers = h
        self.session = requests.session()
        self.session.post(url=rc.get_interface_url("url_login"), headers=h, data=lo_param)
        self.session.get(url=rc.get_interface_url("url_init"), headers=h)
        # logger.info("init以后返回的信息：" + init_resp.content.decode('utf-8'))
        print("\n")

    @ddt.data(*paras)
    def test_ChgMainOffer(self,dic):

        logger.info("开始参数化......")
        index = int(dic.get('No'))
        # # print(svcname)
        accessNum = str(dic.get('accessNum'))
        logger.info("测试号码:"+accessNum)
        busicode = str(dic.get('busicode'))
        mainoffer = str(dic.get('mainoffer'))
        action = str(dic.get('action'))
        suboffer01 = str(dic.get('suboffer01'))
        suboffer02 = str(dic.get('suboffer02'))
        suboffer03 = str(dic.get('suboffer03'))
        suboffer04 = str(dic.get('suboffer04'))
        suboffers_list = dic.get('subOfferList')
        # suboffers_list = json.loads(dic.get('subOfferList'))
        print(type(suboffers_list))
        print(suboffers_list)

        params = {
                    "LOGIN_TYPE_CODE": "P",
                    "SUBMIT_TYPE": "0",
                    "REMARKS": "test_by_APIAuto",
                    "BUSI_ITEM_CODE": busicode,    #业务类型关键参数，需要参数化busicode
                    "OFFER_ID": mainoffer,      #主套餐需要参数化，mainoffer
                    "ACCESS_NUM": accessNum, #需要参数化 accessNum
                    "svcName": "OrderCentre.person.IOffersOrderSV.offersOper"
                }

        mainoffer = {"OFFERS": json.dumps([{
                            "ENABLE_MODE": "4",
                            "OFFER_ID": mainoffer, ##主套餐ID
                            "ACTION": action, #0 -订购，1-退订
                            "OFFER_TYPE": "00"
                        },
                        {
                            "OFFER_ID": suboffer01, #必选产品
                            "ACTION": "0"
                        }
                    ])
            }

        suboffers = { "OFFER_LIST": json.dumps([{
                                    "OFFER_ID": suboffer02, ##必选产品（移动通讯商品）,subOffer1
                                    "ACTION": "0",
                                    "ROLE_ID": "999999999"
                                },
                                {
                                    "OFFER_ID": suboffer03, ##语音subOffer1，这个基本可以取固定值，应用主套餐变更
                                    "ACTION": "0",
                                    "ROLE_ID": "999999999"
                                },
                                {
                                    "OFFER_ID": suboffer04, #
                                    "ACTION": "0",
                                    "ROLE_ID": "999999999"
                                }
                            ])}
        # suboffers = { "OFFER_LIST":json.dumps(suboffers_list)}
        # suboffers = json.loads(suboffers)
        print(type(suboffers))

        logger.info("开始拼装产品变更参数.......")
        logger.info("参数加入mainOffer,主套餐是：" + json.dumps(mainoffer))
        print("参数加入mainOffer,主套餐是：" + json.dumps(mainoffer))
        params.update(mainoffer)
        logger.info("参数加入suboffers，子商品列表:" + json.dumps(suboffers))
        print("参数加入suboffers，子商品列表:" + json.dumps(suboffers))
        params.update(suboffers)

        logger.info("接口名：" + params['svcName'])
        logger.info("拼装商品订购入参完成，接口完整入参：" + json.dumps(params))
        print("拼装商品订购入参完成，接口完整入参：" + json.dumps(params))
        logger.info("接口名：" + params['svcName'])

        logger.info("开始构建请求......"+"\n")
        intf_url = rc.get_interface_url("url_interface")
        logger.info("接口测试地址：" + intf_url )
        intf_res = self.session.post(url=intf_url,headers = h, data = params)
        logger.info("接口完整返回信息：" + intf_res.content.decode(encoding='utf-8'))
        # print(intf_res.content.decode(encoding='utf-8'))
        logger.info("处理接口返回数据....")
        d_intf_res = json.loads(intf_res.content.decode(encoding='utf-8'))
        x_resultcode = dict_get(d_intf_res, 'x_resultcode', None)
        x_resultinfo = dict_get(d_intf_res, 'x_resultinfo', None)
        if x_resultcode == '0':
            flowid = dict_get(d_intf_res, 'flowId', None)
            access_num = dict_get(d_intf_res, 'ACCESS_NUM', None)
            logger.info("接口处理成功，受理号码为：" + access_num + "  订单交互流水号：" + flowid)
            print("接口处理成功，受理号码为：" + access_num + "  订单交互流水号：" + flowid)
            logger.info("开始写入xls数据......")
            write_excel_append(self.file, index, 3, x_resultinfo)
            write_excel_append(self.file, index, 2, flowid)
            logger.info("测试结果写入xls成功......")
        else:
            logger.info("商品订购失败，错误信息：" + x_resultinfo)
            print("接口处理错误信息：" + x_resultinfo)
            logger.info("开始写入xls数据......")
            write_excel_append(self.file, index, 3, x_resultinfo)
            logger.info("测试结果写入xls成功......")

def mySuitePrefixAdd(MyClass,cases):
    '''
    根据前缀添加测试用例-可用于ddt数据用例
    :param MyClass:
    :param cases:
    :return:
    '''
    test_list = []
    testdict = MyClass.__dict__
    if isinstance(cases,str):
        cases = [cases]
    for case in cases:
        tmp_cases = filter(lambda cs:cs.startswith(case) and callable(getattr(MyClass,cs)),testdict)
        for tmp_case in tmp_cases:
            test_list.append(MyClass(tmp_case))
    suite = unittest.TestSuite()
    suite.addTests(test_list)
    return suite

if __name__ == '__main__':
    # test = TestofferOper()
    # test.TestofferOper()

    report_title = u'接口自动化测试报告'
    desc = u'接口测试详情：'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    + report_title + nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCN.HTMLTestReportCN(stream=fp, title=report_title, description=desc,verbosity=2)
        runner.run(mySuitePrefixAdd(TestofferOper,"test_ChgMainOffer"))
