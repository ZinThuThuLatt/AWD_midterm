from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg, Count
from .models import Department, Major, Student
from .serializers import DepartmentSerializer, MajorSerializer, StudentSerializer, DepartmentStatsSerializer
from drf_spectacular.utils import extend_schema

# 1. Standard ViewSet for Students (Covers GET, POST, PUT, DELETE)
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

# 2. List all Majors
#class MajorListView(generics.ListAPIView):
#    queryset = Major.objects.all()
#    serializer_class = MajorSerializer

# New CRUD for Departments (Provides 5 endpoints: List, Create, Get, Update, Delete)
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

# Upgraded CRUD for Majors (Provides 5 endpoints: List, Create, Get, Update, Delete)
class MajorViewSet(viewsets.ModelViewSet):
    queryset = Major.objects.all()
    serializer_class = MajorSerializer

# 3. "Interesting" Query: Top Performers
# Returns students with project scores > 90
class TopPerformersView(generics.ListAPIView):
    serializer_class = StudentSerializer
    
    def get_queryset(self):
        return Student.objects.filter(project_score__gt=90)
    
# 4. Aggregated Stats per Department
@extend_schema(responses={200: DepartmentStatsSerializer(many=True)})
class DepartmentStatsView(APIView):
    """
    Returns statistics for each department by calculating averages 
    across all students and majors within that department.
    """
    def get(self, request):
        stats = Department.objects.annotate(
            average_project_score=Avg('majors__students__project_score'),
            average_attendance=Avg('majors__students__attendance'),
            total_students=Count('majors__students'),
            average_major_salary=Avg('majors__median_salary')
        ).values(
            'name', 'average_project_score', 'average_attendance', 
            'total_students', 'average_major_salary'
        )
        
        # Format the data for the serializer
        formatted_stats = [
            {
                'department_name': s['name'],
                'average_project_score': s['average_project_score'],
                'average_attendance': s['average_attendance'],
                'total_students': s['total_students'],
                'average_major_salary': s['average_major_salary'],
            } for s in stats
        ]
        
        serializer = DepartmentStatsSerializer(formatted_stats, many=True)
        return Response(serializer.data)

# 5. Relational Filter: High-Salary Students
class HighSalaryMajorStudentsView(generics.ListAPIView):
    """
    Returns students enrolled in majors where the median 
    graduate salary is > $60,000.
    """
    serializer_class = StudentSerializer

    def get_queryset(self):
        return Student.objects.filter(major__median_salary__gt=60000)