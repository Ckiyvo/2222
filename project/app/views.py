# 1111/project/app/views.py

import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render
import json

ALLOWED_FILE_EXTENSIONS = ['.txt', '.pdf', '.doc', '.docx', '.csv', '.jpg', '.jpeg', '.png', '.wav', '.mp3', '.aac', '.mp4']

# 项目列表，用于存储已创建的项目信息
projects = []

@csrf_exempt
def upload_files(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        valid_files = []
        invalid_files = []

        for file in files:
            file_extension = os.path.splitext(file.name)[1].lower()
            if file_extension in ALLOWED_FILE_EXTENSIONS:
                valid_files.append(file)
            else:
                invalid_files.append(file.name)

        if invalid_files:
            return JsonResponse({'message': f'以下文件类型不允许上传: {", ".join(invalid_files)}'}, status=400)

        for file in valid_files:
            file_path = os.path.join(settings.MEDIA_ROOT, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

        return JsonResponse({'message': '文件上传成功'})

    return JsonResponse({'message': '无效的请求方法'}, status=400)

@csrf_exempt
def create_project(request):
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        if not project_name:
            return JsonResponse({'message': '项目名称不能为空'}, status=400)

        # 处理文件上传
        files = request.FILES.getlist('files')
        valid_files = []
        invalid_files = []

        for file in files:
            file_extension = os.path.splitext(file.name)[1].lower()
            if file_extension in ALLOWED_FILE_EXTENSIONS:
                valid_files.append(file)
            else:
                invalid_files.append(file.name)

        if invalid_files:
            return JsonResponse({'message': f'以下文件类型不允许上传: {", ".join(invalid_files)}'}, status=400)

        project_folder = os.path.join(settings.MEDIA_ROOT, project_name)
        os.makedirs(project_folder, exist_ok=True)

        for file in valid_files:
            file_path = os.path.join(project_folder, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

        # 将项目信息添加到项目列表
        projects.append({
            'name': project_name,
            'files': [file.name for file in valid_files]
        })

        return JsonResponse({'message': '项目创建成功'})

    return JsonResponse({'message': '无效的请求方法'}, status=400)


@csrf_exempt
def get_projects(request):
    if request.method == 'GET':
        return JsonResponse({'projects': projects})
    return JsonResponse({'message': '无效的请求方法'}, status=400)



from .models import Project

def get_project_list(request):
    projects = Project.objects.all()
    project_list = []
    for project in projects:
        project_data = {
            'id': project.id,
            'name': project.name,
            'created_at': project.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        project_list.append(project_data)
    return JsonResponse({'projects': project_list})

