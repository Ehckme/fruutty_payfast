from .register import Register
from .smtp_mail import SMTP_Mail

mail = Register()

email = mail.userEmail('cody@gmail.com')

app_pw = 'iotf yndm yhkb qmnh'
myMail = 'sender@gmail.com'
mail_server = 'smtp.gmail.com:587'
ehlo = 'Gmail'
mess = 'What about this motchello'
user = 'cody@gmail.com'

sendmail = SMTP_Mail(appKey=app_pw, userMail=user, senderMail=myMail, smtpServer=mail_server, serverEhlo=ehlo,
                     message=mess, )

print(str(sendmail.userMail))
password = Register()

print(password.userPassword('cody'))
