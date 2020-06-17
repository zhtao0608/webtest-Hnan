import unittest,os
import ddt,time
from Base import HTMLTestRunnerCNNew
from PageObj.oc.person.ChangeSimCard import ChangeSimCard
from selenium.webdriver.common.by import By
from PageObj.oc.person.PersonBase import PersonBase
from selenium import webdriver
from Base import ReadConfig
from Common.function import join_dictlists
from Base.OperExcel import write_dict_xls,write_xlsBycolName_append
from Base.Mylog import LogManager
from Base.OracleOper import MyOracle
from Base.GenTestData import GenTestData
from TestCases.suite import mySuitePrefixAdd
from Common.Assert import PageAssert
from Common.TestDataMgnt import get_testDataFile,get_TestData,get_FuncRow


os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('ChangeSimCardTest').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

# ora = MyOracle()
# #取换卡号码
# sql_accessNum = "select rownum No ,'' flowid , '' result_info ,t.access_number,t.icc_id oldSimID  from uop_res.res_num_used t  \
#                 where t.res_state = '4'  and t.access_number like '187%' and t.mgmt_district = '0872'  \
#                 and t.hlr_seg = '8708720' and rownum<=3 "
#
# sql_newSim = "select m.icc_id NewSimId from uop_res.res_sim_origin m  \
#     where  m.res_state = '1' and m.mgmt_district ='0872' and m.access_number is null and m.hlr_seg = '8708720'  \
#     and rownum <=3 "
#
# accessNumList = ora.select(sql_accessNum)
# newSimList = ora.select(sql_newSim)
# paras = join_dictlists(accessNumList,newSimList)
# logger.info('测试准备数据:{}'.format(paras))
# now = time.strftime("%Y%m%d%H%M%S")
# file = ReadConfig.get_data_path() + 'UITest_ChangeSimCardTest_%s.xls' % now
# #生成xls表,方便后续写入测试结果
# write_dict_xls(inputData=paras, sheetName='换卡测试', outPutFile=file)
# logger.info('写入测试数据到xls.....')

paras = get_TestData(FuncCode='ChangeSimCardTest')['params']
file = get_TestData(FuncCode='ChangeSimCardTest')['filename']
row = get_TestData(FuncCode='ChangeSimCardTest')['FuncRow']

@ddt.ddt
class ChangeSimCardTest(unittest.TestCase):
    """[个人业务]换卡测试"""
    @classmethod
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(rc.get_ngboss('url'))     #这里可以切换环境，去ngboss_config.ini配置
        self.driver.maximize_window()
        #self.driver.implicitly_wait(40)    #暂时设置40s，隐式等待

    @ddt.data(*paras)
    def test_chgSimCard(self,dic):
        """换卡"""
        logger.info("开始参数化......")
        # row = int(dic.get('NO'))   #标识行号，后续写入xls使用
        print('开始执行用例,测试数据：{}'.format(dic))
        accessNum = str(dic.get('ACCESS_NUMBER'))
        custName = dic.get('CUST_NAME')
        IdenNr = dic.get('IDENNR')
        simId = str(dic.get('NEWSIMID')) #SIM卡号参数化
        logger.info('开始执行第{}个用例,测试数据：{}'.format(row,dic))
        ####测试用例步骤
        test = ChangeSimCard(self.driver)
        title = '换卡业务受理测试记录'
        test.add_dochead(title)
        text_remark = (By.ID,'REMARKS')  #备注
        loc_commit = (By.ID, 'CSSUBMIT_BUTTON') #提交按钮
        PersonBase(self.driver).Open_PersonMenu(accessNum,password='123123',cataMenuId='crm9400',menuId='crm9431') #登录并进入换卡菜单
        time.sleep(5)
        test.open_ChangSimCardFrame() #进入iframe
        # RuleMsg = test.vaild_BusiRule() #业务检查点（进入菜单时校验）
        RuleMsg = PageAssert(self.driver).check_BusiRule(file,row) #业务检查点（进入菜单时校验）
        print('换卡业务提交前规则:{}'.format(RuleMsg))
        logger.info('换卡业务提交前规则:{}'.format(RuleMsg))
        self.assertNotIn('业务校验失败',RuleMsg)
        test.screen_step('进入换卡菜单')
        test.check_CustInfoByIdcard(custName,IdenNr) #客户名称
        Vaild_custMsg = PageAssert(self.driver).assert_WadePage()
        print('客户验证信息:{}'.format(Vaild_custMsg))
        logger.info('客户验证信息:{}'.format(Vaild_custMsg))
        self.assertNotIn('警告信息',Vaild_custMsg)
        time.sleep(2)
        test.Input_NewSimId(simId)
        test.sendkey(text_remark,'AntoTest') #填写备注信息
        test.find_element_click(loc_commit) #点击提交
        time.sleep(10)
        submitMsg = PageAssert(self.driver).assert_submitAfter(file=file,row=row,index=0) #写入结果到xls
        logger.info('业务受理信息：{}'.format(submitMsg))
        test.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        test.save_docreport(title)
        self.assertIn('业务受理成功',submitMsg)

    def tearDown(self):
        print('测试结束，关闭浏览器器!')
        self.driver.close()


if __name__ == '__main__':
    report_title = u'换卡自动化测试报告'
    desc = u'换卡测试详情：'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath() + report_title +  nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2)
        runner.run(mySuitePrefixAdd(ChangeSimCardTest,"test_chgSimCard"))