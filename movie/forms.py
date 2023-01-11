from django import forms
from .models import Users,Profile
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm


passwordInputWidget = {'password':forms.PasswordInput()}

class SignUpForm(UserCreationForm):
    
    class Meta:
        model = Users
        fields = ('username','email')
        widgets = [passwordInputWidget]

        USERNAME_FIELD = 'username'

    def save(self, commit=True):
        user = super(SignUpForm,self).save(commit=False)
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Users
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']

class PasswordChangingForm(PasswordChangeForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    new_password2 = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    class Meta:
        model = Users
        fields = ['new_password1','new_password2']


# class LoginUserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username,password']
#         widgets = [passwordInputWidget]