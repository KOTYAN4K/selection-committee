from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('form/', views.TestFormView.as_view(), name='form'),
    path('download-table/', views.download_table, name='download-table'),
    path('download-document/', views.download_document, name='download_document'),
    path('update-schools/', views.update_schools, name='update-schools'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
]
