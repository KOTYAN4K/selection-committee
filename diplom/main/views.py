import os

from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, CreateView
from openpyxl.workbook import Workbook

from diplom import settings
from main.forms import ApplicantShortForm
from main.models import Department, Applicant, Parent


# Create your views here.
class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        return context


class TestFormView(CreateView):
    template_name = 'main/form.html'
    form_class = ApplicantShortForm
    success_url = reverse_lazy('home')


# class ApplicantsView(ListView):
#     template_name = ''


def download_table(request):
    # Получите данные из базы данных
    queryset = Applicant.objects.all()

    # Создайте новый файл Excel
    wb = Workbook()
    ws = wb.active
    ws.title = 'Студенты'

    ws.append([
        '№ п/п',
        'ФИО',
        'пол',
        'Кол "5"',
        'Кол "4"',
        'Кол "3"',
        'Снилс',
        'инн',
        'средн балл',
        'оригинал/копия',
        'внебюджет',
        'Документы | забрали',
        'Получил ли расписку',
        'школа',
        'год окончания',
        'ФИС',
        'номер заявления',
        'Электронное заявление',
        'Дата ЭЗ',
        'Дата и время проведения испытания',
        'Статус',
        'Вступительный экзамен',
        'Дата рождения',
        'Личный телефон',
        'Мама',
        'Телефон мамы',
        'Папа',
        'Телефон папы',
        'номер паспорта',
        'Кем выдан',
        'Дата выдачи'
    ])

    # Добавьте данные из базы данных в файл Excel
    for obj in queryset:
        parents = Parent.objects.get(pk=obj.pk)
        ws.append([obj.pk,
                   f'{obj.first_name} {obj.last_name} {obj.patronymic}',  # ФИО
                   f'{obj.gender}',  # Пол
                   'Кол "5"',
                   'Кол "4"',
                   'Кол "3"',
                   'Снилс',
                   'инн',
                   'средн балл',
                   'оригинал/копия',
                   'внебюджет',
                   'Документы | забрали',
                   'Получил ли расписку',
                   f'{obj.school}',
                   f'{obj.graduation_date}',
                   'ФИС',
                   'номер заявления',
                   'Электронное заявление',
                   'Дата ЭЗ',
                   'Дата и время проведения испытания',
                   'Статус',
                   'Вступительный экзамен',
                   'Дата рождения',
                   'Личный телефон',
                   f'{parents.mother_full_name}',
                   f'{parents.mother_phone}',
                   f'{parents.father_full_name}',
                   f'{parents.father_phone}',
                   'номер паспорта',
                   'Кем выдан',
                   'Дата выдачи'
                   ])


    # Создаём HTTP-ответ для скачивания файла
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Applicants.xlsx'

    # Сохраняем файл Excel в HTTP-ответ
    wb.save(response)
    return response


def download_document(request):
    response = FileResponse('documents/tipovaya-forma_soglasie.doc')
    response['Content-Disposition'] = 'attachment; filename="filename.doc"'
    return response


def page_not_found(request):
    return HttpResponse("404 NOT FOUND")
