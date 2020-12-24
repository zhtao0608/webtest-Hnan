drop table DATA_MAPPING ;
create table DATA_MAPPING
(
    TRADE_TYPE_CODE VARCHAR2(5),
    ROUTE           VARCHAR2(10),
    SCENE_NAME     VARCHAR2(2000),
    METHOD_NAME    VARCHAR2(500),
    TAB_NAME       VARCHAR2(30)   not null,
    SQL_REF        VARCHAR2(60)   not null,
    SQL_STMT       VARCHAR2(4000) not null,
    EXPR_COND      VARCHAR2(4000) ,
    RSRV_STR      VARCHAR2(1000) ,
    CREA_STAFF     VARCHAR2(50),
    CREA_DATE      DATE,
    UPD_STAFF      VARCHAR2(50),
    UPD_DATE       DATE,
    REMARKS        VARCHAR2(500)
)
/
alter table DATA_MAPPING
  add constraint PK_DATA_MAPPING primary key (TAB_NAME, SQL_REF)
/
  
comment on table DATA_MAPPING is 'sql数据检查'
/
comment on column DATA_MAPPING.TRADE_TYPE_CODE is '业务类型'
/

comment on column DATA_MAPPING.ROUTE is '路由,数据库uop用户名小写'
/

comment on column DATA_MAPPING.SCENE_NAME is '检查场景'
/

comment on column DATA_MAPPING.METHOD_NAME is 'Python执行方法'
/

comment on column DATA_MAPPING.TAB_NAME is '表名'
/

comment on column DATA_MAPPING.SQL_REF is '语句名'
/

comment on column DATA_MAPPING.SQL_STMT is 'SQL语句模板，SELECT ｛｝ FROM'
/

comment on column DATA_MAPPING.EXPR_COND is 'SQL条件表达式，where后面部分'
/
comment on column DATA_MAPPING.REMARKS is '备注'
/
comment on column DATA_MAPPING.RSRV_STR is '扩展预留'
/

comment on column DATA_MAPPING.CREA_STAFF is '创建工号'
/

comment on column DATA_MAPPING.CREA_DATE is '创建时间'
/

comment on column DATA_MAPPING.UPD_STAFF is '更新员工'
/

comment on column DATA_MAPPING.UPD_DATE is '更新时间'
/
grant select, insert, update, delete on DATA_MAPPING to UOP_CEN1;
