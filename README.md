# webtest
云南WEBTEST自动化项目 \
使用框架:Python + Selenium + UnitTest + DDT + Excel \
接口：Python + Request + + UnitTest + DDT + Excel \
功能简述：

1.UI自动化采用PO分层设计模式 \
2.selenium元素定位和操作进行二次封装，代码：webtest\Base\Base.py \
3.建立测试数据管理，Common\TestDataMgnt.py,功能持续完善中...... \
4.测试试案例管理，allrun.py,将测试案例配置到config\caselist.txt \
5.测试环境信息配置在config\ngboss_config_ini文件，通过ReadConfig读取 \
6.使用Orcale_cx 自动从测试数据库抽取测试数据，并将测试数据自动写入xls，路径：Webtest/Data/YYYYMMDD/*.xls \
7.OperExcle封装了常用的xls操作方法，案例执行后自动将测试结果更新到测试数据xls文件。\
8.使用pythonDoc，UI自动化测试执行关键步骤截图到Doc文档，文档保存路径：webtest\Reports\document\YYYYMMDD/*.docx \
9.关于测试报告，二次开发HTMLTestRunnerCN,实现饼图和截图功能。如脚本执行异常会自动截图展示在Html报告 \
10.测试结果保存三份格式：\
   Doc记录UI自动化脚本执行过程中关键检查点步骤，保存目录：webtest\Reports\document\YYYYMMDD\ \
   xls保存测试脚本生成的测试数据，结果保存在Webtest/Data/YYYYMMDD/*.xls ，如成功记录流水号FlowId，如失败将检查点错误信息记录到RESULT_Info字段 \
   暂时是一个testCase一个表格。\
   Html记录自动化脚本测试报告，汇总测试结果。\
11.目前已实现的案例：\
   UI：个人业务包括：个人用户开户、商品订购、换卡、停开机业务受理、共享业务、家庭网业务、普通付费关系变更、过户、销户、业务返销等核心业务 （后续完善....\.）
       集团业务包括：集团商品业务受理、成员商品业务受理、集团付费关系变更、集团营销活动办理\
   API:商品订购、停开机、实名制资料登记、用户密码变更等...
   
