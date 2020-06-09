import unittest,os
import ddt,time
from Base import HTMLTestRunnerCNNew
from PageObj.oc.person.ChangeProdStatus import ChangeProdStatus
from selenium.webdriver.common.by import By
from selenium import webdriver
from Base import ReadConfig
from Common.function import join_dictlists
from Base.OperExcel import write_dict_xls,write_xlsBycolName_append
from Base.Mylog import LogManager
from Base.OracleOper import MyOracle
from TestCases.suite import mySuitePrefixAdd
from Common.Assert import PageAssert
from Common.TestDataMgnt import get_TestData

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('ChangeProdStatusTest').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

# ora = MyOracle()
#取停开机业务受理号码
'''
:param busiCode: 传入停开机业务受理类型
126 局方开机,136 局方停机
132 挂失
131 报停,133 报开
138 特殊停机
496 担保开机 497 紧急开机
'''
params = []
file = get_TestData('SubscriberStop')['filename']
# 报停
paras_stop = get_TestData(FuncCode='SubscriberStop')['params']
logger.info('停开机业务受理-报停测试准备数据:{}'.format(paras_stop))
params.extend(paras_stop)
# 合帐
paras_open = get_TestData(FuncCode='SubscriberOpen')['params']
logger.info('停开机业务受理-报停测试准备数据:{}'.format(paras_open))
params.extend(paras_open)
print('======合并后=====', params)


# sql_StopMobile = "select rownum No ,'' result_info ,'' flowid,T.ACCESS_NUM,'131' BUSI_CODE from uop_file4.um_subscriber t ,uop_file4.um_prod_sta a \
# where t.remove_tag = '0' and  a.IS_MAIN ='1' and a.PROD_STATUS='0' and a.EXPIRE_DATE> sysdate \
# and  a.PARTITION_ID = t.partition_id and a.SUBSCRIBER_INS_ID = t.subscriber_ins_id \
# and  t.access_num LIKE '187%'  and t.mgmt_district ='0872' \
# and rownum <=3 "
#
# sql_OpenMobile = "select rownum No ,'' result_info ,'' flowid,T.ACCESS_NUM,'133' BUSI_CODE,a.PROD_STATUS from uop_file4.um_subscriber t ,uop_file4.um_prod_sta a \
#     where t.remove_tag = '0' and  a.IS_MAIN ='1' and a.PROD_STATUS = '1' and a.EXPIRE_DATE> sysdate \
#     and  a.PARTITION_ID = t.partition_id and a.SUBSCRIBER_INS_ID = t.subscriber_ins_id \
#     and  t.access_num LIKE '187%'  and t.mgmt_district ='0872' \
#     and rownum <=3"
#
# paras_stopMobile = ora.select(sql_StopMobile) # 报停
# paras_OpenMobile = ora.select(sql_OpenMobile) # 报开
#
# paras = paras_OpenMobile
#
# logger.info('停开机测试准备数据:{}'.format(paras))
# now = time.strftime("%Y%m%d%H%M%S")
# file = ReadConfig.get_data_path() + 'UITest_ChangeProdstsTest_%s.xls' % now
# #生成xls表,方便后续写入测试结果
# write_dict_xls(inputData=paras, sheetName='停开机', outPutFile=file)
# logger.info('写入测试数据到xls.....')

@ddt.ddt
class ChangeProdStsTest(unittest.TestCase):
    """[个人业务]停开机业务受理测试"""
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(rc.get_ngboss('url'))     #这里可以切换环境，去ngboss_config.ini配置
        self.driver.maximize_window()
        #self.driver.implicitly_wait(40)    #暂时设置40s，隐式等待

    @ddt.data(*params)
    def test_acceptStopOrOpen(self,dic):
        """停开机业务受理"""
        logger.info("开始参数化......")
        # row = int(dic.get('NO'))   #标识行号，后续写入xls使用
        print('开始执行用例,测试数据：{}'.format(dic))
        accessNum = str(dic.get('ACCESS_NUM'))
        busicode = str(dic.get('BUSI_CODE'))  #SQL读入
        ####测试用例步骤
        test = ChangeProdStatus(self.driver)
        title = '停开机业务受理测试'
        test.add_dochead(title)
        test.Open_PersonMenu(accessNum,password='123123',cataMenuId='crm9200',menuId='crm9247') #登录并进入停开机业务受理菜单
        test.open_ChangeProdStatusFrame()
        test.screen_step('进入菜单，选择停开机业务类型')
        test.select_BusiType(busicode) # 选择停开机业务受理类型 【暂时在代码里面写死，根据需要修改】
        loc_submit = (By.ID,'CSSUBMIT_BUTTON')
        RuleMsg = test.vaild_BusiRule() #校验号码是否满足停机受理规则
        if '业务校验失败' in RuleMsg:
            print('业务规则校验结果：{}'.format(RuleMsg))
            logger.info('业务规则校验结果：{}'.format(RuleMsg))
            test.screen_step('业务规则校验')
            if busicode == '131': #报停
                write_xlsBycolName_append(file=file,row=get_TestData('SubscriberStop')['FuncRow'],colName='RESULT_INFO',value=RuleMsg)
                test.quit_browse()
            elif busicode == '133': #报开
                write_xlsBycolName_append(file=file,row=get_TestData('SubscriberOpen')['FuncRow'],colName='RESULT_INFO',value=RuleMsg)
                test.quit_browse()
        else:
            print('业务规则校验通过')
            test.find_element_click(loc_submit)
            submitMsg = PageAssert(self.driver).assert_SubmitPage()
            logger.info('业务受理信息：{}'.format(submitMsg))
            test.screen_step('点击提交,受理信息：{}'.format(submitMsg))
            test.save_docreport(title)
            logger.info('写入测试结果到xls.....')
            if busicode == '131': #报停
                PageAssert(self.driver).write_testResult(file=file, row=get_TestData('SubscriberStop')['FuncRow'], index=0)  # 写入结果到xls
            elif busicode == '133':  # 报开
                PageAssert(self.driver).write_testResult(file=file, row=get_TestData('SubscriberOpen')['FuncRow'], index=0)  # 写入结果到xls
            self.driver.close()

    def tearDown(self):
        print('测试结束，关闭浏览器器!')
        self.driver.close()

if __name__ == '__main__':
    report_title = u'停开机业务自动化测试报告'
    desc = u'停开机测试详情：'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath() + report_title + nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2)
        runner.run(mySuitePrefixAdd(ChangeProdStsTest,"test_acceptStopOrOpen"))