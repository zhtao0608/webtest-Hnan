# -*- coding:utf-8 -*-
# __author:Administrator
# date: 2017/12/28
import os,time
import json
import cx_Oracle
from Common import ReadConfig
from Common.Mylog import LogManager

logger = LogManager('test').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
rc = ReadConfig.ReadConfig("ngboss_config.ini")

class MyOracle:

    """
    oracle数据库操作
    """
    global username, password, ip, port, service_name,cp_thin,file4_thin,param_thin
    username = rc.get_oracle('USERNAME')
    password = rc.get_oracle('PASSWORD')
    ip = rc.get_oracle('IP')
    port = rc.get_oracle('PORT')
    service_name = rc.get_oracle('SERVICE_NAME')
    # thin = username + "/" + password + "@" + ip +":" + port+ "/" + service_name
    cp_thin = rc.get_oracle("cp_thin")
    param_thin = rc.get_oracle("param_thin")
    file4_thin = rc.get_oracle("file4_thin")
    port4_thin = rc.get_oracle("port4_thin")
    upc_thin = rc.get_oracle("upc_thin")
    res_thin = rc.get_oracle("res_thin")
    ec_thin = rc.get_oracle("ec_thin")

    def __init__(self):
        """
        初始化
        """
        self.tns = cx_Oracle.makedsn(ip, port,service_name)
        # self.in = self.username +"/"+ self.password+"@"+self.service_name
        print(self.tns)
        self.conn = None
        self.cursor = None

    def ReConnect(self,conn=rc.get_oracle("file4_thin")):
        """
        建立连接
        """
        try:
            # self.conn = cx_Oracle.connect(username, password, self.tns)
            self.conn = cx_Oracle.connect(conn)
            print(self.conn)
            logger.info('连接的DB：{}'.format(conn))
            self.cursor = self.conn.cursor()
            logger.info("Connect DB successfully!")
        except ConnectionError as e:
            logger.error(e)

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

    def select(self,sql,conn=rc.get_oracle('file4_thin')):
        """查询返回字典格式"""
        list = []
        self.ReConnect(conn)
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
        """插入语句"""
        try:
            self.cursor.executemany(sql, list_param)
            self.conn.commit()
            logger.info("Insert Db complete!")
        except Exception as e:
            logger.info(e)
        finally:
            self.disconnect()

    def update(self, sql):
        """数据更新操作"""
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            logger.info("Insert DB Complete!")
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

if __name__ == '__main__':
    test = MyOracle()
    sql = "select t.GROUP_NAME,t.group_id from CB_ENTERPRISE t  where rownum <=3"
    sql_groupOffers = "select b.group_id ,b.group_name,a.access_num,t.SUBSCRIBER_INS_ID,t.OFFER_ID,t.OFFER_INS_ID,t.OFFER_NAME \
    from uop_ec.um_offer t, uop_ec.um_subscriber a ,uop_cp.cb_enterprise b \
    where t.IS_MAIN = '1' and t.EXPIRE_DATE > sysdate and t.OFFER_TYPE = '10' and t.OFFER_ID ='2222' \
    and a.subscriber_ins_id = t.SUBSCRIBER_INS_ID and a.remove_tag = '0' \
    and a.cust_id = b.orga_enterprise_id  and rownum <=10"

    sql_groupMebOffers = "select a.rel_access_num accessNum,a.subscriber_ins_id ,b.group_id groupId,b.group_name,t.OFFER_ID offerId,t.OFFER_INS_ID grp_offer_insId,t.OFFER_NAME  \
    from uop_file4.um_subscriber_rel a  ,uop_ec.um_offer t, uop_ec.um_subscriber m ,uop_cp.cb_enterprise b \
    where 1=1 and a.subscriber_ins_id = m.subscriber_ins_id \
    and a.subscriber_ins_id = t.SUBSCRIBER_INS_ID \
    and t.IS_MAIN = '1' and t.EXPIRE_DATE > sysdate and t.OFFER_TYPE = '10' \
    and t.OFFER_ID ='2222' \
    and a.subscriber_rel_type ='E1' \
    and  m.remove_tag = 0 \
    and  m.cust_id = b.orga_enterprise_id  and rownum <=10 "

    sql_accessNum = " SELECT rownum caseNo ,t.access_num,to_char(t.subscriber_ins_id) subscriber_ins_id ,'' flow_id , '' result_info  \
     FROM  uop_file4.um_subscriber  T where t.remove_tag = 0 and t.access_num like '187%' and rownum<=3  "
    # ex = test.executeSQL(sql)
    # res = json.loads(test.select(sql))
    res = test.select(sql_accessNum)

    # 查询结果到列表
    print(res)
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




