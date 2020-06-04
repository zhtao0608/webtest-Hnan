from Base.base import Base
from selenium.webdriver.common.by import By
from Common import ReadConfig
from Common.Mylog import LogManager
from Common.OperExcel import write_excel_append,write_xlsBycolName_append
import time,sys

# logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
logger = LogManager('PageAssert').get_logger_and_add_handlers(1, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

rc = ReadConfig.ReadConfig("ngboss_config.ini")

class PageAssert(Base):
    '''页面检查点'''
    def assert_Submit(self):
        """判断是否定位到页面返回信息"""
        loc_flow = (By.ID, 'flowId')
        Loc_msg = (By.XPATH,"//*[@class='c_msg c_msg-h c_msg-phone-v c_msg-full c_msg-error' and not(contains(@style,'display: none'))]/div/div[2]/div[1]/div[2]")
        try:
            flag = self.isElementDisplay(loc_flow)
            if flag :
                flowId = self.isElementDisplay(loc_flow,'text')
                time.sleep(2)
                logger.info("业务受理成功，交互流水：" + flowId)
                print("业务受理成功，交互流水：" + flowId)
                self.screen_step('业务受理成功，交互流水：{}'.format(flowId))
                return '业务受理成功：'+ flowId
            else:
                errmsg = self.isElementDisplay(Loc_msg,'text')
                time.sleep(3)
                logger.info('提交失败，错误信息：' + errmsg)
                print('提交失败，错误信息：' + errmsg)
                self.screen_step('业务受理失败：{}'.format(errmsg))
                return '业务受理失败：' + errmsg
        except :
            print('提交异常！测试退出')
            return False

    def assert_HelpPage(self):
        """获取WarnPage-help页面返回的公共信息,使用模糊匹配找出显示在当前页面上的warn提示并关闭"""
        loc_help = (By.XPATH,"//div[@class='c_msg c_msg-h c_msg-phone-v c_msg-full c_msg-help' and not(contains(@style,'display: none'))]")
        try:
            ele_help = self.find(loc_help)
            msg = ele_help.find_element_by_xpath('./div/div[2]/div[1]/div[2]').text
            logger.info('业务受理提示信息：{}'.format(msg))
            ele_btn = ele_help.find_element_by_xpath('./div/div[2]/div[2]/button[1]')
            self.click_on_element(ele_btn)
            # self.click_on_element(ele_btn) #我也不知道怎么点2次
            self.sendEnter()
            time.sleep(3)
            # return msg
        except :
            logger.info('没有弹出校验窗口默认校验通过，或者执行出现异常')
            msg = '校验通过'
        return msg

    def assert_WarnPage(self):
        """获取WarnPage页面返回的公共信息,使用模糊匹配找出显示在当前页面上的warn提示并关闭"""
        loc_warn = (By.XPATH,"//div[@class='c_msg c_msg-h c_msg-phone-v c_msg-full c_msg-warn' and not(contains(@style,'display: none'))]")
        try:
            ele_warn = self.find(loc_warn)
            msg = ele_warn.find_element_by_xpath('./div/div[2]/div[1]/div[2]').text
            step_str = "业务受理提示信息"
            logger.info('业务受理提示信息{}'.format(msg))
            self.screenshot_SaveAsDoc(step_str)
            ele_warn.find_element_by_xpath('./div/div[2]/div[2]/button').click() #关闭提示窗口
            self.sendEnter()
            time.sleep(2)
            msg = '出现警告信息' + msg
        except :
            logger.info('没有弹出告警！')
            msg = '警告校验通过'
        return msg

    def assert_SucPage(self):
        """获取WarnPage页面返回的公共信息,使用模糊匹配找出显示在当前页面上的sucess提示并关闭"""
        loc_suc = (By.XPATH,"//div[contains(@class,'c_msg-success') and not(contains(@style,'display: none'))]")
        try:
            ele_suc = self.find(loc_suc)
            time.sleep(2)
            msg = ele_suc.find_element_by_xpath('./div/div[2]/div[1]/div[2]').text
            time.sleep(3)
            step_str = "业务受理提示信息"
            logger.info('业务受理提示信息'.format(msg))
            self.screenshot_SaveAsDoc(step_str)
            self.screen_step('业务校验')
            ele_btn = ele_suc.find_element_by_xpath('./div/div[2]/div[2]/button')
            self.click_on_element(ele_btn)
            self.sendEnter()
            time.sleep(2)
            msg = '弹出校验成功信息：' + msg
        except :
            logger.info('未弹出assert_SucPage页面，跳过校验')
            msg = '没有弹出成功提示'
            print(msg)
            pass
        return msg

    def assert_ErrPage(self):
        """获取WarnPage页面返回的公共信息,使用模糊匹配找出显示在当前页面上的warn提示并关闭"""
        loc_err = (By.XPATH,"//div[@class='c_msg c_msg-h c_msg-phone-v c_msg-full c_msg-error' and not(contains(@style,'display: none'))]")
        try:
            ele_err = self.find(loc_err)
            time.sleep(2)
            msg = ele_err.find_element_by_xpath('./div/div[2]/div[1]/div[2]').text
            logger.info("业务校验失败:{}".format(msg))
            step_str = "业务校验失败"
            self.screenshot_SaveAsDoc(step_str)
            # ele_err.find_element_by_xpath('./div/div[2]/div[4]/button[1]').click()
            # self.sendEnter()
            time.sleep(2)
            msg = '业务校验失败' + msg
            return msg
        except :
            logger.info('未弹出assert_ErrPage页面，跳过校验')
            return False

    # def assert_ErrsPage(self):
    #     """获取WarnPage页面返回的公共信息,使用模糊匹配找出显示在当前页面上的warn提示并关闭"""
    #     try:
    #         # err_eles = self.driver.find_elements_by_xpath('//div[@class="c_msg c_msg-h c_msg-phone-v c_msg-full c_msg-error"]') #找到所有的errorPage
    #         # err_eles = self.findeles(By.XPATH,'//div[@class="c_msg c_msg-h c_msg-phone-v c_msg-full c_msg-error"]')
    #         err_eles = self.findeles(By.XPATH,'//div[contains(@class,"c_msg-error")]')
    #         time.sleep(5)
    #         print('err_eles错误提示出现:',len(err_eles)) ##为什么始终只找到一个
    #         print('err_eles:',err_eles)
    #         for ele in err_eles:
    #             flag = self.is_element_displayed(ele)
    #             logger.info('错误提示元素是否显示==={}'.format(flag))
    #             if flag:
    #                 ele_content = ele.find_element_by_xpath("./div/div[2]/div[1]/div[2]") #当前路径找内容
    #                 time.sleep(2)
    #                 logger.info('ele_content报错提示内容对应的ID属性值：' + ele_content.get_attribute('id'))
    #                 errMsg = ele_content.text
    #                 logger.info('报错信息：' + errMsg)
    #                 step_str = "业务受理提示信息"
    #                 logger.info('业务受理提示信息{}'.format(errMsg))
    #                 self.screenshot_SaveAsDoc(step_str)
    #                 try:
    #                     ele.find_element_by_xpath("./div/div[2]/div[4]/button[1]").click() #当前路径找取消按钮并点击
    #                     time.sleep(2)
    #                 except:
    #                     ele.find_element_by_xpath("./div/div[2]/div[2]/button").click()
    #                 return errMsg
    #                 break
    #             else:
    #                 logger.info('找不到显示在页面的报错信息')
    #                 continue
    #     except :
    #         logger.info('assert_ErrPage页面异常，无法获取页面返回信息')
    #         return False

    def assert_error(self):
        """获取WarnPage页面返回的公共信息,使用模糊匹配找出显示在当前页面上的warn提示并关闭"""
        loc_err = (By.XPATH,"//div[contains(@class,'c_msg-error' ) and not(contains(@style,'display: none'))]")
        try:
            ele_err = self.find(loc_err)
            logger.info('找到err元素:{}'.format(str(ele_err)))
            time.sleep(2)
            msg = ele_err.find_element_by_xpath('./div/div[2]/div[1]/div[2]').text
            logger.info("业务校验失败:{}".format(msg))
            step_str = "业务校验失败"
            self.screen_step(step_str)  #这个保存在测试记录文档中
            self.screenshot_SaveAsDoc(step_str) #截图单独保存到doc
            time.sleep(3)
            msg = '业务校验失败:' + msg
        except :
            logger.info('业务校验通过!')
            msg = '业务校验通过'
        return msg

    def assert_WadeMsg(self):
        try:
            Msg = self.assert_error()
            if '业务校验通过' in Msg:
                Msg = self.assert_SucPage()
                if '没有弹出成功提示' in Msg:
                    Msg = self.assert_WarnPage()
        except:
            logger.info('未弹出校验提示信息，默认通过')
            Msg = '校验通过'
            pass
        return Msg

    def assert_SubmitPage(self):
        """获取WarnPage页面返回的公共信息,使用模糊匹配找出显示在当前页面上的sucess提示并关闭"""
        loc_suc = (By.XPATH,"//div[contains(@class,'c_msg-success') and not(contains(@style,'display: none'))]")
        try:
            ele_suc = self.find(loc_suc)
            time.sleep(2)
            msg = ele_suc.find_element_by_xpath('./div/div[2]/div[1]/div[2]').text
            time.sleep(3)
            step_str = "业务受理成功：{}".format(msg)
            logger.info('业务受理成功'.format(msg))
            self.screen_step(step_str)
            msg = '业务受理成功,' + msg
        except :
            logger.info('未弹出业务受理成功提示')
            print('未弹出业务受理成功提示')
            msg = self.assert_error()
        return msg


    """==============================处理页面返回信息====================================="""

    """====================处理业务受理异常提示======================"""
    def check_RuleAfter(self):
        '''业务提交后校验'''
        loc_content = (By.XPATH,"//*[starts-with(@id,'wade_messagebox') and contains(@class,'content')]")
        flag = self.is_element_located(loc_content)
        if not flag:
            logger.info("未出现规则校验异常，通过")
            pass
            return True
        else:
            msg = self.isElementDisplay(loc_content, 'text')
            print("错误提示：", msg)
            step_str = "业务受理规则异常{}".format(msg)
            self.screenshot_SaveAsDoc(step_str)
            return False

    def check_RuleBefore(self):
        '''提交前校验，页面出现异常或者业务规则异常'''
        loc_content = (By.XPATH,'//div[contains(@class,"c_msg c_msg-full c_msg-h c_msg-error c_msg-phone-v"]/div/div[2]/div[1]/div[2]')
        flag = self.isElementDisplay(loc_content)
        if not flag:
            logger.info("未出现规则校验异常，通过！")
            return
        else:
            msg = self.isElementDisplay(loc_content, 'text')
            step_str = "错误提示:{}".format(msg)
            logger.info(step_str)
            self.screenshot_SaveAsDoc(step_str)
            return msg

    def deal_resultAftersubmit(self,file,row,index=0):
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
                logger.info("业务受理成功，交互流水号写入xls中FlowId列")
                write_excel_append(file, row, 2, Msg,index)  #向xls模板指定行列写入结果
            elif '业务受理失败':
                logger.info("业务受理失败，错误信息写入xls中x_result_info列")
                write_excel_append(file, row, 3, Msg,index) #向xls模板指定行列写入结果
        except :
            logger.info("测试结果写入xls发生异常！")
            write_excel_append(file, row, 3, '提交发生异常', index)  # 向xls模板指定行列写入结果

    def write_testResult(self,file,row,index=0):
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
            write_xlsBycolName_append(file, row, 'RESULT_INFO', '测试异常', index)  # 向xls模板指定行列写入结果


    def write_vaildErrResult(self,file,row,index=0):
        '''
        测试结果写入xls，按xls模板已将flowId 和errmsg列指定了
        :param file: xls完整路径
        :param row: xls行号
        :param index: xls的sheet页index
        :return:
        '''
        Msg = self.assert_error()
        if '业务校验失败' in Msg:
            logger.info("业务校验，错误信息写入xls中RESULT_INFO列")
            write_xlsBycolName_append(file, row, 'RESULT_INFO', Msg,index)  #向xls模板指定行列写入结果
        return Msg
