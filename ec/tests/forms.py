from django import forms

from EC.tests.models import Test


class TestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        self.base_fields['attendances'].widget = forms.CheckboxSelectMultiple()
    
    class Meta:
        model = Test
        fields = ['classroom', 'date', 'type', 'attendances']