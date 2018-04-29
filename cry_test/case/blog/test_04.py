# coding:utf-8
import unittest
import time
class baidu(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print "start!"
    @classmethod
    def tearDownClass(cls):
        print "stop!"

    def test02(self):
        '''测试登录用例，账号：xx 密码xx'''
        print u"执行测试用例02！"

if __name__=="__main__":
     unittest.main()
