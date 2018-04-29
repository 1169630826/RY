# coding:utf-8
import unittest
import time
class Test(unittest.TestCase):
    def setUp(self):
        print "start!"
    def tearDown(self):
        time.sleep(1)
        print "end!"
    def test01(self):
        '''test_01测试成功'''
        print "执行测试用例01"
    def test02(self):
        print "执行测试用例03"

    @unittest.skipIf(False, u"为False的时候跳过")
    def test03(self):
        '''失败案例'''
        a = "上海-悠悠"
        b = 'yoyo'
        self.assertEqual(a,b,msg="失败原因:%s,%s" %(a,b))

if __name__=="__main__":
    unittest.main()
