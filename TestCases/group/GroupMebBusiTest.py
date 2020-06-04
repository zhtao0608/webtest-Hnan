import unittest,os
from Common import HTMLTestRunnerCNNew
import time,ddt
from PageObj.oc.group.GrpMebBusiOper import GroupMebBusiOper
from selenium import webdriver
from Common import ReadConfig
from Common.OperExcel import write_dict_xls,write_xlsBycolName_append
from Common.Mylog import LogManager
from Common.Assert import PageAssert
from TestCases.suite import mySuitePrefixAdd
from Base.OracleOper import MyOracle
from Common.function import join_dictlists
from Common.TestDataMgnt import GrpTestData
from Common.TestDataMgnt import create_testDataFile

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

# file = ReadConfig.data_path + 'UITest_GrpBusiOper.xls'
# paras = get_exceldata(file,1)

'''已订购OFFER_ID =8000 的集团商品订购信息'''
grpOfferList = GrpTestData().get_GrpOfferInst(groupId="'8711440154','8711440277'",offerId='8000')
logger.info('已订购的集团商品实例列表:{}'.format(grpOfferList))

'''要订购集团商品的成员列表
[800001] 表示要订购的子商品列表 ，800001 VPMN成员商品
'''
grpMeb = GrpTestData().get_MebAccessNumList(subOfferList='800001',AccessNumList="'18760959746','18787270407'")
VpmnMebsubList = join_dictlists(grpOfferList,grpMeb)
logger.info('集团VPMN成员订购列表:{}'.format(VpmnMebsubList))
file_MebAdd = ReadConfig.get_data_path() + 'UITest_GrpMebSubTest_%s.xls' % time.strftime("%Y%m%d%H%M%S")
create_testDataFile(paras=VpmnMebsubList,filename=file_MebAdd) # 生成一个测试数据表格

'''VPMN成员删除取三个'''
DelVpmnMebOfferList = GrpTestData().get_GrpMebOfferInst(grpOfferId='8000')
logger.info('集团VPMN成员退订列表:{}'.format(DelVpmnMebOfferList))
file_MebDel = ReadConfig.get_data_path() + 'UITest_GrpMebDelTest_%s.xls' % time.strftime("%Y%m%d%H%M%S")
create_testDataFile(paras=DelVpmnMebOfferList,filename=file_MebDel) # 生成一个测试数据表格

@ddt.ddt
class GroupMebBusi(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(rc.get_ngboss('url'))     #这里可以切换环境，去ngboss_config.ini配置
        self.driver.maximize_window()

    @ddt.data(*VpmnMebsubList)
    def test01_sub_VpmnMeb(self,dic):
        '''vpmn成员订购'''
        logger.info("开始参数化......")
        row = int(dic.get('NO'))  # 标识行号，后续写入xls使用
        accessNum = str(dic.get('ACCESS_NUM'))
        groupId = str(dic.get('GROUP_ID'))  # SIM卡号参数化
        offerid = str(dic.get('OFFER_ID'))
        grp_offer_insid = str(dic.get('GRP_OFFER_INS_ID'))
        subOfferList = dic.get('SUBOFFERLIST').replace(' ','').split(',') #成员子商品列表去空格并转换成list
        logger.info('开始执行第{}个用例,测试数据：{}'.format(row, dic))
        '''开始执行案例'''
        test = GroupMebBusiOper(self.driver)
        title = u'VPMN成员商品订购测试记录'
        test.add_dochead(title)
        test.Open_GrpMebBusiOrd(groupId)
        test.screen_step('步骤1：打开成员商品受理菜单')
        test.initPage()   #初始化
        test.input_GrpMebNum(accessNum)
        test.screen_step("步骤2：输入成员服务号码")
        test.click_BtnMebSub() #点击可订购按钮
        test.screen_step("步骤3:选择集团商品并点击订购按钮")
        test.choose_grpOfferandsub(offerid,grp_offer_insid) #选择集团商品并点击订购按钮
        print("直接进入子商品设置页面")
        logger.info("开始设置VPMN成员子商品......")
        for i in range(len(subOfferList)):
            print("子商品编码subofferId=" + subOfferList[i])
            print("设置子商品......")
            logger.info("开始设置子商品产品规格特征" + subOfferList[i])
            test.set_MebsubOffer(subOfferList[i]) #子商品点击待设置(注意这里与集团商品有点区别)
            test.screen_step("步骤4：产品规格特征设置页面，点击待设置")
            time.sleep(8)
            test.set_prodSpec() #产品规格特征设置页面，点击待设置
            if (subOfferList[i] =='222201'):
                # 如果成员商品offerid = 222201 多媒体桌面电话成员产品或者短号集群网则要设置短号
                test.set_vpmnMebshortCode()
            if (subOfferList[i] =='800001'):
                test.set_vpmnMebshortCode()
                test.screen_step("步骤5：设置成员短号")
                test.set_DispMode()
            test.confirm_vpmnMebsubOfferSpec()#确认VPMN子商品规格设置
            test.confirm_OfferSpec() #最后确认商品设置
        test.screen_step("步骤6：确认商品配置，点击提交")
        test.Open_SubmitAll()  #订购主页，点击提交
        submitMsg = PageAssert(self.driver).assert_SubmitPage()
        logger.info('业务受理信息：{}'.format(submitMsg))
        test.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        test.save_docreport(title)
        logger.info('写入测试结果到xls.....')
        PageAssert(self.driver).write_testResult(file=file_MebAdd,row=row,index=0) #写入结果到xls
        self.driver.close()

    @ddt.data(*DelVpmnMebOfferList)
    def test02_OpergrpMemDel(self,dic):
        '''成员商品退订'''
        logger.info("开始参数化......")
        row = int(dic.get('NO'))  # 标识行号，后续写入xls使用
        accessNum = str(dic.get('ACCESS_NUM'))
        groupId = str(dic.get('GROUP_ID'))  # SIM卡号参数化
        mainOffer = str(dic.get('OFFER_ID'))
        OfferInstId = str(dic.get('GRP_OFFER_INS_ID'))
        logger.info('开始执行第{}个用例,测试数据：{}'.format(row, dic))
        '''开始执行案例'''
        test = GroupMebBusiOper(self.driver)
        title = u'成员商品业务注销'
        test.add_dochead(title)
        test.Open_GrpMebBusiOrd(groupId)
        test.initPage()   #初始化
        test.screen_step("输入成员服务号码")
        test.input_GrpMebNum(accessNum)
        test.screen_step("选择要注销的集团产品订购实例，点击注销")
        test.choose_grpOfferandCancel(mainOffer,OfferInstId)
        test.confirm_vaildTips()  #有可能重新进行集团认证鉴权
        test.screen_step("点击注销按钮")
        test.submit_cancel()
        print("处理页面返回信息.....")
        logger.info("处理页面返回信息......")
        submitMsg = PageAssert(self.driver).assert_Submit()
        logger.info('业务受理信息：{}'.format(submitMsg))
        test.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        test.save_docreport(title)
        logger.info('写入测试结果到xls.....')
        PageAssert(self.driver).write_testResult(file=file_MebDel,row=row,index=0) #写入结果到xls
        self.driver.close()

if __name__ == '__main__':
    report_title = u'成员商品业务受理自动化测试报告'
    desc = u'成员商品受理测试详情'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath() + report_title + nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2,retry=1)
        # runner.run(mySuitePrefixAdd(GroupMebBusi,"test01_sub_VpmnMeb"))
        runner.run(mySuitePrefixAdd(GroupMebBusi,"test01_sub_VpmnMeb"))
        runner.run(mySuitePrefixAdd(GroupMebBusi,"test02_OpergrpMemDel"))