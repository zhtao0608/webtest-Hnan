prompt Importing table AUTOTEST_CASE...
set feedback off
set define off
insert into AUTOTEST_CASE (CASE_NO, CASE_TYPE, SCENE_NAME, SCENE_CODE, PARAMS, ORDER_ID, RULE_CHECK_INFO, DATA_CHECK_INFO, EXPECT_RESULT, ACTUAL_RESULT, RSRV_STR1, RSRV_STR2, PATH, CREA_STAFF, CREA_DATE, REMARKS)
values ('CASE_013', 'UI', '个人业务受理-产品变更110-变更主产品', 'ChgMainProduct', '{''accessNum'':''18309718709'',''productId'':''18012979'',''elementList'':[]}', null, '没有弹出WadeMessage提示,校验通过', null, null, null, null, null, null, '周涛', to_date('30-11-2020 19:49:51', 'dd-mm-yyyy hh24:mi:ss'), 'PERSON');

insert into AUTOTEST_CASE (CASE_NO, CASE_TYPE, SCENE_NAME, SCENE_CODE, PARAMS, ORDER_ID, RULE_CHECK_INFO, DATA_CHECK_INFO, EXPECT_RESULT, ACTUAL_RESULT, RSRV_STR1, RSRV_STR2, PATH, CREA_STAFF, CREA_DATE, REMARKS)
values ('CASE_001', 'UI', '集团商品受理_集团VPMN订购(8000)', 'CrtUsVPMN', '{
    "groupId": "7100048602",
    "brandCode": "BZBG",
    "offerCode": "8000",
    "contractId": "7100048602",
    "elementAttrBizList": [
        {
            "ELEMENT_ID": "110000008000",
            "OFFER_TYPE": "P",
            "AttrBizList": [
                {
                    "ATTR_VALUE": "1-均显示短号",
                    "ATTR_CODE": "pam_CALL_DISP_MODE"
                }
            ]
        },
        {
            "ELEMENT_ID": "130000060000",
            "OFFER_TYPE": "D",
            "AttrBizList": []
        }
    ]
}', null, '业务校验失败错误编码:-1\n错误信息:CRM_TRADE_354:业务规则校验： 规则【202006018】校验不通过：集团客户已定购此产品 同一产品只能办理一次!\n隐藏详细信息', null, '业务受理成功', null, null, null, null, '周涛', to_date('30-11-2020 19:49:51', 'dd-mm-yyyy hh24:mi:ss'), 'GROUP');

insert into AUTOTEST_CASE (CASE_NO, CASE_TYPE, SCENE_NAME, SCENE_CODE, PARAMS, ORDER_ID, RULE_CHECK_INFO, DATA_CHECK_INFO, EXPECT_RESULT, ACTUAL_RESULT, RSRV_STR1, RSRV_STR2, PATH, CREA_STAFF, CREA_DATE, REMARKS)
values ('CASE_002', 'UI', '集团商品受理_桌面电话订购(2222)', 'CrtUsDeskTopTel', '{
    "groupId": "7100048602",
    "brandCode": "TREX",
    "offerCode": "2222",
    "contractId": "7100048602",
    "elementAttrBizList": [
        {
            "ELEMENT_ID": "110000222201",
            "OFFER_TYPE": "P",
            "AttrBizList": [
                {
                    "ATTR_VALUE": "西宁",
                    "ATTR_CODE": "pam_DIVIDE_DEPART"
                },
                {
                    "ATTR_VALUE": "5: 5分成",
                    "ATTR_CODE": "pam_DIVIDE_BELIEL"
                }
            ]
        }
    ]
}', null, null, null, '业务受理成功', null, null, null, null, '周涛', to_date('30-11-2020 19:49:51', 'dd-mm-yyyy hh24:mi:ss'), 'GROUP');

insert into AUTOTEST_CASE (CASE_NO, CASE_TYPE, SCENE_NAME, SCENE_CODE, PARAMS, ORDER_ID, RULE_CHECK_INFO, DATA_CHECK_INFO, EXPECT_RESULT, ACTUAL_RESULT, RSRV_STR1, RSRV_STR2, PATH, CREA_STAFF, CREA_DATE, REMARKS)
values ('CASE_003', 'UI', '集团商品受理_集团彩铃订购(6200)', 'CrtUsColorRing', '{
    "groupId": "7100048602",
    "brandCode": "BZBG",
    "offerCode": "6200",
    "contractId": "7100048602",
    "elementAttrBizList": [
        {
            "ELEMENT_ID": "3000030473",
            "OFFER_TYPE": "D",
            "AttrBizList": []
        }
    ]
}', null, null, null, '业务受理成功', '错误信息:ASYNC_QUERY_ERROR:执行并行查询异常', null, null, null, '周涛', to_date('30-11-2020 19:49:51', 'dd-mm-yyyy hh24:mi:ss'), 'GROUP');

insert into AUTOTEST_CASE (CASE_NO, CASE_TYPE, SCENE_NAME, SCENE_CODE, PARAMS, ORDER_ID, RULE_CHECK_INFO, DATA_CHECK_INFO, EXPECT_RESULT, ACTUAL_RESULT, RSRV_STR1, RSRV_STR2, PATH, CREA_STAFF, CREA_DATE, REMARKS)
values ('CASE_004', 'UI', '成员商品受理_成员产品订购(8000)', 'CrtMbVPMN', '{
    "groupId": "7100048602",
    "serialNum": "18797098484",
    "offerCode": "8000",
    "grpUserId": "7120112700109681",
    "planType": "G",
    "itemId": "42701",
    "elementAttrBizList": [
        {
            "ELEMENT_ID": "110011003068",
            "OFFER_TYPE": "P",
            "AttrBizList": [
                {
                    "ATTR_VALUE": "610530",
                    "ATTR_CODE": "pam_SHORT_CODE"
                },
                {
                    "ATTR_VALUE": "1-均显示短号",
                    "ATTR_CODE": "pam_pam_CALL_DISP_MODE"
                }
            ]
        },
        {
            "ELEMENT_ID": "3000033663",
            "OFFER_TYPE": "D",
            "AttrBizList": [
            ]
        },
        {
            "ELEMENT_ID": "120000008601",
            "OFFER_TYPE": "S",
            "AttrBizList": [
            ]
        }
    ]
}', null, null, null, '业务受理成功', null, null, null, null, '周涛', to_date('30-11-2020 19:49:51', 'dd-mm-yyyy hh24:mi:ss'), 'GROUP');

insert into AUTOTEST_CASE (CASE_NO, CASE_TYPE, SCENE_NAME, SCENE_CODE, PARAMS, ORDER_ID, RULE_CHECK_INFO, DATA_CHECK_INFO, EXPECT_RESULT, ACTUAL_RESULT, RSRV_STR1, RSRV_STR2, PATH, CREA_STAFF, CREA_DATE, REMARKS)
values ('CASE_005', 'UI', '成员商品受理_成员产品订购(2222)', 'CrtMbDeskTopTel', '{
    "groupId": "7100048602",
    "serialNum": "09717140118",
    "offerCode": "2222",
    "grpUserId": "7120112400099809",
    "planType": "G",
    "itemId": "42701",
    "elementAttrBizList": [
        {
            "ELEMENT_ID": "110000222201",
            "OFFER_TYPE": "P",
            "AttrBizList": [
                {
                    "ATTR_VALUE": "610530",
                    "ATTR_CODE": "pam_SHORT_CODE"
                }
            ]
        },
        {
            "ELEMENT_ID": "120010122813",
            "OFFER_TYPE": "S",
            "AttrBizList": [
            ]
        },
        {
            "ELEMENT_ID": "120000008174",
            "OFFER_TYPE": "S",
            "AttrBizList": [
                {
                    "ATTR_VALUE": "IMS融合通信 - @ ims.qh.chinamobile.com",
                    "ATTR_CODE": "IMPU_TYPE"
                }
            ]
        },
        {
            "ELEMENT_ID": "120000008172",
            "OFFER_TYPE": "S",
            "AttrBizList": [
            ]
        }
    ]
}', null, null, null, '业务受理成功', null, null, null, null, '周涛', to_date('30-11-2020 19:49:51', 'dd-mm-yyyy hh24:mi:ss'), 'GROUP');

insert into AUTOTEST_CASE (CASE_NO, CASE_TYPE, SCENE_NAME, SCENE_CODE, PARAMS, ORDER_ID, RULE_CHECK_INFO, DATA_CHECK_INFO, EXPECT_RESULT, ACTUAL_RESULT, RSRV_STR1, RSRV_STR2, PATH, CREA_STAFF, CREA_DATE, REMARKS)
values ('CASE_006', 'UI', '成员商品受理_成员产品订购(6200)', 'CrtMbColorRing', '{
    "groupId": "7100048602",
    "serialNum": "13897471185",
    "offerCode": "6200",
    "grpUserId": "7120112700109676",
    "planType": "G",
    "itemId": "90001",
    "elementAttrBizList": [
        {
            "ELEMENT_ID": "3000033664",
            "OFFER_TYPE": "D",
            "AttrBizList": [
            ]
        }
    ]
}', null, null, null, '业务受理成功', null, null, null, null, '周涛', to_date('30-11-2020 19:49:51', 'dd-mm-yyyy hh24:mi:ss'), 'GROUP');

insert into AUTOTEST_CASE (CASE_NO, CASE_TYPE, SCENE_NAME, SCENE_CODE, PARAMS, ORDER_ID, RULE_CHECK_INFO, DATA_CHECK_INFO, EXPECT_RESULT, ACTUAL_RESULT, RSRV_STR1, RSRV_STR2, PATH, CREA_STAFF, CREA_DATE, REMARKS)
values ('CASE_007', 'UI', '成员商品受理_成员产品退订(8000)', 'DstMbVPMN', '{''groupId'':''7100048602'',''serialNum'':''13897471185'',''grpUserId'':''7120112400099809''}', null, null, null, '业务受理成功', null, null, null, null, '周涛', to_date('30-11-2020 19:49:51', 'dd-mm-yyyy hh24:mi:ss'), 'GROUP');

insert into AUTOTEST_CASE (CASE_NO, CASE_TYPE, SCENE_NAME, SCENE_CODE, PARAMS, ORDER_ID, RULE_CHECK_INFO, DATA_CHECK_INFO, EXPECT_RESULT, ACTUAL_RESULT, RSRV_STR1, RSRV_STR2, PATH, CREA_STAFF, CREA_DATE, REMARKS)
values ('CASE_008', 'UI', '成员商品受理_成员产品退订(2222)', 'DstMbDeskTopTel', '{''groupId'':''7100048602'',''serialNum'':''13897471185'',''grpUserId'':''7120112400099809''}', null, null, null, '业务受理成功', null, null, null, null, '周涛', to_date('30-11-2020 19:49:51', 'dd-mm-yyyy hh24:mi:ss'), 'GROUP');

insert into AUTOTEST_CASE (CASE_NO, CASE_TYPE, SCENE_NAME, SCENE_CODE, PARAMS, ORDER_ID, RULE_CHECK_INFO, DATA_CHECK_INFO, EXPECT_RESULT, ACTUAL_RESULT, RSRV_STR1, RSRV_STR2, PATH, CREA_STAFF, CREA_DATE, REMARKS)
values ('CASE_009', 'UI', '成员商品受理_成员产品退订(6200)', 'DstMbColorRing', '{''groupId'':''7100048602'',''serialNum'':''13897471185'',''grpUserId'':''7120112400099809''}', null, null, null, '业务受理成功', null, null, null, null, '周涛', to_date('30-11-2020 19:49:51', 'dd-mm-yyyy hh24:mi:ss'), 'GROUP');

insert into AUTOTEST_CASE (CASE_NO, CASE_TYPE, SCENE_NAME, SCENE_CODE, PARAMS, ORDER_ID, RULE_CHECK_INFO, DATA_CHECK_INFO, EXPECT_RESULT, ACTUAL_RESULT, RSRV_STR1, RSRV_STR2, PATH, CREA_STAFF, CREA_DATE, REMARKS)
values ('CASE_010', 'UI', '集团商品受理_集团VPMN退订(8000)', 'DstUsVPMN', '{''groupId'':''7100048602'',''offerCode'':''8000''}', null, null, null, '业务受理成功', null, null, null, null, '周涛', to_date('30-11-2020 19:49:51', 'dd-mm-yyyy hh24:mi:ss'), 'GROUP');

insert into AUTOTEST_CASE (CASE_NO, CASE_TYPE, SCENE_NAME, SCENE_CODE, PARAMS, ORDER_ID, RULE_CHECK_INFO, DATA_CHECK_INFO, EXPECT_RESULT, ACTUAL_RESULT, RSRV_STR1, RSRV_STR2, PATH, CREA_STAFF, CREA_DATE, REMARKS)
values ('CASE_011', 'UI', '集团商品受理_桌面电话退订(2222)', 'DstUsDeskTopTel', '{''groupId'':''7100048602'',''offerCode'':''2222''},{''groupId'':''7100048602'',''offerCode'':''2222''}', null, null, null, '业务受理成功', null, null, null, null, '周涛', to_date('30-11-2020 19:49:51', 'dd-mm-yyyy hh24:mi:ss'), 'GROUP');

insert into AUTOTEST_CASE (CASE_NO, CASE_TYPE, SCENE_NAME, SCENE_CODE, PARAMS, ORDER_ID, RULE_CHECK_INFO, DATA_CHECK_INFO, EXPECT_RESULT, ACTUAL_RESULT, RSRV_STR1, RSRV_STR2, PATH, CREA_STAFF, CREA_DATE, REMARKS)
values ('CASE_012', 'UI', '集团商品受理_集团彩铃退订(6200)', 'DstUsColorRing', '{''groupId'':''7100048602'',''offerCode'':''6200''}', null, null, null, '业务受理成功', null, null, null, null, '周涛', to_date('30-11-2020 19:49:51', 'dd-mm-yyyy hh24:mi:ss'), 'GROUP');

commit ;
prompt Done.
