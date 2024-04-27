# from bs4 import BeautifulSoup
# import requests
from django.core.mail import send_mail

from account.models import User
from diplom.settings import EMAIL_HOST_USER
from main.models import School, Parent, Document


# def parse_schools():
#     # Очистите существующие данные
#     School.objects.all().delete()
#
#     url = 'https://edu.tatar.ru/n_chelny/type/1'
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#
#     for schools in soup.find_all('ul', class_='your-class'):
#         for school in schools.find_all('li'):
#             name = school.school.get_text().strip()
#             School.objects.create(name).save()


def create_account(applicant):
    if not User.objects.filter(email=applicant.email).exists():
        new_user = User()
        new_user.username = applicant.first_name + applicant.last_name + str(applicant.pk)
        new_user.set_password(applicant.patronymic)
        new_user.email = applicant.email
        new_user.student = applicant
        new_user.save()

        send_mail(
            "Ваша заявка принята.",
            f"""Ваша заявка принята, приступайте к заполнению вашей личной страницы с документами.
Вот ваши данные для авторизации на сайте:
Логин:{new_user.username}
Пароль:{applicant.patronymic}

Можно также использовать почту для авторизации.""",
            EMAIL_HOST_USER,
            [new_user.email],
            fail_silently=False,
        )
        parents = Parent.objects.create(student=applicant)
        documents = Document.objects.create(student=applicant)
        parents.save()
        documents.save()
        return True
    return False