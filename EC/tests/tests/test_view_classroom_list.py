from datetime import date
from django.shortcuts import resolve_url as r
from django.test import TestCase

from ecweb.models import ClassRoom


class TestClassroomListGet(TestCase):
    def setUp(self):
        self.classroom = ClassRoom.objects.create(number_class=1, level='Beginner', turn='morning',)

        self.resp = self.client.get(r('tests:classroom_list'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'tests/classroom_list.html')

    def test_context(self):
        classrooms = self.resp.context['classrooms']
        self.assertListEqual(list(classrooms), [self.classroom])

    def test_html(self):
        contents = (self.classroom.level, self.classroom.turn)

        for expected in contents:
            with self.subTest():
                self.assertContains(self.resp, expected)

    def test_has_link_to_create_test(self):
        url = 'href="{}"'.format(r('tests:new', self.classroom.slug))
        self.assertContains(self.resp, url)