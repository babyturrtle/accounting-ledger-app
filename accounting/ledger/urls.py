"""URLs for the ledger app"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.file_upload, name='upload_file'),
    path('view-files/', views.view_files, name='view_files'),
    path('<int:file_id>', views.view_ledger_file, name='ledger_file'),
]
