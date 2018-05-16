# coding:utf-8
import requests
from interfaceTest import readConfig
import os
from xlrd import open_workbook
from xml.etree import ElementTree as ElementTree
from interfaceTest.common.configHttp import ConfigHttp
from interfaceTest.common.Log import MyLog as Log
import json

localReadConfig = readConfig.ReadConfig()
proDir = readConfig.proDir
localConfigHttp = ConfigHttp()
# log = Log.get_log()
# logger = log.get_logger()

caseNo = 0


# 把token信息写入配置文件，以满足接口调用需求
# #sql xml文件中取出信息构成数据库，并定义从数据库中取库和表名的方法
# 从urlxml中取出信息组成 url地址，以满足接口请求的需要
# 执行登陆操作，获取token
def get_visitor_token():
    """
    create a token for visitor
    :return:
    """
    host = localReadConfig.get_http("baseurl")
    port = localReadConfig.get_http("port")
    response = requests.post(host + port + "/user/login")
    jsondata = response.json()
    token_v = jsondata['value']['token']['refresh_token']
    token = "Bearer" + " " + token_v
    # logger.debug("Create token:%s" % (token))
    return token


# 把token保存到配置文件
def set_visitor_token_to_config(token):
    """
    set token that created for visitor to config
    :return:
    """
    # token = get_visitor_token()
    localReadConfig.set_headers("token_u", token)


# 从返回的嵌套的json中取出信息
def get_value_from_return_json(json, name1, name2):
    """
    get value by key
    :param json:
    :param name1:
    :param name2:
    :return:
    """
    info = json['info']
    group = info[name1]
    value = group[name2]
    return value


# 打印出URL和内容,执行完测试之后返回URL。
def show_return_msg(response):
    """
    show msg detail
    :param response:
    :return:
    """
    url = response.url
    msg = response.text
    print(u"\n请求地址：" + url)
    # 可以显示中文
    print(u"\n请求返回值：" + '\n' + json.dumps(json.loads(msg), ensure_ascii=False, sort_keys=True, indent=4))


# ****************************** read testCase excel ********************************

# 从表中取出所有的内容，除标题栏，放到列表里
def get_xls(xls_name, sheet_name):
    """
    get interface data from xls file
    :return:
    """
    cls = []
    # get xls file's path
    xlsPath = os.path.join(proDir, "testFile", 'case', xls_name)
    # open xls file
    file = open_workbook(xlsPath)
    # get sheet by name
    sheet = file.sheet_by_name(sheet_name)
    # get one sheet's rows
    nrows = sheet.nrows
    for i in range(nrows):
        if sheet.row_values(i)[0] != u'case_name':
            cls.append(sheet.row_values(i))
    return cls


# ****************************** read SQL xml ********************************
database = {}


# config DB 表示的是如果数据库存在，如何连接，执行什么操作，而此处是数据库的内容如何组成

# 从xml中取出数据，取出内容，表名和数据库名，构成一个数据库
def set_xml():
    # 如果定义的database = {}为空
    sql_path = os.path.join(proDir, "testFile", "SQL.xml")
    tree = ElementTree.parse(sql_path)
    for db in tree.findall("database"):
        db.findall("table")
        db_name = db.get("name")
        table = {}
        for tb in db.getchildren():
            table_name = tb.get("name")
            '''
            #定义sql为一个列表
            sql=[]
            key=[]
            value=[]
            for data in tb.getchildren():
                key.append(data.get("id"))
                value.append(data.text)
            for i ,j in zip(key,value):
                t = i + ":" + j
                sql.append(t)
          '''
            key = []
            value = []
            for data in tb.getchildren():
                key.append(data.get("id"))
                value.append(data.text)
            sql = dict(map(lambda x, y: [x, y], key, value))
            table[table_name] = sql
        database[db_name] = table
    # return database
    # print (sql_id［select_member］)


# 从组成的数据库中取出数据库名和表名，因为没有定义子啊类中，所以函数之前没有相互关系
def get_table_dict(database_name, table_name):
    # set_xml的作用就是向空的数据库字典里填东西
    set_xml()
    table_dict = database.get(database_name).get(table_name)
    return table_dict


# 从构造是数据库中取出sql语句
def get_sql(database_name, table_name, sql_id, param):
    table_dic = get_table_dict(database_name, table_name)
    sql = table_dic[sql_id]
    if "%s" in sql:
        sql = sql.replace("%s", param)
    return sql


# ****************************** read interfaceURL xml ********************************

# 从xml文件中取出url文字
def get_url_from_xml(name):
    """
    By name get url from interfaceURL.xml
    :param name: interface's url name
    :return: url
    """
    url_list = []
    url_path = os.path.join(proDir, 'testFile', 'interfaceURL.xml')
    tree = ElementTree.parse(url_path)
    for u in tree.findall('url'):
        url_name = u.get('name')
        if url_name == name:
            for c in u.getchildren():
                url_list.append(c.text)
    # print url_list
    url = '/' + '/'.join(url_list)
    # print url
    return url

def dependent_param(key,param):
        value= localReadConfig.get_param(param)
        par = {key:value}
        return par


"""
if __name__ == "__main__":
    print(get_xls("login"))
    set_visitor_token_to_config()  

"""


