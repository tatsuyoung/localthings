from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class UserCreationForms(UserCreationForm):
    email = forms.EmailField(required=True, label='Email',
                             help_text='Passwordを忘れた際に必要になります。\n'
                                       'その他に使用する事はありません。')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model  = Profile
        fields = ['image', 'bio', 'website', 'bg']


class ContactForm(forms.Form):
    contact_name = forms.CharField(max_length=20, required=True)
    contact_email = forms.EmailField(max_length=40, required=True)
    message = forms.CharField(widget=forms.Textarea,
                              max_length=200,
                              required=True)