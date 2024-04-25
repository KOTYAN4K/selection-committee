from django.contrib import admin
from django.core.mail import send_mail
from openpyxl import Workbook
from django.urls import path
from django.http import HttpResponse

from account.models import User
from diplom.settings import EMAIL_HOST_USER
from .models import *


# Register your models here.
@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('last_name',
                    'first_name',
                    'patronymic',
                    'gender',
                    'birth_date',
                    'email',
                    'school',
                    'graduation_date',
                    'address',
                    'status',
                    'updated_at',
                    'created_at')
    ordering = ('-created_at', '-updated_at', '-status', 'last_name', 'first_name', 'patronymic')
    list_editable = ('status',)
    list_filter = ('gender', 'status', 'school', 'created_at', 'updated_at')
    list_display_links = ('last_name', 'first_name', 'patronymic')
    actions = ('confirm_applicant',)
    search_fields = ('last_name',
                     'first_name',
                     'patronymic',)

    @admin.action(description='Принять студента на регистрацию')
    def confirm_applicant(self, request, queryset):
        count = 0
        for obj in queryset:
            response = create_account(obj)
            if response:
                obj.status = 'answered'
                count += 1

        self.message_user(request, f'Успешно приняты {count} пользователей')


@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ('applicant',
                    'department',
                    'admission_date',
                    'out_of_budget',
                    'number_of_5',
                    'number_of_4',
                    'number_of_3',
                    'average_score',
                    'received_receipt',
                    'application_status',
                    'internal_exam_conducted',
                    'application_number',
                    'documents_collected',
                    'application_in_gov_services',
                    'internal_exam'
                    )
    ordering = ('application_status', '-updated_at', 'applicant', )
    list_editable = ('application_status',)
    list_filter = ('department', 'application_status', 'number_of_5', 'number_of_4', 'number_of_3', 'created_at',
                   'updated_at', 'internal_exam_conducted', 'application_in_gov_services')
    list_display_links = ('applicant',)
    search_fields = ('applicant', )


admin.site.register(InternalExam)
admin.site.register(Document)
admin.site.register(Parent)


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

        return True
    return False
