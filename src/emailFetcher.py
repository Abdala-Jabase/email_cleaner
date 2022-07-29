import imaplib                              
import email
from email.header import decode_header
from src.email import Email



class EmailFetcher:

    @staticmethod
    def fetchEmails(username: str, password: str) -> list:
        SMTP_SERVER = "imap-mail.outlook.com"

        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(username, password)
        mail.select('inbox')
        status, data = mail.search(None, 'ALL')
        mail_ids = []
        emails = []
        for block in data:
            mail_ids += block.split()

        for i in mail_ids:
            status, data = mail.fetch(i, '(RFC822)')

            for response_part in data:
                if isinstance(response_part, tuple):
                    message = email.message_from_bytes(response_part[1])

                    mail_from = message['from']
                    mail_subject = message['subject']

                    if message.is_multipart():
                        mail_content = ''
                        for part in message.get_payload():
                            if part.get_content_type() == 'text/plain':
                                mail_content += part.get_payload()
                    else:
                        mail_content = message.get_payload()
                    emails.append(Email(mail_from, mail_subject, mail_content))        
        mail.close()
        mail.logout()
        return emails
                    