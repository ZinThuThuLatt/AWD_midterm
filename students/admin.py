from django.contrib import admin
from .models import Department, Major, Student

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'median_salary')
    list_filter = ('department',) # Adds a filter sidebar
    search_fields = ('name',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'major', 'final_grade')
    list_filter = ('major__department', 'final_grade') # Filter by Department or Grade
    search_fields = ('last_name', 'student_id')
