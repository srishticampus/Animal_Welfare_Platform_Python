from django import forms
from .models import Hospital


class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ['name', 'address', 'state', 'contact_number']