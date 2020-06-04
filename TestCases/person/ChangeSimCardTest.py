import unittest,os
import ddt,time
from Common import HTMLTestRunnerCNNew
from PageObj.oc.person.ChangeSimCard import ChangeSimCard
from selenium.webdriver.common.by import By
from PageObj.oc.person.PersonBase import PersonBase
from selenium import webdriver
from Common import ReadConfig
from Common.function import join_dictlists
from Common.OperExcel import write_dict_xls,write_xlsBycolName_append
from Common.Mylog import LogManager
from Base.OracleOper import MyOracle
from Base.GenTestData import GenTestData
from TestCases.suite import mySuitePrefixAdd
from Common.Assert import PageAssert

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('ChangeSimCardTest').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

ora = MyOracle()
#取换卡号码
sql_accessNum = "select rownum No ,'' flowid , '' result_info ,t.access_number,t.icc_id oldSimID  from uop_res.res_num_used t  \
                where t.res_state = '4'  and t.access_number like '187%' and t.mgmt_district = '0872'  \
                and t.hlr_seg = '8708720' and rownum<=3 "

sql_newSim = "select m.icc_id NewSimId from uop_res.res_sim_origin m  \
    where  m.res_state = '1' and m.mgmt_district ='0872' and m.access_number is null and m.hlr_seg = '8708720'  \
    and rownum <=3 "

accessNumList = ora.select(sql_accessNum)
newSimList = ora.select(sql_newSim)
paras = join_dictlists(accessNumList,newSimList)
logger.info('测试准备数据:{}'.format(paras))
now = time.strftime("%Y%m%d%H%M%S")
file = ReadConfig.get_data_path() + 'UITest_ChangeSimCardTest_%s.xls' % now
#生成xls表,方便后续写入测试结果
write_dict_xls(inputData=paras, sheetName='换卡测试', outPutFile=file)
logger.info('写入测试数据到xls.....')

@ddt.ddt
class ChangeSimCardTest(unittest.TestCase):
    """[个人业务]销户测试"""
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(rc.get_ngboss('url'))     #这里可以切换环境，去ngboss_config.ini配置
        self.driver.maximize_window()
        #self.driver.implicitly_wait(40)    #暂时设置40s，隐式等待

    @ddt.data(*paras)
    def test_chgSimCard(self,dic):
        """换卡"""
        logger.info("开始参数化......")
        row = int(dic.get('NO'))   #标识行号，后续写入xls使用
        print('开始执行第{}个用例,测试数据：{}'.format(row,dic))
        accessNum = str(dic.get('ACCESS_NUMBER'))
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
        RuleMsg = test.vaild_BusiRule() #业务检查点（进入菜单时校验）
        print('换卡业务提交前规则:{}'.format(RuleMsg))
        logger.info('换卡业务提交前规则:{}'.format(RuleMsg))
        if '业务校验失败' in RuleMsg:
            write_xlsBycolName_append(file=file,row=row,colName='RESULT_INFO',value=RuleMsg,index=0)
            test.quit_browse() #业务规则校验失败，直接终止程序
        test.screen_step('进入换卡菜单')
        test.check_CustInfoBypwd() #客户名称
        Vaild_custMsg = test.vaild_Customer()
        print('客户验证信息:{}'.format(Vaild_custMsg))
        logger.info('客户验证信息:{}'.format(Vaild_custMsg))
        time.sleep(2)
        test.Input_NewSimId(simId)
        test.sendkey(text_remark,'AntoTest') #填写备注信息
        test.find_element_click(loc_commit) #点击提交
        time.sleep(10)
        submitMsg = PageAssert(self.driver).assert_SubmitPage()
        logger.info('业务受理信息：{}'.format(submitMsg))
        test.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        test.save_docreport(title)
        logger.info('写入测试结果到xls.....')
        PageAssert(self.driver).write_testResult(file=file,row=row,index=0) #写入结果到xls
        self.driver.close()

if __name__ == '__main__':
    report_title = u'换卡自动化测试报告'
    desc = u'换卡销户测试详情：'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath() + report_title +  nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2,retry=1)
        runner.run(mySuitePrefixAdd(ChangeSimCardTest,"test_chgSimCard"))