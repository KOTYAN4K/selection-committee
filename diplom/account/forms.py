from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from account.models import User
from main.models import Applicant


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Логин/Почта'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-input', 'id': 'password-input', 'placeholder': 'Пароль'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Логин'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-input', 'id': 'password-input', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(
        attrs={'class': 'form-input', 'placeholder': 'Повтор пароля'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'email', ]
        labels = {
            'email': 'E-mail',
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'E-mail'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email


class ProfileUserForm(forms.Form):
    last_name = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput())
    first_name = forms.CharField(disabled=True, label='Почта', widget=forms.TextInput())
    patronymic = forms.CharField(disabled=True, label='Почта', widget=forms.TextInput())

    class Meta:
        model = Applicant
        fields = '__all__'
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }
        widgets = {
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput()
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email',)
