from django import forms
from .models import Consult


class ConsultForm(forms.ModelForm):
    class Meta:
        model = Consult
        fields = ['description', 'transaction_code']
        labels = {
            'description': 'Describe your Concern',
            'transaction_code': ''
        }
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'transaction_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter M-PESA Transaction Code i.e SEL6YPI47I'}),
        }
