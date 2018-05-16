import json
import re
import unittest
import paramunittest
from interfaceTest.common import common
from interfaceTest.common import businessCommon
from interfaceTest.common.Log import MyLog
import interfaceTest.readConfig as readConfig
from interfaceTest.common import configHttp as configHttp
import requests

totalmodelsize_xls= common.get_xls("data.xls", "totalmodelsize")
localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
#print totalmodelsize_xls

@paramunittest.parametrized(*totalmodelsize_xls)
class Totalmodelsize(unittest.TestCase):
    def setParameters(self, case_name, method, token, param, result, stat, msg):
        """
        set params
        :param case_name:
        :param method:
        :param token:
        :param goods_id:
        :param result:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.param = str(param)
        self.result = str(result)
        self.stat = str(stat)
        self.msg = msg
        self.response = None
        self.info = None
        self.logintoken=None

    def description(self):
        """

        :return:
        """
        return self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        self.logintoken=businessCommon.login()
    def testinterface(self):
        """
        test body
        :return:
        """
        # set uel
        self.url = common.get_url_from_xml('totalmodelsize')
        print "11 is", localConfigHttp.set_url(self.url)
        # set params
        if self.param == '' or self.param is None:
            params =None
        else:
            params = json.loads(self.param)
        localConfigHttp.set_data(params)
        # set headers
        if self.token == '0':
            token = localReadConfig.get_headers("token_u")
        else:
            token = self.logintoken
        headers = {'Authorization': str(token),
                   'Content-Type': localReadConfig.get_headers("content-type")}
        localConfigHttp.set_headers(headers)
        # get http
        self.response = localConfigHttp.postWithJson()


        # check result
        self.checkResult()
    def tearDown(self):
        """

        :return:
        """
        self.log.build_case_line(self.case_name, self.info['stat'], self.info['msg'])

    def checkResult(self):
        self.info = self.response.json()
        common.show_return_msg(self.response)

        if self.result == '0':
            self.assertEqual(self.info['stat'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
            #goods_id = common.get_value_from_return_json(self.info, "Product", "goods_id")
            #self.assertEqual(goods_id, self.goodsId)
        if self.result == '1':
            self.assertEqual(self.info['stat'], self.info['stat'])
            self.assertEqual(self.info['msg'], self.msg)
