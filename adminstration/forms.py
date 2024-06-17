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
        fields = ['name', 'title', 'description', 'image']
        labels = {
            'name': '',
            'title': '',
            'description': '',
            'image': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'title': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Title'}),
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


class AssignHandlerForm(forms.ModelForm):
    class Meta:
        model = Consult
        fields = ['handler']

    def __init__(self, *args, **kwargs):
        super(AssignHandlerForm, self).__init__(*args, **kwargs)
        self.fields['handler'].queryset = CustomUser.objects.filter(
            access_level=2)
        self.fields['handler'].required = True
        self.fields['handler'].empty_label = "Select a handler"
        self.fields['handler'].widget.attrs.update({'class': 'form-control'})


class ConsultantPercentageForm(forms.ModelForm):
    class Meta:
        model = ConsultantPercentage
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter percentage',
            }),
        }
        labels = {
            'amount': '',
        }


class AdminResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['accepted', 'admin_response']
        labels = {
            'accepted': '',
            'admin_response': ''
        }
        widgets = {
            'accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'admin_response': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Admin Response'}),
        }


class HeroForm(forms.ModelForm):
    class Meta:
        model = Hero
        fields = ['title', 'description', 'image']
        labels = {
            'title': '',
            'description': '',
            'image': ''
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }


class RiskForm(forms.ModelForm):
    class Meta:
        model = Risk
        fields = ['name', 'description', 'icon']
        labels = {
            'name': '',
            'description': '',
            'icon': ''
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name of the Risk', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Risk Description', 'class': 'form-control'}),
            'icon': forms.FileInput(attrs={'class': 'form-control'})
        }


class Section1Form(forms.ModelForm):
    class Meta:
        model = Section1
        fields = ['name', 'tag1', 'tag2']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter name'
            }),
            'tag1': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tag1'
            }),
            'tag2': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tag2'
            }),
        }
        labels = {
            'name': '',
            'tag1': '',
            'tag2': '',
        }


class Section2Form(forms.ModelForm):
    class Meta:
        model = Section2
        fields = ['name', 'tag1', 'tag2']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter name'
            }),
            'tag1': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tag1'
            }),
            'tag2': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tag2'
            }),
        }
        labels = {
            'name': '',
            'tag1': '',
            'tag2': '',
        }


class HowForm(forms.ModelForm):
    class Meta:
        model = How
        fields = ['name', 'description']
        labels = {
            'name': '',
            'description': ''
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter section name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }


class SpesaForm(forms.ModelForm):
    class Meta:
        model = Risk
        fields = ['description']
        labels = {
            'description': 'How spesa analyzes, interprets, and advises',
        }
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Risk Analysis', 'class': 'form-control'}),

        }


class AdForm(forms.ModelForm):
    class Meta:
        model = Risk
        fields = ['description']
        labels = {
            'description': 'Need advice ?',
        }
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Invest with us text', 'class': 'form-control'}),

        }
