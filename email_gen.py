from email import generator
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Gen_Email():
    def __init__(self, email_to, email_from, filename, a_data, p_data, debug=True):#, email_to, email_from, subject=None, data):
        self.filename = filename
        self.p_data = p_data
        self.debug = debug
        self.email_to = email_to
        self.email_from = email_from
        self.msg = self.emailGen()

        if self.debug == True:
            self.saveToFile()

    def saveToFile(self):
        with open('email/{0}.eml'.format(self.filename), 'w') as outfile:
            gen = generator.Generator(outfile)
            gen.flatten(self.msg)

    def emailGen(self):
        print('hello world')

        msg = MIMEMultipart('alternative')
        msg['Subject'] = ""
        msg['From'] = self.email_from
        msg['To'] = self.email_to

        html = """\
              <html>
                  <head></head>
                  <body>
                      {0}
                  </body>
              </html>
              """.format(self.p_data.to_html(index=False, escape=False))

        part = MIMEText(html, 'html')

        msg.attach(part)

        return msg

