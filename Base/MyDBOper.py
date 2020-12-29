"""
@version: python3.x
@author:周涛
@contact: 617349013@qq.com
@software: PyCharm
@file: dbSql.py
@time: 2018/9/22 17:47
"""

import pymysql
import time
from Base.Mylog import LogManager
from Base import ReadConfig


rc = ReadConfig.ReadConfig("ngboss_config.ini")
# 加入日志
# 获取logger实例
logger = LogManager('MyDBOper').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )


class DbManager:
    # 构造函数
    def __init__(self, host='127.0.0.1', port=3306, user='root',
                 passwd='1234', db='autotest', charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.charset = charset
        # self.conn = None
        # self.cur = None
        try:
            self.conn = pymysql.connect(host = self.host,port=self.port, user = self.user, password = self.passwd,  database = self.db,
                                                 charset=self.charset)
            self.cur = self.conn.cursor()
        except :
            logger.info("DataBase connect error,please check the db config.")


    # 连接数据库
    def connMyDB(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db,
                                        charset=self.charset)
        except:
            logger.info("connect Mysql Database failed")
            return False
        self.cur = self.conn.cursor()
        return True

    # 关闭数据库
    def close(self):
        # 如果数据打开，则关闭；否则没有操作
        if self.conn and self.cur:
            self.cur.close()
            self.conn.close()
        return True

    # 执行数据库的sq语句,主要用来做插入操作
    def execute(self, sql, params=None, commit=True):
        # 连接数据库
        res = self.connMyDB()
        if not res:
            return False
        try:
            if self.conn and self.cur:
                # 正常逻辑，执行sql，提交操作
                rowcount = self.cur.execute(sql, params)
                # print(rowcount)
                if commit:
                    self.conn.commit()
                else:
                    pass
        except:
            logger.info("execute failed: " + sql)
            logger.info("params: " + str(params))
            self.close()
            return False
        return rowcount


    def select(self,sql):
        """查询返回字典列表"""
        list = []
        result = self.queryData(sql)
        # logger.info('查询结果:{}'.format(result))
        col_name = self.cur.description
        for row in result:
            dict = {}
            for col in range(len(col_name)):
                key = col_name[col][0]
                value = row[col]
                dict[key] = value
            list.append(dict)
        ###把返回的list转换成json串,并格式化
        return list


    # 查询所有数据
    def selectAll(self, sql, params=None):
        res = self.execute(sql, params)
        if not res:
            logger.info("查询失败")
            return False
        self.close()
        results = self.cur.fetchall()
        logger.info("查询成功" + str(results))
        return results

    # 查询一条数据
    def selectOne(self, sql, params=None):
        res = self.execute(sql, params)
        if not res:
            logger.info("查询失败")
            return False
        self.close()
        result = self.cur.fetchone()
        logger.info("查询成功" + str(result))
        return result

    # 增删改数据
    def editDatas(self, sql, params=None):
        # res = self.execute(sql, params, True)
        self.execute(sql, params, True)
        # if not res:
        #     logger.info("操作失败")
        #     return False
        self.conn.commit()
        self.close()
        logger.info("数据库更新操作成功" )
        # return res

    def queryFormatrs(self, sql_str):
        '''查询数据，返回一个列表，里面的每一行是一个字典，带字段名
            cursor 为连接光标
            sql_str为查询语句
        '''
        try:
            self.cur.execute(sql_str)
            rows = self.cur.fetchall()
            r = []
            for x in rows:
                r.append(dict(zip(self.cur.column_names, x)))
            return r
        except:
            return False

    def queryData(self, sql_str):
        '''查询数据并返回
             cursor 为连接光标
             sql_str为查询语句
        '''
        try:
            self.cur.execute(sql_str)
            rows = self.cur.fetchall()
            return rows
        except:
            return False


    def execute_update_insert(self, sql):
        '''
        插入或更新记录 成功返回最后的id
        '''
        self.cur.execute(sql)
        self.con.commit()
        return self.cur.lastrowid

if __name__ == '__main__':
    dbManager = DbManager()
    """
    sql = "select * from bandcard WHERE money>%s;"
    values = [1000]
    result = dbManager.fetchall(sql, values)
    """
    results = dbManager.select("SELECT * FROM autotest_case where scene_code = 'AddElements';")
    print(results)



