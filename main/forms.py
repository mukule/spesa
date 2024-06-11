from django import forms
from .models import *


class ConsultForm(forms.ModelForm):
    class Meta:
        model = Consult
        fields = ['description']
        labels = {
            'description': 'Describe your Concern',
        }
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description', 'id': 'description'}),
        }


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['response_doc', 'more_details']
        labels = {
            'response_doc': '',
            'more_details': ''
        }
        widgets = {
            'response_doc': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Response Document'}),
            'more_details': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'More Details'})
        }


class ClientResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['satisfied', 'feedback']
        labels = {
            'satisfied': '',
            'feedback': ''
        }
        widgets = {
            'satsified': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'feedback'}),
        }
