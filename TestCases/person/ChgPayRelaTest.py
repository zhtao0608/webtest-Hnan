import unittest,os
import ddt,time
from Base import HTMLTestRunnerCNNew
from selenium.webdriver.common.by import By
from selenium import webdriver
from Base import ReadConfig
from Base.OperExcel import write_dict_xls,write_xlsBycolName_append
from PageObj.oc.person.ChangePayRela import ChangePayRelaNor
from Base.Mylog import LogManager
from Base.OracleOper import MyOracle
from TestCases.suite import mySuitePrefixAdd
from Common.Assert import PageAssert
from Common.TestDataMgnt import get_TestData,get_testDataFile

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('ChangeProdStatusTest').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

# ora = MyOracle()
# '''
# operCode == '1' 分账
# operCode == '2' 合账
# '''
# #分账
# sql_sep = "select rownum No ,'' result_info ,'' flowid,T.ACCESS_NUM ,'1' Oper_code from uop_file4.um_subscriber t ,uop_file4.um_prod_sta a \
# where t.remove_tag = '0' and  a.IS_MAIN ='1' and a.PROD_STATUS='0' and a.EXPIRE_DATE> sysdate \
# and  a.PARTITION_ID = t.partition_id and a.SUBSCRIBER_INS_ID = t.subscriber_ins_id \
# and  t.access_num LIKE '187%'  and t.mgmt_district ='0872' \
# and rownum <=3 "
#
# # 合帐
# sql_merg =  "select rownum No ,'' result_info ,'' flowid,T.ACCESS_NUM ,'2' Oper_code from uop_file4.um_subscriber t ,uop_file4.um_prod_sta a \
# where t.remove_tag = '0' and  a.IS_MAIN ='1' and a.PROD_STATUS='0' and a.EXPIRE_DATE> sysdate \
# and  a.PARTITION_ID = t.partition_id and a.SUBSCRIBER_INS_ID = t.subscriber_ins_id \
# and  t.access_num LIKE '187%'  and t.mgmt_district ='0872' \
# and rownum <=3 "

# paras_sep= ora.select(sql_sep) #  分账
# paras_merg= ora.select(sql_merg) #  分账
#
# paras = paras_sep
# # paras = paras_merg
file = get_testDataFile()
params = []
# 分账
paras_sep = get_TestData(FuncCode='ChgPayRelaSeprate')['params']
logger.info('普通付费关系变更-分账测试准备数据:{}'.format(paras_sep))
params.extend(paras_sep)
# 合帐
paras_merge = get_TestData(FuncCode='ChgPayRelaMerge')['params']
logger.info('普通付费关系变更-合帐测试准备数据:{}'.format(paras_merge))
params.extend(paras_merge)
params = params
print('======合并后=====', params)
# now = time.strftime("%Y%m%d%H%M%S")
# file = ReadConfig.get_data_path() + 'UITest_ChgPayRelaTest_%s.xls' % now
# #生成xls表,方便后续写入测试结果
# write_dict_xls(inputData=paras, sheetName='普通付费关系变更', outPutFile=file)
# logger.info('写入测试数据到xls.....')

@ddt.ddt
class ChgPayRelaTest(unittest.TestCase):
    '''普通普通关系变更'''
    @classmethod
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(rc.get_ngboss('url'))     #这里可以切换环境，去ngboss_config.ini配置
        self.driver.maximize_window()
        #self.driver.implicitly_wait(40)    #暂时设置40s，隐式等待

    @ddt.data(*params)
    def test_accept_chgPayRela(self,dic):
        """普通付费关系变更受理"""
        logger.info("开始参数化......")
        print('开始执行用例,测试数据：{}'.format(dic))
        accessNum = str(dic.get('ACCESS_NUM'))
        operCode = str(dic.get('OPER_CODE'))  #SQL读入
        logger.info('开始执行用例，测试数据：{}'.format(dic))
        ####测试用例步骤
        test = ChangePayRelaNor(self.driver)
        title = '普通付费关系变更测试记录'
        loc_separater = (By.XPATH,'//*[@id="change_account_type_span"]/span[1]') #分账
        loc_remark = (By.ID,'remarks') #备注
        loc_commit = (By.ID, 'CSSUBMIT_BUTTON') #提交按钮
        test.add_dochead(title)
        test.Open_PersonMenu(accessNum,password='123123',cataMenuId='crm9200',menuId='crm9257') #登录并进入普通付费关系变更菜单
        time.sleep(2)
        test.open_ChangePayRelaNorFrame() #进入iframe
        RuleMsg = test.vaild_BusiRule() #验证号码办理规则
        logger.info('普通付费关系变更规则验证结果:{}'.format(RuleMsg))
        time.sleep(3)
        #业务办理
        if operCode == '1' :  #分账
            row = get_TestData('ChgPayRelaSeprate')['FuncRow']
            logger.info('选择的是分账操作')
            test.find_element_click(loc_separater)
        elif operCode == '2': #合账
            logger.info('选择的是合帐操作')
            row = get_TestData('ChgPayRelaMerge')['FuncRow']
            SerialNum = str(dic.get('SERIAL_NUM'))
            test.set_mergeSerialNum(SerialNum)
            vaildMsg = PageAssert(self.driver).assert_error()
            logger.info('付费号码校验结果：{}'.format(vaildMsg))
            if '业务校验失败' in vaildMsg:
                test.quit_browse()  # 如果校验失败，直接跳出
        else:
            print('OperCode只能传入1或者2，当前传入：{}'.format(operCode))
            test.quit_browse()
        test.sendkey(loc_remark,'AutoTest')
        time.sleep(2)
        test.find_element_click(loc_commit) #点击提交
        time.sleep(10)
        submitMsg = PageAssert(self.driver).assert_SubmitPage()
        logger.info('业务受理信息：{}'.format(submitMsg))
        test.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        test.save_docreport(title)
        PageAssert(self.driver).write_testResult(file=file,row=row,index=0) #写入结果到xls
        self.driver.close()

    def tearDown(self):
        print('测试结束，关闭浏览器器!')

if __name__ == '__main__':
    report_title = u'普通付费关系变更自动化测试报告'
    desc = u'普通付费关系测试详情：'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath() + report_title + nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2)
        runner.run(mySuitePrefixAdd(ChgPayRelaTest,"test_accept_chgPayRela"))
