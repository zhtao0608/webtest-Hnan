import xlrd,os
from Common.function import project_path

def read_excel_byList(file_name, index):
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

def read_excel(filename,index):
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

def read_xls_by_row(filename,index):
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

def get_exceldata(filename,index):
	boot_data = xlrd.open_workbook(filename)
	book_sheet = boot_data.sheet_by_index(index)
	rowsnum = book_sheet.nrows
	print("列表行数："+str(rowsnum))
	#第一行当做字段的键
	rows0 = book_sheet.row_values(0)
	rows0_num = len(rows0)
	print("列表列数:"+str(rows0_num))
	list = []
    #获取列表数据，并转换成字典List，格式处理成json
	for i in range(1,rowsnum):
		rows_data = book_sheet.row_values(i)  ###取第一行的值作为列表
		rows_dic = {}
		for y in range(0,rows0_num):
			rows_dic[rows0[y]]=rows_data[y]
		list.append(rows_dic)
	return list

def get_dicvalue(list,key):
    """处理嵌套dict的列表"""
    for i in range(len(list)):
        value = list[i][key]
        print(value)
    return value


if __name__ == '__main__':
    data_01 = read_excel(project_path() + '/Data/testdata2.xls',0)
    data_02 = read_excel_byList(project_path() + '/Data/testdata2.xls',0)
    data_03 = get_exceldata(project_path() + '/Data/testdata2.xls',0)
    data_04 = read_xls_by_row(project_path() + '/Data/testdata2.xls',0)
    print("打印read_excel方法：*********************")
    print(data_01)
    print("打印read_excel_byList方法：*********************")
    print(data_02)
    print("打印get_exceldata方法：*********************")
    print(data_03)
    print("read_xls_by_row：*********************")
    print(data_04)
    print("##########第一种##########")
    print(data_01.get(0))
    print("########第二种############")
    print(data_02.pop(1))
    print("#########第三种###########")
    # print(data_03['user'])
    # dict_01 = dict(data_03[1])
    # print(dict_01)
    # print(data_03[1]['user'])
    for i in range(len(data_03)):
        dic = data_03[i]
        # print(dic['IP'])
        # for keys in data_03[i]:
        #     print(data_03[i].items())
        for key,value in data_03[i].items():
            print(key,value)

    print("##########第四种##########")
    print(data_04.get(0))
    print(data_04.get(1)[0],data_04.get(1)[1],data_04.get(1)[2])


    print("+++++测试数据准备+++++")
    print(data_01.get(1)[0],data_01.get(1)[1],data_01.get(1)[2])
    print(data_04.get(1)[0],data_04.get(1)[1],data_04.get(1)[2])
    print("######################################################")
    # get_dicvalue(data_03,'leave')
    # get_dicvalue(data_03,'arrive')
    # get_dicvalue(data_03,'leave_date')

    for i in range(len(data_03)):
         print(data_03[i]['leave'],data_03[i]['arrive'],data_03[i]['leave_date'])




