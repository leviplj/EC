from django.urls import include, re_path

from EC.tests.views import test_list

app_name = 'tests'
urlpatterns = [
    re_path(r'^$', test_list, name='list'),
]
