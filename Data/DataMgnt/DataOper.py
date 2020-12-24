import os,time
from Base.Mylog import LogManager
from Base.OracleOper import MyOracle
from Base import ReadConfig
from Common.function import retDigitListFromStr
from Common.function import getDigitFromStr
from DataMap import DataMap
from Data.DataMgnt.GenTestData import GenTestData as Gen
from Common.TestAsserts import Assertion as Assert
# from Check.DataCheck import DataCheck as DC
import datetime
import json

logger = LogManager('DataOper').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")
ora = MyOracle()

class DataOper(DataMap):
    '''从Oracle获取数据'''
    def getSmsContent(self,accessNum):
        '''
        根据accessNum从数据库中提取短信内容
        :param accessNum:传入手机号码
        :return:SmsContentList 短信内容列表
        '''
        smsContent = self.qryDataMapExcatByCond(tabName='TI_O_SMS',sqlref='SEL_BY_SERIAL',cond=accessNum)
        logger.info('获取的短信内容:{}'.format(smsContent))
        # Assert().assertTrue(len(smsContent)>0,msg='没有查询到短信内容')
        if isinstance(smsContent,dict):
            logger.info('只有一条')
            sms = smsContent['NOTICE_CONTENT']
            logger.info('sms内容:{}'.format(sms))
        elif isinstance(smsContent,list):
            sms =[]
            for i in range(len(smsContent)):
                SmsContent = smsContent[i]['NOTICE_CONTENT']
                logger.info('短信内容是：{}'.format(SmsContent))
                sms.append(SmsContent)
        return sms

    def getSmsCode(self,accessNum):
        '''
        获取短信验证码
        :param accessNum: 手机号码
        :return:SmsCode 验证码默认返回最新的一个
        '''
        SmsContent = self.getSmsContent(accessNum)
        if len(SmsContent) == 0:
            logger.info('没有获取到短信内容，获取验证码失败！')
        elif isinstance(SmsContent,str):
            SmsCode = getDigitFromStr(SmsContent)
        elif isinstance(SmsContent,list):
            SmsCode = []
            for i in range(len(SmsContent)):
                if '验证码' in SmsContent[i]:
                    logger.info(SmsContent[i])
                    SmsCodeList = retDigitListFromStr(SmsContent[i])
                    print('========',SmsCodeList)
                    for k in range(len(SmsCodeList)):
                        if len(SmsCodeList[k]) == 6:
                            smsCode = SmsCodeList[k]
                            SmsCode.append(smsCode)
        return SmsCode

    def getRealNameInfoBySerialNum(self,serialNum):
        '''
        通过serialNum查询实名制信息
        :param serialNum: 手机号码
        :return:
        '''
        sqlParams = self.retDicParserCode(tabName='TF_F_REALNAME_INFO',sqlref='SelBySerialNum')
        sql = sqlParams['SQL'] %serialNum
        route = sqlParams['ROUTE']
        print(sql)
        print(route)
        return self.select(sql=sql,route='cp')

    def getCustRelaInfoBySerialNum(self,serialNum):
        '''
        通过serialNum查询实名制信息
        :param serialNum: 手机号码
        :return:
        '''
        userInfo = self.qryDataMapExcatByCond(tabName='TF_F_USER',sqlref='SEL_UserBySerialNum',cond=serialNum)
        logger.info('查询出来都用户信息：{}'.format(userInfo))
        custRelaInfo = self.qryDataMapExcatByCond(tabName='TF_F_CUST_PERSON_RELA',sqlref='SEL_BY_CUSTID',cond=userInfo['CUST_ID'])
        return custRelaInfo


    def updateRealNameInfoNew(self,accessNum):
        '''
        根据手机号码更新实名制信息-新增场景：如开户等
        :param assessNum: 手机号码
        :return:
        '''
        IdCard = Gen().Create_Idcard()  #随机gen一个身份证号码
        birthday = IdCard[6:10] + '-' + IdCard[10:12] + '-' + IdCard[12:14]
        cust_name = Gen().create_CustName() #随机gen一个客户姓名
        sysDate = self.getSysDate(route='cp')
        colValue = {'cust_name':cust_name,'pspt_id':IdCard,'verif_result':'1','pspt_addr':'湖南长沙市芙蓉区车站北路459号',
                    'sex':'1','nation':'1','birthday':birthday,'issuing_authority':'长沙市芙蓉区','cert_validdate':'2013-11-12',
                    'cert_expdate':'2033-11-12','state':'0','nationality':'1','pass_pspt':'123456789','pspt_issuesnum':'1'
                    }
        realNameInfo = self.qryDataMapExcatByCond(tabName='TF_F_REALNAME_INFO',sqlref='SEL_TRANID_BY_SERIAL',cond=accessNum)
        logger.info('====最近实名制认证信息:{}'.format(realNameInfo))
        Assert().assertTrue(len(realNameInfo)>0,msg='查询结果为空')
        dt_cond = {'TRANSACTION_ID':realNameInfo['TRANSACTION_ID']}
        self.updateData(route='cp',table='tf_f_realname_info',dt_update=colValue,dt_condition=dt_cond)

    def updateRealNameInfoExist(self, accessNum):
        '''
        根据手机号码更新实名制信息-存量场景：如补卡、过户等
        :param custAddr: 客户地址
        :param assessNum: 手机号码
        :return:
        '''
        IdCard = self.getCustRelaInfoBySerialNum(accessNum)['PSPT_ID']
        birthday = IdCard[6:10] + '-' + IdCard[10:12] + '-' + IdCard[12:14]
        cust_name = self.getCustRelaInfoBySerialNum(accessNum)['CUST_NAME']  # 取存量客户名称
        pspt_addr = self.getCustRelaInfoBySerialNum(accessNum)['PSPT_ADDR']  # 取存量证件地址
        colValue = {'cust_name': cust_name, 'pspt_id': IdCard, 'verif_result': '1', 'pspt_addr':pspt_addr ,
                    'sex': '1', 'nation': '1', 'birthday': birthday, 'issuing_authority': '长沙市芙蓉区',
                    'cert_validdate': '2013-11-12',
                    'cert_expdate': '2033-11-12', 'state': '0', 'nationality': '1', 'pass_pspt': '123456789',
                    'pspt_issuesnum': '1'
                    }
        realNameInfo = self.qryDataMapExcatByCond(tabName='TF_F_REALNAME_INFO',sqlref='SEL_TRANID_BY_SERIAL',cond=accessNum)
        logger.info('====最近实名制认证信息:{}'.format(realNameInfo))
        Assert().assertTrue(len(realNameInfo)>0,msg='查询结果为空')
        dt_cond = {'TRANSACTION_ID':realNameInfo['TRANSACTION_ID']}
        self.updateData(route='cp', table='tf_f_realname_info', dt_update=colValue, dt_condition=dt_cond)

    def getCasePara(self,sceneCode):
        '''
        根据场景编码获取案例执行参数
        :param sceneCode: 场景编码
        :return: list列表
        '''
        # paras = self.retDataMapList(tabName='AUTOTEST_CASE',sqlref='SEL_BY_SCENE_CODE',cond=sceneCode)
        paras = self.qryDataMapExcatByCond(tabName='AUTOTEST_CASE',sqlref='SEL_BY_SCENE_CODE',cond=sceneCode)
        logger.info('传入的Paras参数:{}'.format(paras))
        logger.info('传入的Paras的参数类型:{}'.format(type(paras)))
        if isinstance(paras,dict):
            logger.info('字典类型直接返回:{}'.format(paras))
            return paras
        elif isinstance(paras,list):
            listpara = []
            for i in range(0,len(paras)):
                # 因为读取出来的参数list数组里的元素都是Str先转换成字典后再讲参数部分组装到list返回
                param = {key: value for key, value in paras[i].items() if not key=='PARAMS'}
                if isinstance(paras[i]['PARAMS'],str):
                    paras[i]['PARAMS'].replace('\r','').replace('\n','')
                    logger.info('PARAMS数据库读取出来都类型是Str,需要转换成Dict')
                    inputPara = eval(paras[i]['PARAMS'])
                    print('==============',inputPara)
                    print('==============',type(inputPara))
                    if isinstance(inputPara,dict):
                        inputPara.update(param)
                        logger.info('转换后都Dict参数:{}'.format(inputPara))
                        listpara.append(inputPara)
                    if isinstance(inputPara,tuple):
                        print('转换都InPutPara都数据类型是tuple')
                        inputPara = list(inputPara)
                        for i in range(len(inputPara)):
                            Para = inputPara[i]
                            Para.update(param)
                            print('******再次转换成员dict后{}'.format(inputPara))
                            listpara.append(inputPara)
            logger.info('读取出来的原始参数:{}'.format(listpara))
            return listpara

    def getSysMenu(self,menuId):
        '''
        根据传入的menuId 获取菜单配置
        :param menuId: 菜单编码
        :return:
        '''
        paras = self.qryDataMapExcatByCond(tabName='AUTOTEST_MENU',sqlref='SEL_BY_FUNCID',cond=menuId)
        # logger.info('传入的Paras参数:{}'.format(paras))
        # logger.info('传入的Paras的参数类型:{}'.format(type(paras)))
        Assert().assertIsInstance(paras,dict,msg='获取的菜单配置不是字典，请检查配置')
        Assert().assertTrue(len(paras)>0,msg='获取菜单配置为空')
        Assert().assertIsNotNone(paras['menu_cata'],msg='菜单目录不能为空！')
        Assert().assertIsNotNone(paras['parent_func_id'],msg='父菜单不能为空！')
        Assert().assertIsNotNone(paras['func_id'],msg='菜单编码不能为空！')
        Assert().assertIsNotNone(paras['dll_path'],msg='菜单路径不允许为空！')
        Assert().assertIsNotNone(paras['module'],msg='所属模块不能为空！')
        return paras

    def getSysMenuByParentFuncId(self,parentFuncId):
        '''
        根据传入的menuId 获取菜单配置
        :param parentFuncId: 父菜单编码
        :return:
        '''
        paras = self.qryDataMapExcatByCond(tabName='AUTOTEST_MENU',sqlref='SEL_BY_PARENTFUNCID',cond=parentFuncId)
        # logger.info('传入的Paras参数:{}'.format(paras))
        # logger.info('传入的Paras的参数类型:{}'.format(type(paras)))
        Assert().assertIsInstance(paras,list,msg='获取的菜单配置不是列表，请检查配置！')
        Assert().assertTrue(len(paras) > 0, msg='获取菜单配置为空!')
        return paras


if __name__ == '__main__':
    # data =UpdateOraData()
    # sqlParams = {'pspt_id':'630121199311304817','cust_name':'朱丽华','verif_result':'1','pass_pspt':'123456789'}
    # sql = data.updateRealNameInfoBySerialNum(assessNum='15297156027',IdCard='630121199311304817',custName='王成林')
    # print(sql)
    # sel = SelectOraData()
    # result = sel.getSmsCode(accessNum='15809705551')
    # print('短信验证码：',result)
    # data.updateTabColValue(thin='cp',tabName='tf_f_realname_info',sqlParams=sqlParams,cond="SERIAL_NUMBER='15297156027'")
    # print (result)
    test = DataOper()
    # result = test.updateRealNameInfoBySerialNum(accessNum='13639750374')
    # result = test.getSysMenu(menuId='crm9115')

    result = test.getSysMenuByParentFuncId(parentFuncId=('crm9A00','crm9100'))
    print(result)

    # result = test.updateRealNameInfoExist(accessNum='13907491805')
    # # result = test.getSmsCode(accessNum='13897492180')
    # print(result)
    # print(type(result))


    # result = json.loads(result)

    # print(result)
    # print(type(result))

