from django.contrib import admin
from django.core.mail import send_mail
from openpyxl import Workbook
from django.urls import path
from django.http import HttpResponse

from account.models import User
from diplom.settings import EMAIL_HOST_USER
from .models import *

# Register your models here.
admin.site.register(School)
admin.site.register(Department)
admin.site.register(Document)
admin.site.register(Parent)


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'patronymic', 'gender', 'birth_date', 'email',
                    'phone', 'address', 'parents', 'school', 'graduation_date', 'status', 'time_created')
    ordering = ('-time_created', 'last_name', 'first_name', 'patronymic')
    list_display_links = ('last_name', 'first_name', 'patronymic')
    actions = ('confirm_applicant',)

    @admin.action(description='Принять студента на регистрацию')
    def confirm_applicant(self, request, queryset):
        count = 0
        for obj in queryset:
            response = create_account(obj)
            if response:
                count += 1

        self.message_user(request, f'Успешно приняты {count} пользователей')


admin.site.register(InternalExam)
admin.site.register(Admission)


def create_account(applicant):
    if not User.objects.filter(email=applicant.email).exists():
        new_user = User()
        new_user.username = applicant.first_name + applicant.last_name + str(applicant.pk)
        new_user.set_password(applicant.patronymic)
        new_user.email = applicant.email
        new_user.student = applicant
        new_user.save()
        response = send_mail(
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
        applicant.status = 'answered'

        return True
    return False