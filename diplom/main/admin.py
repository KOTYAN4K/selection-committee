from django.contrib import admin
from .utils import create_account, send_invite_email, confirm_student, deny_student, warn_student
from .models import *


# Register your models here.
class DocumentInline(admin.StackedInline):  # или TabularInline, в зависимости от предпочтений дизайна
    model = Document
    can_delete = False  # если вы не хотите удалять документы из приемов
    verbose_name_plural = 'Документы'


class ParentsInline(admin.StackedInline):  # или TabularInline, в зависимости от предпочтений дизайна
    model = Parent
    can_delete = False  # если вы не хотите удалять документы из приемов
    verbose_name_plural = 'Абитуриенты'


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    order = 0
    inlines = [DocumentInline, ParentsInline]
    list_display = ('last_name',
                    'first_name',
                    'patronymic',
                    'gender',
                    'birth_date',
                    'email',
                    'school',
                    'get_graduation_date',
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

    @admin.action(description='Принять заявку на регистрацию')
    def confirm_applicant(self, request, queryset):
        count = 0
        for obj in queryset:
            response = create_account(obj)
            if response:
                count += 1

        self.message_user(request, f'Успешно приняты {count} пользователей')


@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    order = 1

    list_display = ('id',
                    'get_fio',
                    'get_departments',
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

    fields = (
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
              'application_in_gov_services',)
    ordering = ('-application_status', 'admission_date', '-updated_at', '-created_at', 'applicant',)
    list_editable = (
        'number_of_5',
        'number_of_4',
        'number_of_3',
        'internal_exam',
        'application_status',
        'original_or_copy',
        'out_of_budget',
        'received_receipt',
        'documents_collected',
        'application_in_gov_services',
        'internal_exam_conducted',)
    list_filter = ('department', 'application_status', 'created_at',
                   'updated_at', 'internal_exam_conducted', 'application_in_gov_services')
    list_display_links = ('get_fio',)
    search_fields = ('applicant__last_name', 'applicant__first_name', 'applicant__patronymic',)
    actions = ('confirm_applicant', 'deny_applicant', 'warn_applicant')

    @admin.action(description='Принять студента')
    def confirm_applicant(self, request, queryset):
        count = 0
        for obj in queryset:
            response = confirm_student(obj)

            if response:
                count += 1

        self.message_user(request, f'Успешно приняты {count} студенты')

    @admin.action(description='Отказать студенту')
    def deny_applicant(self, request, queryset):
        count = 0
        for obj in queryset:
            subject = "Ваша заявка отклонена."
            message = f"""Добрый день, вы не прошли на конкурс для вступления на бюджет ."""
            response = deny_student(obj)
            if response:
                count += 1
        self.message_user(request, f'Успешно отклонены {count} студенты')

    @admin.action(description='Отправить предупреждение о нехватке данных студента')
    def warn_applicant(self, request, queryset):
        count = 0
        for obj in queryset:
            subject = "Ваша заявка отклонена."
            message = f"""Добрый день, вы подали недостаточное количество документов. Пожалуйста зайдите в свой личный кабинет и укажите недостающие данные."""
            response = warn_student(obj)
            if response:
                count += 1
        self.message_user(request, f'Успешно предупреждены {count} студенты')


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    actions = ('send_invite_to_meet',)

    @admin.action(description='Отправить приглашение на собеседование выбранным студентам')
    def send_invite_to_meet(self, request, queryset):
        for interview in queryset:
            interview_date = interview.interview_date
            subject = "Приглашение на собеседование."
            message = f"""Добрый день, мы одобряем вашу заявку и приглашаем пройти собеседование.
Вам необходимо явиться {interview_date.day} {interview_date.month} в {interview_date.hour}:{str(interview_date.minute).zfill(2)} для прохождения экзамена. Явка обязательна."""

            for student in interview.students.all():
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
Вам необходимо явиться {exam_date.date()} в {exam_date.hour}:{exam_date.minute} для прохождения экзамена. Явка обязательна."""
            for student in internal_exam.students.all():
                send_invite_email(student.email, subject, message)
        self.message_user(request, f'Сообщения успешно отправлены.')


# admin.site.register(Document)
admin.site.register(Parent)

admin.site.sortable_by = 'order'

# admin.site.register(School)
# admin.site.register(Department)
