from rest_framework import serializers
from .models import Department, Major, Student

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class MajorSerializer(serializers.ModelSerializer):
    # This shows the department name instead of just an ID
    department_name = serializers.ReadOnlyField(source='department.name')
    
    class Meta:
        model = Major
        fields = ['id', 'name', 'department_name', 'median_salary', 'unemployment_rate']

class StudentSerializer(serializers.ModelSerializer):
    major_name = serializers.ReadOnlyField(source='major.name')
    department_name = serializers.ReadOnlyField(source='major.department.name')

    # dropdown menu in API interface
    major = serializers.PrimaryKeyRelatedField(queryset=Major.objects.all())

    class Meta:
        model = Student
        fields = ['student_id', 'first_name', 'last_name', 'major', 'major_name', 'department_name', 'attendance', 'project_score', 'final_grade']

class DepartmentStatsSerializer(serializers.Serializer):
    department_name = serializers.CharField()
    average_project_score = serializers.FloatField()
    average_attendance = serializers.FloatField()
    total_students = serializers.IntegerField()
    average_major_salary = serializers.FloatField()