from PIL import ImageGrab
import pytesseract
import clipboard
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
import time
from datetime import datetime

# 设置tesseract-ocr安装路径
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # 根据实际路径修改

# 提前构建好附件
message = MIMEMultipart()
filename = '【类别一户籍类】陆港一幼2024年秋季招生报名信息登记表.docx'
with open(filename, 'rb') as file:
    attachment = MIMEApplication(file.read(), Name=filename)
    attachment['Content-Disposition'] = f'attachment; filename={filename}'
    message.attach(attachment)
# 成功的邮件地址
success_mail_address = []
mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "1258454532@qq.com"  # 用户名
mail_pass = "gaaqvnchreptgeei"  # 口令
smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 25 为 SMTP 端口号
smtpObj.login(mail_user, mail_pass)




def send_mail(mail_address, message):
    # 第三方 SMTP 服务
    sender = '1258454532@qq.com'
    receiver = mail_address  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    text = ""
    message['From'] = Header(f"{sender}")
    message['To'] = Header(f"{receiver}")

    subject = '类别一+王书逸+610111202009281579+15091751738'
    message['Subject'] = Header(subject, 'utf-8')
    # 邮件正文
    message.attach(MIMEText(text, 'plain', 'utf-8'))

    try:
        smtpObj.sendmail(sender, receiver, message.as_string())
        print("邮件发送成功" + mail_address + "   " + datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        return True
    except Exception as e:
        print("Error: 无法发送邮件" + mail_address + "   " + datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        print(e)
        return False


def ocr_send_mail():
    print("程序开始运行" + datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    while True:
        # 捕获屏幕
        screenshot = ImageGrab.grab()
        # 从截图中提取文本
        text = pytesseract.image_to_string(screenshot)
        split = text.split("\n")
        for s in split:
            if ("163" in s and "@" in s and 'com' in s) or ("qq" in s and "@" in s and 'com' in s) or ("foxmail" in s and 'com' in s):
                mail_address = s.replace(' ', '').replace('|', '')
                if "\\" in mail_address:
                    continue
                else:
                    clipboard.copy(mail_address)
                    print("识别到邮箱地址：" + mail_address + "   " + datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
                    if mail_address in success_mail_address:
                        break
                    # if send_mail(mail_address, message):
                    #     success_mail_address.append(mail_address)
                    #     return True


if __name__ == '__main__':
    ocr_send_mail()
    # while True:
    #     print(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
