import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# TODO: cleanup, test, integrate, spam giveaways to domain emails,
# write template to read and open link and get referal points
'''
Firstly, you'll need to allow access for less secure apps 
in your Gmail settings. Go to your Google Account settings, 
then Security, and enable "Less secure app access."
'''

# Email content
sender_email = "your_email@gmail.com"
receiver_email = "recipient@example.com"
subject = "Subject of the email"
message_body = "This is the message body of the email."

# Gmail SMTP configuration
smtp_server = "smtp.gmail.com"
smtp_port = 587  # SSL: 465, TLS: 587
smtp_username = "your_email@gmail.com"
smtp_password = "your_password_here"

# Compose the email
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = subject
message.attach(MIMEText(message_body, 'plain'))

# Connect to Gmail's SMTP server
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.send_message(message)

print("Email sent successfully!")