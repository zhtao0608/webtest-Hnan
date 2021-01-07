import time
from Base.base import Base
from selenium.webdriver.support.ui import WebDriverWait  # 用于处理元素等待
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Check.PageCheck import PageAssert
from Common.TestAsserts import Assertion
from Common.SuiteExec import DealSuiteExec as dse
from Base import ReadConfig
from Base.Mylog import LogManager
from Data.DataMgnt.TestResult import TestResultOper as TR

logger = LogManager('RuleCheck').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

#================处理页面元素公共类，包含主套餐、服务、优惠、平台服务等======================#

class RuleCheckBefore(Base):
    '''公共规则检查'''
    def checkRule(self,scene='ruleCheck'):
        '''页面执行规则判断'''
        '''处理Wade弹出的各种提示窗口（Error、Success、Warn、Help、Tips）'''
        loc_WadeMessage = (By.XPATH,'//div[starts-with(@id,"wade_messagebox") and not(contains(@style,"display: none"))]')
        try:
            ele_wadeMsg = self.find(loc_WadeMessage)
            logger.info('找到WadeMsg弹出框:{}'.format(str(ele_wadeMsg)))
            classname = self.get(loc_WadeMessage,Type='attribute',name='class') #取出WadeMsg的class属性值，判断是什么类型弹出
            logger.info('wadeMsg的类型:{}'.format(classname))
            time.sleep(2)
            WadeMsg = ele_wadeMsg.find_element_by_xpath('./div/div[2]/div[1]/div[2]').text
            logger.info('WadeMessageBox返回的信息：{}'.format(WadeMsg))
            '''根据classname类型按钮处理'''
            if 'c_msg-error' in classname:
                print('弹出WadeMsg的是错误提示')
                logger.info("业务校验失败:{}".format(WadeMsg))
                print('业务校验信息:{}'.format(WadeMsg))
                step_str = "业务校验"
                self.screen_step(step_str)  # 这个保存在测试记录文档中
                self.screenshot_SaveAsDoc(step_str)  # 截图单独保存到doc
                time.sleep(3)
                WadeMsg = '业务校验失败' + WadeMsg
            elif 'c_msg-success' in classname:
                print('弹出WadeMsg的是成功提示')
                ele_suc = ele_wadeMsg.find_element_by_xpath('./div/div[2]/div[2]/button')
                self.click_on_element(ele_suc)
                self.sendEnter()
                time.sleep(2)
                WadeMsg = '弹出校验成功信息：' + WadeMsg
            elif 'c_msg-warn' in classname:
                print('弹出WadeMsg的是告警提示')
                step_str = "业务受理提示信息"
                self.screenshot_SaveAsDoc(step_str)
                ele_wadeMsg.find_element_by_xpath('./div/div[2]/div[2]/button').click()  # 关闭提示窗口
                self.sendEnter()
                time.sleep(2)
                WadeMsg = '警告信息:' + WadeMsg
            elif 'c_msg-however' in classname:
                print('弹出WadeMsg的是however')
                step_str = "业务受理提示信息"
                self.screenshot_SaveAsDoc(step_str)
                ele_wadeMsg.find_element_by_xpath('./div/div[2]/div[2]/button').click()  # 关闭提示窗口
                self.sendEnter()
                time.sleep(2)
                WadeMsg = '业务校验:' + WadeMsg
                logger.info(WadeMsg)
            elif 'c_msg-help' in classname:
                print('弹出WadeMsg的是帮助提示')
                ele_help = ele_wadeMsg.find_element_by_xpath('./div/div[2]/div[2]/button[1]')
                self.click_on_element(ele_help)
                self.sendEnter()
                time.sleep(3)
            elif 'c_msg c_msg-h c_msg-phone-v c_msg-full' == classname:
                print('弹出WadeMsg的是普通提示')
                step_str = "业务受理提示信息"
                logger.info('业务受理提示信息:{}'.format(WadeMsg))
                self.screenshot_SaveAsDoc(step_str)
                ele_wadeMsg.find_element_by_xpath('./div/div[2]/div[2]/button[1]').click()  # 关闭提示窗口
                time.sleep(2)
                WadeMsg = '出现提示信息:' + WadeMsg
                self.sendEnter()
        except:
            WadeMsg = '没有弹出WadeMessage提示,校验通过'
        logger.info('======WadeMessageBox页面返回============={}'.format(WadeMsg))
        # TR().updateRuleCheckInfo(msg=WadeMsg,sceneCode=scene)
        #将规则校验结果更新到AUTOTEST_SUITE_EXEC.RULE_CHECK_INFO字段
        dse().upd_RuleChkBySuiteCaseId(suite_case_id=scene,rule_chkmsg=WadeMsg)
        Assertion().assertNotIn('校验失败',WadeMsg,msg='[规则校验通过]')
        Assertion().assertNotIn('校验不通过',WadeMsg,msg='[规则校验通过]')
        return WadeMsg

    def checkBefore(self,scene='RULE_CHECK_BEFORE'):
        '''
        根据场景编码校验业务受理前置规则
        :param scene:
        :return:
        '''
        '''个人业务前置业务规则判断'''
        self.screen_step('CheckRuleBefore业务规则判断')
        rulemsg = PageAssert(self.driver).assert_WadePage()
        logger.info('Wade页面返回的业务规则校验信息:'.format(rulemsg))
        TR().updateRuleCheckInfo(msg=rulemsg,sceneCode=scene)
        Assertion().assertNotIn('校验失败',rulemsg,msg='[规则校验通过]')
        Assertion().assertNotIn('校验不通过',rulemsg,msg='[规则校验通过]')
        return rulemsg

