from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth import get_user_model

from diplom import settings
from main.models import Applicant, School


class ApplicantShortForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Applicant
        fields = ('last_name',
                  'first_name',
                  'patronymic',
                  'gender',
                  'birth_date',
                  'school',
                  'graduation_date',
                  'email',
                  'captcha')
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'input-control', 'placeholder': 'Фамилия'}),
            'first_name': forms.TextInput(attrs={'class': 'input-control', 'placeholder': 'Имя'}),
            'patronymic': forms.TextInput(attrs={'class': 'input-control', 'placeholder': 'Отчество'}),
            'school': forms.TextInput(attrs={'class': 'input-control', 'placeholder': 'Школа'}),
            'email': forms.EmailInput(attrs={'class': 'input-control', 'placeholder': 'Электронная почта'}),
            'gender': forms.RadioSelect(attrs={'class': 'radio-input'}),
            'birth_date': forms.TextInput(attrs={'class': 'input-control date-input',
                                                 'placeholder': "Дата рождения",
                                                 'onfocus': "(this.type='date')",
                                                 'onblur': "(this.type='text')"}),
            'graduation_date': forms.Select(attrs={'class': 'input-control select-date-input',
                                                   'data-placeholder': 'Год окончания школы'
                                                   })
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email


class ExportForm(forms.Form):
    table_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-control', }))
    id = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # '№ п/п',
    FIO = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'ФИО',
    gender = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'пол',
    grades_five = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'Кол "5"',
    grades_four = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'Кол "4"',
    grades_three = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'Кол "3"',
    SNILS = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'Снилс',
    INN = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'инн',
    average_score = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'средн балл',
    original_or_copy = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'оригинал/копия',
    out_of_budget = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'внебюджет',
    documents_collected = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'Документы | забрали',
    received_receipt = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'Получил ли расписку',
    school = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'школа',
    graduation_date = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'год окончания',
    FIS = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'ФИС',
    application_id = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'номер заявления',
    application_in_gov_services = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'Электронное заявление',
    exam_date = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'Дата ЭЗ',
    exam_result = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'Дата и время проведения испытания',
    application_status = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'Статус',
    internal_exam_conducted = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'Вступительный экзамен',
    birth_date = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'Дата рождения',
    phone = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'Личный телефон',
    mother_full_name = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'Мама',
    mother_phone = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'Телефон мамы',
    father_full_name = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'Папа',
    father_phone = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'Телефон папы',
    passport_number = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'номер паспорта',
    issued_by = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'Кем выдан',
    issue_date = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'input-control', }))  # 'Дата выдачи'
