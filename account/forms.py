from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='parol', widget=forms.PasswordInput)
    password2= forms.CharField(label='parol', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 is None or password2 is None or password1!=password2:
            raise forms.ValidationError('parollarni bir xil ekanligini tekshiring')
        return password2
    def save(self, commit=True):

        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=120, label='username')
    password = forms.CharField(label='parol', widget=forms.PasswordInput)



















