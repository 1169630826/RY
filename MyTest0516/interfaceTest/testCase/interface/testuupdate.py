# coding:utf-8
import json
import unittest
import requests
import paramunittest
from interfaceTest.common import common
from interfaceTest.common import businessCommon
from interfaceTest.common.Log import MyLog
import interfaceTest.readConfig as readConfig
from interfaceTest.common import configHttp as configHttp

updateu_xls= common.get_xls("data.xls", "Uupdate")
localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
#print updateu_xls
@paramunittest.parametrized(*updateu_xls)
class Uupdate(unittest.TestCase):
    def setParameters(self, case_name, method, token,params, result, stat, msg):
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.params = str(params)
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
        """
        test body
        :return:
        """
        # set uel
        self.url = common.get_url_from_xml('u-update')
        localConfigHttp.set_url(self.url)
        print "localConfigHttp.url is", localConfigHttp.url

        # set params
        if self.params == '' or self.params is None:
            params=localReadConfig.get_param("mid")
        else:
            params=self.params
        localConfigHttp.set_data(params)
        print "localConfigHttp.data is", localConfigHttp.data
        if self.token=="0":
           token=localReadConfig.get_headers("token_u")
           print "token form conf.ini is", token
        else:
           token=self.logintoken
        self.headers = {"Authorization": token,
                         "Content-Type":localReadConfig.get_headers("content-type") }
        localConfigHttp.set_headers(self.headers)
        print "localConfigHttp.headers is", localConfigHttp.headers
        self.response =localConfigHttp.postWithJson()
        # check result
        self.checkResult()

    def tearDown(self):       
        self.log.build_case_line(self.case_name, self.info['stat'], self.info['msg'])
        print "end!"
    def checkResult(self):
        self.info = self.response.json()
        common.show_return_msg(self.response)

        if self.result == '0':
            self.assertEqual(self.info['stat'], self.code)
            #self.assertEqual(self.info['msg'], self.msg)
            #goods_id = common.get_value_from_return_json(self.info, "Product", "goods_id")
            #self.assertEqual(goods_id, self.goodsId)
        if self.result == '1':
            self.assertEqual(self.info['stat'], self.info['stat'])
            #self.assertEqual(self.info['msg'], self.msg)
