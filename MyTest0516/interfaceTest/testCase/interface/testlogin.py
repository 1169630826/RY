import json
import unittest
import paramunittest
from interfaceTest.common import common
from interfaceTest.common import businessCommon
from interfaceTest.common.Log import MyLog
import interfaceTest.readConfig as readConfig
from interfaceTest.common import configHttp as configHttp

login_xls= common.get_xls("data.xls", "login")
localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()


@paramunittest.parametrized(*login_xls)
class Login(unittest.TestCase):
    def setParameters(self, case_name, method, token, param, result, stat, msg):
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.param = str(param)
        self.result = str(result)
        self.stat = stat
        self.msg = msg
        self.response = None
        self.info = None
        self.logintoken=None

    def description(self):
        return self.case_name
    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        self.logintoken=businessCommon.login()
        common.set_visitor_token_to_config(self.logintoken)
    def testinterface(self):
        # set uer
        self.url = common.get_url_from_xml('login')
        localConfigHttp.set_url(self.url)
        #config param
        params = json.loads(self.param)
        localConfigHttp.set_data(params)
        # set headers
        if self.token == '0':
            token = localReadConfig.get_headers("token_u")
        else:
            token = self.logintoken
        headers = {"Authorization": str(token),
                   'Content-Type': localReadConfig.get_headers("content-type")}
        localConfigHttp.set_headers(headers)
        # get http
        self.response = localConfigHttp.postWithJson()
        # check result
        self.checkResult()

    def tearDown(self):
        self.log.build_case_line(self.case_name, self.info['stat'], self.info['msg'])

    def checkResult(self):
        self.info = self.response.json()

        print "\n"
        print self.case_name
        common.show_return_msg(self.response)

        if self.result == '0':
            self.assertEqual(self.info['stat'], self.stat)
            self.assertEqual(self.info['msg'], self.msg)
        if self.result == '1':
            self.assertEqual(self.info['stat'], self.info['stat'])
