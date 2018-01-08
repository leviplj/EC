from datetime import date
from django.shortcuts import resolve_url as r
from django.test import TestCase

from EC.tests.models import Test
from ecweb.models import ClassRoom


class TestListGet(TestCase):
    def setUp(self):
        self.cr = ClassRoom.objects.create(number_class=1, level='Beginner', turn='morning',)

        self.obj = Test.objects.create(
            classroom=self.cr,
            date=date(2018, 1, 7),
            type=Test.LISTENING,
        )

        self.resp = self.client.get(r('tests:list'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'tests/list.html')

    def test_context(self):
        tests = self.resp.context['tests']
        self.assertListEqual(list(tests), [self.obj])

    def test_html(self):
        contents = (self.obj.classroom.level, self.obj.classroom.turn,
                    self.obj.date)

        for expected in contents:
            with self.subTest():
                self.assertContains(self.resp, expected)