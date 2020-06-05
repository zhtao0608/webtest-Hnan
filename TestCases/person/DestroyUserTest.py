import unittest,os
import ddt,time
from Base import HTMLTestRunnerCNNew
from PageObj.oc.person.DestroyUser import DestroyUser
from selenium.webdriver.common.by import By
from PageObj.oc.person.PersonBase import PersonBase
from selenium import webdriver
from Base import ReadConfig
from Base.OperExcel import write_dict_xls,write_xlsBycolName_append
from Base.Mylog import LogManager
from Base.OracleOper import MyOracle
from TestCases.suite import mySuitePrefixAdd
from Common.Assert import PageAssert

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('DestroyUserTest').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

ora = MyOracle()
sql = "SELECT rownum No ,t.access_num,to_char(t.subscriber_ins_id) subscriber_ins_id ,'' flowid , '' result_info \
    FROM  uop_file4.um_subscriber  T where t.access_num in ('18887010689','18887029851','18887032321') "
paras = ora.select(sql)

logger.info('测试准备数据:{}'.format(paras))
now = time.strftime("%Y%m%d%H%M%S")
file = ReadConfig.get_data_path() + 'UITest_DestroyUser_%s.xls' % now
#生成xls表,方便后续写入测试结果
write_dict_xls(inputData=paras, sheetName='销户测试', outPutFile=file)
logger.info('写入测试数据到xls.....')

@ddt.ddt
class DestroyUserTest(unittest.TestCase):
    """[个人业务]销户测试"""
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(rc.get_ngboss('url'))     #这里可以切换环境，去ngboss_config.ini配置
        self.driver.maximize_window()
        #self.driver.implicitly_wait(40)    #暂时设置40s，隐式等待

    @ddt.data(*paras)
    def test_destroyUser(self,dic):
        """销户"""
        logger.info("开始参数化......")
        row = int(dic.get('NO'))   #标识行号，后续写入xls使用
        print('开始执行第{}个用例,测试数据：{}'.format(row,dic))
        accessNum = str(dic.get('ACCESS_NUM'))
        logger.info('开始执行第{}个用例,测试数据：{}'.format(row,dic))
        ####测试用例步骤
        test = DestroyUser(self.driver)
        title = '个人销户受理测试记录'
        test.add_dochead(title)
        loc_vaild = (By.XPATH,'//*[@id="MYSELF_div"]/div[1]')
        loc_commit = (By.ID,'CSSUBMIT_BUTTON')
        #登录进入菜单：
        PersonBase(self.driver).Open_PersonMenu(accessNum,password='123123',cataMenuId='crm9300',menuId='crm9311') #进入菜单
        # test.Open_PersonMenu(accessNum,password='123123',cataMenuId='crm9300',menuId='crm9311') #进入菜单
        test.open_DestroyUserFrame() #进入销户iframe
        errMsg = PersonBase(self.driver).vaild_BusiRule() #业务检查点（进入菜单时校验）
        logger.info('业务校验结果:{}'.format(errMsg))
        if '业务校验失败' in errMsg:
            # print('业务规则校验失败：{}'.format(errMsg))
            #业务规则校验异常信息写入RESULT_INFO列
            write_xlsBycolName_append(file=file,row =row ,colName='RESULT_INFO',value=errMsg,index=0)
            logger.info('业务校验信息写入xls成功......')
            print('业务校验信息写入xls成功......')
            test.quit_browse() #关闭浏览器
        else:
            PageAssert(self.driver).assert_HelpPage()
            test.close_UIstep()
        test.find_element_click(loc_vaild) #移动到认证并点击
        time.sleep(2)
        test.set_destroyReason()
        test.find_element_click(loc_commit)  #点击提交
        time.sleep(10)  #销户业务提交比较慢
        submitMsg = PageAssert(self.driver).assert_Submit()  #提交后返回信息，flowId或者报错
        test.screen_step('点击提交,受理信息：{}'.format(submitMsg))
        test.save_docreport(title)
        logger.info('写入测试结果到xls.....')
        PageAssert(self.driver).write_testResult(file=file,row=row,index=0) #写入结果到xls
        self.driver.close()

if __name__ == '__main__':
    report_title = u'个人销户自动化测试报告'
    desc = u'个人销户测试详情：'
    nowtime = time.strftime("%Y%m%d%H%M%S")
    logger.info("开始执行testSuite......")
    print("开始执行testSuite......")
    with open(ReadConfig.get_reportPath() + report_title +  nowtime + ".html", 'wb') as fp:
        runner = HTMLTestRunnerCNNew.HTMLTestRunner(stream=fp, title=report_title, description=desc,verbosity=2,retry=1)
        runner.run(mySuitePrefixAdd(DestroyUserTest,"test_destroyUser"))



