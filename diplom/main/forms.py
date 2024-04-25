from django import forms
from django.contrib.auth import get_user_model

from diplom import settings
from main.models import Applicant


class ApplicantShortForm(forms.ModelForm):
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
                  )
        widgets = {
            'gender': forms.RadioSelect(attrs={'class': 'cool'}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'graduation_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email
