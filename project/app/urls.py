# 1111/project/app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('api/upload/', views.upload_files, name='upload_files'),
    path('api/create_project/', views.create_project, name='create_project'),
    path('api/get_projects/', views.get_projects, name='get_projects'),
    path('api/get_project_list/', views.get_project_list, name='get_project_list'),
]

