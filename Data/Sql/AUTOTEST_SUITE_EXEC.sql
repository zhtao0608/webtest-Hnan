drop table AUTOTEST_SUITE_EXEC;
create table AUTOTEST_SUITE_EXEC
(
    SUITE_CASE_ID  VARCHAR2(20)  not null,
    SUITE_NAME     VARCHAR2(2000) ,
    SUITE_CODE     VARCHAR2(30)   not null,
    SCENE_CODE     VARCHAR2(30)   not null,
    STATE          VARCHAR2(2)   not null,
    EXEC_PARAMS    VARCHAR2(4000) not null,
    EXEC_PATH      VARCHAR2(500),
    EXEC_INDEX      VARCHAR(10),
    EXEC_TIME      DATE,
    ORDER_ID       VARCHAR2(20) ,
    TRADE_TYPE_CODE VARCHAR2(10),
    RULE_CHECK_INFO  VARCHAR2(4000) ,
    DATA_CHECK_INFO  VARCHAR2(4000) ,
    EXPECT_RESULT    VARCHAR2(1000)  ,
    ACTUAL_RESULT    VARCHAR2(1000)  ,   
    CREA_STAFF     VARCHAR2(50),
    CREA_DATE      DATE,
    RSRV_STR1       VARCHAR2(1000) ,
    RSRV_STR2       VARCHAR2(1000) , 
    REMARKS        VARCHAR2(500)
)
/
alter table AUTOTEST_SUITE_EXEC
  add constraint PK_AUTOTEST_SUITE_EXEC primary key(SUITE_CASE_ID,SUITE_CODE)
/

alter table AUTOTEST_SUITE_EXEC modify STATE default '1'
/

comment on table AUTOTEST_SUITE_EXEC is '自动化用例测试套件'
/
comment on column AUTOTEST_SUITE_EXEC.SUITE_CASE_ID is '套件与CASE关联关系ID'
/

comment on column AUTOTEST_SUITE_EXEC.SUITE_NAME is '自定义测试套件名称'
/

comment on column AUTOTEST_SUITE_EXEC.SCENE_CODE is '用例场景编码,来自AUTOTEST_CASE.SCENE_CODE字段'
/

comment on column AUTOTEST_SUITE_EXEC.EXEC_PARAMS is '用例执行参数，自动化用例执行过程中参数化实例'
/

comment on column AUTOTEST_SUITE_EXEC.EXEC_INDEX is '用例执行顺序'
/


comment on column AUTOTEST_SUITE_EXEC.ORDER_ID is '订单编码'
/

comment on column AUTOTEST_SUITE_EXEC.TRADE_TYPE_CODE is '业务类型,来自AUTOTEST_CASE'
/

comment on column AUTOTEST_SUITE_EXEC.RULE_CHECK_INFO is '用例执行规则检查结果,来自AUTOTEST_CASE'
/

comment on column AUTOTEST_SUITE_EXEC.DATA_CHECK_INFO is '用例执行数据检查结果,来自AUTOTEST_CASE'
/
comment on column AUTOTEST_SUITE_EXEC.EXPECT_RESULT is '预期结果,来自AUTOTEST_CASE'
/
comment on column AUTOTEST_SUITE_EXEC.ACTUAL_RESULT is '实际结果,来自AUTOTEST_CASE'
/
comment on column AUTOTEST_SUITE_EXEC.RSRV_STR1 is '扩展预留1'
/
comment on column AUTOTEST_SUITE_EXEC.RSRV_STR2 is '扩展预留2'
/
comment on column AUTOTEST_SUITE_EXEC.EXEC_PATH is '用例执行路径，来自AUTOTEST_CASE.PATH字段'
/
comment on column AUTOTEST_SUITE_EXEC.CREA_STAFF is '创建工号'
/
comment on column AUTOTEST_SUITE_EXEC.CREA_DATE is '创建时间'
/
comment on column AUTOTEST_SUITE_EXEC.REMARKS is '备注'
/

grant select, insert, update, delete on AUTOTEST_SUITE_EXEC to UOP_CEN1;
