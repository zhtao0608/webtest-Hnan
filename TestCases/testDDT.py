import unittest
from ddt import ddt, data, unpack

# param = [{"username":"ljx","password":"123456"},{"username":"wuhan","password":"152738748"}]
# param = [{'accessNum': '13574114343', 'busiName': '报停', 'SUITE_CASE_ID': '202101041139501070', 'SUITE_CODE': 'SvcStateChgTest', 'SUITE_NAME': '停开机业务测试', 'EXPECT_RESULT': '业务受理成功', 'EXEC_TIME': None, 'SCENE_CODE': 'ChgSvcState_01', 'PATH': './person/ChgSvcStateTest'}], [{'accessNum': '13574114343', 'busiName': '报开', 'SUITE_CASE_ID': '202101041139501071', 'SUITE_CODE': 'SvcStateChgTest', 'SUITE_NAME': '停开机业务测试', 'EXPECT_RESULT': '业务受理成功', 'EXEC_TIME': None, 'SCENE_CODE': 'ChgSvcState_02', 'PATH': './person/ChgSvcStateTest'}], [{'accessNum': '13574114343', 'busiName': '局方停机', 'SUITE_CASE_ID': '202101041139501072', 'SUITE_CODE': 'SvcStateChgTest', 'SUITE_NAME': '停开机业务测试', 'EXPECT_RESULT': '业务受理成功', 'EXEC_TIME': None, 'SCENE_CODE': 'ChgSvcState_03', 'PATH': './person/ChgSvcStateTest'}], [{'accessNum': '13574114343', 'busiName': '局方开机', 'SUITE_CASE_ID': '202101041139501073', 'SUITE_CODE': 'SvcStateChgTest', 'SUITE_NAME': '停开机业务测试', 'EXPECT_RESULT': '业务受理成功', 'EXEC_TIME': None, 'SCENE_CODE': 'ChgSvcState_04', 'PATH': './person/ChgSvcStateTest'}]
param = [{'accessNum': '13574114343', 'busiName': '报停', 'SUITE_CASE_ID': '202101041139501070', 'SUITE_CODE': 'SvcStateChgTest', 'SUITE_NAME': '停开机业务测试', 'EXPECT_RESULT': '业务受理成功', 'EXEC_TIME': None, 'SCENE_CODE': 'ChgSvcState_01', 'PATH': './person/ChgSvcStateTest'}, {'accessNum': '13574114343', 'busiName': '报开', 'SUITE_CASE_ID': '202101041139501071', 'SUITE_CODE': 'SvcStateChgTest', 'SUITE_NAME': '停开机业务测试', 'EXPECT_RESULT': '业务受理成功', 'EXEC_TIME': None, 'SCENE_CODE': 'ChgSvcState_02', 'PATH': './person/ChgSvcStateTest'}, {'accessNum': '13574114343', 'busiName': '局方停机', 'SUITE_CASE_ID': '202101041139501072', 'SUITE_CODE': 'SvcStateChgTest', 'SUITE_NAME': '停开机业务测试', 'EXPECT_RESULT': '业务受理成功', 'EXEC_TIME': None, 'SCENE_CODE': 'ChgSvcState_03', 'PATH': './person/ChgSvcStateTest'}, {'accessNum': '13574114343', 'busiName': '局方开机', 'SUITE_CASE_ID': '202101041139501073', 'SUITE_CODE': 'SvcStateChgTest', 'SUITE_NAME': '停开机业务测试', 'EXPECT_RESULT': '业务受理成功', 'EXEC_TIME': None, 'SCENE_CODE': 'ChgSvcState_04', 'PATH': './person/ChgSvcStateTest'}]
print('******************',*param)
@ddt
class TestDdt(unittest.TestCase):
    def setUp(self):
        print("setUp!")

    def tearDown(self):
        print("tearDown!")
        print('=====测试结束！=====')

    @data(*param)
    # @unpack
    def test_work(self,value):
        print('========测试开始==========')
        print(value)
        print(type(value))
        # value=value[0]
        print(value['accessNum'])
        print(value['busiName'])
        print(value['SUITE_CASE_ID'])





if __name__ == '__main__':
    unittest.main()