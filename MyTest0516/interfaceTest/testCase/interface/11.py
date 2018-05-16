import requests
# coding:utf-8
import json
from interfaceTest.common import common
from interfaceTest.common import businessCommon
import interfaceTest.common.configHttp as configHttp
from interfaceTest import readConfig as readConfig
localReadConfig = readConfig.ReadConfig()
localConfigHttp =configHttp.ConfigHttp()
'''
localLogin_xls = common.get_xls("data.xls", "Rupdate")
#print localLogin_xls[0][3]
#print localLogin_xls[0][4]
#data = json.loads(localLogin_xls[0][4])
#print data
# login

def login():

    # set url
    url = common.get_url_from_xml('r-update')
    localConfigHttp.set_url(url)

    # set header
    header = {'Authorization': businessCommon.login(),
              'Content-Type': localReadConfig.get_headers("Content-Type")}
    localConfigHttp.set_headers(header)
    #print 'self.headers is', localConfigHttp.headers

    # set param
    data =json.loads(localLogin_xls[4][4])
    #b={"mid": "f5dd862f-4a36-42b6-8749-433d86ac4988"}
    #data.update(b)
    print  data
    #localConfigHttp.set_data(data)
    #response = localConfigHttp.postWithJson()
    #print response.json()
login()
'''

