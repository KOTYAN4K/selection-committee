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


class ProfileUserForm(forms.ModelForm):
    # last_name = forms.CharField(disabled=True, label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input'}))
    # first_name = forms.CharField(disabled=True, label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    # patronymic = forms.CharField(disabled=True, label='Отчество', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True, label='Эл.Почта', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Applicant
        fields = '__all__'


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email',)
