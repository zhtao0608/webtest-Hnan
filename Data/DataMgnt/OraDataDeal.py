import os,time
from Base.Mylog import LogManager
from Base.OracleOper import MyOracle
from Base import ReadConfig
from Common.function import retDigitListFromStr

logger = LogManager('OracleDataDeal').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")
ora = MyOracle()


class SelectOraData(MyOracle):
    '''从Oracle获取数据'''
    def getTabColValue(self,thin,tabName,ColName,expr='1=1'):
        '''
        按传入的表达式获取相应字段的值
        :param thin: 连接串
        :param tabName: 表名
        :param ColName: 字段名，
        :param expr:表达式，where条件
        :return:
        '''
        chkSql = "SELECT {} FROM {} WHERE {}" .format(ColName,tabName,expr)
        logger.info(chkSql)
        result = ora.select(conn=rc.get_oracle(thin),sql= chkSql) #sql执行，返回的是字典列表
        # if len(result) == 0:  #如果查询结果是空,则返回False
        #     return False
        # else:
        logger.info(result)
        return result

    def getSmsContent(self,accessNum):
        '''
        根据accessNum从数据库中提取短信内容
        :param accessNum:传入手机号码
        :return:SmsContentList 短信内容列表
        '''
        expr = " RECV_OBJECT = '%s' order by DEAL_TIME desc"  % accessNum
        paras= self.getTabColValue(thin='crm1_thin',tabName='TI_O_SMS',ColName='NOTICE_CONTENT',expr=expr)
        print(len(paras))
        # Assertion().assertNotEqual(len(paras),0,msg='没有获取到短信内容')
        SmsContentList = []
        if len(paras) == 0 :
            logger.info('没有查询到短信内容')
            return SmsContentList
        else:
            for i in range(len(paras)):
                SmsContent = paras[i]['NOTICE_CONTENT']
                logger.info('短信内容是：{}'.format(SmsContent))
                SmsContentList.append(SmsContent)
            return SmsContentList

    def getSmsCode(self,accessNum):
        '''
        获取短信验证码
        :param accessNum: 手机号码
        :return:SmsCode 验证码默认返回最新的一个
        '''
        SmsContentList = self.getSmsContent(accessNum)
        if len(SmsContentList) == 0:
            logger.info('没有获取到短信内容，获取验证码失败！')
        else:
            ListSmsCode = []
            for i in range(len(SmsContentList)):
                if '验证码' in SmsContentList[i]:
                    logger.info(SmsContentList[i])
                    SmsCodeList = retDigitListFromStr(SmsContentList[i])
                    print('========',SmsCodeList)
                    for k in range(len(SmsCodeList)):
                        if len(SmsCodeList[k]) == 6:
                            smsCode = SmsCodeList[k]
                            ListSmsCode.append(smsCode)
                            return ListSmsCode[0] #默认返回第一个也就是最近的一个验证码


class UpdateOraData(MyOracle):
    '''更新Oracle数据'''
    def updateTabColValue(self,thin,tabName,sqlParams={},expr='1=1'):
        '''
        按传入的表达式获取相应字段的值
        :param thin: 连接串
        :param tabName: 表名
        :param ColName: 字段名，
        :param expr:表达式，where条件
        :return:
        '''
        if not isinstance(sqlParams,dict):
            logger.info('sqlParams入参必须是dict类型')
        if len(sqlParams)==0:
            logger.info('sqlParams入参为空')
        for colName,value in sqlParams.items():
            print(colName,value)
            if isinstance(value,str):
                value = "'" + value + "'"
            UPDSQL = "UPDATE {} SET ".format(tabName) + colName + "=" + value + " WHERE " + expr
            logger.info(UPDSQL)
            self.updateSQL(conn=rc.get_oracle(thin),sql=UPDSQL)  #执行update
        # return UPDSQL
        #cur.execute('insert into SCOTT.STUDENTS (id, name, age) values (:student_id, :student_name, :student_age)',student)



    def updateRealNameInfoBySerialNum(self,assessNum,IdCard,custName,custAddr='湖南省长沙市芙蓉区车站北路459号'):
        '''
        根据手机号码更新实名制信息
        :param IdCard: 身份证
        :param custName: 客户名称
        :param custAddr: 客户地址
        :param assessNum: 手机号码
        :return:
        '''
        birthday = IdCard[6:10] + '-' + IdCard[10:12] + '-' + IdCard[12:14]
        updRealNameInfoSQL = "update UOP_CP.tf_f_realname_info t \
           set cust_name         = '{}' ,\
               pspt_id           = '{}',\
               verif_result      = '1',\
               pspt_addr         = '{}',\
               sex               = '0',\
               nation            = '1',\
               birthday          = '{}',\
               issuing_authority = '长沙市芙蓉区',\
               cert_validdate    = '2013-11-12',\
               cert_expdate      = '2033-11-12',\
               state             = '0',\
               nationality       = '1',\
               pass_pspt         = '123456789',\
               pspt_issuesnum    = '1'\
         where t.SERIAL_NUMBER = '{}'".format(custName,IdCard,custAddr,birthday,assessNum)
        logger.info(updRealNameInfoSQL)
        self.updateSQL(sql=updRealNameInfoSQL,conn=rc.get_oracle('cp_thin'))
        return updRealNameInfoSQL

if __name__ == '__main__':
    # data =UpdateOraData()
    # sql = data.updateRealNameInfoBySerialNum(assessNum='15297156027',IdCard='630121199311304817',custName='王成林')
    # print(sql)
    sel = SelectOraData()
    result = sel.getSmsCode(accessNum='15809705551')
    print('短信验证码：',result)
    # sqlParams = {'pspt_id':'630121199311304817','cust_name':'王成林'}
    # data.updateTabColValue(thin='cp_thin',tabName='tf_f_realname_info',sqlParams=sqlParams,expr="SERIAL_NUMBER='15297156027'")
    # # print (result)