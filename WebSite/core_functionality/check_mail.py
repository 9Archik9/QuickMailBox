import requests
import os

API = "https://www.1secmail.com/api/v1/"  # сайт документации к используемой API: https://www.1secmail.com/api/#


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