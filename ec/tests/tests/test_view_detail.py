from datetime import date
from django.shortcuts import resolve_url as r
from django.test import TestCase

from EC.tests.models import Test
from ecweb.models import ClassRoom, Student, BasicUser


class TestDetailGet(TestCase):
    def setUp(self):
        self.cr = ClassRoom.objects.create(number_class=1, level='Beginner', turn='morning',)

        self.obj = Test.objects.create(
            classroom=self.cr,
            date=date(2018, 1, 7),
            type=Test.LISTENING,
        )

        u1 = BasicUser.objects.create_superuser(
            username='user',
            first_name='User 1',
            password='pass',
            email="user1@mail.com"
        )

        u2 = BasicUser.objects.create_superuser(
            username='user',
            first_name='User 2',
            password='pass',
            email="user2@mail.com"
        )

        self.s1 = Student.objects.create(user=u1, cod=1, type_of_course='1-month')
        self.s2 = Student.objects.create(user=u2, cod=2, type_of_course='1-month')
        
        self.obj.attendances.add(self.s1)
        self.obj.attendances.add(self.s2)

        self.resp = self.client.get(r('tests:detail', self.obj.pk))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'tests/detail.html')

    def test_context(self):
        test = self.resp.context['test']
        self.assertIsInstance(test, Test)

    def test_html(self):
        contents = (self.obj.classroom.level, self.obj.classroom.turn,
                    self.obj.date, self.obj.type, self.s1, self.s2)

        for expected in contents:
            with self.subTest():
                self.assertContains(self.resp, expected)