from django.test import TestCase
from eh_app.models import GPAStatus, Semester, Student, StudentSectionEnrollment, StudentSemesterStatus

class GPAStatusTestCase(TestCase):
    fixtures = ['GPADeficiency']

    def test_get_status_queryset(self):
        status = GPAStatus.objects.get_status('D1', 2.6)
        self.assertEqual(status.status, 'Stay on Grace Period-GPA Def')

        status = GPAStatus.objects.get_status('D4', 3.8)
        self.assertEqual(status.status, 'Good Standing(Prev Prob)')

        self.assertRaises(
            ValueError,
            GPAStatus.objects.get_status,
            'D4',
            -1,
        )

        self.assertRaises(
            ValueError,
            GPAStatus.objects.get_status,
            'D10',
            1,
        )

class SemesterTestCase(TestCase):
    fixtures = ['test_seed']

    def test_current_queryset(self):
        sem = Semester.objects.get_current()
        self.assertEqual(sem.semester, 'Spring')
        self.assertEqual(sem.academic_year, '2018-2019')
        self.assertTrue(sem.current_semester())
        self.assertFalse(sem.past_semester())

    def test_new_current(self):
        # Where a semester is created newly
        Semester.objects.new_current(id=201921)
        self.assertEqual(Semester.objects.get_current().id, 201921)
        self.assertEqual(Semester.objects.get_current().predecessor.id, 201911)

        # Existing semester is found
        Semester.objects.new_current(id=202211)
        self.assertEqual(Semester.objects.get_current().id, 202211)
        self.assertEqual(Semester.objects.get_current().predecessor.id, 201921)

    def test_past_semester(self):
        sem = Semester.objects.get(id=201831)
        self.assertTrue(sem.past_semester())
        self.assertFalse(sem.current_semester())

class StudentTestCase(TestCase):
    fixtures = ['test_seed', 'GPADeficiency']

    def test_cumulative_gpa(self):
        student = Student.objects.get(uin=218009384)
        self.assertEqual(student.cumulative_gpa(), 4.0)

        student = Student.objects.get(uin=402009991)
        self.assertEqual(student.cumulative_gpa(), 'n/a')

    def test_first_year_grace(self):
        student = Student.objects.get(uin=358003821)
        self.assertTrue(student.first_year_grace())

        student = Student.objects.get(uin=329003124)
        self.assertTrue(student.first_year_grace())

        student = Student.objects.get(uin=987001241)
        self.assertFalse(student.first_year_grace())

        student = Student.objects.get(uin=402009991)
        self.assertEqual(student.first_year_grace(), 'Invalid record')

    def test_major_names(self):
        student = Student.objects.get(uin=218009384)
        self.assertEqual(student.major_names(), ['CPSC'])

    def test_minor_names(self):
        student = Student.objects.get(uin=218009384)
        self.assertEqual(student.minor_names(), [])

    def test_status_gpa_alone(self):
        student = Student.objects.get(uin=218009384)
        self.assertEqual(student.status_gpa_alone(), 'Stay on Grace Period-GPA Ok')

        student = Student.objects.get(uin=987001241)
        self.assertEqual(student.status_gpa_alone(), 'n/a')

        student = Student.objects.get(uin=402009991)
        self.assertEqual(student.status_gpa_alone(), 'n/a')

class StudentSectionEnrollmentTestCase(TestCase):
    fixtures = ['test_seed']

    def test_semester(self):
        student_enrollment = StudentSectionEnrollment.objects.get(id=1)
        self.assertEqual(student_enrollment.semester().semester, 'Spring')

    def test_credits(self):
        student_enrollment = StudentSectionEnrollment.objects.get(id=1)
        self.assertEqual(student_enrollment.credits(), 3)

class StudentSemesterStatusTestCase(TestCase):
    fixtures = ['test_seed']

    def test_post_init(self):
        status = StudentSemesterStatus.objects.get(id=1)
        self.assertEqual(status.overall_hours_attempted, 0)
        self.assertEqual(status.status, 'Good Standing')
        self.assertEqual(status.previous_status, 'Good Standing')

        status = StudentSemesterStatus.objects.get(id=2)
        self.assertEqual(status.hours_attempted, 3)
        self.assertEqual(status.previous_status, 'Good Standing')
        self.assertEqual(status.overall_hours_attempted, 3)
        self.assertEqual(status.overall_quality_points, 12)
