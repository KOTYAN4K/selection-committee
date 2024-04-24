from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView, View

from account.forms import CustomUserCreationForm, LoginUserForm, ProfileUserForm
from main.models import Applicant


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'account/authorization.html'
    context_object_name = 'login'


class UserCreation(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'account/authorization.html'
    context_object_name = 'registration'
    success_url = reverse_lazy('account:login')


class ProfileUser(TemplateView, LoginRequiredMixin):
    template_name = 'account/profile.html'

    def get_success_url(self):
        return reverse_lazy('account:profile', args=[self.request.user.pk])

    def get_object(self, queryset=None):
        return self.request.user


class EditProfile(UpdateView, LoginRequiredMixin):
    model = Applicant
    form_class = ProfileUserForm
    template_name = 'account/profile_edit.html'

    def get_success_url(self):
        return reverse_lazy('account:profile', args=[self.request.user.pk])

    def get_object(self, queryset=None):
        return self.request.user


