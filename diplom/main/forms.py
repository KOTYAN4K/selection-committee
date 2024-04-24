from django.forms import forms, ModelForm

from main.models import Applicant


class ApplicantShortForm(ModelForm):

    class Meta:
        model = Applicant
        fields = ('photo', 'last_name', 'first_name', 'patronymic', 'gender',
                  'birth_date', 'email', 'phone', 'address',)


