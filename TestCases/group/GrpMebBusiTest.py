import unittest,os
from Base import HTMLTestRunnerCNNew
import time,ddt
from PageObj.order.group.GrpMebBusiOper import GroupMebBusiOper
from selenium import webdriver
from Base import ReadConfig
from Base.Mylog import LogManager
from Check.PageCheck import PageAssert
from TestCases.suite import mySuitePrefixAdd
from Base.OracleOper import MyOracle
# from Common.function import join_dictlists
# from Common.TestDataMgnt import GrpTestData
# from Common.TestDataMgnt import create_testDataFile

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

# file = get_TestData('SubGrpVpmnMeb')['filename']
file = get_testDataFile()

AdcMebsubList = get_TestData('SubGrpAdcMeb')['params'] # ADC集团管家成员订购
# GrpMebsubList.extend(AdcMebsubList)

GrpMebsubList = []
VpmnMebsubList = get_TestData('SubGrpVpmnMeb')['params'] #Vpmn成员订购
GrpMebsubList.extend(VpmnMebsubList)
ImsMebsubList = get_TestData('SubGrpImsMeb')['params'] #多媒体桌面电话成员订购
GrpMebsubList.extend(ImsMebsubList)
print('集团成员订购参数:{}'.format(GrpMebsubList))
DelGrpMebList = get_TestData('DelGrpMebOffer')['params']  #成员商品注销


# file = ReadConfig.data_path + 'UITest_GrpBusiOper.xls'
# paras = get_exceldata(file,1)

'''已订购OFFER_ID =8000 的集团商品订购信息'''
# grpOfferList = GrpTestData().get_GrpOfferInst(groupId="'8711440154','8711440277'",offerId='8000')
# logger.info('已订购的集团商品实例列表:{}'.format(grpOfferList))

'''要订购集团商品的成员列表
[800001] 表示要订购的子商品列表 ，800001 VPMN成员商品
'''
# grpMeb = GrpTestData().get_MebAccessNumList(subOfferList='800001',AccessNumList="'18760959746','18787270407'")
# VpmnMebsubList = join_dictlists(grpOfferList,grpMeb)
# logger.info('集团VPMN成员订购列表:{}'.format(VpmnMebsubList))
# file_MebAdd = ReadConfig.get_data_path() + 'UITest_GrpMebSubTest_%s.xls' % time.strftime("%Y%m%d%H%M%S")
# create_testDataFile(paras=VpmnMebsubList,filename=file_MebAdd) # 生成一个测试数据表格

'''VPMN成员删除取三个'''
# DelVpmnMebOfferList = GrpTestData().get_GrpMebOfferInst(grpOfferId='8000')
# logger.info('集团VPMN成员退订列表:{}'.format(DelVpmnMebOfferList))
# file_MebDel = ReadConfig.get_data_path() + 'UITest_GrpMebDelTest_%s.xls' % time.strftime("%Y%m%d%H%M%S")
# create_testDataFile(paras=DelVpmnMebOfferList,filename=file_MebDel) # 生成一个测试数据表格

@ddt.ddt
class GroupMebBusi(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(rc.get_ngboss('url'))     #这里可以切换环境，去ngboss_config.ini配置
        self.driver.maximize_window()

    @ddt.data(*AdcMebsubList)
    def test00_subGrpAdcMeb(self,dic):
        '''ADC成员订购'''
        logger.info("开始参数化......")
        row = get_TestData('SubGrpAdcMeb')['FuncRow']
        accessNum = str(dic.get('ACCESS_NUM'))
        groupId = str(dic.get('GROUP_ID'))  # SIM卡号参数化
        offerid = str(dic.get('OFFER_ID'))
        grp_offer_insid = str(dic.get('GRP_OFFER_INS_ID'))
        subOfferList = dic.get('SUBOFFERLIST').replace(' ','').split(',') #成员子商品列表去空格并转换成list
        logger.info('开始执行ADC成员商品订购用例,测试数据：{}'.format(dic))
        print('开始执行成员商品订购用例,测试数据：{}'.format(dic))
        '''开始执行案例'''
        test = GroupMebBusiOper(self.driver)
        title = u'VPMN成员商品订购测试记录'
        test.add_dochead(title)
        test.Open_GrpMebBusiOrd(groupId)
        test.screen_step('步骤1：打开成员商品受理菜单')
        test.initPage()   #初始化
        test.input_GrpMebNum(accessNum)
        time.sleep(2)
        test.screen_step("步骤2：输入成员服务号码")
        test.click_BtnMebSub() #点击可订购按钮
        test.screen_step("步骤3:选择集团商品并点击订购按钮")
        test.choose_grpOfferandsub(offerid,grp_offer_insid) #选择集团商品并点击订购按钮
        #加个规则校验
        ruleMsg = PageAssert(self.driver).check_BusiRule(file=file,row=row)
        logger.info('成员商品订购业务规则校验结果:{}'.format(ruleMsg))
        self.assertNotIn('校验失败',ruleMsg)
        print("直接进入子商品设置页面")
        logger.info("开始设置ADC成员子商品......")
        for i in range(len(subOfferList)):
            print("子商品编码subofferId=" + subOfferList[i])
            print("设置子商品......")
            logger.info("开始设置子商品产品规格特征" + subOfferList[i])
            test.set_MebsubOffer(subOfferList[i]) #子商品点击待设置(注意这里与集团商品有点区别)
            test.screen_step("步骤4：产品规格特征设置页面，点击待设置")
            time.sleep(8)
            test.set_prodSpec() #产品规格特征设置页面，点击待设置
            if subOfferList[i] =='648001':  #集团管家成员主商品
                test.set_vpmnMebshortCode()
                test.screen_step("步骤5：设置成员短号")
                test.set_DispMode()
                test.confirm_MebsubMainOfferSpec() #完成成员主商品设置
            else:
                test.confirm_AdcMebsubOfferSpec()#确认ADC子商品规格设置
            test.confirm_OfferSpec() #最后确认商品设置
        test.screen_step("步骤6：确认商品配置，点击提交")
        test.Open_SubmitAll()  #订购主页，点击提交
        time.sleep(10)
        submitMsg = PageAssert(self.driver).assert_submitAfter(file=file,row=row,index=0) #写入结果到xls
        logger.info('业务受理信息：{}'.format(submitMsg))
        test.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        test.save_docreport(title)
        self.assertIn('业务受理成功',submitMsg)

    @ddt.data(*GrpMebsubList)
    def test01_subGrpVpmnMeb(self,dic):
        '''vpmn成员订购(VPMN+Ims)'''
        logger.info("开始参数化......")
        # row = int(dic.get('NO'))  # 标识行号，后续写入xls使用
        accessNum = str(dic.get('ACCESS_NUM'))
        groupId = str(dic.get('GROUP_ID'))  # SIM卡号参数化
        offerid = str(dic.get('OFFER_ID'))
        grp_offer_insid = str(dic.get('GRP_OFFER_INS_ID'))
        subOfferList = dic.get('SUBOFFERLIST').replace(' ','').split(',') #成员子商品列表去空格并转换成list
        row = get_TestData('SubGrpVpmnMeb')['FuncRow'] if offerid == '8000' else get_TestData('SubGrpImsMeb')['FuncRow']
        logger.info('开始执行成员商品订购用例,测试数据：{}'.format(dic))
        print('开始执行成员商品订购用例,测试数据：{}'.format(dic))
        '''开始执行案例'''
        test = GroupMebBusiOper(self.driver)
        title = u'VPMN成员商品订购测试记录'
        test.add_dochead(title)
        test.Open_GrpMebBusiOrd(groupId)
        test.screen_step('步骤1：打开成员商品受理菜单')
        test.initPage()   #初始化
        test.input_GrpMebNum(accessNum)
        time.sleep(2)
        test.screen_step("步骤2：输入成员服务号码")
        test.click_BtnMebSub() #点击可订购按钮
        test.screen_step("步骤3:选择集团商品并点击订购按钮")
        test.choose_grpOfferandsub(offerid,grp_offer_insid) #选择集团商品并点击订购按钮
        ruleMsg = PageAssert(self.driver).check_BusiRule(file=file,row=row)
        logger.info('成员商品订购业务规则校验结果:{}'.format(ruleMsg))
        self.assertNotIn('校验失败',ruleMsg)
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
                # row = get_TestData('SubGrpImsMeb')['FuncRow']
                test.set_vpmnMebshortCode()
            elif (subOfferList[i] =='800001'):  #Vpmn或者集团管家成员商品
                # row = get_TestData('SubGrpVpmnMeb')['FuncRow']
                test.set_vpmnMebshortCode()
                test.screen_step("步骤5：设置成员短号")
                test.set_DispMode()
            test.confirm_MebsubMainOfferSpec()#确认成员主商品规格设置
            test.confirm_OfferSpec() #最后确认商品设置
        test.screen_step("步骤6：确认商品配置，点击提交")
        test.Open_SubmitAll()  #订购主页，点击提交
        submitMsg = PageAssert(self.driver).assert_submitAfter(file=file,row=row,index=0) #写入结果到xls
        logger.info('业务受理信息：{}'.format(submitMsg))
        test.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        test.save_docreport(title)
        self.assertIn('业务受理成功',submitMsg)

    @ddt.data(*DelGrpMebList)
    def test02_DelgrpMemOffer(self,dic):
        '''成员商品退订'''
        logger.info("开始参数化......")
        row = get_TestData('DelGrpMebOffer')['FuncRow']
        accessNum = str(dic.get('ACCESS_NUM'))
        groupId = str(dic.get('GROUP_ID'))
        mainOffer = str(dic.get('OFFER_ID'))
        OfferInstId = str(dic.get('GRP_OFFER_INS_ID'))
        logger.info('开始执行集团成员商品注销用例,测试数据：{}'.format( dic))
        print('开始执行集团成员商品注销用例,测试数据：{}'.format( dic))
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
        ruleMsg = PageAssert(self.driver).check_BusiRule(file,row) #验证下规则
        self.assertNotIn('校验失败',ruleMsg) #断点判断
        test.confirm_vaildTips()  #有可能重新进行集团认证鉴权
        test.screen_step("点击注销按钮")
        test.submit_cancel()
        print("处理页面返回信息.....")
        logger.info("处理页面返回信息......")
        submitMsg = PageAssert(self.driver).assert_submitAfter(file=file,row=row,index=0) #写入结果到xls
        logger.info('业务受理信息：{}'.format(submitMsg))
        test.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        test.save_docreport(title)
        self.assertIn('业务受理成功',submitMsg)

    def tearDown(self):
        print('测试结束，关闭浏览器器!')
        self.driver.close()


if __name__ == '__main__':
    report_title = u'成员商品业务受理自动化测试报告'
    desc = u'成员商品受理测试详情'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath() + report_title + nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2,retry=1)
        runner.run(mySuitePrefixAdd(GroupMebBusi,"test00_subGrpAdcMeb"))
        runner.run(mySuitePrefixAdd(GroupMebBusi,"test01_subGrpVpmnMeb"))
        runner.run(mySuitePrefixAdd(GroupMebBusi,"test02_DelgrpMemOffer"))