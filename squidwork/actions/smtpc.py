import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from typing import Union, List
class SMTPController:
  PROVIDER = 'Gmail'

  def __init__(self) -> None:
    self.user_email = os.environ.get("USER_EMAIL")
    self.user_email_passwd = os.environ.get("USER_EMAIL_PASSWD")
    if self.user_email == None or self.user_email_passwd == None:
      raise Exception("Account credentials not defined in environment variables")
    self.server = smtplib.SMTP('smtp.gmail.com:587')
    self.server.ehlo(self.PROVIDER)
    self.server.starttls()
    self.server.login(self.user_email, self.user_email_passwd)

  def _send(self, to: str, subject: str, content: str):
    message = MIMEMultipart()
    message["From"] = self.user_email
    message["To"] = to
    message["Subject"] = subject
    messageText = MIMEText(content,'html')
    message.attach(messageText)
    fromaddr = self.user_email
    toaddrs  = to
    self.server.sendmail(fromaddr,toaddrs,message.as_string())
    return message.as_string()

  def __del__(self):
    self.server.quit()

  def send(self, to: Union[List, str], subject: str, content: str, n:int=1):
    ret = ""
    for _ in range(n):
      if isinstance(to, List):
        for _to in to:
          ret += self._send(_to, subject, content)
      else:
        ret = self._send(to, subject, content)
    return ret

if __name__ == "__main__":
  mailc = SMTPController()
  mailc.send(to=["squidwork@rodfer.online", "squidwork1@rodfer.online"], subject="Test", content="squidwork rules", n=1)
  del mailc
