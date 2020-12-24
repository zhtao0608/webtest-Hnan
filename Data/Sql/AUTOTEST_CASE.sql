drop table AUTOTEST_CASE ;
create table AUTOTEST_CASE
(
    CASE_NO        VARCHAR2(20)  not null,
    CASE_TYPE			 VARCHAR2(100) ,
    STATE	 VARCHAR(2) ,
    SCENE_NAME     VARCHAR2(2000),
    SCENE_CODE     VARCHAR2(30)   not null,
    PARAMS         VARCHAR2(4000) not null,
    ORDER_ID       VARCHAR2(20) ,
    RULE_CHECK_INFO  VARCHAR2(4000) ,
    DATA_CHECK_INFO  VARCHAR2(4000) ,
    EXPECT_RESULT    VARCHAR2(1000)  ,
    ACTUAL_RESULT    VARCHAR2(1000)  ,
    RSRV_STR1       VARCHAR2(1000) ,
    RSRV_STR2       VARCHAR2(1000) ,
    PATH           VARCHAR2(500),
    CREA_STAFF     VARCHAR2(50),
    CREA_DATE      DATE,
    REMARKS        VARCHAR2(500)
)
/
alter table AUTOTEST_CASE
  add constraint PK_AUTOTEST_CASE primary key(SCENE_CODE)
/

alter table AUTOTEST_CASE modify STATE default  '1'
/

comment on table AUTOTEST_CASE is '自动化用例执行计划'
/
comment on column AUTOTEST_CASE.CASE_NO is '用例编码'
/

comment on column AUTOTEST_CASE.CASE_TYPE is '用例类型 UI、INTF、DB等'
/

comment on column AUTOTEST_CASE.STATE is '用例状态 0 -失效，1-生效'
/

comment on column AUTOTEST_CASE.SCENE_NAME is '场景名称'
/

comment on column AUTOTEST_CASE.SCENE_CODE is '场景编码，必须唯一'
/

comment on column AUTOTEST_CASE.PARAMS is '用例执行参数，自动化用例执行过程中参数化实例'
/

comment on column AUTOTEST_CASE.ORDER_ID is '订单编码'
/

comment on column AUTOTEST_CASE.RULE_CHECK_INFO is '用例执行规则检查结果'
/

comment on column AUTOTEST_CASE.DATA_CHECK_INFO is '用例执行数据检查结果'
/
comment on column AUTOTEST_CASE.EXPECT_RESULT is '预期结果'
/
comment on column AUTOTEST_CASE.ACTUAL_RESULT is '实际结果'
/
comment on column AUTOTEST_CASE.RSRV_STR1 is '扩展预留1'
/
comment on column AUTOTEST_CASE.RSRV_STR2 is '扩展预留2'
/
comment on column AUTOTEST_CASE.PATH is '用例执行路径'
/
comment on column AUTOTEST_CASE.CREA_STAFF is '创建工号'
/
comment on column AUTOTEST_CASE.CREA_DATE is '创建时间'
/
comment on column AUTOTEST_CASE.REMARKS is '备注'
/

grant select, insert, update, delete on AUTOTEST_CASE to UOP_CEN1;
