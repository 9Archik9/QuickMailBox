import random
import string


def generate_mail():  # функция генерация случайного email
    name = string.ascii_lowercase + string.digits  # используем для генерации рандомного имени словарь
    # из латинских букв нижнего регистра + цифры
    username = ''.join(random.choice(name) for _ in range(10))  # генерируем случайный username самого email на основе
    # созданного выше имени
    return username
