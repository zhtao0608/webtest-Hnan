create table AUTOTEST_SUITE_DEF
(
    SUITE_ID       VARCHAR2(20)  not null,
    SUITE_TYPE	   VARCHAR2(100) ,
    SUITE_NAME     VARCHAR2(2000),
    SUITE_CODE     VARCHAR2(30)   not null,
    STATE           VARCHAR(2) not null ,
    RSRV_STR1       VARCHAR2(1000) ,
    RSRV_STR2       VARCHAR2(1000) ,
    CREATE_USER_ID     VARCHAR2(50),
    CREATE_TIME      DATE,
    REMARKS        VARCHAR2(500)
)
/
alter table AUTOTEST_SUITE_DEF
  add constraint PK_AUTOTEST_SUITE_DEF primary key(SUITE_CODE)
/

alter table AUTOTEST_SUITE_DEF modify STATE default '1'
/
comment on table AUTOTEST_SUITE_DEF is '自动化用例套件定义'
/
comment on column AUTOTEST_SUITE_DEF.SUITE_ID is '套件编码'
/

comment on column AUTOTEST_SUITE_DEF.SUITE_TYPE is '类型 UI、INTF、DB等'
/

comment on column AUTOTEST_SUITE_DEF.SUITE_NAME is '套件名称'
/

comment on column AUTOTEST_SUITE_DEF.SUITE_CODE is '套件编码，必须唯一'
/

comment on column AUTOTEST_SUITE_DEF.STATE is '套件状态：0-失效 1-生效'
/

comment on column AUTOTEST_SUITE_DEF.RSRV_STR1 is '扩展预留1'
/
comment on column AUTOTEST_SUITE_DEF.RSRV_STR2 is '扩展预留2'
/

comment on column AUTOTEST_SUITE_DEF.CREATE_USER_ID is '创建工号'
/
comment on column AUTOTEST_SUITE_DEF.CREATE_TIME is '创建时间'
/
comment on column AUTOTEST_SUITE_DEF.REMARKS is '备注'
/

grant select, insert, update, delete on AUTOTEST_SUITE_DEF to UOP_CEN1;
