import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mail:

    def __init__(self, sender, password):
        self.sender = sender
        self.password = password

    def send(self, recipient, subject, text, smtp_host='smtp.gmail.com'):
        message = MIMEMultipart()
        message['From'] = self.sender
        message['To'] = ', '.join(recipient)
        message['Subject'] = subject
        message.attach(MIMEText(text))

        smtp_server = smtplib.SMTP(smtp_host, 587)
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.ehlo()
        smtp_server.login(self.sender, self.password)
        smtp_server.sendmail(self.sender,
                             recipient,
                             message.as_string()
                             )
        smtp_server.quit()

    def retrieve(self, header=None, imap_host='imap.gmail.com'):
        imap_server = imaplib.IMAP4_SSL(imap_host)
        imap_server.login(self.sender, self.password)
        imap_server.list()
        imap_server.select('INBOX')

        search_criteria = '(HEADER Subject "%s")' % header if header else 'ALL'
        search_result, search_data = imap_server.uid('search', None, search_criteria)
        assert search_data[0], 'There are no letters with current header'
        last_email_uid = search_data[0].split()[-1]
        fetch_result, fetch_data = imap_server.uid('fetch', last_email_uid, '(RFC822)')
        raw_email = fetch_data[0][1]
        email_message = email.message_from_string(str(raw_email))
        imap_server.logout()


if __name__ == '__main__':
    mail = Mail('sender@gmail.com', 'password')
    mail.send(['recipient@gmail.com'], 'subject', 'text')
    mail.retrieve()
