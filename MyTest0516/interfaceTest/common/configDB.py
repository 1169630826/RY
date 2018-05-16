# coding:utf-8
import MySQLdb
from interfaceTest import readConfig
from interfaceTest.common.Log import MyLog

localReadConfig = readConfig.ReadConfig()
# 配置数据库的连接与操作
class MyDB:

    def __init__(self):
       global host, user, passwd, port, database, config
       host = localReadConfig.get_db("host")
       user = localReadConfig.get_db("username")
       passwd = localReadConfig.get_db("password")
       port = localReadConfig.get_db("port")
       database = localReadConfig.get_db("database")
       self.log = MyLog().get_log()
       self.logger = self.log.get_logger()

       self.db = None
       self.cursor=None

    #连接数据库,把连接后数据数据库的游标赋值给初始化定义的游标，以便后面操作的使用。不要使用return 游标。
    #因为return  的函数不更改原值，而赋值则是将None改为实际的游标。
    def connectDB(self):

        """
        connect to database
        :return:
        """
        try:
            # connect to DB
            self.db = MySQLdb.connect(host,user,passwd,database,use_unicode=True, charset="utf8")
            print "self.db is",self.db
            self.cursor=self.db.cursor()
            print("Connect DB successfully!")
        except MySQLdb.Error as ex:
            self.logger.error(str(ex))
            print "Connect DB faild"

    #通过初始化函数中的self.cursor = self.db.cursor()获得游标，执行sql语句。
    def executeSQL(self, sql):
        """
        execute sql
        :param sql:
        :return:
        """
        self.connectDB()
        # executing sql，游标执行之前一定要保证是连接了数据库
        self.cursor.execute(sql)
        # executing by committing to DB
        self.db.commit()
        return self.cursor
    #不用self.cursor原因是任何数据库操作的执行都需要先链接，获取curse。gett all是在执行数据库操作之后获取数据，所以是在
    # executeSQL执行之后执行的函数，因此可以将 executeSQL执行后返回的curse传入get_allh函数获取数据。因此此处定义了一个变量。
    #而使用全局的sel.curser是不需要定义变量的
    def get_all(self,cursor):
        """
        get all result after execute sql
        :param cursor:
        :return:
        """
        value = cursor.fetchall()
        return value

    def get_one(self,cursor):
        """
        get one result after execute sql
        :param cursor:
        :return:
        """
        value =cursor.fetchone()
        return value

    def closeDB(self):
        """
        close database
        :return:
        """
        self.db.close()
        print("Database closed!")


#本机的连接名为空，密码为空
if __name__ == '__main__':

    MD= MyDB()
    MD.connectDB()

    sql =""
    cur2= MD.executeSQL(sql)
    x =MD.get_one(cur2)
    print(x)
    MD.closeDB()
