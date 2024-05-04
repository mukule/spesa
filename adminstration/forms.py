from django import forms
from main.models import *
from ckeditor.widgets import CKEditorWidget


class SpecialityForm(forms.ModelForm):
    class Meta:
        model = Speciality
        fields = ['name', 'icon', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Speciality Name'}),
            'icon': forms.FileInput(attrs={'class': 'form-control-file'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
        }
        labels = {
            'name': '',
            'icon': '',
            'price': '',
        }


class FinancialConcernForm(forms.ModelForm):
    class Meta:
        model = FinancialConcern
        fields = ['name', 'price', 'banner']
        labels = {
            'name': '',
            'price': '',
            'banner': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'banner': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ['name', 'description', 'icon']
        labels = {
            'name': '',
            'description': '',
            'icon': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'icon': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


class PanelForm(forms.ModelForm):
    class Meta:
        model = Panel
        fields = ['name', 'description', 'image']
        labels = {
            'name': '',
            'description': '',
            'image': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


class WorksForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WorksForm, self).__init__(*args, **kwargs)
        self.fields['question'].label = ''
        self.fields['answer'].label = ''

    class Meta:
        model = Works
        fields = ['question', 'answer']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter question'}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter answer', 'rows': 4}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': ''
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
        }


class BlogForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        # Update widget attributes
        self.fields['category'].widget.attrs.update({
            'placeholder': 'Select category'
        })
        self.fields['name'].widget.attrs['placeholder'] = 'Enter blog Title'
        self.fields['banner'].widget.attrs['placeholder'] = 'Upload banner'

    description = forms.CharField(
        required=False,
        widget=CKEditorWidget(attrs={'id': 'id_description'})
    )

    class Meta:
        model = Blog
        fields = ['category', 'name', 'banner', 'description']
        labels = {
            'category': '',
            'name': '',
            'banner': '',
            'description': ''
        }
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'banner': forms.FileInput(attrs={'class': 'form-control'}),
        }
