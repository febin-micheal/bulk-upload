from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload-file/', views.upload_file, name='upload-file'),
    path('bulk-upload/', views.bulk_upload, name='bulk-upload'),
    path('list-view/', views.list_view, name='list-view'),
]
