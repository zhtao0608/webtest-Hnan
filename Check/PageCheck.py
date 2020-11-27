from Base.base import Base
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait  # 用于处理元素等待
from Base import ReadConfig
from Base.Mylog import LogManager
from Base.OperExcel import write_excel_append,write_xlsBycolName_append
from Common import TestAsserts
import time,sys

logger = LogManager('PageAssert').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

rc = ReadConfig.ReadConfig("ngboss_config.ini")

class PageAssert(Base):
    '''页面检查点'''
    def assert_Submit(self):
        """判断是否定位到页面返回信息"""
        loc_flow = (By.ID, 'SUBMIT_MSG_CONTENT')
        Loc_msg = (By.XPATH,"//*[@class='c_msg c_msg-h c_msg-phone-v c_msg-popup c_msg-error' and not(contains(@style,'display: none'))]/div/div[2]/div[1]/div[2]")
        try:
            ele = WebDriverWait(self.driver, 30, 1).until(EC.presence_of_element_located(Loc_msg))
            errmsg = ele.text
            logger.info('提交失败，错误信息：' + errmsg)
            print('提交失败，错误信息：' + errmsg)
            self.screen_step('业务受理失败：{}'.format(errmsg))
            submitMsg = '业务受理失败：' + errmsg
        except :
            flowId = self.get(loc_flow)
            logger.info("业务受理成功，交互流水：" + flowId)
            print("业务受理成功，交互流水：" + flowId)
            self.screen_step('业务受理成功，交互流水：{}'.format(flowId))
            submitMsg = flowId
        return submitMsg

    """==============================处理页面返回信息====================================="""
    """====================处理WadeMessageBox受理异常提示======================"""
    def assert_WadePage(self):
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
        return WadeMsg

    def dealDialogPage(self):
        '''个人业务在鉴权时，可能弹出比如营销鉴权等窗口，强制查看并关闭'''
        loc_Dialog = (By.XPATH, '//div[starts-with(@id,"dialog") and not(contains(@style,"display: none"))]')
        try:
            ele_Dialog = self.find(loc_Dialog)
            logger.info('找到DialogPage弹出框:{}'.format(str(ele_Dialog)))
            time.sleep(1)
            ele_Dialog.find_element_by_xpath('./div/div[1]/div[2]/div').click()  #关闭DialogPage
        except:
            logger.info('没有弹出DialogPage提示,跳出')

    def pageLoading(self):
        '''页面加载时间判断,目前设置最长时间为30s'''
        loc_wadeLoading = (By.ID,'x-wade-loading-global')
        eleLoading = WebDriverWait(self.driver, 30, 1).until(EC.presence_of_element_located(loc_wadeLoading))
        while True:
            flag = self.is_element_displayed(eleLoading) #如果页面还显示页面加载中一直等待
            if not flag:
                break
        return flag


    def assert_submitAfter(self,file,row,index=0):
        '''
        测试结果写入xls，按xls模板已将flowId 和errmsg列指定了
        :param file: xls完整路径
        :param row: xls行号
        :param index: xls的sheet页index
        :return:
        '''
        try:
            Msg = self.assert_Submit()
            if '业务受理成功' in Msg:
                logger.info("业务受理成功，交互流水号写入xls中FLOWID列")
                write_xlsBycolName_append(file, row, 'FLOWID', Msg,index)  #向xls模板指定行列写入结果
            elif '业务受理失败' in Msg:
                logger.info("业务受理失败，错误信息写入xls中RESULT_INFO列")
                write_xlsBycolName_append(file, row, 'RESULT_INFO', Msg,index)  #向xls模板指定行列写入结果
        except :
            logger.info("测试结果写入xls发生异常！")
            Msg = '测试异常'
            write_xlsBycolName_append(file, row, 'RESULT_INFO', '测试异常', index)  # 向xls模板指定行列写入结果
        return Msg


    def write_vaildErrResult(self,file,row,index=0):
        '''
        测试结果写入xls，按xls模板已将flowId 和errmsg列指定了
        :param file: xls完整路径
        :param row: xls行号
        :param index: xls的sheet页index
        :return:
        '''
        Msg = self.assert_WadePage()
        if '业务校验失败' in Msg:
            logger.info("业务校验，错误信息写入xls中RESULT_INFO列")
            write_xlsBycolName_append(file, row, 'RESULT_INFO', Msg,index)  #向xls模板指定行列写入结果
        return Msg

    def check_BusiRule(self,file,row):
        '''业务规则校验，包括Error、Success、Warn、Help、Tips等各类Wade校验'''
        ruleMsg = self.assert_WadePage()
        if ('校验失败' in ruleMsg) or ('警告信息' in ruleMsg):
            write_xlsBycolName_append(file, row, 'RULE_CHECK',value=ruleMsg,index=0)
            logger.info('规则校验信息写入RULE_CHECK字段成功')
        else:
            ruleMsg = '业务规则校验通过'
        return ruleMsg