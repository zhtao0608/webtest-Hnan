prompt Importing table ucr_cen1.DATA_MAPPING...
set feedback off
set define off
insert into ucr_cen1.DATA_MAPPING (TRADE_TYPE_CODE, ROUTE, SCENE_NAME, METHOD_NAME, TAB_NAME, SQL_REF, SQL_STMT, EXPR_COND, RSRV_STR, CREA_STAFF, CREA_DATE, UPD_STAFF, UPD_DATE, REMARKS)
values (null, 'cp', '查询下发工单号', '通过手机号码查询最近一次实名制验证工单', 'TF_F_REALNAME_INFO', 'SEL_TRANID_BY_SERIAL', 'SELECT * FROM TF_F_REALNAME_INFO', 'SERIAL_NUMBER=''%s'' AND ROWNUM<=1 ORDER BY TRANSACTION_ID DESC', null, null, null, null, null, null);

insert into ucr_cen1.DATA_MAPPING (TRADE_TYPE_CODE, ROUTE, SCENE_NAME, METHOD_NAME, TAB_NAME, SQL_REF, SQL_STMT, EXPR_COND, RSRV_STR, CREA_STAFF, CREA_DATE, UPD_STAFF, UPD_DATE, REMARKS)
values (null, 'crm1', '获取短信内容', '通过服务号码获取最近下发的短信', 'TI_O_SMS', 'SEL_BY_SERIAL', 'SELECT NOTICE_CONTENT,SMS_TEMPLET_CODE,TO_CHAR(SMS_NOTICE_ID)  FROM TI_O_SMS ', 'RECV_OBJECT =''%s'' AND ROWNUM <=1 ORDER BY SMS_NOTICE_ID DESC', null, null, null, null, null, null);

insert into ucr_cen1.DATA_MAPPING (TRADE_TYPE_CODE, ROUTE, SCENE_NAME, METHOD_NAME, TAB_NAME, SQL_REF, SQL_STMT, EXPR_COND, RSRV_STR, CREA_STAFF, CREA_DATE, UPD_STAFF, UPD_DATE, REMARKS)
values (null, 'cp', '实名制认证', '通过服务号码查询用户实名制信息', 'TF_F_REALNAME_INFO', 'SelBySerialNum', 'SELECT * FROM TF_F_REALNAME_INFO', 'SERIAL_NUMBER=''%s''', null, null, null, null, null, null);

insert into ucr_cen1.DATA_MAPPING (TRADE_TYPE_CODE, ROUTE, SCENE_NAME, METHOD_NAME, TAB_NAME, SQL_REF, SQL_STMT, EXPR_COND, RSRV_STR, CREA_STAFF, CREA_DATE, UPD_STAFF, UPD_DATE, REMARKS)
values (null, 'cp', '实名制认证', '通过工单流水查询用户实名制信息', 'TF_F_REALNAME_INFO', 'SelByTransactionId', 'SELECT * FROM TF_F_REALNAME_INFO', 'transaction_id=''%s''', null, null, null, null, null, null);

insert into ucr_cen1.DATA_MAPPING (TRADE_TYPE_CODE, ROUTE, SCENE_NAME, METHOD_NAME, TAB_NAME, SQL_REF, SQL_STMT, EXPR_COND, RSRV_STR, CREA_STAFF, CREA_DATE, UPD_STAFF, UPD_DATE, REMARKS)
values (null, 'crm1', '获取用户信息', '通过服务号码获取用户信息', 'TF_F_USER', 'SEL_UserBySerialNum', 'select to_char(USER_ID) USER_ID,to_char(CUST_ID) CUST_ID,SERIAL_NUMBER,USER_TYPE_CODE,REMOVE_TAG,EPARCHY_CODE,USER_STATE_CODESET
FROM TF_F_USER', '1=1 AND REMOVE_TAG = ''0'' and SERIAL_NUMBER=''%s''', null, null, null, null, null, null);

insert into ucr_cen1.DATA_MAPPING (TRADE_TYPE_CODE, ROUTE, SCENE_NAME, METHOD_NAME, TAB_NAME, SQL_REF, SQL_STMT, EXPR_COND, RSRV_STR, CREA_STAFF, CREA_DATE, UPD_STAFF, UPD_DATE, REMARKS)
values (null, 'cp', '获取客户证件信息', '通过客户编码获取客户证件等信息', 'TF_F_CUST_PERSON_RELA', 'SEL_BY_CUSTID', 'select a.cust_name,to_char(a.cust_id) cust_id,to_char(a.pspt_id) pspt_id,a.pspt_type_code,a.pspt_addr from uop_cp.Tf_f_Cust_Person_rela a ', 'a.cust_id=''%s''', null, null, null, null, null, null);

insert into ucr_cen1.DATA_MAPPING (TRADE_TYPE_CODE, ROUTE, SCENE_NAME, METHOD_NAME, TAB_NAME, SQL_REF, SQL_STMT, EXPR_COND, RSRV_STR, CREA_STAFF, CREA_DATE, UPD_STAFF, UPD_DATE, REMARKS)
values (null, 'crm1', '获取用户产品信息', '通过产品编码活动已订购产品信息', 'TF_F_USER_PRODUCT', 'SelByProdId', 'select a.PRODUCT_ID,a.BRAND_CODE,b.USER_ID,b.SERIAL_NUMBER,
b.USER_STATE_CODESET , t.STATE_CODE,
to_char(t.END_DATE,''YYYY-MM-DD HH:MM:SS'') END_DATE ,
to_char(t.START_DATE,''YYYY-MM-DD HH:MM:SS'') START_DATE
from TF_F_USER_PRODUCT a ,TF_F_USER b ,TF_F_USER_SVCSTATE t ', 'a.USER_ID = b.USER_ID
and a.MAIN_TAG =''1''  and t.END_DATE > sysdate
and a.END_DATE> sysdate
and t.USER_ID = b.USER_ID
and b.REMOVE_TAG =''0'' and b.USER_STATE_CODESET = ''0'' and a.PRODUCT_ID in (''%s'')
and b.EPARCHY_CODE = ''0971'' AND ROWNUM<=3 order by a.START_DATE desc', null, null, null, null, null, null);

insert into ucr_cen1.DATA_MAPPING (TRADE_TYPE_CODE, ROUTE, SCENE_NAME, METHOD_NAME, TAB_NAME, SQL_REF, SQL_STMT, EXPR_COND, RSRV_STR, CREA_STAFF, CREA_DATE, UPD_STAFF, UPD_DATE, REMARKS)
values (null, 'jour1', '获取订单信息', '通过订单编号活动订单信息', 'TF_B_TRADE', 'SelByOrderID', 'select * from tf_b_trade', '1=1 AND order_id =''%s''', null, null, null, null, null, null);

insert into ucr_cen1.DATA_MAPPING (TRADE_TYPE_CODE, ROUTE, SCENE_NAME, METHOD_NAME, TAB_NAME, SQL_REF, SQL_STMT, EXPR_COND, RSRV_STR, CREA_STAFF, CREA_DATE, UPD_STAFF, UPD_DATE, REMARKS)
values (null, 'jour1', '获取订单信息', '通过tradeId获取所有订单信息', 'TF_B_TRADE', 'SELECT_ALL_BY_TRADEID', 'select * from tf_b_trade', null, null, null, null, null, null, null);

insert into ucr_cen1.DATA_MAPPING (TRADE_TYPE_CODE, ROUTE, SCENE_NAME, METHOD_NAME, TAB_NAME, SQL_REF, SQL_STMT, EXPR_COND, RSRV_STR, CREA_STAFF, CREA_DATE, UPD_STAFF, UPD_DATE, REMARKS)
values (null, 'cen1', '获取用例执行参数', '通过场景编码获取用例执行参数', 'AUTOTEST_CASE', 'SEL_BY_SCENE_CODE', 'SELECT T.CASE_NO,T.SCENE_NAME,T.SCENE_CODE,T.PARAMS,T.EXPECT_RESULT FROM AUTOTEST_CASE T', 'SCENE_CODE=''%s''', null, null, null, null, null, null);

commit ;
prompt Done.
