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
