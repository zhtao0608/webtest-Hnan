# -*- coding:utf-8 -*-
# __author:Administrator
# date: 2017/12/28
import os,time
import json
import cx_Oracle
from Base import ReadConfig
from Base.Mylog import LogManager
from Common import function
from Common.function import sqlJoiningDic


logger = LogManager('MyOracle').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")

class MyOracle:
    """
    oracle数据库操作
    """
    global username, password, ip, port, service_name,cp,crm1,base
    username = rc.get_oracle('USERNAME')
    password = rc.get_oracle('PASSWORD')
    ip = rc.get_oracle('IP')
    port = rc.get_oracle('PORT')
    service_name = rc.get_oracle('SERVICE_NAME')
    # thin = username + "/" + password + "@" + ip +":" + port+ "/" + service_name
    cp = rc.get_oracle("cp")
    base = rc.get_oracle("base")
    crm1 = rc.get_oracle("crm1")
    jour1 = rc.get_oracle("jour1")
    # upc = rc.get_oracle("upc_thin")
    # res = rc.get_oracle("res_thin")

    def __init__(self):
        """
        初始化
        """
        self.tns = cx_Oracle.makedsn(ip, port,service_name)
        # self.in = self.username +"/"+ self.password+"@"+self.service_name
        print(self.tns)
        self.conn = None
        self.cursor = None

    def getRoute(self,route):
        '''
        获取路由
        :param route: 传入cp.crm1.jour1等字符串
        :return:
        '''
        return rc.get_oracle(route)


    def ReConnect(self,route):
        """
        建立连接
        """
        try:
            # self.conn = cx_Oracle.connect(username, password, self.tns)
            conn = self.getRoute(route)
            self.conn = cx_Oracle.connect(conn)
            # print(self.conn)
            logger.info('连接的DB：{}'.format(conn))
            self.cursor = self.conn.cursor()
            logger.info("Connect DB successfully!")
        except ConnectionError as e:
            print('数据库连接异常',e)
            logger.info(e)

    def disconnect(self):
        """关闭连接"""
        self.cursor.close()
        logger.info("Database closed!")
        self.conn.close()

    def executeSQL(self, sql):
        """
        数据操作
        :param sql:
        :return:
        """
        self.ReConnect()
        self.cursor.execute(sql)
        self.conn.commit()
        return self.cursor

    def get_all(self, cursor):
        """
        get all result after execute sql
        :param cursor:
        :return:
        """
        value = cursor.fetchall()
        return value

    def get_one(self, cursor):
        """
        get one result after execute sql
        :param cursor:
        :return:
        """
        value = cursor.fetchone()
        return value

    def select(self,sql,route):
        """查询返回字典格式"""
        list = []
        self.ReConnect(route)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        col_name = self.cursor.description
        for row in result:
            dict = {}
            for col in range(len(col_name)):
                key = col_name[col][0]
                value = row[col]
                dict[key] = value
            list.append(dict)
        ###把返回的list转换成json串,并格式化
        # js = json.dumps(list, ensure_ascii=False, indent=2, separators=(',', ':'))
        # 测试需要，我只返回列表即可
        self.disconnect()
        return list


    def insert(self, sql, list_param):
        '''
         list_param=[('ww1','job003',1333,2),('ss1','job004',1444,2)]
        #test_oracle.insert("insert into bonus(ENAME,JOB,SAL,COMM)values(:1,:2,:3,:4)",param)
        #也可以下面这样解决
        test_oracle.insert("insert into bonus(ENAME,JOB,SAL,COMM)values(:ENAME,:JOB,:SAL,:COMM)",param)
        '''

        try:
            self.cursor.executemany(sql, list_param)
            self.conn.commit()
            logger.info("Insert Db complete!")
        except Exception as e:
            logger.info(e)
        finally:
            self.disconnect()

    def insertData(self,table,dt,route):
        '''
        insert表数据
        :param route:路由
        :param table:表名
        :param dt:一个字典，要insert都列和值
        :return:
        '''
        try:
            ls = [(k, dt[k]) for k in dt if dt[k] is not None]
            self.ReConnect(route)
            sql = 'insert into %s (' % table + ','.join(i[0] for i in ls) + \
                  ') values (' + ','.join('%r' % i[1] for i in ls) + ')'
            print(sql)
            self.cursor.execute(sql)
            self.conn.commit()
            logger.info("Insert Db complete!")
        except Exception as e:
            logger.info(e)
            self.conn.rollback()
        finally:
            self.disconnect()

    def updateSQL(self, sql,route):
        """数据更新操作"""
        try:
            self.ReConnect(route)
            self.cursor.execute(sql)
            self.conn.commit()
            logger.info("Update DB Complete!")
        except Exception as e:
            logger.info(e)
        finally:
            self.disconnect()

    def updateData(self,route, dt_update, dt_condition, table):
        '''
        更新数据
        :param route:路由
        :param dt_update:update字典
        :param dt_condition:条件
        :param table:表名
        :return:
        '''
        try:
            self.ReConnect(route)
            sql = 'UPDATE %s SET ' % table + ','.join('%s=%r' % (k, dt_update[k]) for k in dt_update) \
                  + ' WHERE ' + ' AND '.join('%s=%r' % (k, dt_condition[k]) for k in dt_condition)
            logger.info(sql)
            # self.cursor.setinputsizes(t_val=cx_Oracle.TIMESTAMP)
            self.cursor.execute(sql)
            self.conn.commit()
            logger.info("Update DB Complete!")
        except Exception as e:
            logger.info(e)
            self.conn.rollback()
        finally:
            self.disconnect()

    def updateMany(self, tabName,route,colList,valueList,expr='1=1'):
        '''
        数据批量更新操作
        :param tabName: 表名
        :param conn: 连接
        :param colList: 表列名List，必须是list
        :param valueList:表列对应都必须是list
        :param expr:where条件表达式
        :return:
        '''
        if not isinstance(colList,list):
            logger.error('colList必须传入list类型')
        if not isinstance(valueList,list):
            logger.error('valueList必须传入list类型')
        if (len(colList)==0 or len(valueList)==0 ):
            logger.error('colList或者valueList不允许为空!')
        if not len(colList) == len(valueList) :
            logger.error('colList或者valueList长度必须一致!')
        colValueList = [(colList[i], valueList[i]) for i in range(len(valueList))]
        # colValueList必须是list[tuple(),tuple()...]或tuple(tuple(),tuple()...)的形式
        logger.info(colValueList)
        for i in range(len(colValueList)):
            try:
                self.ReConnect(route)
                sql = "UPDATE {} SET ".format(tabName) + "%s = '%s'" % colValueList[i] + " where {}".format(expr)
                logger.info(sql)
                self.cursor.execute(sql)
                self.conn.commit()
                logger.info("Update DB Complete!")
            except Exception as e:
                logger.info(e)
            finally:
                self.disconnect()


    def delete(self, sql):
        """删除操作"""
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            logger.info("Delete Db ok!")
        except Exception as e:
            logger.info(e)
        finally:
            self.disconnect()

    def getTabColValue(self,thin,tabName,ColName,expr='1=1 '):
        '''
        按传入的表达式获取相应字段的值
        :param thin: 连接串
        :param tabName: 表名
        :param ColName: 字段名，
        :param expr:表达式，where条件表达式
        :return:
        '''

        Sql = "SELECT {} FROM {}  WHERE {}" .format(ColName,tabName,expr)
        logger.info(Sql)
        result = self.select(route=thin,sql= Sql) #sql执行，返回的是字典列表
        logger.info(result)
        return result

    def updateTabColValue(self,route,tabName,sqlParams={},cond='1=1'):
        '''
        按传入的表达式获取相应字段的值
        :param route: 路由
        :param tabName: 表名
        :param sqlParams: 一个字典，{'COLNAME':'value'} 对应要更新都字段和值
        :param cond:表达式，where条件
        :return:
        '''
        updateExpr = sqlJoiningDic(sqlParams)  #先获取要更新都表达式
        UPDSQL = "UPDATE {} SET ".format(tabName) + updateExpr + " WHERE " + cond
        logger.info(UPDSQL)
        self.updateSQL(route=route,sql=UPDSQL)  #执行update

    def getSysDate(self,route,sql="SELECT SYSDATE FROM DUAL"):
        '''活动ORA系统时间'''
        return self.select(route=route,sql=sql)[0]['SYSDATE']

    def toSysDate(self):
        tupleDate = (time.strftime('%Y-%m-%d :%H:%M:%S'), 'YYYY-MM-DD HH24:MI:SS')
        return tupleDate

if __name__ == '__main__':
    test = MyOracle()
    test.ReConnect(route='cen1')
    # print(test.toSysDate())
    # 查询结果到列表

    # for i in range(len(res)):
    #     logger.info('获取查询结果，打印入参：{}'.format(res[i]))
    #     print(res[i])
    #     for key,value in res[i].items():
    #         print(key,value)
    # ####另一种处理
    # for i in range(len(res)):
    #     print (res[i]['groupId'],res[i]['accessNum'],res[i]['offerId'],res[i]['grp_offer_insId'])
    #
    # print(test.get_one(ex)[0])
    # print(test.get_all(ex))
    # print(test.get_all(ex)[1])
    # colList = ["cust_name", "pspt_id"]  # 存储Colname的值,对应表字段
    # valueList = ["张伶萍", "630121197704223621"]  # 存储value的值，对应表字段都值
    # expr = " SERIAL_NUMBER = '15202502265'"
    # test.updateMany(tabName='tf_f_realname_info',route='cp',
    #                 colList=colList,valueList=valueList,expr=expr)
    # tbVaule = {'ROUTE':'crm1','SCENE_NAME':'获取用户信息','METHOD_NAME':'通过服务号码获取','TAB_NAME':'TF_F_USER',
    #            'SQL_REF':'SEL_UserBySerialNum','SQL_STMT':'select USER_ID,SERIAL_NUMBER,USER_TYPE_CODE,REMOVE_TAG,EPARCHY_CODE,USER_STATE_CODESET',
    #            'EXPR_COND':'1=1 AND REMOVE_TAG = 0 and SERIAL_NUMBER=''%s'''
    #            }
    # condition = {'SQL_REF':'SEL_BySerialNum'}
    #
    # test.updateData(table='DATA_MAPPING',dt_condition=condition,dt_update=tbVaule,route='cen1')




