# coding:utf-8
import json
from interfaceTest.common import common
import interfaceTest.common.configHttp as configHttp
from interfaceTest import readConfig as readConfig
localReadConfig = readConfig.ReadConfig()
localConfigHttp =configHttp.ConfigHttp()

localLogin_xls = common.get_xls("data.xls", "login")
#print localLogin_xls
#data = json.loads(localLogin_xls[0][4])
#print data
# login

def login():

    # set url
    url = common.get_url_from_xml('login')
    localConfigHttp.set_url(url)
    #print 'self.url is',localConfigHttp.url

    # set header
    header = {'Content-Type':localReadConfig.get_headers("Content-Type")}
    localConfigHttp.set_headers(header)
    #print 'self.headers is', localConfigHttp.headers

    # set param
    data= json.loads(localLogin_xls[0][3])
    localConfigHttp.set_data(data)
    #print "priramry data is",data
    #print 'self.data is',localConfigHttp.data
    # login
    response = localConfigHttp.postWithJson().json()
    token_v = response['value']['token']['refresh_token']
    token = "Bearer" + " " + token_v
    #print "token is", token
    #print 'businessCommon token is ',token
    return token
# logout
def logout(token):

    # set url

    url = common.get_url_from_xml('logout')
    localConfigHttp.set_url(url)

    # set header
    header = {'token': token}
    localConfigHttp.set_headers(header)

    # logout
login()