# coding:utf-8
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
import threading
from interfaceTest import readConfig
from interfaceTest.common.Log import MyLog
import zipfile
import glob
# 配置邮件相关参数及发送方法

localReadConfig = readConfig.ReadConfig()


class Email:
    def __init__(self):
        global host, user, psw, port, sender, title
        #有几个变量以下其实并未用到
        host = localReadConfig.get_email("mail_host")
        user = localReadConfig.get_email("mail_user")
        psw = localReadConfig.get_email("mail_pass")
        port = localReadConfig.get_email("mail_port")
        sender = localReadConfig.get_email("sender")
        title = localReadConfig.get_email("subject")
        # content = localReadConfig.get_email("content")
        #receiver=localReadConfig.get_email("receiver")
        self.receivers = []

        #get receiver list
        value = localReadConfig.get_email("receiver")
        for n in str(value).split("/"):
            self.receivers.append(n)
        #print self.receivers

        # defined email subject
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.subject = u"接口测试报告" + " " + date

        self.log = MyLog().get_log()
        self.logger = self.log.get_logger()
        self.msg = MIMEMultipart('related')


    def config_header(self, receivers=None):
        """
        defined email header include subject, sender and receiver
        :return:
        """
        self.msg['subject'] = title
        self.msg['from'] = sender
        #添加多个接收人
        self.msg['to'] =",".join(self.receivers)
        print self.msg['to']

    def config_content(self):
        """
        write the content of email
        :return:
        """
        f = open(os.path.join(readConfig.proDir, 'testFile', 'emailStyle.txt'))
        content = f.read()
        f.close()
        content_plain = MIMEText(content, 'html', 'UTF-8')
        #上传文件
        self.msg.attach(content_plain)
        #上传图片
        self.config_image()

    def config_image(self):
        """
        config image that be used by content
        :return:
        """
        # defined image path
        image1_path = os.path.join(readConfig.proDir, 'testFile', 'img', '1.png')
        fp1 = open(image1_path, 'rb')
        msgImage1 = MIMEImage(fp1.read())
        # self.msg.attach(msgImage1)
        fp1.close()

        # defined image id
        msgImage1.add_header('Content-ID', '<image1>')
        self.msg.attach(msgImage1)

        image2_path = os.path.join(readConfig.proDir, 'testFile', 'img', 'logo.jpg')
        fp2 = open(image2_path, 'rb')
        msgImage2 = MIMEImage(fp2.read())
        # self.msg.attach(msgImage2)
        fp2.close()

        # defined image id
        msgImage2.add_header('Content-ID', '<image2>')
        self.msg.attach(msgImage2)

    def config_file(self):
        """
        config email file
        :return:
        """

        # if the file content is not null, then config the email file
        if self.check_file():

            reportpath = self.log.get_result_path()
            zippath = os.path.join(readConfig.proDir, "result", "test.zip")

            # zip file
            files = glob.glob(reportpath + '\*')
            f = zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED)
            for file in files:
                # 修改压缩文件的目录结构
                f.write(file, '/report/'+os.path.basename(file))
            f.close()

            reportfile = open(zippath, 'rb').read()
            filehtml = MIMEText(reportfile, 'base64', 'utf-8')
            filehtml['Content-Type'] = 'application/octet-stream'
            filehtml['Content-Disposition'] = 'attachment; filename="test.zip"'
            self.msg.attach(filehtml)

    def check_file(self):
        """
        check test report
        :return:
        """
        reportfile = self.log.get_report_path()
        if os.path.isfile(reportfile) and not os.stat( reportfile) == 0:
            return True
        else:
            return False

    def send_email(self):
       try:
          self.config_header()
          self.config_content()
          self.config_file()
          try:
                smtp = smtplib.SMTP()
                smtp.connect(host)
                smtp.login(sender,psw)
          except:
                smtp = smtplib.SMTP_SSL(host)
                smtp.login(sender, psw)
          smtp.sendmail(sender,self.receivers, self.msg.as_string())
          smtp.quit()
          #print "The test report has send to developer by email!"
          self.logger.info("The test report has send to developer by email.")
       except Exception as ex:
            self.logger.error(str(ex))





class MyEmail:
    email = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_email():

        if MyEmail.email is None:
            MyEmail.mutex.acquire()
            MyEmail.email = Email()
            MyEmail.mutex.release()
        return MyEmail.email


if __name__ == "__main__":
    #MyEmail.get_email()真正调用了Email()实例，email来接收，则emali是Email()的实例
    Email
