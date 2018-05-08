# coding:utf-8
import os
#用到了 readConfig的proDir变量
from interfaceTest import readConfig as readConfig
#用到了时间函数
from datetime import datetime
#下面用到了线程锁
import threading
import logging

#这句话在以下函数中没有用到
localReadConfig = readConfig.ReadConfig()


class Log:
    def __init__(self):
        #日志路径  结果路径    工程路径
        #总的意思就是拼接定义了2个路径，结果路径，日志路径，然后创建日志记录器，加入日志管理程序
        global logPath, resultPath, proDir,result_date
        #不再具体指定 proDir 路径是什么了，直接引用readConfig文件，readConfig类中的proDir
        proDir = readConfig.proDir
        resultPath = os.path.join(proDir, "result")
        if not os.path.exists(resultPath):
            os.mkdir(resultPath)
        result_date = os.path.join(resultPath, str(datetime.now().strftime('%Y%m%d%H%M%S')))
        #print result_date
        if not os.path.exists(result_date):
            os.mkdir(result_date)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        # defined handler
        handler = logging.FileHandler(os.path.join(result_date,"output.log"))
        # defined formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def get_logger(self):
        """
        get logger
        :return:
        """
        return self.logger

    def build_start_line(self, case_no):
        """
        write start line
        :return:
        """
        self.logger.info("--------" + case_no + " START--------")

    def build_end_line(self, case_no):
        """
        write end line
        :return:
        """
        self.logger.info("--------" + case_no + " END--------")

    def build_case_line(self, case_name, code, msg):
        """
        write test case line
        :param case_name:
        :param code:
        :param msg:
        :return:
        """
        self.logger.info(case_name+" - Code:"+str(code)+" - msg:"+msg)

    def get_report_path(self):
        """
        get report file path
        :return:
        """
        report_path = os.path.join(result_date,"report.html")
        return report_path

    def get_result_path(self):
        """
        get test result path
        :return:
        """
        return result_date

    def write_result(self, result):
        """
        :param result:
        :return:
        """
        #区分 resultPath是结果文件夹的路径，result_path是测试报告的路径
        result_path = os.path.join(resultPath, "report.txt")
        fb = open(result_path, "wb")
        try:
            fb.write(result)
        except BaseException as e:
            self.logger.error(str(e))




class MyLog:
    log = None
    mutex = threading.Lock()

    def __init__(self):
        print
        pass
   #或得线程锁

    @staticmethod
    def get_log():
        if MyLog.log is None:
            MyLog.mutex.acquire()
            MyLog.log = Log()
            MyLog.mutex.release()
        return MyLog.log

if __name__=="__main__":
    log=MyLog.get_log()
    logger=log.get_logger()
    logger.info("test")
