from django.shortcuts import render

from EC.tests.models import Test
from ecweb.models import ClassRoom


def test_list(request):
    tests = Test.objects.all()
    classrooms = ClassRoom.objects.all()
    return render(request, 'tests/list.html', {'tests': tests, 'classrooms': classrooms})
