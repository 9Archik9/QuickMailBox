import requests
import random
import string
import time
import os

API = "https://www.1secmail.com/api/v1/"  # сайт документации к используемой API: https://www.1secmail.com/api/#
domain_list = ["1secmail.com", "1secmail.org", "1secmail.net"]
domain = random.choice(domain_list)


def generate_username():  # функция генерация случайного email
    name = string.ascii_lowercase + string.digits  # используем для генерации рандомного имени словарь
    # из латинских букв нижнего регистра + цифры
    username = ''.join(random.choice(name) for _ in range(10))  # генерируем случайный username самого email на основе
    # созданного выше имени

    return username


def check_mail(mail=""):  # функция проверки на наличие писем в ящике
    req_link = f"{API}?action=getMessages&login={mail.split('@')[0]}&domain={mail.split('@')[1]}"
    # кастомными параметрами (mail.split) достаем username и domain из переданной(сгенерированной) почты
    r = requests.get(req_link).json()  # отправляем запрос по ссылке и забираем овтет в качестве json
    length = len(r)  # количество элементов в массиве с возвращенными json данными

    if length == 0:
        print("[INFO] Новых писем нет. Проверка происходит автоматически каждые 5 секунд")
    else:  # если lenght не равно 0, ожидается, что мы получили какоето сообщение или сообщения
        # данные приходят в виде списка со словарями с основными ключами:
        # [id, from, subject, date, attachments, body, textBody, htmlBody]

        id_list = []  # список с id приходящих писем. в дальнейшем нужен для извлечения сообщения конкретного письма

        for i in r:  # парсим ключи и значения пришедшего словаря
            for k, v in i.items():
                if k == "id":  # если есть ключ со значением id, забираем его значение и кладем в созданный список
                    id_list.append(v)

        print(f'[+] У вас {length} входящих сообщений! Почта обновляется автоматически каждые 5 секунд!')
        # какого значение lenght, такое и кол-во пришедших писем

        current_dir = os.getcwd()  # получаем текущую директорию. в дальнейшем там будет хранить сообщения
        final_dir = os.path.join(current_dir, 'all_mails')

        if not os.path.exists(final_dir):  # создаем текущую дирректорию, если она отсутсвтует
            os.makedirs(final_dir)

        for i in id_list:  # получение информации из писем. "i"  в данном случае id сообщения
            read_msg = f"{API}?action=readMessage&login={mail.split('@')[0]}&domain={mail.split('@')[1]}&id={i}"
            r = requests.get(read_msg).json()

            sender = r.get('from')
            subject = r.get('subject')
            date = r.get('date')
            content = r.get('textBody')
            # описанные выше строки забирают данные по ключам: отправителя, тему, дату отправки и текст сообщения

            mail_file_path = os.path.join(final_dir, f'{i}.txt')  # сохранение вышеописанной информации в файл
            # f'{i}.txt' используется для предотвращение перезаписи путем сохранения информации под id сообщения

            with open(mail_file_path, 'w') as file:  # запись данных в файл
                file.write(f'Sender: {sender}\nTo: {mail}\nSubject: {subject}\nDate: {date}\nContent: {content}')


def delete_mail(mail=""):  # функция удаления созданной почты. по умолчанию время жизни 1 час
    url = "https://www.1secmail.com/mailbox"

    data = {
        'action': 'deleteMailbox',
        'login': mail.split('@')[0],
        'domain': mail.split('@')[1]
    }  # payload с данными для удаления почты

    r = requests.post(url, data=data)
    print(f'[X] Почтовый адрес {mail} - удален!\n')  # информационный вывод


def main():
    try:
        username = generate_username()
        mail = f"{username}@{domain}"  # готовый случайный почтовый адрес из имени и домена
        print(f"[+] Ваш почтовый адрес: {mail}")

        mail_req = requests.get(f"{API}?login={mail.split('@')[0]}&domain={mail.split('@')[1]}")
        # отправка запроса к API и логин

        while True:
            check_mail(mail=mail)
            time.sleep(5)

    except KeyboardInterrupt:
        delete_mail(mail=mail)
        print("Программа прервана!")


if __name__ == '__main__':
    main()
