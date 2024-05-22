import os

from django.db.models import Q
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView, CreateView
from openpyxl.workbook import Workbook

from main.forms import ApplicantShortForm
from main.models import Department, Applicant, Parent, School
from main.utils import parse_schools


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
        ws.append([obj.pk,
                   f'{obj.first_name} {obj.last_name} {obj.patronymic}',  # ФИО
                   f'{obj.gender}',  # Пол
                   f'{obj.applicant.number_of_5}',
                   f'{obj.applicant.number_of_4}',
                   f'{obj.applicant.number_of_3}',
                   f'{obj.document.SNILS}',
                   f'{obj.document.INN}',
                   f'{obj.applicant.average_score}',
                   f'{obj.applicant.original_or_copy}',
                   f'{obj.applicant.out_of_budget}',
                   f'{obj.applicant.documents_collected}',
                   f'{obj.applicant.received_receipt}',
                   f'{obj.school}',
                   f'{obj.graduation_date}',
                   f'{obj.document.FIS}',
                   f'{str(obj.id).zfill(5)}',
                   f'{obj.applicant.application_in_gov_services}',
                   f'',
                   f'',
                   f'{obj.applicant.application_status}',
                   f'{obj.applicant.internal_exam}',
                   f'{obj.birth_date}',
                   f'{obj.phone}',
                   f'{obj.parents.mother_full_name}',
                   f'{obj.parents.mother_phone}',
                   f'{obj.parents.father_full_name}',
                   f'{obj.parents.father_phone}',
                   f'{obj.document.passport_number}',
                   f'{obj.document.issued_by}',
                   f'{obj.document.issue_date}'
                   ])

    # Создаём HTTP-ответ для скачивания файла
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Applicants.xlsx'

    # Сохраняем файл Excel в HTTP-ответ
    wb.save(response)
    return response


def download_document(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filename = 'tipovaya-forma_soglasie.doc'
    # Define the full file path
    filepath = BASE_DIR + '\\static\\documents\\' + filename
    # Open the file for reading content
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = 'attachment; filename="your_file.doc"'
    # Return the response value
    return response


def update_schools(request):
    parse_schools()
    return redirect('home')


def autocomplete(request):
    if 'term' in request.GET:
        term_request = request.GET.get('term')

        qs = School.objects.filter(name__iregex=term_request)
        title = []
        for school in qs:
            title.append(school.name)
        return JsonResponse(title, safe=False)

    render(request, 'main/form.html')


def export_data(request):
    if request.method == 'GET':
        form = ApplicantShortForm()

        return render(request, 'admin/export_data.html')

    if request.method == 'POST':
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
            parents = Parent.objects.get(student_id=obj.pk)
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


def page_not_found(request):
    return HttpResponse("404 NOT FOUND")
