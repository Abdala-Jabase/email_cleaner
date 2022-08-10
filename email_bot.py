import imaplib
import email
from email.header import decode_header

username = ''
password = ''

# Greeting Method runs in the beginning of program to collect user info and decide whether to use from, subject or both, and stores keywords for from subject or both
def greeting() -> None:
    global username, password
    username = input('Username: ')
    password = input('Password: ')

# Decides whether to delete email based on subject and list of keywords collected
def decideSubject(subject: str) -> bool:
    return True

# Decides whether to delete email based on sender and list of keywords collected
def decideFrom(sender: str) -> bool:
    return True

# Uses decideFrom and decideSubject to decide whether a email should be deleted
def decideToRemove(sender: str, subject: str) -> bool:
    return True

SMTP_SERVER = "imap-mail.outlook.com"
mail_from = ''
mail_subject = ''
mail_content = ''
mail = imaplib.IMAP4_SSL(SMTP_SERVER)

mail.login(username, password)
mail.select('inbox')
status, messages = mail.search(None, '(UNSEEN)')
# convert messages to a list of email IDs
messages = messages[0].split(b' ')
for message in messages:
    _, msg = mail.fetch(message, "(RFC822)")
    # you can delete the for loop for performance if you have a long list of emails
    # because it is only for printing the SUBJECT of target email to delete
    for response in msg:
        if isinstance(response, tuple):
            m = email.message_from_bytes(response[1])
            mail_from = m['from']
            mail_subject = m['subject']
            if m.is_multipart():
                for part in m.get_payload():
                    if part.get_content_type() == 'text/plain':
                        mail_content += part.get_payload()
            else:
                mail_content = message.get_payload()
            
    if decideToRemove(mail_content):
        mail.store(message, "+FLAGS", "\\Deleted")
        print("Deleting", mail_subject)
# from the selected mailbox (in this case, INBOX)
mail.expunge()
# close the mailbox
mail.close()
# logout from the account
mail.logout()



    # mark the mail as deleted
    
# status, data = mail.search(None, '(UNSEEN)')
# mail_ids = []
# emails = []

# for block in data:
#     mail_ids += block.split()

# for i in mail_ids:
#     status, data = mail.fetch(i, '(RFC822)')

#     for response_part in data:
#         if isinstance(response_part, tuple):
#             message = email.message_from_bytes(response_part[1])

#             mail_from = message['from']
#             mail_subject = message['subject']

#             if message.is_multipart():
#                 mail_content = ''
#                 for part in message.get_payload():
#                     if part.get_content_type() == 'text/plain':
#                         mail_content += part.get_payload()
#             else:
#                 mail_content = message.get_payload()
#             emails.append(Email(mail_from, mail_subject, mail_content))       
# 
#  
# permanently remove mails that are marked as deleted

