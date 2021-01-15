import os,time
from Base.Mylog import LogManager
from Base.OracleOper import MyOracle
from Base import ReadConfig
from Common.function import retDigitListFromStr,getDigitFromStr,isNotBlank,isEmpty
from Common.dealParas import convert_to_diclistUpper,capital_to_upper
from DataMap import DataMap
from Data.DataMgnt.GenTestData import GenTestData as Gen
from Common.TestAsserts import Assertion as Assert
from Common.dealParas import ConvertParas
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
        Assert().assertFalse(isEmpty(userInfo),msg='查询的用户信息返回空')
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
        # sysDate = self.getSysDate(route='cp')
        colValue = {'cust_name':cust_name,'pspt_id':IdCard,'verif_result':'1','pspt_addr':'湖南长沙市芙蓉区车站北路459号','serial_number':accessNum,
                    'sex':'1','nation':'1','birthday':birthday,'issuing_authority':'长沙市芙蓉区','cert_validdate':'2013-11-12',
                    'cert_expdate':'2033-11-12','state':'0','nationality':'1','pass_pspt':'123456789','pspt_issuesnum':'1'
                    }
        # realNameInfo = self.qryDataMapExcatByCond(tabName='TF_F_REALNAME_INFO',sqlref='SEL_TRANID_BY_SERIAL',cond=accessNum)
        realNameInfo = self.qryDataMapExcatByCond(tabName='TF_F_REALNAME_INFO',sqlref='SEL_MIN_1',cond=None)
        logger.info('====最近实名制认证信息:{}'.format(realNameInfo))
        Assert().assertTrue(isNotBlank(realNameInfo),msg='查询结果为空')
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
        # birthday = IdCard[6:10] + '-' + IdCard[10:12] + '-' + IdCard[12:14]
        birthday = '1994-05-06'  #因湖南证件号码RELA表模糊化了，这里先写死
        cust_name = self.getCustRelaInfoBySerialNum(accessNum)['CUST_NAME']  # 取存量客户名称
        pspt_addr = self.getCustRelaInfoBySerialNum(accessNum)['PSPT_ADDR']  # 取存量证件地址
        colValue = {'cust_name': cust_name, 'pspt_id': IdCard, 'verif_result': '1', 'pspt_addr':pspt_addr ,
                    'sex': '1', 'nation': '1', 'birthday': birthday, 'issuing_authority': '长沙市芙蓉区',
                    'cert_validdate': '2013-11-12',
                    'cert_expdate': '2033-11-12', 'state': '0', 'nationality': '1', 'pass_pspt': '123456789',
                    'pspt_issuesnum': '1'
                    }
        realNameInfo = self.qryDataMapExcatByCond(tabName='TF_F_REALNAME_INFO',sqlref='SEL_MIN_1',cond=None)
        logger.info('====最近实名制认证信息:{}'.format(realNameInfo))
        # Assert().assertTrue(len(realNameInfo)>0,msg='查询结果为空')
        Assert().assertTrue(isNotBlank(realNameInfo),msg='查询结果为空')
        dt_cond = {'TRANSACTION_ID':realNameInfo['TRANSACTION_ID']}
        self.updateData(route='cp', table='tf_f_realname_info', dt_update=colValue, dt_condition=dt_cond)

    def getCasePara(self,sceneCode):
        '''
        根据场景编码获取案例执行参数
        为了实现TestCase执行时使用DDT驱动，这里使用retDataMapListByCond，将结果务必转换成list
        :param sceneCode: 场景编码
        :return: list列表
        '''
        #为了实现TestCase执行时使用DDT驱动，这里使用retDataMapListByCond，将结果务必转换成list
        paras = self.retDataMapListByCond(tabName='AUTOTEST_CASE',sqlref='SEL_BY_SCENE_CODE',cond=sceneCode)
        return ConvertParas(paras)


    def getSysMenu(self,menuId):
        '''
        根据传入的menuId 获取菜单配置
        :param menuId: 菜单编码
        :return:
        '''
        paras = capital_to_upper(self.qryDataMapExcatByCond(tabName='AUTOTEST_MENU',sqlref='SEL_BY_FUNCID',cond=menuId))
        # logger.info('传入的Paras参数:{}'.format(paras))
        # logger.info('传入的Paras的参数类型:{}'.format(type(paras)))
        Assert().assertIsInstance(paras,dict,msg='获取的菜单配置不是字典，请检查配置')
        Assert().assertTrue(len(paras)>0,msg='获取菜单配置为空')
        Assert().assertIsNotNone(paras['MENU_CATA'],msg='菜单目录不能为空！')
        Assert().assertIsNotNone(paras['PARENT_FUNC_ID'],msg='父菜单不能为空！')
        Assert().assertIsNotNone(paras['FUNC_ID'],msg='菜单编码不能为空！')
        Assert().assertIsNotNone(paras['DLL_PATH'],msg='菜单路径不允许为空！')
        Assert().assertIsNotNone(paras['MODULE'],msg='所属模块不能为空！')
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

    def getCoreMenuByCataId(self,cataId):
        '''
        根据传入的cataId菜单目录 获取重点菜单配置【目前只包括个人业务和家庭业务】
        :param cataId: 父菜单编码
        :return:
        '''
        paras = self.qryDataMapExcatByCond(tabName='AUTOTEST_MENU',sqlref='SEL_BY_CATAID',cond=cataId)
        Assert().assertIsInstance(paras,list,msg='获取的菜单配置不是列表，请检查配置！')
        Assert().assertTrue(len(paras) > 0, msg='获取菜单配置为空!')
        return paras

if __name__ == '__main__':
    test = DataOper()
    # test.updateRealNameInfoNew(accessNum='15274912179')
    test.updateRealNameInfoExist(accessNum='15274912179')
    # # params = test.getCasePara('CrtUsVPMN')
    # print(params)
    # print(type(params))


    # data =UpdateOraData()
    # sqlParams = {'pspt_id':'630121199311304817','cust_name':'朱丽华','verif_result':'1','pass_pspt':'123456789'}
    # sql = data.updateRealNameInfoBySerialNum(assessNum='15297156027',IdCard='630121199311304817',custName='王成林')
    # print(sql)
    # sel = SelectOraData()
    # result = sel.getSmsCode(accessNum='15809705551')
    # print('短信验证码：',result)
    # data.updateTabColValue(thin='cp',tabName='tf_f_realname_info',sqlParams=sqlParams,cond="SERIAL_NUMBER='15297156027'")
    # print (result)
    # result = test.updateRealNameInfoBySerialNum(accessNum='13639750374')
    # result = test.getSysMenu(menuId='crm9115')
    # result = test.getCoreMenuByCataId(cataId='crm991A')
    # print(result)
    # print(len(result))

    # result = test.updateRealNameInfoExist(accessNum='13907491805')
    # # result = test.getSmsCode(accessNum='13897492180')
    # print(result)
    # print(type(result))


    # result = json.loads(result)

    # print(result)
    # print(type(result))

