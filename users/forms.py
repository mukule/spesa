from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import PasswordResetForm
from .models import *
from django.contrib.auth.forms import UserChangeForm
import pycountry

country_choices = [(country.alpha_2, country.name)
                   for country in pycountry.countries]


class ClientRegistrationForm(UserCreationForm):
    username = forms.CharField(
        label='',  # Empty label
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Username', 'class': 'form-control'})
    )

    first_name = forms.CharField(
        label='',  # Empty label
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'First Name', 'class': 'form-control'})
    )

    last_name = forms.CharField(
        label='',  # Empty label
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Last Name', 'class': 'form-control'})
    )

    email = forms.EmailField(
        label='',  # Empty label
        help_text='A valid email address, please.',
        required=True,
        widget=forms.EmailInput(
            attrs={'placeholder': 'Email', 'class': 'form-control'})
    )

    phone = forms.CharField(
        label='',  # Empty label
        max_length=15,
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Phone', 'class': 'form-control'})
    )

    region = forms.CharField(
        label='',  # Empty label
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'City, Province or Region', 'class': 'form-control'})
    )

    country = forms.ChoiceField(
        label='',  # Empty label
        choices=[('', 'Select Country')] + country_choices,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'placeholder': 'Date Started', 'type': 'date'}),
        label='', required=True
    )

    password1 = forms.CharField(
        label='',  # Empty label
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password', 'class': 'form-control'})
    )

    password2 = forms.CharField(
        label='',  # Empty label
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirm Password', 'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone',
                  'region', 'country', 'date_of_birth', 'password1', 'password2']


class ConsultantRegistrationForm(ClientRegistrationForm):
    certifications = forms.FileField(
        label='Certification',  # Empty label
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    isifa_number = forms.CharField(
        label='',  # Empty label
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'ISIFA Number', 'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2', 'access_level', 'certifications', 'isifa_number']

    def __init__(self, *args, **kwargs):
        super(ConsultantRegistrationForm, self).__init__(*args, **kwargs)

        # Remove date_of_birth field
        self.fields.pop('date_of_birth')


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
        label="")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label="")


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']


class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)


class UserUpdateForm(UserChangeForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, required=False)
    is_active = forms.BooleanField(required=False)
    access_level = forms.ChoiceField(
        choices=get_user_model().ACCESS_LEVEL_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'password',
                  'confirm_password', 'access_level', 'is_active']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
