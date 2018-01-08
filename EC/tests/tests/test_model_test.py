from datetime import date
from django.core.exceptions import ValidationError
from django.test.testcases import TestCase

from EC.tests.models import Test
from ecweb.models import ClassRoom, Student, BasicUser


class TestModelTest(TestCase):
    def setUp(self):
        self.cr = ClassRoom.objects.create(number_class=1, level='Beginner', turn='morning',)

        u1 = BasicUser.objects.create_superuser(
            username='user',
            password='pass',
            email="user1@mail.com"
        )

        u2 = BasicUser.objects.create_superuser(
            username='user',
            password='pass',
            email="user2@mail.com"
        )

        s1 = Student.objects.create(user=u1, cod=1, type_of_course='1-month')
        s2 = Student.objects.create(user=u2, cod=2, type_of_course='1-month')

        self.obj = Test.objects.create(
            classroom=self.cr,
            date=date(2018, 1, 7),
            type=Test.LISTENING,
        )
        self.obj.attendances.add(s1)
        self.obj.attendances.add(s2)

    def test_create(self):
        self.assertTrue(Test.objects.exists())

    def test_str(self):
        obj_str = f'2018-01-07: {Test.LISTENING}'
        self.assertEqual(obj_str, str(self.obj))

    def test_choices(self):
        """Test type should be limited to listening or reading"""
        test = Test(
            classroom=self.cr,
            date=date(2018, 1, 7),
            type='writing'
        )

        self.assertRaises(ValidationError, test.full_clean)

    def test_has_attendances(self):
        test = Test.objects.first()
        self.assertTrue(test.attendances.exists())