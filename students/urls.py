from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, MajorListView, MajorViewSet, DepartmentViewSet, TopPerformersView, DepartmentStatsView, HighSalaryMajorStudentsView

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'majors', MajorViewSet)          # New CRUD route
router.register(r'departments', DepartmentViewSet) # New CRUD route

urlpatterns = [
    path('', include(router.urls)),
    path('majors/', MajorListView.as_view(), name='major-list'),
    path('top-performers/', TopPerformersView.as_view(), name='top-performers'),
    path('department-stats/', DepartmentStatsView.as_view(), name='dept-stats'),
    path('high-salary-students/', HighSalaryMajorStudentsView.as_view(), name='high-salary'),
]