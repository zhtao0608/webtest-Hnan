import unittest,os
import ddt,time
from Base import HTMLTestRunnerCNNew
from PageObj.oc.person.ShareCluster import ShareCluster
from selenium.webdriver.common.by import By
from selenium import webdriver
from Base import ReadConfig
from Common.function import join_dictlists
from Base.OperExcel import write_dict_xls,write_xlsBycolName_append
from Base.Mylog import LogManager
# from Base.OracleOper import MyOracle
# from Base.GenTestData import GenTestData
from TestCases.suite import mySuitePrefixAdd
from Common.Assert import PageAssert
from Common.TestDataMgnt import get_TestData,get_testDataFile,get_FuncRow

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('ShareClusterTest').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

# ora = MyOracle()
# # #取共享主卡号码
# # sql_accessNum = "select distinct rownum No ,'' RESULT_INFO ,'' flowid ,t.rel_access_num access_Num,t.rel_subscriber_ins_id ,\
# #     t.subscriber_ins_id 虚用户 \
# #     from uop_file4.um_subscriber_rel t ,uop_file4.um_prod_sta a ,uop_file4.um_share_rel b ,uop_file4.um_offer_06 m \
# #      where t.subscriber_rel_type = 'G4' and a.SUBSCRIBER_INS_ID = t.rel_subscriber_ins_id \
# #     and t.rel_subscriber_role = '1'and t.expire_date > sysdate and t.rel_access_num is not null \
# #     and a.IS_MAIN ='1' and a.PROD_STATUS='0' and a.EXPIRE_DATE> sysdate \
# #     and b.expire_date > sysdate and b.role_code='01' and t.subscriber_ins_id = b.share_id \
# #     and m.SUBSCRIBER_INS_ID = t.rel_subscriber_ins_id and m.EXPIRE_DATE > sysdate and m.IS_MAIN = '1' \
# #     and t.PARTITION_ID = a.PARTITION_ID  and b.partition_id = a.PARTITION_ID \
# #     and m.OFFER_ID in ('399091342','399091343','399091344','399091345','399091346','399091347','399091348','399091349','99091151','399091152','99091153','99091154','99091155','99091165','99091166','399991173','99091282','99091281','99091283','99091284','99091285','99091286','99091287','99091288','99091289','99091290','99091292','99091271','399091272','99091273','99091274','99091275','99091341','637501','399004098','648001','800001','648001')\
# #     and rownum <=3 "
# #
# # #取没有办理共享套餐的号码
# # sql_serialNum = "select t.access_num serial_Num from uop_file4.um_subscriber t ,uop_file4.um_prod_sta a  \
# #         where t.remove_tag = '0' and  a.IS_MAIN ='1' and a.PROD_STATUS='0' and a.EXPIRE_DATE> sysdate  \
# #         and  a.PARTITION_ID = t.partition_id and a.SUBSCRIBER_INS_ID = t.subscriber_ins_id \
# #         and  t.access_num like '188%' and  and t.mgmt_district ='0872' and  t.subscriber_ins_id  in   \
# #         (select m.rel_subscriber_ins_id from uop_file4.um_subscriber_rel m WHERE  m.expire_date > sysdate ) \
# #         and rownum <=3 "
# #
# # accessNumList = ora.select(sql_accessNum) #取主卡号码
# # serialNumList = ora.select(sql_serialNum) # 未订购共享套餐的成员号码
# # add_paras = join_dictlists(accessNumList,serialNumList)
# # logger.info('共享成员新增测试准备数据:{}'.format(add_paras))
# #
# # #================已经办理共享套餐的副卡号码==================================
# # sql_mainAcessNum = "select rownum No ,'' RESULT_INFO ,'' flowid ,t.access_num from uop_file4.um_share_rel t \
# #     where t.share_id in ('7215062751669810') and t.role_code = '01' and t.expire_date > sysdate"
# # sql_serialNum2 = " select  t.access_num serial_num from uop_file4.um_share_rel t \
# #     where t.share_id in ('7215062751669810') and t.role_code = '02' and t.expire_date > sysdate"
# # mainNumList = ora.select(sql_mainAcessNum) #主卡号码
# # serialNumorderedList = ora.select(sql_serialNum2) # 未订购共享套餐的成员号码
# # del_paras = join_dictlists(mainNumList,serialNumorderedList)
# # logger.info('共享成员删除测试准备数据:{}'.format(del_paras))
# #
# # now = time.strftime("%Y%m%d%H%M%S")
# # file_addMeb = ReadConfig.get_data_path() + 'UITest_ShareClusterAddMebTest_%s.xls' % now
# # file_DelMeb = ReadConfig.get_data_path() + 'UITest_ShareClusterDelMebTest_%s.xls' % now
# # #生成xls表,方便后续写入测试结果
# # write_dict_xls(inputData=add_paras, sheetName='新增共享成员测试', outPutFile=file_addMeb)
# # write_dict_xls(inputData=del_paras, sheetName='删除共享成员测试', outPutFile=file_DelMeb)
# #
# # logger.info('写入测试数据到xls.....')
file = get_testDataFile()
add_paras = get_TestData('ShareClusterAddMeb')['params']
del_paras = get_TestData('ShareClusterDelMeb')['params']
cancel_paras = get_TestData('cancelShareCluster')['params']


@ddt.ddt
class ShareClusterTest(unittest.TestCase):
    """[个人业务]4G家庭共享套餐业务测试"""
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(rc.get_ngboss('url'))     #这里可以切换环境，去ngboss_config.ini配置
        self.driver.maximize_window()

    @ddt.data(*add_paras)
    def test01_acceptaddMember(self,dic):
        """新增共享成员"""
        logger.info("开始参数化......")
        # row = int(dic.get('NO'))   #标识行号，后续写入xls使用
        row = get_FuncRow('ShareClusterAddMeb')   #标识行号，后续写入xls使用
        print('开始执行第{}个用例,测试数据：{}'.format(row,dic))
        logger.info('开始执行第{}个用例,测试数据：{}'.format(row,dic))
        AccessNum = dic.get('ACCESS_NUM')  #主卡号码
        serialNum = dic.get('SERIAL_NUM') #副卡号码
        #开始测试
        test = ShareCluster(self.driver)
        title = '4G家庭共享套餐业务新增成员'
        test.add_dochead(title)
        loc_commit = (By.ID, 'CSSUBMIT_BUTTON') #提交按钮
        test.Open_PersonMenu(AccessNum,password='123123',cataMenuId='crm9400',menuId='crm4G10') #登录并进入主卡菜单
        time.sleep(5)
        test.open_ShareClusterFrame() #进入iframe
        # RuleMsg = test.vaild_BusiRule() #业务检查点（进入菜单时校验）
        RuleMsg = PageAssert(self.driver).check_BusiRule(file=file,row=row)  # 业务检查点（进入菜单时校验）
        print('4G家庭共享套餐业务提交前规则:{}'.format(RuleMsg))
        logger.info('4G家庭共享套餐业务提交前规则:{}'.format(RuleMsg))
        self.assertNotIn('业务校验失败',RuleMsg)
        # if '业务校验失败' in RuleMsg:
        #     write_xlsBycolName_append(file=file,row=row,colName='RESULT_INFO',value=RuleMsg,index=0)
        #     test.quit_browse() #业务规则校验失败，直接终止程序
        test.screen_step('进入主卡操作菜单')
        test.add_MebAccessNum(serialNum)
        time.sleep(2)
        test.find_element_click(loc_commit) #点击提交
        time.sleep(10)
        submitMsg = PageAssert(self.driver).assert_SubmitPage()
        logger.info('业务受理信息：{}'.format(submitMsg))
        test.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        test.save_docreport(title)
        time.sleep(10)
        submitMsg = PageAssert(self.driver).assert_submitAfter(file=file,row=row,index=0) #写入结果到xls
        logger.info('业务受理信息：{}'.format(submitMsg))
        test.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        test.save_docreport(title)
        self.assertIn('业务受理成功',submitMsg)
        self.driver.close()

    @ddt.data(*del_paras)
    def test02_acceptDelMember(self,dic):
        '''删除共享成员'''
        logger.info("开始参数化......")
        # row = int(dic.get('NO'))   #标识行号，后续写入xls使用
        row = get_FuncRow('ShareClusterDelMeb')   #标识行号，后续写入xls使用
        print('开始执行第{}个用例,测试数据：{}'.format(row,dic))
        logger.info('开始执行第{}个用例,测试数据：{}'.format(row,dic))
        AccessNum = dic.get('ACCESS_NUM')  #主卡号码
        serialNum = dic.get('SERIAL_NUM') #副卡号码
        #开始测试
        test = ShareCluster(self.driver)
        title = '4G家庭共享套餐业务删除成员'
        test.add_dochead(title)
        loc_commit = (By.ID, 'CSSUBMIT_BUTTON') #提交按钮
        test.Open_PersonMenu(AccessNum,password='123123',cataMenuId='crm9400',menuId='crm4G10') #登录并进入主卡菜单
        time.sleep(5)
        test.open_ShareClusterFrame() #进入iframe
        RuleMsg = test.vaild_BusiRule() #业务检查点（进入菜单时校验）
        print('4G家庭共享套餐业务提交前规则:{}'.format(RuleMsg))
        logger.info('4G家庭共享套餐业务提交前规则:{}'.format(RuleMsg))
        if '业务校验失败' in RuleMsg:
            write_xlsBycolName_append(file=file,row=row,colName='RESULT_INFO',value=RuleMsg,index=0)
            test.quit_browse() #业务规则校验失败，直接终止程序
        test.screen_step('进入主卡操作菜单')
        test.del_MebAccessNum(serialNum)
        time.sleep(2)
        test.find_element_click(loc_commit) #点击提交
        time.sleep(10)
        submitMsg = PageAssert(self.driver).assert_SubmitPage()
        logger.info('业务受理信息：{}'.format(submitMsg))
        test.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        test.save_docreport(title)
        logger.info('写入测试结果到xls.....')
        PageAssert(self.driver).assert_submitAfter(file=file,row=row,index=0) #写入结果到xls
        self.driver.close()

    @ddt.data(*cancel_paras)
    def test03_acceptcancelShare(self,dic):   # 只取主卡即可
        """取消群组"""
        logger.info("开始参数化......")
        # row = int(dic.get('NO'))   #标识行号，后续写入xls使用
        row = get_FuncRow('cancelShareCluster')
        print('开始执行第{}个用例,测试数据：{}'.format(row,dic))
        logger.info('开始执行第{}个用例,测试数据：{}'.format(row,dic))
        AccessNum = dic.get('ACCESS_NUM')  #主卡号码
        #开始测试
        test = ShareCluster(self.driver)
        title = '4G家庭共享套餐业务取消群组'
        test.add_dochead(title)
        loc_commit = (By.ID, 'CSSUBMIT_BUTTON') #提交按钮
        test.Open_PersonMenu(AccessNum,password='123123',cataMenuId='crm9400',menuId='crm4G10') #登录并进入主卡菜单
        time.sleep(5)
        test.open_ShareClusterFrame() #进入iframe
        RuleMsg = test.vaild_BusiRule() #业务检查点（进入菜单时校验）
        print('4G家庭共享套餐业务提交前规则:{}'.format(RuleMsg))
        logger.info('4G家庭共享套餐业务提交前规则:{}'.format(RuleMsg))
        if '业务校验失败' in RuleMsg:
            write_xlsBycolName_append(file=file,row=row,colName='RESULT_INFO',value=RuleMsg,index=0)
            test.quit_browse() #业务规则校验失败，直接终止程序
        test.screen_step('进入主卡操作菜单')
        test.cancel_ShareCluster() #点击取消群组按钮
        Msg = PageAssert(self.driver).assert_WarnPage()
        print('取消共享群组时，提醒信息:{}'.format(Msg))
        logger.info('取消共享群组时，提醒信息:{}'.format(Msg))
        time.sleep(2)
        test.find_element_click(loc_commit) #点击提交
        time.sleep(10)
        submitMsg = PageAssert(self.driver).assert_SubmitPage()
        logger.info('业务受理信息：{}'.format(submitMsg))
        test.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        test.save_docreport(title)
        logger.info('写入测试结果到xls.....')
        PageAssert(self.driver).assert_submitAfter(file=file,row=row,index=0) #写入结果到xls
        self.driver.close()



if __name__ == '__main__':
    report_title = u'4G家庭共享套餐业务测试'
    desc = u'4G家庭共享套餐测试详情：'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath() + report_title +  nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2,retry=1)
        runner.run(mySuitePrefixAdd(ShareClusterTest,"test02_acceptDelMember"))