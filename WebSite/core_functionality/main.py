import time
import requests
import random
from core_functionality.generate_mail import generate_mail
from core_functionality.check_mail import check_mail
from core_functionality.delete_mail import delete_mail

API = "https://www.1secmail.com/api/v1/"  # сайт документации к используемой API: https://www.1secmail.com/api/#
domain_list = ["1secmail.com", "1secmail.org", "1secmail.net"]
domain = random.choice(domain_list)


def setup():
    username = generate_mail()
    mail = f"{username}@{domain}"  # готовый случайный почтовый адрес из имени и домена
    return mail
