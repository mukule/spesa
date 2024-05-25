from django import forms
from .models import Consult


class ConsultForm(forms.ModelForm):
    class Meta:
        model = Consult
        fields = ['description']
        labels = {
            'description': 'Describe your Concern',
        }
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }
