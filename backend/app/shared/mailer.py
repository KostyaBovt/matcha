from flask_mail import Mail
from flask_mail import Message
from flask import current_app

class Mailer(object):
  _mail = None;  

  def __init__(self):
    self._mail = Mail(current_app)

  def send_email(self, subject, sender, recipient, body):
      msg = Message(sender=sender,
                    recipients=[recipient],
                    subject=subject,
                    body=body
                    )
      self._mail.send(msg)

  def send_register_confirm(self, recipient_name, recipient_email, email_hash, confirm_hash):
      subject = 'Matcha - Confirm the Registration'
      sender = 'matcha.application.unit@gmail.com'
      confirm_link = "http://localhost:4200/confirm/{:s}/{:s}".format(email_hash, confirm_hash)
      body = """
        Hello, {:s}!
        You just registred on Matcha application!
        To finish registration, please follow this link:
        {:s}
        
        Your Matcha!
      """.format(recipient_name, confirm_link)
      self.send_email(subject, sender, recipient_email, body)
