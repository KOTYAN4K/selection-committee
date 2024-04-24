from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('form/', views.TestFormView.as_view(), name='form'),
    path('download-table/', views.download_table, name='download-table'),
]
