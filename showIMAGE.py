import pytesseract
from PIL import Image
IMG_PATH = 'E:\Sublime\demo.png'
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

# # 实现图片识别
# def getPicContent():
#     img = Image.open(IMG_PATH)
#     img.load()
#     data = pytesseract.image_to_string(img, lang="chi_sim")
#     print(data)

my_sender = '1806060082@qq.com'  # 发件人邮箱账号
my_password = 'ksecsojhahkbegci'  # 发件人邮箱密码(当时申请smtp给的口令)
my_user = '1806060082@qq.com'  # 收件人邮箱账号，我这边发送给自己


def senmail(keyword,userlist,item):
    try:
        message = MIMEText(item['title']+item['url'], 'plain', 'utf-8')
        for user in userlist:

            message['From'] = formataddr(["发件人", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            message['To'] = formataddr(["收件人", user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            message['Subject'] = "您有新的新招标信息到达，请及时查看"  # 邮件的主题，也可以说是标题
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
            server.login(my_sender, my_password)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender, [user, ], message.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的
        pass




def mail():
    ret = True
    try:
        msg = MIMEText('填写邮件内容', 'plain', 'utf-8')
        msg['From'] = formataddr(["发件人昵称", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["收件人昵称", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "邮件主题-测试"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret


ret = mail()
if ret:
    print("邮件发送成功")
else:
    print("邮件发送失败")

    try:
        message = MIMEText(item['title'] + item['url'], 'plain', 'utf-8')
        for user in userlist:
            message['From'] = formataddr(["招标信息网", my_sender])
            message['To'] = formataddr([user['name'], user['mail']])
            message['Subject'] = "您有新的新招标信息到达，请及时查看"
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)
            server.login(my_sender, my_password)
            server.sendmail(my_sender, [user.mail, ], message.as_string())
            server.quit()
    except Exception:
        pass
