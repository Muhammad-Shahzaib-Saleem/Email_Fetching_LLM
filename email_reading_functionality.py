import imaplib
import email
from bs4 import BeautifulSoup





def fetching_email(user_email,app_password,from_email,mail_box):

    user_name = user_email
    app_password = app_password
    FROM = from_email

    select_mail_box = {
        "inbox": "inbox",
        "sent": None,
        "drafts": None,
        "trash":None

    }
    # sent = "sent.txt"

    if mail_box == "sent":
        select_mail_box[mail_box] = '"[Gmail]/Sent Mail"'
    elif mail_box == "drafts":
        select_mail_box[mail_box] = '"[Gmail]/Drafts"'
    elif mail_box == "trash":
        select_mail_box[mail_box] = '"[Gmail]/Trash"'
    elif mail_box == "starred":
        select_mail_box[mail_box] = '"[Gmail]/Starred"'






    gmail_host = "imap.gmail.com"

    mail = imaplib.IMAP4_SSL(gmail_host)

    mail.login(user_name, app_password)


    mail.select(select_mail_box[mail_box])

    status, mailboxes = mail.list()
    if status == 'OK':
        print("Available mailboxes:")
        for mailbox in mailboxes:
            print(mailbox)

    _, selected_mails = mail.search(None, f'(FROM {FROM})')

    print("selected mails", selected_mails)
    print(f"Total number of messages from  ", len(selected_mails[0].split()))

    with open(f'/Users/dotenterprises/Desktop/AI-IT Oasis/Read_Email/emails.txt', 'w', encoding='utf-8') as file:

        file.write(f"Total Number of Email from {FROM.split('@')[0]}: {len(selected_mails[0].split())}\n")
        file.write("--------------------------------\n")

        for num in selected_mails[0].split():
            _, data = mail.fetch(num, '(RFC822)')
            _, bytes_data = data[0]
            email_message = email.message_from_bytes(bytes_data)

            print("\n===========================================")

            # access data
            print("Subject: ", email_message["subject"])
            print("To:", email_message["to"])
            print("From: ", email_message["from"])
            print("Date: ", email_message["date"])



            file.write(f"Subject: , {email_message['subject']}\n")
            file.write(f"To:,{email_message['to']}\n")
            file.write(f"From:,{email_message['from']}\n")
            file.write(f"Date: {email_message['date']}\n")

            for part in email_message.walk():
                if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
                    message = part.get_payload(decode=True)
                    soup = BeautifulSoup(message, "html.parser")
                    plain_message = soup.getText()

                    # print("Message: \n", plain_message)
                    file.write(f"body: {plain_message}\n")
                    file.write("=========================\n")
                    print("==========================================\n")
                    break