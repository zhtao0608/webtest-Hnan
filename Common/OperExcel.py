# -*- coding:utf-8 -*-
import xlrd,xlwt,os
from Common import ReadConfig
from xlutils.copy import copy
from openpyxl import Workbook

Lable = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
workbook = None

def open_excel(file):
    """
    打开Excel
    :param path: Excel路径
    :return:
    """
    global workbook
    if workbook == None:
        workbook = xlrd.open_workbook(file)
    return workbook

def get_sheet(sheetName):
    global workbook
    return workbook.sheet_by_name(sheetName)

def get_sheet_by_index(index):
    global workbook
    return workbook.sheet_by_index(index)

def get_row(sheet):
    return sheet.nrows

def get_col(sheet):
    return sheet.ncols

def get_cell_content(sheet, row, col):
    """
    获取单元格内容
    :param sheet: sheet名
    :param row: 行
    :param col: 列
    :return:
    """
    return sheet.cell_value(row, col)

def getColumnIndex(file,columnName,index=0):
    xl = xlrd.open_workbook(file)
    sheet = xl.sheet_by_index(index)
    table = sheet.row_values(0)
    # print('获取的table:',table)
    for i in range(len(table)):
        if table[i] == columnName:
            columnIndex = i
            break
    return columnIndex

def get_xls(xls_name, sheet_name):
    """
    获取excel表中指定sheet数据，保存到列表中返回
    :param xls_name: excel文件名
    :param sheet_name: sheet表名
    :return:
    """
    cls = []
    xls_path = os.path.join(ReadConfig.data_path, xls_name)
    # print(xls_path)
    file = open_excel(xls_path)
    sheet = file.sheet_by_name(sheet_name)
    sheet_nrows = sheet.nrows
    for i in range(sheet_nrows):
        if sheet.row_values(i)[0] != u'case_name':
            cls.append(sheet.row_values(i))
    return cls

def get_datas(file,name):
    xl = xlrd.open_workbook(file)
    sheet = xl.sheet_by_name(name)
    items = sheet.row_values(0)
    datas = []
    for nrow in range(1,sheet.nrows):
        data = dict()
        values = sheet.row_values(nrow)
        for ncol in range(0,len(items)):
            data[items[ncol]]=values[ncol]
            datas.append(data)
        return datas

#     获取xls数据，并转换成字典List，格式处理成json
#     :param filename: 完整路径
#     :param index: xls表格sheet页，如第一个sheet ,则index = 0
#     :return:数组，每个元素为dic
#     [{'leave': '昆明', 'arrive': '长沙', 'leave_date': '2020-04-30'},
#     {'leave': '上海', 'arrive': '南京', 'leave_date': '2020-05-30'},
#     {'leave': '北京', 'arrive': '武汉', 'leave_date': '2020-04-22'}]

def get_exceldata(filename,index=0):
	boot_data = xlrd.open_workbook(filename)
	book_sheet = boot_data.sheet_by_index(index)
	rowsnum = book_sheet.nrows
	# print("列表行数："+str(rowsnum))
	#第一行当做字段的键
	rows0 = book_sheet.row_values(0)
	rows0_num = len(rows0)
	# print("列表列数:"+str(rows0_num))
	list = []
    #获取列表数据，并转换成字典List，格式处理成json
	for i in range(1,rowsnum):
		rows_data = book_sheet.row_values(i)  ###取第一行的值作为列表
		rows_dic = {}
		for y in range(0,rows0_num):
			rows_dic[rows0[y]]=rows_data[y]
		list.append(rows_dic)
	return list

def read_excel_byList(file_name, index=0):
    '''按行读取xls，并将xls内容（包含表头），返回list
    ['leave', 'arrive', 'leave_date', '昆明', '长沙', '2020-04-30', '上海', '南京', '2020-05-30', '北京', '武汉', '2020-04-22']
    '''
    xls = xlrd.open_workbook(file_name)
    sheet = xls.sheet_by_index(index)
    print(sheet.nrows)
    print(sheet.ncols)
    data = []
    for j in range(sheet.nrows):
        for i in range(sheet.ncols):
            data.append(sheet.row_values(j)[i])
            print(sheet.row_values(j)[i])
            # print("函数体类")
        # dic[j] = data
    print(data)
    return data

def read_excel(filename,index=0):
    ''' 按xls列逐个读取，按列返回字典，列数为key ,每列内容为value
    :param filename:
    :param index:
    :return:
    {0: ['leave', '昆明', '上海', '北京'],
    1: ['arrive', '长沙', '南京', '武汉'],
    2: ['leave_date', '2020-04-30', '2020-05-30', '2020-04-22']}
    '''
    xls = xlrd.open_workbook(filename)
    sheet = xls.sheet_by_index(index)
    print(sheet.nrows)
    print(sheet.ncols)
    dic = {}
    for j in range(sheet.ncols):
        data =[]
        for i in range(sheet.nrows):
            data.append(sheet.row_values(i)[j])
        dic[j]=data
    return dic

def read_xls_by_row(filename,index=0):
    '''按xls行读取，返回dic,每行内容做为一个数组
    {
    0: ['leave', 'arrive', 'leave_date'],
    1: ['昆明', '长沙', '2020-04-30'],
    2: ['上海', '南京', '2020-05-30'],
    3: ['北京', '武汉', '2020-04-22']}
    '''
    xls = xlrd.open_workbook(filename)
    sheet = xls.sheet_by_index(index)
    print(sheet.nrows)
    print(sheet.ncols)
    dic = {}
    for i in range(sheet.nrows):
        data = []
        for j in range(sheet.ncols):
            data.append(sheet.row_values(i)[j])
        dic[i] = data
    return dic

def write_excel_xls(file, sheet_name, value):
    '''新建表格写入'''
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlwt.Workbook()  # 新建一个工作簿
    sheet = workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.write(i, j, value[i][j])  # 像表格中写入数据（对应的行和列）
    workbook.save(file)  # 保存工作簿
    print("xls格式表格写入数据成功！")


def write_dict_xls(inputData,sheetName,outPutFile):
    '''
    :param inputData: 列表，含有多个字典;例如：[{'key_a':'123'},{'key_b':'456'}]
    :param outPutFile: 输出文件名，例如：'data.xlsx'
    :return:
    '''
    wb = Workbook()
    # wb = xlrd.open_workbook()
    sheet = wb.active
    sheet.title = sheetName
    item_0 = inputData[0]
    print('要写入xls的数据：',inputData)
    i = 0
    for key in item_0.keys():
        sheet[Lable[i]+str(1)].value = key
        i = i+1
    j = 1
    for item in inputData:
        k = 0
        for key in item:
            sheet[Lable[k]+str(j+1)].value = item[key]
            k = k+1
        j = j+1
    wb.save(outPutFile)
    print('数据写入xls完毕!xls文件名:{}'.format(outPutFile))


def write_excel_append(file,row,col,value,index=0):
    '''追加写入xls，在xls指定行列写入数据'''
    workbook = xlrd.open_workbook(file,formatting_info=True)  # 打开工作簿
    worksheet = workbook.sheet_by_index(index)  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    # 将xlrd对象拷贝转化为xlwt对象
    new_workbook = copy(workbook)
    new_worksheet = new_workbook.get_sheet(index)  # 获取转化后工作簿中的第一个表格
    new_worksheet.write(row, col, value) # 像指定行列写入数据
    new_workbook.save(file)  # 保存工作簿
    print("xls格式表格【追加】写入数据成功！")


def write_xlsBycolName_append(file,row,colName,value,index=0):
    '''追加写入xls，在xls指定行列写入数据'''
    filename = file
    # workbook = xlrd.open_workbook(filename,formatting_info=True)  # 打开工作簿
    workbook = xlrd.open_workbook(filename)  # 打开工作簿
    worksheet = workbook.sheet_by_index(index)  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    # 将xlrd对象拷贝转化为xlwt对象
    new_workbook = copy(workbook)
    new_worksheet = new_workbook.get_sheet(index)  # 获取转化后工作簿中的第一个表格
    columnName = colName
    col = getColumnIndex(file,columnName,index)  #根据colName获取对应的列数
    new_worksheet.write(row, col, value) # 像指定行列写入数据
    new_workbook.save(file)  # 保存工作簿
    print("xls格式表格【追加】写入数据成功！")


if __name__ == '__main__':
    # wb = open_excel(ReadConfig.data_path+"TestCase.xls")
    # ws = get_sheet_by_index(0)
    # row = get_row(ws)
    # col = get_col(ws)
    # cell_content = get_cell_content(ws, 3, 2)
    # print(type(cell_content))
    # print(ws.name, row, col, cell_content)
    # datas = get_exceldata(ReadConfig.data_path+"testdata2.xls",0)
    offers_para = get_exceldata(ReadConfig.data_path+"UITest_GrpBusiOper.xls",0)[0]
    print(type(offers_para))
    print("业务受理参数：", offers_para)
    # for i in range(len(offers_para)):
    #     # print(offers_para[i])
    #     print(offers_para[i]['subofferList'])
    index = int(offers_para.get('No'))  # 标识行号，后续写入xls使用
    print("index:" + str(index))
    groupId = str(offers_para.get('groupId'))
    print("集团编码:" + groupId)
    offerid = str(offers_para.get('mainoffer'))  # 集团主商品ID
    subOfferList = offers_para.get('subofferList').replace(" ", "").split(',')
    # subOfferList = dict_get(offers_para,'subofferList',None).split(',')
    print("subOfferList:" ,subOfferList)
    print(type(subOfferList))

    # xls = get_xls("TestCase.xls","intf_test")
    # print(xls)
    # value = ['ok']
    # print(len(value))
    # write_excel_append(ReadConfig.data_path+"testdata2.xls", value)
    # colIndex = getColumnIndex(ReadConfig.data_path+"UITest_GrpBusiOper.xls", 'subofferList', index=0)
    # print('subofferList对应的列数：',colIndex)
    # file = ReadConfig.data_path+"UITest_data_20200525005.xls"
    # print(file)
    # write_xlsBycolName_append(file, 2, 'RESULT_INFO', 'testtest-nonono')  # 向xls模板指定行列写入结果

    file = ReadConfig.data_path+"UITest_ShareActive.xls"
    value = [{'NO': 1, 'ACCESS_NUM': '18708700011', 'SUBSCRIBER_INS_ID': '7012082036480364', 'FLOW_ID': None, 'RESULT_INFO': None}, {'NO': 2, 'ACCESS_NUM': '18708700018', 'SUBSCRIBER_INS_ID': '7015102653160225', 'FLOW_ID': None, 'RESULT_INFO': None}, {'NO': 3, 'ACCESS_NUM': '18708700048', 'SUBSCRIBER_INS_ID': '7014011344200264', 'FLOW_ID': None, 'RESULT_INFO': None}]
    # write_dict_xls(inputData =value, sheetName='testData', outPutFile=file)
    write_xlsBycolName_append(file, 1, '检查点', '测试测试')
    write_xlsBycolName_append(file, 1, '交互流水号', '1231231231231233')







