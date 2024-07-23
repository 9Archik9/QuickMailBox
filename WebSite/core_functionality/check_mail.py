import requests
import os
from main_page.models import UserEmail
from receive_message.models import EmailMessage, Attachment

API = "https://www.1secmail.com/api/v1/"


def fetch_messages(mail=""):
    req_link = f"{API}?action=getMessages&login={mail.split('@')[0]}&domain={mail.split('@')[1]}"
    response = requests.get(req_link).json()
    return response


def read_message(mail, message_id):
    read_msg = f"{API}?action=readMessage&login={mail.split('@')[0]}&domain={mail.split('@')[1]}&id={message_id}"
    response = requests.get(read_msg).json()
    return response


def check_mail(mail=""):
    messages = fetch_messages(mail)
    length = len(messages)

    if length == 0:
        print("[INFO] Новых писем нет. Проверка происходит автоматически каждые 5 секунд")
        return []

    print(f'[+] У вас {length} входящих сообщений! Почта обновляется автоматически каждые 5 секунд!')

    current_dir = os.getcwd()
    final_dir = os.path.join(current_dir, 'all_mails')

    if not os.path.exists(final_dir):
        os.makedirs(final_dir)

    email_messages = []
    for message in messages:
        message_id = message['id']
        email_data = read_message(mail, message_id)

        sender = email_data.get('from')
        subject = email_data.get('subject')
        date = email_data.get('date')
        content = email_data.get('textBody')
        html_body = email_data.get('htmlBody', '')

        # Проверяем, существует ли уже сообщение с таким api_id
        if not EmailMessage.objects.filter(api_id=message_id).exists():
            user_email = UserEmail.objects.get(email=mail)
            EmailMessage.objects.create(
                email=user_email,
                api_id=message_id,
                sender=sender,
                subject=subject,
                content=content,
                html_body=html_body
            )

        email_messages.append({
            'api_id': message_id,
            'sender': sender,
            'subject': subject,
            'date': date,
            'content': content
        })

        mail_file_path = os.path.join(final_dir, f'{message_id}.txt')
        with open(mail_file_path, 'w') as file:
            file.write(f'Sender: {sender}\nTo: {mail}\nSubject: {subject}\nDate: {date}\nContent: {content}')

    return email_messages

