# coding:utf-8
import os
import codecs
import configparser

# 路径看做两部分，D:\zdh\接口\interfaceTest\interfaceTest\readConfig.py
# （文件夹路径D:\zdh\接口\interfaceTest\interfaceTest\ + （文件）readConfig.py   取0 就是文件夹路径
#在初始化函数中除去BOM,以避免配置文件打开后读取写入的编码问题，接下来就是读取各项配置。
#为什么要把路径写在开头，因为类中除了初始化函数，其他函数也用到了configPath变量。写在类前面，则类的所有函数都可以调用，
# 如果不这样写，也可以把这个变量configPath写在初始化函数中，但是用global声明一下。
proDir = os.path.split(os.path.realpath(__file__))[0]
#print proDir
configPath = os.path.join(proDir, "config.ini")
class ReadConfig:
    def __init__(self):
        fd = open(configPath)
        data = fd.read()
        #print data
        #  remove BOM
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(configPath, "w")
            file.write(data)
            file.close()
        fd.close()

        self.cf = configparser.ConfigParser()
        self.cf.read(configPath)

    def get_email(self, name):
        value = self.cf.get("EMAIL", name)
        return value

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_headers(self, name):
        value = self.cf.get("HEADERS", name)
        return value

    def set_headers(self, name, value):
        self.cf.set("HEADERS", name, value)
        with open(configPath, 'w+') as f:
            self.cf.write(f)

    def get_url(self, name):
        value = self.cf.get("URL", name)
        return value

    def get_db(self, name):
        value = self.cf.get("DATABASE", name)
        return value

    def get_param(self,name):
        value=self.cf.get("PARAM", name)
        return value

    def set_param(self, name,value):
        self.cf.set("PARAM", name, value)
        with open(configPath, 'w+') as f:
            self.cf.write(f)
"""
if __name__=="__main__":
  cf=ReadConfig()
  cf.set_headers("TOKEN_V", "123")
"""
