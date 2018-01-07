from django.contrib import admin
from django.forms import CheckboxSelectMultiple

from EC.tests.models import Test


class TestAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(TestAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['attendances'].widget = CheckboxSelectMultiple()
        return form


admin.site.register(Test, TestAdmin)