# coding:utf-8
import os
import requests
#导入了readConfig文件
from interfaceTest import readConfig
#  Log必须调用get_logger函数才能真正调用 Log类实例
from interfaceTest.common.Log import MyLog as Log
import json
import time
# 类readConfig实例化
localReadConfig = readConfig.ReadConfig()
#该类是定义了请求需要的各个参数以及不同类型的请求的执行方法及返回值

class ConfigHttp:

    def __init__(self):
        global scheme, host, port, timeout
        scheme = localReadConfig.get_http("scheme")
        host = localReadConfig.get_http("baseurl")
        port = localReadConfig.get_http("port")
        timeout = localReadConfig.get_http("timeout")
        #真正调用了Log示例，在线程中只有一个线程在执行（线程锁）
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        #print self.logger
        self.url = None
        self.headers = {}
        self.params = {}
        self.data = {}
        self.files = {}
        self.state = 0
    # 因为self.url已经在初始化函数中定义，所以在一个函数中url传参赋值给self.url,则初始化函数的self.url就有了值。简单的说
    #这些函数就起到了一个赋值的作用。

    def set_url(self, url,flag=1):
        if flag==1:
          self.url = scheme+'://'+host+url
        else:
          self.url = scheme + '://' +localReadConfig.get_param("host") + url
          print (self.url)
          return self.url

    def set_headers(self, header):
        """
        set headers
        :param header:
        :return:
        """
        self.headers = header
        return self.headers
    def set_params(self, param):
        """
        set params
        :param param:
        :return:
        """
        self.params = param

    def set_data(self, data):
        """
        set data
        :param data:
        :return:
        """
        self.data = data
        #print self.data

    def set_files(self, filename):
        """
        set upload files
        :param filename:
        :return:
        """
        if filename != '':
            filepath = os.path.dirname(os.path.dirname(__file__))
            file_path = filepath + '/testFile/img/' + filename
            self.files = {'file': open(file_path, 'rb')}

        if filename == '' or filename is None:
            self.state = 1
        print (filename)
    # defined http get method
    def get(self):
        """
        defined get method
        :return:
        """
        try:
            response = requests.get(self.url, headers=self.headers, params=self.params, timeout=float(timeout))
            # response.raise_for_status()
            return response
        except BaseException:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # include get params and post data
    # uninclude upload file
    def post(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data, timeout=float(timeout))
            # response.raise_for_status()
            return response
        except BaseException:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # include upload file
    def postWithFile(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data, files=self.files, timeout=float(timeout))
            return response
        except BaseException:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # for json
    def postWithJson(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, json=self.data, timeout=float(timeout))
            return response
        except BaseException:
            self.logger.error("Time out!")
            return None

#if __name__ == "__main__":
    #ConfigHttp()
    #print("ConfigHTTP")

