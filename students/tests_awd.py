import pytest
from hypothesis import given, strategies as st
from rest_framework.test import APIClient
from students.models import Major, Department

@pytest.mark.django_db
class TestStudentAPI:
    def setup_method(self):
        self.client = APIClient()
        # Setup at least one major so the random students have somewhere to go
        dept = Department.objects.create(name="Science")
        self.major = Major.objects.create(
            name="Physics", department=dept, median_salary=50000, unemployment_rate=0.05
        )

    @given(
        first_name=st.text(min_size=1),
        last_name=st.text(min_size=1),
        score=st.floats(min_value=0, max_value=100)
    )
    def test_create_student_hypothesis(self, first_name, last_name, score):
        # This will run multiple times with random names and scores
        payload = {
            "student_id": "TEST_ID",
            "first_name": first_name,
            "last_name": last_name,
            "major": self.major.id,
            "attendance": 90.0,
            "project_score": score,
            "final_grade": "A"
        }
        response = self.client.post('/api/students/', payload)
        # We check that the server doesn't crash (should be 201 or 400, not 500)
        assert response.status_code != 500