import os,time
from Base.Mylog import LogManager
from Base.OracleOper import MyOracle
from Base import ReadConfig
from Common.function import retDigitListFromStr
from Common.function import sqlJoiningDic
from Common.function import isNotBlank,isEmpty
from Base.MyDBOper import DbManager
from Common.TestAsserts import Assertion as alert



logger = LogManager('DataMap').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")
ora = MyOracle()

class DataMap(MyOracle):
    '''从Oracle获取数据'''
    def getDataMapSql(self,tabName,sqlref,conn=''):
        '''
        准备将DATA_MAPPING表迁移到本地Mysql数据库
        :param tabName: 表名
        :param sqlref: 语句标识
        :return: 返回一个sql语句
        '''
        if tabName == '' or sqlref == '':
            raise RuntimeError('必须传入tabName和sqlref入参!')

        Sqlexpr = """SELECT SQL_STMT,EXPR_COND,ROUTE FROM data_mapping  WHERE TAB_NAME = '{}' 
                     AND SQL_REF = '{}';""".format(tabName, sqlref)

        # if conn =='':
        #     Sqlexpr = """SELECT SQL_STMT,EXPR_COND,ROUTE FROM data_mapping  WHERE TAB_NAME = '{}' AND SQL_REF = '{}';""".format(tabName,sqlref)
        # else:
        #     Sqlexpr = """SELECT SQL_STMT,EXPR_COND,ROUTE FROM data_mapping  WHERE TAB_NAME = '{}' AND SQL_REF = '{}' AND ROUTE ='{}';""".format(tabName, sqlref,conn)
        # # logger.info('查询DATAMAPPING的sql语句：'.format(Sqlexpr))
        try:
            result = DbManager().select(Sqlexpr)
            logger.info('查询DATA_MAPPING结果:{}'.format(result))
            alert().assertFalse(isEmpty(result),msg='查询结果为空!')
            listResult = []
            for i in range(0, len(result)):
                if not conn =='':
                    route=conn   #如果传入了conn则按传入的查询
                else:
                    route = result[i]['ROUTE']
                logger.info(result[i])
                logger.info(result[i]['EXPR_COND'])
                if result[i]['EXPR_COND'] == None or result[i]['EXPR_COND'] == '':
                    sql = result[i]['SQL_STMT']
                else:
                    sql = result[i]['SQL_STMT'] + ' WHERE ' + result[i]['EXPR_COND']
                    print(sql)
                sqlDictRet = {'ROUTE': route, 'SQL': sql.replace('\n',' ').replace('\r',' ')} #可能存在多条记录，用listDict返回
                logger.info('查询返回的字典结果:{}'.format(sqlDictRet))
                listResult.append(sqlDictRet)
            logger.info('查询DataMapping结果返回:{}'.format(listResult))
            # return {'ROUTE': route, 'SQL': sql.replace('\n',' ').replace('\r',' ')}
            return listResult

        except:
            logger.info('查询异常!')


    def qryByCodeParser(self,tabName,sqlref):
        '''
        通过tabName和sqlref组合条件查询DATA_MAPPING
        :param tabName: 表名
        :param sqlref: 语句标识
        :return: 返回一个sql语句
        '''
        Tab = 'DATA_MAPPING'
        Col = 'SQL_STMT,EXPR_COND,ROUTE'
        Sqlexpr = "TAB_NAME = '{}' AND SQL_REF = '{}'".format(tabName,sqlref)
        try:
            qryResult = self.getTabColValue(thin='cen1',tabName=Tab,ColName=Col,expr=Sqlexpr)
            print(qryResult)
            if len(qryResult) == 0:
                logger.info('查询结果为空')
            else:
                for i in range(0, len(qryResult)):
                    if not qryResult[i]['EXPR_COND'] is None :
                        sql = qryResult[i]['SQL_STMT'] + ' WHERE ' + qryResult[i]['EXPR_COND']
                    else:
                        sql = qryResult[i]['SQL_STMT'] + ' WHERE '
        except :
            logger.info('查询异常!')
        return sql

    def qryByCodeParserList(self,tabName):
        '''
        通过tabName和sqlref组合条件查询DATA_MAPPING
        :param tabName: 表名
        :param sqlref: 语句标识
        :return:返回一个list
        '''
        Tab = 'DATA_MAPPING'
        Col = 'SQL_STMT,EXPR_COND,ROUTE'
        Sqlexpr = "TAB_NAME = '{}'".format(tabName)
        SQL = []
        try:
            qryResult = self.getTabColValue(thin='cen1',tabName=Tab,ColName=Col,expr=Sqlexpr)
            print(qryResult)
            if len(qryResult) == 0:
                logger.info('查询结果为空')
            else:
                for i in range(0, len(qryResult)):
                    sql = qryResult[i]['SQL_STMT'] + ' WHERE ' + qryResult[i]['EXPR_COND']
                    SQL.append(sql)
        except :
            logger.info('查询异常!')
        return SQL

    def retDicParserCode(self,tabName,sqlref):
        '''
        通过tabName和sqlref组合条件查询DATA_MAPPING
        :param tabName: 表名
        :param sqlref: 语句标识
        :return:返回一个字典
        '''
        Tab = 'DATA_MAPPING'
        Col = 'SQL_STMT,EXPR_COND,ROUTE'
        Sqlexpr = "TAB_NAME = '{}' AND SQL_REF = '{}'".format(tabName,sqlref)
        dicResult = {}
        try:
            qryResult = self.getTabColValue(thin='cen1',tabName=Tab,ColName=Col,expr=Sqlexpr)
            logger.info(qryResult)
            if len(qryResult) == 0:
                logger.info('查询结果为空')
            else:
                for i in range(0, len(qryResult)):
                    route = qryResult[i]['ROUTE']
                    if not  qryResult[i]['EXPR_COND'] is None :
                        sql = qryResult[i]['SQL_STMT'] + ' WHERE ' + qryResult[i]['EXPR_COND'] + ' '
                        logger.info(sql)
                    else:
                        sql = qryResult[i]['SQL_STMT'] + ' WHERE '
                        logger.info(sql)
                    dicResult = {'ROUTE': route, 'SQL': sql}
        except :
            logger.info('查询异常!')
        logger.info('查询结果:{}'.format(dicResult))
        return dicResult


    def retDicParserList(self,tabName):
        '''
        通过tabName和sqlref组合条件查询DATA_MAPPING
        :param tabName: 表名
        :param sqlref: 语句标识
        :return:返回一个list
        '''
        Tab = 'DATA_MAPPING'
        Col = 'ROUTE,SQL_STMT,EXPR_COND'
        Sqlexpr = "TAB_NAME = '{}'".format(tabName)
        result = []
        try:
            qryResult = self.getTabColValue(thin='cen1',tabName=Tab,ColName=Col,expr=Sqlexpr)
            if len(qryResult) == 0:
                logger.info('查询结果为空')
            else:
                for i in range(0, len(qryResult)):
                    sql = qryResult[i]['SQL_STMT'] + ' WHERE ' + qryResult[i]['EXPR_COND']
                    route = qryResult[i]['ROUTE']
                    dicResult = {'ROUTE':route,'SQL':sql}
                    print(dicResult)
                    result.append(dicResult)
        except :
            logger.info('查询异常!')
        return result

    def qryDataMapExcatByCond(self,tabName,sqlref,cond,route=''):
        '''
        通过tabName和sqlref和cond组合条件查询DATA_MAPPING并执行sql
        :param tabName: 表名
        :param sqlref: 语句标识
        :param cond: 查询条件参数化
        :return:返回一个list
        '''
        retDict = self.getDataMapSql(tabName, sqlref,conn=route) #迁移到本地Mysql库，从本地库读取
        if len(retDict) == '0':
            logger.info('dataMapping返回结果为空!')
        else:
            for i in range(0,len(retDict)):
                sql = retDict[i]['SQL'].replace('\n',' ')
                route = retDict[i]['ROUTE']
                if isinstance(cond,tuple) or isinstance(cond,str):
                    sql = sql % cond    #如果传入都条件是字符串或者数组
                    logger.info('======查询sql语句:{}'.format(sql))
                elif isinstance(cond,dict):#如果传入字典
                    sql = sql + ' AND '.join('%s=%r' % (k, cond[k]) for k in cond) #查询条件，通过字典传入
                    logger.info('======查询sql语句:{}'.format(sql))
                ##注意如果route=-1则表示要在mysql查询
                if route == '-1':
                    res = DbManager().select(sql=sql)
                else:
                    res = self.select(sql=sql,route=route)
                logger.info('======查询sql语句数据库返回结果:{}'.format(res))
                alert().assertFalse(isEmpty(res),msg='查询dataMap数据结果为空!')
                if len(res) == 0:
                    logger.info('查询结果为空')
                elif len(res) == 1:
                    logger.info('返回当前查询结果:{}'.format(res[0]))
                    result = res[0]  #如果查询出来的结果集只有一条数据，则直接取出来当做dict返回
                elif len(res)>1:   #查询数据库返回结果多条的话返回list
                    logger.info('返回当前查询结果:{}'.format(res))
                    result = res
        return result

    def retDataMapListByCond(self,tabName,sqlref,cond,route=''):
        '''
        通过tabName和sqlref和cond组合条件查询DATA_MAPPING并执行sql
        :param tabName: 表名
        :param sqlref: 语句标识
        :param cond: 查询条件参数化
        :return:返回一个list,不判断都返回list
        '''
        retDict = self.getDataMapSql(tabName, sqlref,conn=route) #迁移到本地Mysql库，从本地库读取
        alert().assertFalse(isEmpty(retDict),msg='dataMapping返回结果为空!')
        for i in range(0,len(retDict)):
            sql = retDict[i]['SQL'].replace('\n',' ')
            route = retDict[i]['ROUTE']
            if isinstance(cond,tuple) or isinstance(cond,str):
                sql = sql % cond    #如果传入都条件是字符串或者数组
                logger.info('======查询sql语句:{}'.format(sql))
            elif isinstance(cond,dict):#如果传入字典
                sql = sql + ' AND '.join('%s=%r' % (k, cond[k]) for k in cond) #查询条件，通过字典传入
                logger.info('======查询sql语句:{}'.format(sql))
            ##注意如果route=-1则表示要在mysql查询
            if route == '-1':
                result = DbManager().select(sql=sql)
            else:
                result = self.select(sql=sql,route=route)
            logger.info('======查询sql语句数据库返回结果:{}'.format(result))
            alert().assertFalse(len(result) == 0,msg='查询结果为空')

        return result


    def retDataMapList(self,tabName,sqlref,cond):
        '''
        通过tabName和sqlref和cond组合条件查询DATA_MAPPING并执行sql
        :param tabName: 表名
        :param sqlref: 语句标识
        :param cond: 查询条件参数化
        :return:返回一个list
        '''
        retDict = self.retDicParserCode(tabName,sqlref)
        alert().assertFalse(isEmpty(retDict),msg= 'dataMapping返回结果为空!')
        sql = retDict['SQL'].replace('\n',' ')
        route = retDict['ROUTE']
        if isinstance(cond,tuple) or isinstance(cond,str):
            sql = sql % cond    #如果传入都条件是字符串或者数组
            logger.info('======查询sql语句:{}'.format(sql))
        elif isinstance(cond,dict):#如果传入字典
            sql = sql + ' AND '.join('%s=%r' % (k, cond[k]) for k in cond) #查询条件，通过字典传入
            logger.info('======查询sql语句:{}'.format(sql))
        if route =='-1':
            paras = DbManager().select(sql=sql)
        else:
            paras = self.select(sql=sql, route=route)
        return paras

    def editDataMapByCond(self,tabName,sqlref,cond,route=''):
        '''
        通过tabName和sqlref和cond组合条件查询DATA_MAPPING并执行sql更新操作
        :param tabName: 表名
        :param sqlref: 语句标识
        :param cond: 查询条件参数化
        :return:返回一个list,不判断都返回list
        '''
        retDict = self.getDataMapSql(tabName, sqlref,conn=route) #迁移到本地Mysql库，从本地库读取
        alert().assertFalse(isEmpty(retDict),msg= 'dataMapping返回结果为空!')
        for i in range(0,len(retDict)):
            sql = retDict[i]['SQL'].replace('\n',' ')
            route = retDict[i]['ROUTE']
            if isinstance(cond,tuple) or isinstance(cond,str):
                sql = sql % cond    #如果传入都条件是字符串或者数组
                logger.info('======查询sql语句:{}'.format(sql))
            elif isinstance(cond,dict):#如果传入字典
                sql = sql + ' AND '.join('%s=%r' % (k, cond[k]) for k in cond) #查询条件，通过字典传入
                logger.info('======查询sql语句:{}'.format(sql))
            ##注意如果route=-1则表示要在mysql查询
            if route == '-1':
                # result = DbManager().select(sql=sql)
                DbManager().editDatas(sql)
            else:
                self.updateSQL(sql=sql,route=route)


if __name__ == '__main__':
    test = DataMap()
    # SQL = test.getDataMapSql(tabName='TF_F_USER_PRODUCT',sqlref='SelByProdId')
    # print(SQL)
    # test.qryDataMapExcatByCond(tabName='TF_F_REALNAME_INFO',sqlref='SelBySerialNum',cond='13997242287')
    # res = test.qryDataMapExcatByCond(tabName='TF_B_TRADE',sqlref='SelByOrderID',cond='7119013105881916')
    # res2 = test.qryDataMapExcatByCond(tabName='TF_B_TRADE_BROADBAND',sqlref='SELECT_ALL_BY_TRADEID',cond=('3120121187922472',time.strftime('%Y'),'3120121187922472'))
    # res2 = test.qryDataMapExcatByCond(tabName='AUTOTEST_CASE',sqlref='SEL_BY_SCENE_CODE',cond=('ChgMainProduct'))
    res2 = test.retDataMapListByCond(tabName='AUTOTEST_CASE',sqlref='SEL_BY_SCENE_CODE',cond=('ChgMainProduct'))

    print(res2)


    # sql = test.qryByCodeParser(tabName='TF_F_REALNAME_INFO',sqlref='SelBySerialNum')
    # sql = test.retDicParserList(tabName='TF_F_REALNAME_INFO')
    # res = test.retDicParserCode(tabName='TF_F_REALNAME_INFO',sqlref='SelByTransactionId')
    # print(res)
    # transaction_id = '97120201128103219080228'
    # sql = res['SQL'] %transaction_id
    # print(sql)
    # route = res['ROUTE']
    # result= MyOracle().select(sql=sql,route=route)
    # print(result)







