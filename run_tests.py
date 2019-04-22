import time, sys
sys.path.append('./interface')
sys.path.append('./db_fixture')
from HTMLTestRunner import HTMLTestRunner
from unittest import defaultTestLoader
from db_fixture import test_data
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import smtplib
import unittest
import time
import os

# ============定义发送邮件===============

def send_mail(file_new):
	f = open(file_new,'rb')
	mail_body = f.read()
	f.close()

	# msg = MIMEText(mail_body,'html','utf-8')
	msg = MIMEMultipart()
	msg['Subject'] = Header("自动化测试报告",'utf-8')
	msgtext = MIMEText("<font color=red>&nbsp;&nbsp;&nbsp;各位领导:<br>这是XXX接口自动化测试报告<br>详细测试情况，请下载附件进行查看！</font>" , "html", "utf-8")
	msg.attach(msgtext)
	body = MIMEText(mail_body, "html", "utf-8")
	msg.attach(body)
    #添加附件
	att = MIMEText(mail_body, "html", "utf-8")
	att["Content-Type"] = "application/octet-stream"
	att["Content-Disposition"] = 'attachment; filename="APItest-report.html"'  #定义附件名称
	msg.attach(att)

	msg['from'] = 'Jerry_347862945@126.com'
	msg['to'] = 'jiale.sheng@zhiyoubao.com'

	smtp = smtplib.SMTP()
	smtp.connect('smtp.126.com')
	smtp.login('Jerry_347862945@126.com','shengjiale123456')
	smtp.sendmail('Jerry_347862945@126.com','jiale.sheng@zhiyoubao.com',msg.as_string())
	smtp.quit()

	# =================查找测试报告目录，找到最新生成的测试报告文件===================
	
def new_report(report):
	lists = os.listdir(report)	# 获取目录下的所有文件和文件夹保存到lists
	lists.sort(key=lambda fn: os.path.getmtime(report + "\\"+ fn))	#对目录下的文件按照时间排序
	file_new = os.path.join(report,lists[-1])	#获取最新的文件保存到file_new
	# print(file_new)
	return file_new


if __name__ == "__main__":
    test_data.init_data() # 初始化接口测试数据
    # 指定测试用例为当前文件夹下的 interface 目录
    test_dir = './interface'
    testsuit = defaultTestLoader.discover(test_dir, pattern='*_test.py')

    now = time.strftime("%Y-%m-%d %H_%M_%S")
    test_report = './report/'
    filename = './report/' + now + '_result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp,
                            title='发布会签到系统接口自动化测试',
                            description='运行环境：MySQL(PyMySQL), Requests, unittest')
    runner.run(testsuit)
    fp.close()
    new_report = new_report(test_report)
    send_mail(new_report)	#发送测试报告
'''
pymysql 驱动 --> MySQL
requests 库(HTTP/HTT、S)
unittest单元测试
HTMLTestRunner 生成测试报告
'''