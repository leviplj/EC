from django.shortcuts import render, resolve_url as r
from django.http import HttpResponseRedirect

from EC.tests.models import Test
from EC.tests.forms import TestForm
from ecweb.models import ClassRoom


def test_list(request):
    tests = Test.objects.all()
    classrooms = ClassRoom.objects.all()
    return render(request, 'tests/list.html', {'tests': tests, 'classrooms': classrooms})

def classroom_list(request):
    classrooms = ClassRoom.objects.all()
    return render(request, 'tests/classroom_list.html', {'classrooms': classrooms})

def new(request, classroom):
    if request.method == 'POST':
        return create(request, classroom)

    return empty_form(request, classroom)

def create(request, classroom):
    form = TestForm(request.POST)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(r('tests:list')) 
    else:        
        return render(request, 'tests/test_form.html', {'form': form, 'classroom': classroom})
        

def empty_form(request, classroom):
    cr = ClassRoom.objects.get(slug=classroom)

    student_choices = []
    for student in cr.students.all():
        student_id = student.id
        student_name = '{}, {}'.format(
            student.user.last_name, student.user.first_name)
        student_choices.append((student_id, student_name))
    
    form = TestForm(initial={'classroom': cr})
    # form.fields['classroom'].widget.attrs['disabled'] = True
    form.fields['attendances'].choices = tuple(student_choices)
    
    return render(request, 'tests/test_form.html', {'form': form, 'classroom': classroom})

def detail(request, id):
    test = Test.objects.get(pk=id)
    return render(request, 'tests/detail.html', {'test': test})