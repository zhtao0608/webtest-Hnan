import cx_Oracle as Oracle
import pyperclip
import re

def OutputCustInfo(custinfo:str):
    GetNumInfo = re.findall('[0-9]+',custinfo)
    GetCustInfo = {'cust_name':'','serial_number':'13897876765','pspt_id':'','transaction_id':''}
    for i in GetNumInfo:
        if i.isdigit() and len(i) == 11:
            GetCustInfo['serial_number'] = i
        elif i.isdigit() and len(i) == 18 :
            GetCustInfo['pspt_id'] = i
        elif i.isdigit() and len(i) == 17 and GetCustInfo['pspt_id'] == '':
            GetCustInfo['pspt_id'] = str(i) + 'X'            
        elif i.isdigit() and len(i) == 23:
            GetCustInfo['transaction_id'] = i       
    cust_name = re.findall('姓名[^\s].*',custinfo)
    cust_name = cust_name if cust_name else re.findall('名字[^\s].*',custinfo)
    # print(cust_name)
    if ':' in cust_name[0] :
        GetCustInfo['cust_name'] = cust_name[0].split(':')[-1].replace('\r','')
    elif '：'in cust_name[0]:
        GetCustInfo['cust_name'] = cust_name[0].split('：')[-1].replace('\r','')
    else:
        GetCustInfo['cust_name'] = cust_name[0].replace('姓名','') if '姓名' in cust_name[0] else cust_name[0].replace('名字','')
        
    return(GetCustInfo)

# print(OutputCustInfo(pyperclip.paste()))

def GetCustIdBySerialNumber(serial_number):
    tns_crm1 = "UOP_CRM1/qh_Crmdb_1234@10.230.59.93:10909/qhcrmdb"
    Sqlofgetcustid = "select t.cust_id from uop_crm1.tf_f_User t where t.serial_number = '{serial_number}' and t.remove_tag = '0'"
    db = Oracle.connect(tns_crm1)
    cursor = db.cursor()
    cursor.execute(Sqlofgetcustid.format(serial_number = serial_number))
    cust_id = cursor.fetchone()
    cursor.close()
    db.close()
    return cust_id[0]

def UpdateOracleInfo(custinfo):
    tns_cp = "UOP_CP/qh_Crmdb_1234@10.230.59.93:10909/qhcrmdb"
    # tns_cmr1 = "UOP_CRM1/qh_Crmdb_1234@10.230.59.93:10909/qhcrmdb"
    GetCustInfo = OutputCustInfo(custinfo)
    cust_id = GetCustIdBySerialNumber(GetCustInfo['serial_number'])
    GetCustInfo['cust_id'] = cust_id
    if GetCustInfo['serial_number'] == '' or GetCustInfo['transaction_id'] == '' or GetCustInfo['cust_id'] == '':
        print(GetCustInfo)
        print('\n'+'信息不全，请检查！！'+'\n'*3)
    else:
        sql_update = """
                update ucr_cp.tf_f_realname_info t
                set t.verif_result  = '1',
                    t.cust_name     = (select a.cust_name from uop_cp.Tf_f_Cust_Person_rela a where a.cust_id ='{cust_id}' ),
                    t.pspt_id       = (select a.pspt_id from uop_cp.Tf_f_Cust_Person_rela a where a.cust_id ='{cust_id}' ),
                    t.pspt_addr     = (select a.pspt_addr from uop_cp.Tf_f_Cust_Person_rela a where a.cust_id ='{cust_id}' ),
                    t.sex = '0',
                    t.nation = '汉',
                    t.birthday = '1997-08-09',
                    t.issuing_authority = '湖南省衡阳县',
                    t.state = '0',
                    t.cert_validdate = '2013-11-12',
                    t.cert_expdate = '2050-12-31'
                where t.transaction_id = '{transaction_id}'
        """
        db = Oracle.connect(tns_cp)
        cursor = db.cursor()
        sql_update_all = sql_update.format(cust_id = GetCustInfo['cust_id'],transaction_id = GetCustInfo['transaction_id'])
        print(sql_update_all)
        cursor.execute(sql_update_all)
        db.commit()
        cursor.close()
        db.close()

UpdateOracleInfo(pyperclip.paste())



