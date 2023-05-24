import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def mail(receiver_address, subject, mail_content):
    # # For Sender in GSuite 
    
    # # The mail addresses and password
    sender_address = 'no-reply@albanero.io'
    # # App Password

    # sender_pass = 'xxxxxxxx'

    # #Setup the MIME
    # message = MIMEMultipart()
    # message['From'] = sender_address
    # message['To'] = receiver_address
    # message['Subject'] = subject
    
    # # The body and the attachments for the mail
    # message.attach(MIMEText(mail_content, 'plain'))
    
    # # Create SMTP session for sending the mail
    # # use gmail with port
    # session = smtplib.SMTP('smtp.gmail.com', 587)

    # # enable TLS
    # session.starttls()

    # # login with mail_id and password
    # session.login(sender_address, sender_pass)
    # text = message.as_string()
    # session.sendmail(sender_address, receiver_address, text)
    # session.quit()
    # print('Mail Sent')

    print("----------------------------------------")
    print()

    print(f"Sending mail to {receiver_address} from {sender_address}")
    print(f"Subject: {subject}")
    print(f"Body: {mail_content}")

    print()
    print("----------------------------------------")
