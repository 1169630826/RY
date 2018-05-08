# coding:utf-8
import json
import unittest
import paramunittest
from interfaceTest.common import common1
from interfaceTest.common import businessCommon
from interfaceTest.common.Log import MyLog
import interfaceTest.readConfig as readConfig
from interfaceTest.common import configHttp as configHttp

model_xls= common1.get_xls("data.xls", "model")
localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
#print updater_xls

@paramunittest.parametrized(*model_xls)
class remove(unittest.TestCase):
    def setParameters(self, case_name, method, token, param, result, stat, msg):
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.param = str(param)
        self.result = str(result)
        self.stat = str(stat)
        self.msg =msg
        self.response = None
        self.info = None
        self.logintoken=None

    def description(self):
        return self.case_name

    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        self.logintoken=businessCommon.login()

    def testinterface(self):
        url = common1.get_url_from_xml('model')
        nurl = url + "/" + localReadConfig.get_param("mid")
        localConfigHttp.set_url(nurl,flag=2)
        print localConfigHttp.url

        if self.token=="0":
           token=localReadConfig.get_headers("token_u")
           print "token form conf.ini is", token
        else:
           token=self.logintoken

        if self.param == '' or self.param is None:
            param ={"token":token}
            print "param A is", param
        else:
            param = json.loads(self.param)
            print "param B is" ,param

        localConfigHttp.set_params(param)
        print "localConfigHttp.params is", localConfigHttp.params

        headers = {"Authorization": token}
        localConfigHttp.set_headers(headers)

        self.response=localConfigHttp.get()
        print self.response.url
        print self.response.text

        # check result
        self.checkResult()

    def tearDown(self):
        #self.log.build_case_line(self.case_name, self.info['stat'], self.info['msg'])
        print "end!"

    def checkResult(self):
        #方法一  直接判断是不是为空
        self.assertIsNotNone(self.response.text)
        #方法二  判断结果赋值给bool，然后用assert验证结果bool是不是True
        bool=self.response.text!= None
        self.assertTrue(bool)
        #方法三判断结果赋值给bool，然后用assert验证结果bool与True是不是相等
        bool = self.response.text != None
        self.assertEqual(bool,True)




    """
    def checkResult(self):
     url = self.response.url
     print(u"\n请求地址：" + url)
     self.assertNotEqual( len(self.response.text),0)
    """