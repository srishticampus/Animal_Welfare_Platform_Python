from django import forms
from .models import Hospital

class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ['name', 'address', 'state', 'contact_number']
        labels = {
            'name': 'Name',
            'address': 'Address',
            'state': 'State',
            'contact_number': 'Contact Number',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-orange-500 focus:border-orange-500',
                'placeholder': 'e.g. ABC Hospital'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-orange-500 focus:border-orange-500',
                'placeholder': 'e.g. 123 Main Street',
                'rows': 3
            }),
            'state': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-orange-500 focus:border-orange-500',
                'placeholder': 'e.g. Maharashtra'
            }),
            'contact_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-orange-500 focus:border-orange-500',
                'placeholder': 'e.g. 9876543210'
            }),
        }
