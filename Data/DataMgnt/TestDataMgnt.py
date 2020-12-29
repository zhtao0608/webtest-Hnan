import os,time
import xlrd
from Base.OperExcel import write_dict_xls,getColumnIndex,getRowIndex
from Base.Mylog import LogManager
from Base.OracleOper import MyOracle
from Base import ReadConfig
from Common.dealParas import convertParatoList

logger = LogManager('TestDataMgnt').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")
ora = MyOracle()

class TestDataExcel():
    '''处理TestData 表格'''
    def __init__(self):
        # self.file = ReadConfig.data_path + 'UITest_TestData_%s.xls' %(time.strftime(("%Y%m%d")))
        self.file = ReadConfig.data_path + 'UITest_TestData.xls'

    def get_testDataFile(self):
        filepath = self.file
        return filepath

    def get_TestData(self,FuncCode,index=0):
        '''
        根据FuncCode获取测试数据，并统一转换成List数据结构，方便DDT数据驱动
        :param FuncCode:案例编码
        :param filename:测试数据管理文件
        :param index:xls模板的sheet索引，默认第一个sheet页
        :return:返回一个字典，数据文件Filename和对应的参数Params（List类型）
        '''
        filename = self.file
        xl = xlrd.open_workbook(filename)
        sheet = xl.sheet_by_index(index)
        row = getRowIndex(file=filename,value=FuncCode)
        col = getColumnIndex(file=filename,columnName ='PARAMS') #该列指定
        paras = sheet.cell_value(row,col)  #取出来是个字符串
        logger.info('测试案例编码:{},读取出来的原始参数:{},数据类型:{}'.format(FuncCode,paras,type(paras)))
        params = convertParatoList(paras)  #将传入参数类型统一成List列表返回
        row = self.get_FuncRow(FuncCode)
        dic_fileParas = {'filename':filename,'params':params,'FuncRow':row}
        return dic_fileParas # 转换成字典返回

    def get_FuncRow(self,FuncCode):
        '''根据测试函数获取对应的行数'''
        filename = self.file
        return getRowIndex(file=filename,value=FuncCode)

    def create_testDataFile(self,paras,filename):
        '''自动生成测试数据file，返回完整的dataFile路径'''
        file = filename
        write_dict_xls(inputData=paras, sheetName='AutoTestData', outPutFile=file)
        logger.info('写入测试数据到xls.....')
        return file


class GrpTestData():
    '''集团测试数据管理'''
    def get_GrpOffer(self,groupId,offerId,subOfferlist):
        '''
        订购ADC的测试数据
        测试集团groupId = 8711400346
        主商品：6480 可变
        '''
        sql_groupOffer = "select rownum No ,'' result_info ,'' flowid ,t.group_id,t.group_name ,'%s' offer_id,  \
         '%s' subOfferList from uop_cp.cb_enterprise t \
        where group_id in (%s)"  % (offerId,subOfferlist,groupId)
        logger.info('获取集团商品订购的sql语句:{}'.format(sql_groupOffer))
        paras = ora.select(route='crm1',sql= sql_groupOffer)
        return paras

    def get_GrpOfferInst(self,groupId,offerId):
        '''
        注销集团商品数据
        groupId 集团编码
        offerId 集团主商品Offer_id
        '''
        sql_GrpOfferInst = "select rownum No ,'' result_info ,'' flowid , b.group_id ,b.group_name, \
            to_char(t.SUBSCRIBER_INS_ID) SUBSCRIBER_INS_ID,t.OFFER_ID,to_char(t.OFFER_INS_ID) grp_offer_ins_id ,t.OFFER_NAME \
            from uop_ec.um_offer_06 t, uop_ec.um_subscriber a ,uop_cp.cb_enterprise b ,uop_ec.UM_PROD_STA m \
            where t.IS_MAIN = '1' and t.EXPIRE_DATE > sysdate and t.OFFER_TYPE = '10' and t.OFFER_ID ='%s' \
            and a.subscriber_ins_id = t.SUBSCRIBER_INS_ID and a.remove_tag = 0  and b.mgmt_district = '0872' \
            and a.subscriber_ins_id = m.SUBSCRIBER_INS_ID  and m.IS_MAIN = '1' \
            and a.cust_id = b.orga_enterprise_id and group_id in (%s) and rownum <=3" %(offerId,groupId)

        logger.info('获取集团商品订购实例sql语句:{}'.format(sql_GrpOfferInst))
        paras = ora.select(route='ec',sql= sql_GrpOfferInst)
        return paras

    def get_GrpMebOfferInst(self,grpOfferId):
        '''活动集团成员订购实例信息
        grpOfferId 集团主商品ID
        '''
        sql_MebOfferList = "select rownum No,'' result_info ,'' flowid, a.rel_access_num access_Num ,to_char(a.subscriber_ins_id) grp_subscriber_ins_id, \
        b.group_id,b.group_name,to_char(t.OFFER_ID) OFFER_ID ,to_char(t.OFFER_INS_ID) GRP_OFFER_INS_ID,t.OFFER_NAME \
        from uop_file4.um_subscriber_rel a  ,uop_ec.um_offer_06 t, uop_ec.um_subscriber m ,uop_cp.cb_enterprise b \
        where 1=1 and a.subscriber_ins_id = m.subscriber_ins_id \
        and a.subscriber_ins_id = t.SUBSCRIBER_INS_ID  \
        and t.IS_MAIN = '1' and t.EXPIRE_DATE > sysdate and t.OFFER_TYPE = '10' \
        and t.OFFER_ID ='%s' and a.expire_date > sysdate \
        and  m.remove_tag = 0 and  m.cust_id = b.orga_enterprise_id \
        and rownum <=3" %(grpOfferId)

        logger.info('获取集团成员商品订购实例sql语句:{}'.format(sql_MebOfferList))
        paras = ora.select(route='crm1',sql= sql_MebOfferList)
        return paras

    def get_MebAccessNumList(self,AccessNumList,subOfferList):
        '''
        获取集团成员订购号码以及订购的子商品
        :param AccessNum:
        :param subOfferList:
        :return:
        '''
        sql_GrpMeb = "select t.access_num ,'%s' subofferList from uop_file4.um_subscriber t \
        where t.access_num in (%s)  and t.remove_tag = '0' and rownum <=3 "  % (subOfferList,AccessNumList)

        logger.info('获取集团成员sql语句:{}'.format(sql_GrpMeb))
        paras = ora.select(conn=rc.get_oracle('crm1'),sql= sql_GrpMeb)
        return paras


class MainPageData():
    '''登录首页测试数据，如菜单等'''
    def get_personMenu(self):
        '''个人业务菜单'''
        sql_menu = "select rownum No ,'' Result_info ,t.parent_id,t.func_code,t.name,t.viewname \
            from uop_param_c.sec_function t  where t.parent_id in ('crm9250','crm9220','crm9256','crm9260','crm9240','crm9200') \
            and t.viewname is not null and t.state ='1' "
        logger.info('获取个人业务菜单sql语句:{}'.format(sql_menu))
        paras = ora.select(conn=rc.get_oracle('base'), sql=sql_menu)
        return paras

    def get_groupMenu(self):
        '''集团业务菜单'''
        sql_menu = "select rownum No ,'' Result_info ,t.parent_id,t.func_code,t.name,t.viewname \
            from uop_param_c.sec_function t  where t.parent_id in ('crm8100','crm8100','crm8100') \
            and t.viewname is not null and t.state ='1' "
        logger.info('获取个人业务菜单sql语句:{}'.format(sql_menu))
        paras = ora.select(conn=rc.get_oracle('base'), sql=sql_menu)
        return paras

if __name__ == '__main__':
    now = time.strftime("%Y%m%d%H%M%S")
    Data = TestDataExcel()
    paras = Data.get_TestData('CrtMbColorRing')
    # paras = get_TestData('CanelGrpIms')['params']
    print(paras)
    print(type(paras))
    print(len(paras))
    # for i in range(0,len(paras)):
    #     print(paras[i])
    #     print(type(paras[i]))
    #     subOfferList = paras[i]['SUBOFFERLIST']
    #     print(subOfferList)
    #     print(type(subOfferList))

    # print('=====',subOfferList)
    # print('=====',type(subOfferList))

    # paras_sep = get_TestData(FuncCode='ChgPayRelaSeprate')['params']
    # logger.info('普通付费关系变更测试准备数据:{}'.format(paras_sep))
    # params.extend(paras_sep)
    # # 合帐
    # paras_merge = get_TestData(FuncCode='ChgPayRelaMerge')['params']
    # logger.info('普通付费关系变更测试准备数据:{}'.format(paras_merge))
    # params.extend(paras_merge)
    # params = params
    # print(params)
    # print('======合并后=====',params)


    # rowIndex = get_FuncRow('ChangeSimCardTest')
    # print('row=',rowIndex)
    # print(len(params))
    # paras = list(params)
    # GrpMebsubList = []
    # file = get_TestData('SubGrpVpmnMeb')['filename']
    # AdcMebsubList = get_TestData('SubGrpAdcMeb')['params']  # ADC集团管家成员订购
    # # GrpMebsubList.extend(AdcMebsubList)
    # VpmnMebsubList = get_TestData('SubGrpVpmnMeb')['params']  # Vpmn成员订购
    # GrpMebsubList.extend(VpmnMebsubList)
    # ImsMebsubList = get_TestData('SubGrpImsMeb')['params']  # 多媒体桌面电话成员订购
    # GrpMebsubList.extend(ImsMebsubList)
    # print('集团成员订购参数:{}'.format(GrpMebsubList))
    # DelVpmnMebOfferList = get_TestData('DelGrpMebOffer')['params']  # 成员商品注销
    # print('成员商品注销参数:{}'.format(DelVpmnMebOfferList))
    #
    # paras = get_TestData('FamilyNetTest')['params']
    # row = get_FuncRow('FamilyNetTest')
    # print('亲情网受理参数:{}'.format(paras))
    #
    # paras = get_TestData(FuncCode='OpenGrpVpmn')['params']
    # # file = get_TestData(FuncCode='ChangeSimCardTest')['filename']
    # # row = get_TestData(FuncCode='ChangeSimCardTest')['FuncRow']
    # print('换卡参数:{}'.format(paras))
    #
    # Paras = get_TestData('SubscriberOpen')['params'][0]
    # busicode = Paras['BUSI_CODE']
    # row = get_TestData('SubscriberStop')['FuncRow'] if busicode == '131' else get_TestData('SubscriberOpen')['FuncRow']
    # print('====row=：',row)
