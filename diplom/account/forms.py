from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from account.models import User
from main.models import Applicant, Parent, Document, Admission


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'input-control', 'placeholder': 'Логин/Почта'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'input-control', 'id': 'password-input', 'placeholder': 'Пароль'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'input-control', 'placeholder': 'Логин'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'input-control', 'id': 'password-input', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(
        attrs={'class': 'input-control', 'placeholder': 'Повтор пароля'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'email', ]
        labels = {
            'email': 'E-mail',
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'input-control', 'placeholder': 'E-mail'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email',)


class ProfileUserForm(forms.ModelForm):
    last_name = forms.CharField(disabled=True, label='Фамилия', widget=forms.TextInput(attrs={'class': 'input-control'}))
    first_name = forms.CharField(disabled=True, label='Имя', widget=forms.TextInput(attrs={'class': 'input-control'}))
    patronymic = forms.CharField(disabled=True, label='Отчество', widget=forms.TextInput(attrs={'class': 'input-control'}))
    email = forms.CharField(disabled=True, label='Эл.Почта', widget=forms.TextInput(attrs={'class': 'input-control'}))

    class Meta:
        model = Applicant
        fields = (
            'photo',
            'last_name',
            'first_name',
            'patronymic',
            'email',
            'phone',
            'address',
            'consent'
        )
        widgets = {
            'photo': forms.FileInput(attrs={
                'class': 'input-control',
                'type': "file",
                'id': "input__file",
                'accept': "image/*"
            }),
            'gender': forms.Select(attrs={'disabled': 'disabled'}),
            'address': forms.Textarea(attrs={'class': 'input-control', 'placeholder': 'Адрес'}),
            'phone': forms.TextInput(attrs={'class': 'input-control', 'placeholder': 'Телефон'}),
            'consent': forms.FileInput(attrs={
                'class': 'input-control',
                'type': "file",
                'id': "input__file",
                'accept': ".doc,.docx,.xml,application/msword,"
                          "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            }),
        }


class ParentsEditForm(forms.ModelForm):
    class Meta:
        model = Parent

        fields = ('mother_full_name',
                  'mother_phone',
                  'father_full_name',
                  'father_phone')

        widgets = {
            'mother_full_name': forms.TextInput(attrs={'class': 'input-control', 'placeholder': 'ФИО Мамы'}),
            'mother_phone': forms.TextInput(attrs={'class': 'input-control', 'placeholder': 'Телефон Мамы'}),
            'father_full_name': forms.TextInput(attrs={'class': 'input-control', 'placeholder': 'ФИО Папы'}),
            'father_phone': forms.TextInput(attrs={'class': 'input-control', 'placeholder': 'Телефон Папы'}),
        }


class DocumentEditForm(forms.ModelForm):
    class Meta:
        model = Document

        fields = ('SNILS',
                  'INN',
                  'passport_number',
                  'issued_by',
                  'issue_date',)

        widgets = {
            'SNILS': forms.TextInput(attrs={'class': 'input-control',
                                            'placeholder': 'Снилс',
                                            # 'pattern': '\d{3}-\d{3}-\d{3} \d{2}',
                                            'data-mask': '999-999-999 99'}),
            'INN': forms.TextInput(attrs={'class': 'input-control',
                                          'placeholder': 'ИНН',
                                          # 'pattern': '\d{12}',
                                          'data-mask': '999999999999'}),
            'passport_number': forms.TextInput(attrs={'class': 'input-control',
                                                      'placeholder': 'Номер паспорта',
                                                      # 'pattern': '\d{4} \d{6}',
                                                      'data-mask': '9999 999999'}),
            'issue_date': forms.DateInput(attrs={'class': 'input-control', 'type': 'date'}),
            'issued_by': forms.Textarea(attrs={'class': 'input-control',
                                               # 'pattern': '[\w\s,]+',
                                               'placeholder': 'Кем выдан паспорт'}),
        }


class AdmissionEditForm(forms.ModelForm):
    class Meta:
        model = Admission

        fields = (
            'department',
        )

        widgets={
            'department': forms.CheckboxSelectMultiple(attrs={'class': '    '}),
        }
