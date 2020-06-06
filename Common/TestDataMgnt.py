import os,time
import xlrd
from Base.GenTestData import GenTestData
from Base.OperExcel import write_dict_xls,getColumnIndex,getRowIndex
from Base.Mylog import LogManager
from Base.OracleOper import MyOracle
from Base import ReadConfig
from Common.function import join_dictlists

logger = LogManager('GroupBusiTest').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")
ora = MyOracle()

file = ReadConfig.data_path + 'UITest_TestData.xls'

def get_testDataFile(filepath = file):
    return filepath

def get_TestData(FuncCode,filename = file,index=0):
    '''根据FuncCode获取测试数据'''
    xl = xlrd.open_workbook(filename)
    sheet = xl.sheet_by_index(index)
    row = getRowIndex(file=filename,value=FuncCode)
    col = getColumnIndex(file=filename,columnName ='PARAMS') #该列指定
    paras = sheet.cell_value(row,col)  #取出来是个字符串
    paras = eval(paras)
    if isinstance(paras, tuple):
        params = list(paras)
    elif isinstance(paras,dict):
        params = paras
    return params # 转换成字典返回

def get_FuncRow(FuncCode,filename = file):
    '''根据测试函数获取对应的行数'''
    return getRowIndex(file=filename,value=FuncCode)

def create_testDataFile(paras,filename):
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
        paras = ora.select(conn=rc.get_oracle('cp_thin'),sql= sql_groupOffer)
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
        paras = ora.select(conn=rc.get_oracle('ec_thin'),sql= sql_GrpOfferInst)
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
        paras = ora.select(conn=rc.get_oracle('file4_thin'),sql= sql_MebOfferList)
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
        paras = ora.select(conn=rc.get_oracle('file4_thin'),sql= sql_GrpMeb)
        return paras


class MainPageData():
    '''登录首页测试数据，如菜单等'''
    def get_personMenu(self):
        '''个人业务菜单'''
        sql_menu = "select rownum No ,'' Result_info ,t.parent_id,t.func_code,t.name,t.viewname \
            from uop_param_c.sec_function t  where t.parent_id in ('crm9250','crm9220','crm9256','crm9260','crm9240','crm9200') \
            and t.viewname is not null and t.state ='1' "
        logger.info('获取个人业务菜单sql语句:{}'.format(sql_menu))
        paras = ora.select(conn=rc.get_oracle('param_thin'), sql=sql_menu)
        return paras

    def get_groupMenu(self):
        '''集团业务菜单'''
        sql_menu = "select rownum No ,'' Result_info ,t.parent_id,t.func_code,t.name,t.viewname \
            from uop_param_c.sec_function t  where t.parent_id in ('crm8100','crm8100','crm8100') \
            and t.viewname is not null and t.state ='1' "
        logger.info('获取个人业务菜单sql语句:{}'.format(sql_menu))
        paras = ora.select(conn=rc.get_oracle('param_thin'), sql=sql_menu)
        return paras



if __name__ == '__main__':
    now = time.strftime("%Y%m%d%H%M%S")
    # file_MebDel = ReadConfig.get_data_path() + 'UITest_GrpMebBusiDelTest_%s.xls' % now
    # filename =  ReadConfig.get_data_path() + 'UITest_GrpBusiSubTest_' + time.strftime("%Y%m%d%H%M%S") + '.xls'
    # file = create_testDataFile(paras = GrpTestData().get_GrpOfferInst(groupId= "'8712239560','8711400346'",offerId='6480',subOfferlist='100648000,100648001'),filename= filename)
    # print(file)
    params = get_TestData(filename=file,FuncCode='ChangeSimCardTest')
    print('params=',params)
    print(type(params))

    rowIndex = get_FuncRow('ChangeSimCardTest')
    print('row=',rowIndex)
    print(len(params))
    paras = list(params)