drop table autotest_api_def;
create table autotest_api_def
(
    SERVICE_ID           decimal(12)  not null comment '服务标识'
        primary key,
    SERVICE_CODE         text         null comment '服务编码 ',
    CENTER_CODE          varchar(128) null comment '服务提供方 关联服务所属中心',
    SERVICE_NAME         text         null comment '服务名称 服务的唯一标识，用于加载到编排客户端资源管理器',
    DESCRIPTION          text         null comment '服务描述 服务描述,服务的具体功能介绍',
    SRV_INTERFACE        text         null comment '服务接口类 ',
    SRV_IMPL_CLASS       text         null comment '服务实现类 ',
    SRV_METHOD           varchar(128) null comment '服务方法 ',
    SRV_PARAMS           text         null comment 'api入参 ',
    SRV_RETURN           varchar(128) null comment '返回类型 java的类型，如果是Map类型，具体的key对应到“服务参数表”的出参对应',
    PROTOCOL             varchar(32)  null comment '调用协议 注明服务调用者使用哪种协议 http+xml、http+hession、http+json、ws、socket、FTP等',
    VERSION              varchar(32)  null comment '服务版本 "1-当前版本（新版本）0-旧版本"',
    STATUS               char         null comment '状态 "C--创建M--修改W--待上线 F--正常，已上线X--已下线D--已废弃E--审批不通过"',
    REMARKS              text         null comment '备注 ',
    TENANT_CODE          varchar(128) null,
    TENANT_NAME          varchar(128) null
)
    comment '服务基本信息表';