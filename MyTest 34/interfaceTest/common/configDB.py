import pymysql
from interfaceTest import readConfig
from interfaceTest.common.Log import MyLog as Log

localReadConfig = readConfig.ReadConfig()


class MyDB:
    global config
    host = localReadConfig.get_db("host")
    user = localReadConfig.get_db("username")
    passwd = localReadConfig.get_db("password")
    port = localReadConfig.get_db("port")
    database = localReadConfig.get_db("database")
    config = {
        'host': str(host),
        'user': user,
        'passwd': passwd,
        'port': int(port),
        'db': database
    }

    def __init__(self):
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.db = None
        self.cursor = None

    def connectDB(self):
        """
        connect to database
        :return:
        """
        try:
            # connect to DB
            self.db = pymysql.connect(**config)
            # create cursor
            self.cursor = self.db.cursor()
            print("Connect DB successfully!")
        except ConnectionError as ex:
            self.logger.error(str(ex))

    def executeSQL(self, sql):
        """
        execute sql
        :param sql:
        :return:
        """
        self.connectDB()
        # executing sql
        self.cursor.execute(sql)
        # executing by committing to DB
        self.db.commit()
        return self.cursor

    def get_all(self, cursor):
        """
        get all result after execute sql
        :param cursor:
        :return:
        """
        value = cursor.fetchall()
        return value

    def get_one(self, cursor):
        """
        get one result after execute sql
        :param cursor:
        :return:
        """
        value = cursor.fetchone()
        return value

    def closeDB(self):
        """
        close database
        :return:
        """
        self.db.close()
        print("Database closed!")

if __name__=='__main__':
     MD=MyDB()
     MD.connectDB()
     sql1="select * from user.userinfo where username='jojo'"
     sql2 = "select * from sys.sys_config where value='OFF'"
     cursor=MD.executeSQL(sql2)
     result=MD.get_all(cursor)
     print(result)
     MD.closeDB()