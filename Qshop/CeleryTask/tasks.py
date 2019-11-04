from  __future__ import absolute_import
import smtplib
from email.mime.text import MIMEText
from Shop.celery import app
@app.task
def add():
    x=1
    y=1
    return x+y
def sendMial(content,email):
    from Qshop.settings import MAIL_SENDER,MAIL_PASSWORD,MAIL_SERVER,MAIL_PORT
    content = """
        如果确认是本人修改密码，请点击下放链接进行密码修改
        <a href="%s">点击链接确认</a>
    """%content
    print(content)
    # 构建邮件格式
    message = MIMEText(content, "html", "utf-8")
    message["To"] = email
    message["From"] = MAIL_SENDER
    message["Subject"] = "密码修改"

    # 发送邮件
    smtp = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT)
    smtp.login(MAIL_SENDER, MAIL_PASSWORD)
    smtp.sendmail(MAIL_SENDER, [email], message.as_string())
    smtp.close()
    return "发送成功"
