from django import forms
from django.core import validators
from user.models import registrationmodel

def name_check(value):
    if value.isalpha() != True:
        raise forms.ValidationError("only string are allowed")

class registrationform(forms.ModelForm):
    loginid = forms.CharField(widget=forms.TextInput(), required=True, max_length=100, validators=[name_check])
    password = forms.CharField(widget=forms.PasswordInput(), required=True, max_length=100)
    email = forms.EmailField(widget=forms.TextInput(), required=True)
    mobile = forms.CharField(widget=forms.TextInput(), required=True, max_length=100, validators=[validators.MaxLengthValidator(10), validators.MinLengthValidator(10)])
    place = forms.CharField(widget=forms.TextInput(), required=True, max_length=100)
    city = forms.CharField(widget=forms.TextInput(), required=True, max_length=100)
    authkey = forms.CharField(widget=forms.HiddenInput(), initial='waiting', max_length=100)
    status = forms.CharField(widget=forms.HiddenInput(), initial='waiting', max_length=100)

    class Meta:
        model = registrationmodel
        fields = ['loginid', 'password', 'email', 'mobile', 'place', 'city', 'authkey', 'status']
