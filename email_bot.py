import imaplib
import email
from email.header import decode_header

username = ''
password = ''

# These variables need to be set in the greeting Method
useSubject: bool = True
useSender: bool = True
deleteOnlyUnseen: bool = True
subjectKeywords = {}
senderKeywords = {}

# Greeting Method runs in the beginning of program to collect user info and decide whether to use from, subject or both, and stores keywords for from subject or both
def greeting() -> None:
    global username, password
    username = input('Username: ')
    password = input('Password: ')

# Decides whether to delete email based on subject and list of keywords collected
def decideSubject(subject: str) -> bool:
    global useSubject
    if useSubject:
        # implement checking the subject
        return True
    else:
        return False


# Decides whether to delete email based on sender and list of keywords collected
def decideFrom(sender: str) -> bool:
    global useSender
    if useSender:
        # implement checking the sender
        return True
    else:
        return False



# Uses decideFrom and decideSubject to decide whether a email should be deleted
def decideToRemove(sender: str, subject: str) -> bool:
    return decideFrom(sender) or decideSubject(subject)

greeting()
SMTP_SERVER = "imap-mail.outlook.com"
mail_from = ''
mail_subject = ''
mail = imaplib.IMAP4_SSL(SMTP_SERVER)

mail.login(username, password)
mail.select('inbox')
status, messages = mail.search(None, '(UNSEEN)') if deleteOnlyUnseen else mail.search(None, 'All')
# convert messages to a list of email IDs
messages = messages[0].split(b' ')
for message in messages:
    
    _, msg = mail.fetch(message, "(RFC822)")

    for response in msg:
        if isinstance(response, tuple):
            m = email.message_from_bytes(response[1])
            mail_from = m['from']
            mail_subject = m['subject']
            
    if decideToRemove(mail_from, mail_subject):
        mail.store(message, "+FLAGS", "\\Deleted")
        print("Deleting", mail_subject)

# from the selected mailbox (in this case, INBOX)
mail.expunge()
# close the mailbox
mail.close()
# logout from the account
mail.logout()
