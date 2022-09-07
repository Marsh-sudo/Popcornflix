from dataclasses import fields
from pyexpat import model
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class PasswordChangingForm(PasswordChangeForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    new_password2 = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    class Meta:
        model = User
        fields = ['new_password1','new_password2']

		  

class LoginUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1']