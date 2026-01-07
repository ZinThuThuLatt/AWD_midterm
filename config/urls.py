"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.shortcuts import render
import sys
import django
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

def api_root_info(request):
    context = {
        "project": "University Enrollment API",
        "python_version": sys.version,
        "django_version": django.get_version(),
        "packages": ["djangorestframework", "django-filter"],
        "admin_access": "User: AWD / Pass: AWD",
        "documentation": "http://127.0.0.1:8000/api/docs/",
        "endpoints": {
            "students": "/api/students/",
            "majors": "/api/majors/",
            "top_performers": "/api/top-performers/",
            "department_stats": "/api/department-stats/",
            "high_salary_students": "/api/high-salary-students/"
        }
    }
    # renders HTML
    return render(request, 'students/index.html', context)

urlpatterns = [
    path('', api_root_info),
    path('admin/', admin.site.urls),
    path('api/', include('students.urls')),

    # swagger UI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
