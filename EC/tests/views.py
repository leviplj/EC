from django.shortcuts import render, resolve_url as r
from django.http import HttpResponseRedirect

from EC.tests.models import Test
from EC.tests.forms import TestForm
from ecweb.models import ClassRoom


def test_list(request):
    tests = Test.objects.all()
    classrooms = ClassRoom.objects.all()
    return render(request, 'tests/list.html', {'tests': tests, 'classrooms': classrooms})

def new(request, classroom):
    if request.method == 'POST':
        return create(request)

    return empty_form(request, classroom)

def create(request):
    form = TestForm(request.POST)

    if form.is_valid():
        form.save()

    return HttpResponseRedirect(r('tests:list')) 

def empty_form(request, classroom):
    classroom = ClassRoom.objects.get(slug=classroom)

    student_choices = []
    for student in classroom.students.all():
        student_id = student.id
        student_name = '{}, {}'.format(
            student.user.last_name, student.user.first_name)
        student_choices.append((student_id, student_name))
    
    form = TestForm(initial={'classroom': classroom})
    form.fields['classroom'].widget.attrs['disabled'] = True
    form.fields['attendances'].choices = tuple(student_choices)
    
    return render(request, 'tests/test_form.html', {'form': form})