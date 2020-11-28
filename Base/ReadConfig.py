# -*- coding:utf-8 -*-
# __author:Administrator
# date: 2019/12/28
import os,time,datetime
import configparser

# 不要使用这种获取项目根目录的方式，如果在其它类中引用，是相对其它类的目录进行。
# proDir1 = os.path.abspath(os.path.join(os.getcwd(), ".."))
proDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
conf_path = proDir + r"\config\\"
case_path = proDir + r"\TestCases\\"
data_path = proDir + r"\Data\\"
page_path = proDir + r"\PageObj\\"
report_path = proDir + r"\Reports\\"
reportDoc_path = proDir + r"\Reports\\document\\"
log_path = proDir + r"\Logs\\"
image_path = proDir + r"\Image\\" + time.strftime("%Y%m%d")

def find_Newfile(dir):
    '''查找dir目录下最新的文件'''
    # 列出目录下所有的文件
    try:
        list = os.listdir(dir)
        #对文件修改时间进行升序排列
        list.sort(key=lambda fn:os.path.getmtime(dir+'\\'+fn))
        #获取最新修改时间的文件
        filetime = datetime.datetime.fromtimestamp(os.path.getmtime(dir+list[-1]))
        #获取文件所在目录
        filepath = os.path.join(dir,list[-1])
        print("最新修改的文件(夹)："+list[-1])
        print("时间："+filetime.strftime('%Y-%m-%d %H-%M-%S'))
        return filepath
    except:
        print('该目录下没有文件')

def get_data_path():
    datapath = proDir + r"\Data\\" + time.strftime("%Y%m%d")
    if not os.path.exists(datapath):
        os.makedirs(datapath)
    return datapath + r"\\"

def get_reportPath():
    reportPath = report_path + time.strftime("%Y%m%d")
    if not os.path.exists(reportPath):
        os.makedirs(reportPath)
    return reportPath + r"\\"

def get_reportDoc_path():
    reportDocPath = reportDoc_path + time.strftime("%Y%m%d")
    if not os.path.exists(reportDocPath):
        os.makedirs(reportDocPath)
    return reportDocPath + r"\\"

def get_image_path():
    if not os.path.exists(image_path):
        os.makedirs(image_path)
    return image_path + r"\\"

class ReadConfig:
    """
    创建ConfigParser对象，读取指定目录conf_path配置文件config_name
    """
    def __init__(self, config_name):
        self.conf = configparser.ConfigParser()
        # 中文乱码问题需要添加encoding="utf-8-sig"
        self.conf.read(conf_path + config_name, encoding="utf-8-sig")

    def get_ngboss(self, name):
        value = self.conf.get("NGBOSS", name)
        return value

    def get_oracle(self, name):
        value = self.conf.get("ORACLE", name)
        return value

    def get_interface_url(self, name):
        value = self.conf.get("INTERFACE_URL", name)
        return value

    def get_data_path(self):
        proDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = proDir + r"\Data\\"
        return path

    def get_report_path(self):
        proDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = proDir + r"\Repots\\"
        return path

if __name__ == '__main__':
    co = ReadConfig("ngboss_config.ini")
    print(co.get_ngboss("url"))
    print(proDir)
    conn = co.get_oracle("cp")
    print(conn)
    print(case_path)
    # print(get_reportPath())
    print(get_reportDoc_path())

    # print(find_Newfile(dir = get_reportPath()))






