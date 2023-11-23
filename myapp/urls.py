from django.urls import path
from .views import create_excel_file, download_csv

urlpatterns = [
    path('api/create_excel', create_excel_file, name='create_excel_file'),
    path('static/<str:file_name>', download_csv, name='download_excel'),
]