from django.shortcuts import resolve_url as r
from django.test import TestCase

from EC.tests.forms import TestForm
from EC.tests.models import Test
from ecweb.models import ClassRoom

class TestNewGet(TestCase):
    def setUp(self):
        cr = ClassRoom(number_class=1, level='Beginner', turn='morning',)
        cr.save()
        self.resp = self.client.get(r('tests:new', cr.slug))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'tests/test_form.html')

    def test_html(self):
        tags = (('<form', 1),
                ('<input', 2),
                ('<select', 2),
                ('type="submit"', 1))

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_csrf(self):
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, TestForm)

class SubscriptionsNewPostValid(TestCase):
    def setUp(self):
        cr = ClassRoom(number_class=1, level='Beginner', turn='morning',)
        cr.save()

        data = dict(classroom=cr.id, date='2018-01-08', type=Test.LISTENING)

        self.resp = self.client.post(r('tests:new', cr.slug), data)

    def test_post(self):
        self.assertEqual(302, self.resp.status_code)
        self.assertRedirects(self.resp, r('tests:list'))

    def test_save_test(self):
        self.assertTrue(Test.objects.exists())
    