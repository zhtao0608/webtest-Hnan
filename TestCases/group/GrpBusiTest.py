import unittest,os
from Base import HTMLTestRunnerCNNew
import time,ddt
from PageObj.oc.group.GrpBusiOper import GroupBusiOper
from selenium import webdriver
from Base import ReadConfig
from Base.GenTestData import GenTestData
from Base.Mylog import LogManager
from Common.Assert import PageAssert
from TestCases.suite import mySuitePrefixAdd
from Common.TestDataMgnt import GrpTestData
from Common.TestDataMgnt import get_TestData,get_testDataFile

logger = LogManager('GroupBusiTest').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")

AdminNum = '15240837862'
# file = get_TestData('OpenGrpAdc')['filename']
file = get_testDataFile()

paras_GrpADCSub = get_TestData('OpenGrpAdc')['params']   # ADC受理参数
paras_GrpVpmnSub = get_TestData('OpenGrpVpmn')['params']  #VPMN集团订购受理参数
paras_GrpImsSub = get_TestData('OpenGrpIms')['params']    #IMS多媒体电话集团订购受理参数
paras_GrpBusiCancel = get_TestData('CanelGrpIms')['params']

# paras_GrpBusiSub = GrpTestData().get_GrpOffer(groupId= "'8712239560'",offerId='6480',subOfferlist='100648000,100648001')
# file_GrpBusiSub = ReadConfig.get_data_path() + 'UITest_GrpBusiSubTest_' + time.strftime("%Y%m%d%H%M%S") + '.xls'
# create_testDataFile(paras=paras_GrpBusiSub,filename=file_GrpBusiSub)
#
# paras_GrpVpmnSub = GrpTestData().get_GrpOffer(groupId= "'8721420598'",offerId='2222',subOfferlist='')
# file_GrpVpmnSub = ReadConfig.get_data_path() + 'UITest_GrpVpmnSubTest_' + time.strftime("%Y%m%d%H%M%S") + '.xls'
# create_testDataFile(paras=paras_GrpVpmnSub,filename=file_GrpVpmnSub)
#
# file_grpBusiCancel = ReadConfig.get_data_path() + 'UITest_GrpBusiCancelTest_' + time.strftime("%Y%m%d%H%M%S") + '.xls'
# paras_GrpBusiCancel = GrpTestData().get_GrpOfferInst(groupId="'8711440277'",offerId='8000')
# create_testDataFile(paras=paras_GrpBusiCancel,filename=file_grpBusiCancel)

@ddt.ddt
class GroupBusi(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(rc.get_ngboss('url'))     #这里可以切换环境，去ngboss_config.ini配置
        self.driver.maximize_window()

    @ddt.data(*paras_GrpADCSub)
    def test01_OpenGrpAdc(self,dic):
        '''订购ADC集团管家'''
        logger.info("开始参数化......")
        # row = int(dic.get('NO'))  # 标识行号，后续写入xls使用
        groupId = dic.get('GROUP_ID')
        offerid = dic.get('OFFER_ID') #集团主商品ID
        if not dic.get('SUBOFFERLIST') == None:
            subOfferList = dic.get('SUBOFFERLIST').replace(' ', '').split(',') #集团子商品ID,读入的都是str，通过split转成List
            logger.info('订购的子商品列表:{}'.format(subOfferList))
        else:
            subOfferList = []
        accessNum = AdminNum    #管理员电话号码（在网号码即可）
        singname = '中文签名'
        print("子商品列表：%s",str(subOfferList))
        logger.info('开始执行ADC集团商品订购用例,测试数据：{}'.format( dic))
        test = GroupBusiOper(self.driver)
        title = '集团商品业务订购测试记录'
        test.add_dochead(title)
        test.Open_GrpBusiOrd(groupId)
        test.search_grpOffer(offerid)
        #这里加个校验，判断集团商品是否允许订购
        busiRuleMsg = test.vaild_GroupBusiRule()
        if '校验失败' in busiRuleMsg:
            PageAssert(self.driver).write_vaildErrResult(file=file,row=get_TestData('OpenGrpAdc')['FuncRow'])
        test.screen_step("点击集团商品待设置按钮")
        test.set_mainOffer(offerid) #商品订购主页点击待设置
        logger.info("商品设置开始......")
        test.screen_step("设置集团商品规格特征")
        test.set_OfferSpec(subOfferList) #商品设置下点击确定,判断是否需要点击商品待设置
        logger.info("商品设置完成")
        for i in range(len(subOfferList)):
            logger.info("子商品编码subofferId=" + subOfferList[i])
            logger.info("设置子商品......")
            logger.info("开始设置子商品:{}产品规格特征" .format(subOfferList[i]))
            test.screen_step("点击集团子商品,待设置按钮")
            test.set_subOffer(subOfferList[i]) #子商品点击设置
            test.screen_step("进入子商品_%s产品规格特征设置页面" % subOfferList[i])
            '''设置产品规格特征'''
            test.set_prodSpec()  #产品规格点击待设置
            test.input_ADC_ECGN_ZH(singname)
            test.input_ADC_ManagePhoneNum(accessNum)
            test.screen_step("ADC平台产品属性设置完成，点击确认")
            test.submit_subOfferProdSpec() #点击确认
            test.submit_subOfferProdSpec() #不知道是否再次提交一次
            logger.info("子商品产品规格特征设置结束" + subOfferList[i])
            test.screen_step("点击确认，完成集团商品订购设置")
            test.confirm_OfferSpec() #商品设置再确认
        test.screen_step("点击商品提交按钮")
        test.Open_SubmitAll()#商品订购提交
        submitMsg = PageAssert(self.driver).assert_Submit()
        logger.info('业务受理信息：{}'.format(submitMsg))
        test.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        test.save_docreport(title)
        PageAssert(self.driver).write_testResult(file=file,row=get_TestData('OpenGrpAdc')['FuncRow'],index=0) #写入结果到xls
        self.driver.close()

    @ddt.data(*paras_GrpBusiCancel)
    def test02_Cancel_GrpOrder(self,dic):
        '''集团商品注销'''
        logger.info("开始参数化......")
        # row = int(dic.get('NO'))  # 标识行号，后续写入xls使用
        groupId = dic.get('GROUP_ID')
        offerid = str(dic.get('OFFER_ID')) #集团主商品ID
        offerInsId = dic.get('GRP_OFFER_INS_ID')
        remark = '自动化测试'
        print("集团商品实例：%s",str(offerInsId))
        logger.info('开始集团用户用例,测试数据：{}'.format( dic))
        test = GroupBusiOper(self.driver)
        test.Cancel_GrpOrder(groupId,offerid,offerInsId,remark)
        PageAssert(self.driver).write_testResult(file=file,row=get_TestData('CanelGrpIms')['FuncRow'],index=0) #写入结果到xls
        self.driver.close()

    @ddt.data(*paras_GrpVpmnSub)
    def test03_OpenGrpVpmn(self,dic):
        '''订购短号集群网8000'''
        logger.info("开始参数化......")
        # row = int(dic.get('NO'))  # 标识行号，后续写入xls使用
        groupId = dic.get('GROUP_ID')
        offerid = dic.get('OFFER_ID') #集团主商品ID
        if not dic.get('SUBOFFERLIST') == None:
            subOfferList = dic.get('SUBOFFERLIST').replace(' ', '').split(',') #集团子商品ID,读入的都是str，通过split转成List
            logger.info('订购的子商品列表:{}'.format(subOfferList))
        else:
            subOfferList = []
        logger.info('订购的子商品列表:{}'.format(subOfferList))
        print("子商品列表：%s",str(subOfferList))
        logger.info('开始执行集团短号集群网商品订购用例,测试数据：{}'.format(dic))
        print('开始执行集团短号集群网商品订购用例,测试数据：{}'.format(dic))
        test = GroupBusiOper(self.driver)
        test.Open_GrpVpmn(groupId,offerid,subOfferList)
        PageAssert(self.driver).write_testResult(file=file,row=get_TestData('OpenGrpVpmn')['FuncRow'],index=0) #写入结果到xls
        self.driver.close()

    @ddt.data(*paras_GrpImsSub)
    def test04_OpenGrpIMS(self,dic):
        '''订购多媒体桌面电话2222'''
        logger.info("开始参数化......")
        # row = int(dic.get('NO'))  # 标识行号，后续写入xls使用
        groupId = dic.get('GROUP_ID')
        offerid = dic.get('OFFER_ID') #集团主商品ID
        if not dic.get('SUBOFFERLIST') == None:
            subOfferList = dic.get('SUBOFFERLIST').replace(' ', '').split(',') #集团子商品ID,读入的都是str，通过split转成List
            logger.info('订购的子商品列表:{}'.format(subOfferList))
        else:
            subOfferList = []
        logger.info('订购的子商品列表:{}'.format(subOfferList))
        print("子商品列表：%s",str(subOfferList))
        logger.info('开始执行集团多媒体桌面电话商品订购用例,测试数据：{}'.format(dic))
        print('开始执行集团多媒体桌面电话商品订购用例,测试数据：{}'.format(dic))
        test = GroupBusiOper(self.driver)
        test.Open_GrpVpmn(groupId,offerid,subOfferList)
        PageAssert(self.driver).write_testResult(file=file,row=get_TestData('OpenGrpIms')['FuncRow'],index=0) #写入结果到xls
        self.driver.close()

    def tearDown(self):
        print('测试结束，关闭浏览器器!')
        self.driver.close()
if __name__ == '__main__':
    report_title = u'集团商品业务受理自动化测试报告'
    desc = u'集团商品受理测试详情'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath() + report_title + nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2)
        runner.run(mySuitePrefixAdd(GroupBusi,"test01_OpenGrpAdc"))
