from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from datetime import date

from django.contrib.auth import logout
from django.views.generic.list import ListView

from .forms import PhotoForm, AttendanceForm
from .models import ClassRoom, Teacher, Student, Class, BasicUser, Coordinator


@login_required
def home_dashboard(request):
    current_user = request.user
    user = Coordinator.objects.filter(user__id=current_user.id)

    if user:
        return render(request, 'ecweb/coordinator-dashboard.html',
                      {'coordinator': user.first(),
                       'current_user': current_user})

    user = Teacher.objects.filter(user__id=current_user.id)
    if user:
        return render(request, 'ecweb/teacher-dashboard.html',
                      {'teacher': user.first(),
                       'current_user': current_user})

    user = Student.objects.filter(user__id=current_user.id)
    if user:
        date_start = current_user.date_joined.date()
        days_con = date.today() - date_start
        days_cont_int = int(days_con.days)
        if user[0].type_of_course == "1-month":
            count_day = 30 - days_cont_int
            percent = int(-100.0 * (count_day / 30))

        else:
            count_day = 30 * 6 - days_cont_int
            percent = int(100.0 * (count_day / (30 * 6)))

        return render(request, 'ecweb/student-dashboard.html',
                      {'student': user.first(),
                       'current_user': current_user,
                       'days_cont_int': days_cont_int})

    raise Http404

@login_required
def user_detail(request):
    current_user = request.user
    insta = get_object_or_404(BasicUser, pk=int(current_user.id))
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=insta)
        if form.is_valid():
            profil = form.save()
            profil.user = current_user
            profil.save()

            return redirect('user_detail')
    else:
        form = PhotoForm()
    return render(request, 'ecweb/student.html',
                  {'current_user': current_user, 'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')


@login_required
def calendar_view(request):
    events = Calendar.objects.all()
    return render(request, 'ecweb/calendar.html', {'events': events})


class ClassRoomListView(ListView):

    model = ClassRoom
    template_name = 'ecweb/classroom.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ClassRoomListView, self).get_context_data(
            *args, **kwargs
        )

        queryset = self.get_queryset()

        return context

    def get_queryset(self):
        current_user = self.request.user

        queryset = super(ClassRoomListView, self).get_queryset()

        if current_user.is_staff:
            teacher = Teacher.objects.filter(user=current_user.id)

            if teacher.exists():
                queryset = ClassRoom.objects.filter(
                    teachers=teacher.first().id
                )

            else:
                queryset = ClassRoom.objects.all()

        else:
            student = Student.objects.get(user=current_user.id)
            queryset = ClassRoom.objects.filter(students=student.id)

        return queryset


@login_required
def classes_view(request):
    all_classes = Class.objects.all()
    current_user = request.user

    return render(request, 'ecweb/classes.html', {'all_classes': all_classes, 'current_user': current_user})


@login_required
def class_view(request, class_id):
    current_user = request.user
    class_obj = Class.objects.get(id=class_id)

    choices_student = []
    for student in class_obj.classroom.students.all():
        student_id = student.id
        student_name = '{}, {}'.format(student.user.last_name, student.user.first_name)
        choices_student.append((student_id, student_name))

    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        form.fields['students'].choices = tuple(choices_student)

        if form.is_valid():
            students_to_update = [int(s) for s in form.cleaned_data['students']]
            class_obj.attendances.clear()
            class_obj.attendances.add(*students_to_update)

        return HttpResponseRedirect('/class')

    else:
        attendanced_students = [s.id for s in class_obj.attendances.all()]

        form = AttendanceForm(initial={'class_id': class_id, 'students': attendanced_students})
        form.fields['students'].choices = tuple(choices_student)

    return render(request, 'ecweb/class_attendance.html',
                  {'form': form, 'current_user': current_user, 'class_id': class_id, 'class_obj': class_obj})
