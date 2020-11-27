import unittest
import time
from Base import ReadConfig
from Base.Mylog import LogManager

rc = ReadConfig.ReadConfig("ngboss_config.ini")
logger = LogManager('MainPlanSelectPart').get_logger_and_add_handlers(1,is_add_stream_handler=True, log_path=ReadConfig.log_path, log_filename=time.strftime("%Y-%m-%d")+'.log' )


class Assertion(unittest.TestCase):
    '''
     为了使我们的Assert验证多条用例或者方法是否正确,
    所以需要设定一个boolean值来进行判断识别,私有变量,防止外部访问
     * */
    '''
    def __init__(self):
        self.flag = True
        self._type_equality_funcs ={}

    def currentFlag(self):
        return self.flag

    def setFlag(self,flag):
        self.flag = flag;

    def verifyEquals(self,actual, expected):
        '''
        校验实际结果与预期结果是否一致
        :param actual:
        :param expected:
        :return:
        '''

        try:
            self.assertEqual(actual,expected)
        except  AssertionError as e:
            print(e)
            self.setFlag(False)  #如果断言失败则设置flag 为False


    def verifyassertIn(self, actual, expected,message=None):
        '''
        校验实际结果与预期结果是否一致
        :param actual:
        :param expected:
        :param msg:
        :return:
        '''

        try:
            self.assertIn(actual, expected,msg=message)
        except AssertionError as e:
            print(e)
            self.setFlag(False)  # 如果断言失败则设置flag 为False

    def verifyassertTrue(self, flag,message=None):
        '''
        校验实际结果与预期结果是否一致
        :param actual:
        :param expected:
        :param msg:
        :return:
        '''
        try:
            self.assertTrue(flag,msg=message)
        except AssertionError as e:
            print(e)
            self.setFlag(False)  # 如果断言失败则设置flag 为False

if __name__ == '__main__':
    MyAssert = Assertion()
    a='111661'
    b='2221111'
    c = False
    d = None
    # MyAssert.assertEqual(a,b,msg='断言失败')
    # MyAssert.assertEquals(a,c,msg='断言失败')
    MyAssert.assertIsNone(a)

