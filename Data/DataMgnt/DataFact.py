import os,time
from Base.Mylog import LogManager
from Base.OracleOper import MyOracle
from Base import ReadConfig
from Common.TestAsserts import Assertion as alert
from Common.function import retDigitListFromStr
from Common.function import sqlJoiningDic
from Base.MyDBOper import DbManager
from Data.DataMgnt.DataOper import DataOper as Dto


logger = LogManager('DataFact').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")
ora = MyOracle()

class DataFact(DbManager):
    '''数据工厂'''
    def getVauleByAttrCode(self,idType,attrCode):
        '''
        根据ID_TYPE 和 ATTR_CODE查询业务配置
        :param idType 类型_
        :param  attrCode: 属性编码
        :return:
        '''
        alert().assertIsNotNone(idType,msg='idType不允许为空！')
        alert().assertIsNotNone(attrCode,msg='attrCode不允许为空！')
        idType_attrCode =(idType,attrCode)
        alert().assertIsInstance(idType_attrCode,tuple,msg='必须传入元祖')
        valueParam = Dto().qryDataMapExcatByCond(tabName='AUTOTEST_FACTORY',sqlref='SEL_BY_IDTYPE_ATTRCODE',cond=idType_attrCode)
        if isinstance(valueParam,dict):
            attrValue = valueParam['ATTR_VALUE']
        elif isinstance(valueParam,list):
            attrValue = [valueParam[i].get('ATTR_VALUE') for i in range(0,len(valueParam))]
        return attrValue

    def getDataFact(self,attrCode,cond):
        '''
        获取数据工厂定义并执行sql获取结果
        :param idType:
        :param cond:查询条件
        :param attrCode:编码必须唯一
        :return:a
        '''
        attrValue = self.getVauleByAttrCode(idType='sql',attrCode=attrCode)
        listValue = attrValue.split('@')
        logger.info('返回的attrValue:{}'.format(listValue))
        alert().assertTrue(len(listValue)==3)
        return Dto().qryDataMapExcatByCond(route=listValue[0],tabName=listValue[1],sqlref=listValue[2],cond=cond)





if __name__ == '__main__':
    test = DataFact()
    # res = test.getVauleByAttrCode(idType='sql',attrCode='GetUserInfo')
    res = test.getDataFact(attrCode='GetUserSaleDepositInfo',cond='13755097494')
    print(res)

    # test.getVauleByAttrCode(idType_attrCode='22')

