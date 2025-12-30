import os
import csv
import django

# 1. Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from students.models import Department, Major, Student

def run():
    # Clear existing data so you can run this multiple times without errors
    print("Cleaning database...")
    Student.objects.all().delete()
    Major.objects.all().delete()
    Department.objects.all().delete()

    # 2. Define our 4 core Departments
    dept_names = ['Mathematics', 'Computer Science', 'Business', 'Engineering']
    dept_map = {}
    for name in dept_names:
        d, created = Department.objects.get_or_create(name=name)
        dept_map[name] = d

    # 3. Load Majors (Small Dataset)
    print("Loading Majors...")
    with open('majors_data.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Map the CSV category to our Department objects
            cat = row['Major_category']
            target_dept = None
            
            if 'Engineering' in cat: target_dept = dept_map['Engineering']
            elif 'Business' in cat: target_dept = dept_map['Business']
            elif 'Computers' in cat: target_dept = dept_map['Computer Science']
            else: target_dept = dept_map['Mathematics']

            Major.objects.create(
                name=row['Major'],
                department=target_dept,
                median_salary=int(row['Median']),
                unemployment_rate=float(row['Unemployment_rate'])
            )

    # 4. Load Students (Big Dataset)
    print("Loading 5,000 Students...")
    # Get all majors into a list to assign them randomly to students 
    # (since the student CSV doesn't specify a specific major, only a dept)
    all_majors = list(Major.objects.all())
    import random

    with open('students_data.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        count = 0
        for row in reader:
            # Pick a random major that belongs to the student's department
            student_dept_name = row['Department']
            # Simple fix for naming discrepancies
            if student_dept_name == "Computer Science": dept_key = "Computer Science"
            else: dept_key = student_dept_name

            # Filter majors to find one in the right department
            available_majors = [m for m in all_majors if m.department.name == dept_key]
            assigned_major = random.choice(available_majors) if available_majors else all_majors[0]

            Student.objects.create(
                student_id=row.get('Student_ID', f"STU{count}"),
                first_name=row.get('First_Name', 'First'),
                last_name=row.get('Last_Name', 'Last'),
                major=assigned_major,
                attendance=float(row.get('Attendance', 0)),
                project_score=float(row.get('Projects_Score', 0)),
                final_grade=row.get('Grade', 'F')
            )
            count += 1
            if count % 1000 == 0:
                print(f"Loaded {count} students...")

    print(f"Success! Total rows: {Department.objects.count() + Major.objects.count() + Student.objects.count()}")

if __name__ == '__main__':
    run()