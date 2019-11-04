import smtplib
from email.mime.text import MIMEText

content = """
    程序员，1024，你准备这么过，过的咋样？
"""

sender = "1508204276@qq.com"
recver = """3115688577@qq.com,"""
# 2816474335@qq.com,
# 1320629993@qq.com,
# 1015174363@qq.com,
# 1693580010@qq.com,
# 15733129082@163.com,
# 1339566602@qq.com,
# 1502377018@qq.com,
# 1985054961@qq.com,
# 329844268@qq.com,
# 876911388@qq.com,
# 794067332@qq.com"""
password = "solblwosressjjjg"

#构建邮件格式
message = MIMEText(content,"plain","utf-8")
message["To"] = recver
message["From"] = sender
message["Subject"] = "老边的问候"

#发送邮件
smtp = smtplib.SMTP_SSL("smtp.qq.com",465)
smtp.login(sender,password)
smtp.sendmail(sender,recver.split(",\n"),message.as_string())
smtp.close()
