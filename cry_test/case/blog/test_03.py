# coding=utf-8
import unittest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import HtmlTestRunner
import time
@unittest.skip(u"无条件跳过此用例")
class Bloghome(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver=webdriver.Firefox()
        url="http://www.cnblogs.com/yoyoketang/"
        cls.driver.get(url)
        cls.driver.implicitly_wait(5)
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


    def test_01(self):
        loactor = ("id", "blog_nav_sitehome")
        text = u"博客园"
        result = EC.text_to_be_present_in_element(loactor, text)(self.driver)
        self.assertTrue(result)
    def test_03(self):
        loactor=("id", "blog_nav_newpost")
        text = u"新随笔"
        result = EC.text_to_be_present_in_element(loactor,text)(self.driver)
        self.assertTrue(result)

    def test_02(self):
         locator = ("id", "blog_nav_myhome")
         text = u"首页"
         result=EC.text_to_be_present_in_element(locator,text)(self.driver)
         self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()










