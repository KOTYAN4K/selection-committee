from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView, ListView

from account.forms import CustomUserCreationForm, LoginUserForm, ProfileUserForm, ParentsEditForm, DocumentEditForm, \
    AdmissionEditForm
from main.models import Applicant, Parent, Document, Admission


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
        return reverse_lazy('account:profile', args=[self.request.user.id])

    def get_object(self, queryset=None):
        return self.request.user


class EditProfile(UpdateView, LoginRequiredMixin):
    model = Applicant
    template_name = 'account/profile_edit.html'
    form_class = ProfileUserForm

    def get_success_url(self):
        return reverse_lazy('account:profile', args=[self.request.user.id])


class ParentsProfileView(UpdateView, LoginRequiredMixin):
    model = Parent
    template_name = 'account/profile_edit.html'
    form_class = ParentsEditForm

    def get_success_url(self):
        return reverse_lazy('account:profile', args=[self.request.user.id])

    def get_object(self, queryset=None):
        return Parent.objects.get(student=self.request.user.student)


class DocumentsProfileView(UpdateView, LoginRequiredMixin):
    model = Document
    template_name = 'account/profile_edit.html'
    form_class = DocumentEditForm

    def get_success_url(self):
        return reverse_lazy('account:profile', args=[self.request.user.id])

    def get_object(self, queryset=None):
        return Document.objects.get(student=self.request.user.student)


class AdmissionProfileView(UpdateView, LoginRequiredMixin):
    model = Admission
    template_name = 'account/profile_edit.html'
    form_class = AdmissionEditForm

    def get_success_url(self):
        return reverse_lazy('account:profile', args=[self.request.user.id])

    def get_object(self, queryset=None):
        return Admission.objects.get(applicant=self.request.user.student)


class RankProfileView(ListView, LoginRequiredMixin):
    template_name = 'account/profile_rank.html'
    model = Admission