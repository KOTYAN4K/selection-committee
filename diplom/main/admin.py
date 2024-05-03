from django.contrib import admin
from .utils import create_account, send_invite_email
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
    ordering = ('-status', '-created_at', '-updated_at', 'last_name', 'first_name', 'patronymic')
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
                count += 1

        self.message_user(request, f'Успешно приняты {count} пользователей')


@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'applicant',
                    'admission_date',
                    'number_of_5',
                    'number_of_4',
                    'number_of_3',
                    'average_score',
                    'internal_exam',
                    'original_or_copy',
                    'application_status',
                    'internal_exam_conducted',
                    'received_receipt',
                    'out_of_budget',
                    'documents_collected',
                    'application_in_gov_services',
                    )
    ordering = ('application_status', '-updated_at', 'applicant',)
    list_editable = (
        'number_of_5',
        'number_of_4',
        'number_of_3',
        'application_status',
        'out_of_budget',
        'received_receipt',
        'documents_collected',
        'application_in_gov_services',
        'internal_exam_conducted',)
    list_filter = ('department', 'application_status', 'created_at',
                   'updated_at', 'internal_exam_conducted', 'application_in_gov_services')
    list_display_links = ('applicant',)
    search_fields = ('applicant',)


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    actions = ('send_invite_to_meet',)

    @admin.action(description='Отправить приглашение на собеседование выбранным студентам')
    def send_invite_to_meet(self, request, queryset):
        for interview in queryset:
            interview_date = interview.interview_date
            subject = "Приглашение на собеседование."
            message = f"""Добрый день, мы одобряем вашу заявку и приглашаем пройти собеседование.
Вам необходимо явиться {interview_date.date()} в {interview_date.time()} для прохождения экзамена. Явка обязательна."""

            for student in interview.student.all():
                send_invite_email(student.email, subject, message)
        self.message_user(request, f'Сообщения успешно отправлены.')


@admin.register(InternalExam)
class InternalExamAdmin(admin.ModelAdmin):
    actions = ('send_invite_to_exam',)

    @admin.action(description='Отправить приглашение на вступительный экзамен выбранным студентам')
    def send_invite_to_exam(self, request, queryset):
        for internal_exam in queryset:
            exam_date = internal_exam.exam_date
            subject = "Приглашение на собеседование."
            message = f"""Добрый день, мы одобряем вашу заявку и приглашаем пройти вступительный экзамен.
Вам необходимо явиться {exam_date.date()} в {exam_date.time()} для прохождения экзамена. Явка обязательна."""
            for student in internal_exam.student.all():
                send_invite_email(student.email, subject, message)
        self.message_user(request, f'Сообщения успешно отправлены.')


admin.site.register(Document)
admin.site.register(Parent)
# admin.site.register(School)
# admin.site.register(Department)
