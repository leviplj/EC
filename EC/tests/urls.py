from django.urls import path, re_path

from EC.tests.views import test_list, new, detail

app_name = 'tests'
urlpatterns = [
    re_path(r'^$', test_list, name='list'),
    path('new/<slug:classroom>', new, name='new'),
    re_path(r'^detail/(?P<id>\d+)', detail, name='detail'),
]
