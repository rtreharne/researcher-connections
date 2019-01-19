from email import generator, charset
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from EMAIL_SETTINGS import *
import time



# Ensure 7-bit encoding (so that eml html is readable).
charset.add_charset('utf-8', charset.SHORTEST, charset.QP)

class Gen_Email():
    def __init__(self, email_to, email_from, a_data, p_data, dir=None, debug=True):#, email_to, email_from, subject=None, data):
        self.dirname = dir
        self.a_data = a_data
        self.p_data = p_data
        self.debug = debug
        self.email_to = email_to
        self.email_from = email_from
        self.msg = self.emailGen()
        self.saveToFile()

        if debug==False:
            print("Sending email ...")
            self.s = self.smtpLogin()
            self.s.send_message(self.msg)
            print("... Email sent")
            self.s.quit()

    def smtpLogin(self):
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # start TLS for security
        s.starttls()
        # Authentication
        s.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        return s

    def saveToFile(self):
        name = self.a_data["Your name"].split(" ")
        module = self.a_data["Module Code"].replace(" ", "").upper()[:8]
        ts = int(time.time())
        filename = ""
        for n in name:
            filename += n.capitalize()
            filename += "_"
        filename += str(module)
        filename += "_"
        filename += str(ts)
        with open('email/{0}/{1}.eml'.format(self.dirname, filename), 'w') as outfile:
            gen = generator.Generator(outfile)
            gen.flatten(self.msg)
            print('Saving "email/{0}/{1}.eml to file'.format(self.dirname, filename))

    def emailGen(self):
        msg = MIMEMultipart('html')
        msg['Subject'] = "PDRAs have expressed an interest in your Teaching Opportunity"
        msg['From'] = "R.Treharne@liverpool.ac.uk"
        msg['To'] = "R.Treharne@liverpool.ac.uk"

        html = """\
              <html>
                  <head></head>
                  <body>
                      <p>{2}: {3}</p>
                      <p>----------------------------------------------------------------------------------------</p>
                      <p>Dear {1},</p>
                      <p>Regarding your PDRA teacing opportunity:</p>
                      <p><b>{2}: {3}</b>
                      <p>The following researchers have expressed an interest in your opportunity.\
                      Please make contact with those that are best suited to your opporunity via email</p>
                      {0}
                  </body>
              </html>
              """.format(self.p_data.to_html(index=False, escape=False), self.a_data["Your name"].split(" ")[0].capitalize(), self.a_data["Module Code"].upper(), self.a_data["Module Title"].upper())

        part = MIMEText(html, 'html')

        msg.attach(part)

        return msg

