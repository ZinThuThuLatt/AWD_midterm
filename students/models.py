from django.db import models

# R2 - appropriate data model

class Department(models.Model):
    # Holds the four majors, Mathematics, Computer Science, Business, Engineering
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Major(models.Model):
    # 173 entries dataset from 'College Majors. source link - https://www.kaggle.com/datasets/tunguz/college-majors'
    name = models.CharField(max_length=150, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='majors')
    median_salary = models.IntegerField()
    unemployment_rate = models.FloatField()

    def __str__(self):
        return self.name

class Student(models.Model):
    # 5,000-row dataset, source link - https://www.kaggle.com/datasets/mahmoudelhemaly/students-grading-dataset
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    # Link student to a specific Major
    major = models.ForeignKey(Major, on_delete=models.CASCADE, related_name='students')
    
    # Performance Data
    attendance = models.FloatField()
    project_score = models.FloatField()
    final_grade = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
