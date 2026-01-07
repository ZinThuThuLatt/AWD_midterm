# students/tests.py
from rest_framework.test import APITestCase
from rest_framework import status

class StudentAPITests(APITestCase):
    # verify analytical stats endpoint
    def test_get_department_stats(self):
        response = self.client.get('/api/department-stats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # verify main students list
    def test_get_students_list(self):
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # check if serializer rejects attendance over 100%
    def test_invalid_attendance_validation(self):
        invalid_data = {"first_name": "John", "attendance": 150.0} # Invalid attendance
        response = self.client.post('/api/students/', invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)