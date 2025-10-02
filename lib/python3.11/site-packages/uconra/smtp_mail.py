import dns.resolver


class SMTP_Mail():
    """ send email to clients
    Usage example:

    app_pw = 'iotf yndm yhkb qmnh'
    myMail = 'sender@gmail.com'
    mail_server = 'smtp.gmail.com:587'
    ehlo = 'Gmail'
    mess = 'What about this motchello'
    user = 'cody@gmail.com'

    sendmail = SMTP_Mail(appKey=app_pw, userMail=user, senderMail=myMail,smtpServer=mail_server,serverEhlo=ehlo,
                     message=mess,)

    sendmail.sendMail()

    """
    def __init__(self, appKey, userMail, senderMail, serverEhlo, smtpServer,
                 userName=None, subject=None, message=None):

        self.appKey = appKey
        self.userMail = userMail
        self.senderMail = senderMail
        self.serverEhlo = serverEhlo
        self.smtpServer = smtpServer
        self.userName = userName
        self.message = message
        self.subject = subject

    def sendMail(self,): # appKey=None, userMail=None, senderMail=None):
        """-----------  Split domain from user_email input  -------------"""
        self.domain = self.userMail.split('@')[1]

        """---------    Check the existence of DNS domain
            and catch  the error with try-except method -----------------. 
        """
        try:
            dns_address = dns.resolver.resolve(f'{self.domain}', 'A')
            for dns_a in dns_address:
                print('A record : ', dns_a.to_text())

                ###############################################################
                ### The following is a block for sending email with smtplib ###
                ###############################################################

                """------------     import smtplib modules    ------------"""

                import smtplib
                from email.mime.multipart import MIMEMultipart
                from email.mime.text import MIMEText

                message = MIMEMultipart()

                """ -------------   Send SMTP message to user_email input   ------------ """

                message['To'] = self.userMail
                message['From'] = self.senderMail
                message['Subject'] = self.subject

                title = '<b> CONFIRM OTP-CODE </b>'

                message_text = MIMEText(
                    f''' {self.message} ''', 'html'
                )
                message.attach(message_text)

                """ ----------- Sender infor email and app password ---------- """
                sender_email = self.senderMail
                app_password = self.appKey

                server = smtplib.SMTP(self.smtpServer)
                server.ehlo(self.serverEhlo)
                server.starttls()
                server.login(sender_email, app_password)

                fromaddr = self.senderMail
                toaddr = self.userMail
                server.sendmail(fromaddr, toaddr, message.as_string())
                server.quit()

                print( 'message successfully sent')

        except dns.exception.DNSException:
            print('Invalid email, message was unsuccessfully sent')

    def __str__(self,):
        f'{self.subject}, {self.userMail}, {self.senderMail}, {self.smtpServer}, {self.message} '



if __name__ == '__main__':
    SMTP_Mail()