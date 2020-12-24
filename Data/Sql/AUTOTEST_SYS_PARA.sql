DROP TABLE AUTOTEST_SYS_PARA;
create table AUTOTEST_SYS_PARA
(
  prov_code        VARCHAR(10) not null,
  param_attr       VARCHAR(10) not null,
  param_code       VARCHAR2(50) not null,
  param_name       VARCHAR2(200),
  param_value	   VARCHAR2(500),
  start_date       DATE not null,
  end_date         DATE not null,
  create_user_id   VARCHAR(10),
  remark           VARCHAR2(100)
)
/
alter table AUTOTEST_SYS_PARA
  add constraint PK_AUTOTEST_SYS_PARA primary key(prov_code,param_attr,param_code,param_value)
/
-- Add comments to the table 
comment on table AUTOTEST_SYS_PARA is '用例系统编码映射关系'
/
comment on column AUTOTEST_SYS_PARA.prov_code is '省份编码:QHAI,HNAN,YHAN,XINJ,TJIN,HAIN等'
/

comment on column AUTOTEST_SYS_PARA.param_attr is '系统参数属性'
/

comment on column AUTOTEST_SYS_PARA.param_code is '系统参数编码'
/

comment on column AUTOTEST_SYS_PARA.param_value is '系统参数值'
/

comment on column AUTOTEST_SYS_PARA.create_user_id is '创建员工'
/

comment on column AUTOTEST_SYS_PARA.start_date is '开始时间'
/

comment on column AUTOTEST_SYS_PARA.end_date is '结束时间'
/

comment on column AUTOTEST_SYS_PARA.remark is '备注'
/

-- Grant/Revoke object privileges 
grant select, insert, update, delete on AUTOTEST_SYS_PARA to UOP_CEN1;

