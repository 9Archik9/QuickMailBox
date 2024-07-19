import requests


def delete_mail(mail=""):  # функция удаления созданной почты. по умолчанию время жизни 1  час
    url = "https://www.1secmail.com/mailbox"

    data = {
        'action': 'deleteMailbox',
        'login': mail.split('@')[0],
        'domain': mail.split('@')[1]
    }  # payload с данными для удаления почты

    r = requests.post(url, data=data)
    print(f'[X] Почтовый адрес {mail} - удален!\n')  # информационный вывод