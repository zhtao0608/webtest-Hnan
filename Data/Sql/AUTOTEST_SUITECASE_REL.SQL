create table AUTOTEST_SUITECASE_REL
(
    REL_ID       VARCHAR2(20)  not null,
    SUITE_ID		 VARCHAR2(20)  not null,
    SUITE_CODE   VARCHAR2(30)   not null,
    SCENE_CODE   VARCHAR2(30)   not null,
    STATE        VARCHAR(2) not null ,
    RSRV_STR1       VARCHAR2(1000) ,
    RSRV_STR2       VARCHAR2(1000) ,
    CREATE_USER_ID  VARCHAR2(50),
    CREATE_TIME      DATE,
    REMARKS        VARCHAR2(500)
)
/
alter table AUTOTEST_SUITECASE_REL
  add constraint PK_AUTOTEST_SUITECASE_REL primary key(REL_ID)
/
alter table AUTOTEST_SUITECASE_REL modify STATE default '1'
/
  
comment on table AUTOTEST_SUITECASE_REL is '自动化测试套件与案例关联关系'
/
comment on column AUTOTEST_SUITECASE_REL.REL_ID is '关联编码'
/

comment on column AUTOTEST_SUITECASE_REL.SUITE_ID is '测试套件定义编码'
/

comment on column AUTOTEST_SUITECASE_REL.SUITE_CODE is '套件编码'
/

comment on column AUTOTEST_SUITECASE_REL.SCENE_CODE is '案例编码'
/

comment on column AUTOTEST_SUITECASE_REL.STATE is '套件状态：0-失效 1-生效'
/

comment on column AUTOTEST_SUITECASE_REL.RSRV_STR1 is '扩展预留1'
/
comment on column AUTOTEST_SUITECASE_REL.RSRV_STR2 is '扩展预留2'
/

comment on column AUTOTEST_SUITECASE_REL.CREATE_USER_ID is '创建工号'
/
comment on column AUTOTEST_SUITECASE_REL.CREATE_TIME is '创建时间'
/
comment on column AUTOTEST_SUITECASE_REL.REMARKS is '备注'
/

grant select, insert, update, delete on AUTOTEST_SUITECASE_REL to UOP_CEN1;
