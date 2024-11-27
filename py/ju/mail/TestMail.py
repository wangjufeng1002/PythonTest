import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "1258454532@qq.com"  # 用户名
mail_pass = "gaaqvnchreptgeei"  # 口令

sender = '1258454532@qq.com'
receiver = '4757687511@qq.com'  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
text = '''
    田富洋：
      根据《中华人民共和国数据安全法》规定要求，从2021年9月1号起，当当开放平台的接口将个人敏感信息进行脱敏输出，未不影响您的正常使用及订单的正常履约，请及时完成接口的升级改造。
      涉及接口及入参和出参变更的详细信息，请见：https://open.dangdang.com/index.php?c=documentCenter&f=show&page_id=266
'''
message = MIMEText(text, 'plain', 'utf-8')
message['From'] = Header(f"{sender}")
message['To'] = Header(f"{receiver}")

subject = '当当开放平台数据加密接口升级提醒'
message['Subject'] = Header(subject, 'utf-8')

try:
    smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 25 为 SMTP 端口号
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receiver, message.as_string())
    print( "邮件发送成功")
except smtplib.SMTPException as e:
    print("Error: 无法发送邮件")
    print(e)