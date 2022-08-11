import imaplib
import email
from email.header import decode_header
#testing my github
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
    global username, password, useSubject, useSender, senderKeywords, subjectKeywords, deleteOnlyUnseen
    unseenQBool = True
    while unseenQBool:
        senderQ = input('Would you like to delete from all emails or just unseen ones, reply "y" for only unseen and "n" for all.')
        if senderQ == 'y':
            unseenQBool = False
        elif senderQ == 'n':
            deleteOnlyUnseen = False
            unseenQBool = False
        else:
            print('Incorrect input, please try again...')
    sendQBool = True
    while sendQBool:
        senderQ = input('Would you like to use sender email to delete emails? Reply with y or n')
        if senderQ == 'y':
            sendQBool = False
        elif senderQ == 'n':
            useSender = False
            sendQBool = False
        else:
            print('Incorrect input, please try again...')
    if useSender:
        print('Please enter senders (names, emails, or companies), you would like to delete, when done enter "..." ')
        senderKeyword = ''
        while senderKeyword != '...':
            senderKeyword = input('Add: ')
            senderKeywords[senderKeyword] = 0
    subQBool = True
    while subQBool:
        subQ = input('Would you like to use keywords in subjects to delete emails? Reply with y or n')
        if subQ == 'y':
            subQBool = False
        elif subQ == 'n':
            useSubject = False
            subQBool = False
        else:
            print('Incorrect input, please try again...')
    if useSubject:
        print('Please enter keywords, that you would like emails whose subjects include to be deleted, when done enter "..." ')
        senderKeyword = ''
        while senderKeyword != '...':
            subjectKeyword = input('Add: ')
            subjectKeywords[subjectKeyword] = 0
    username = input('Please input your email address: ')
    password = input('Please input your password: ')

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
status, messages =  mail.search(None, '(UNSEEN)') if deleteOnlyUnseen else mail.search(None, 'ALL')

# convert messages to a list of email IDs
mail_ids = []

for block in messages:
    mail_ids += block.split()

for message in mail_ids:
    
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