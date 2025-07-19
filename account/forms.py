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

class ChangePassForm(forms.Form):
    old_pass = forms.CharField(label='eski parol', widget=forms.PasswordInput)
    new_pass = forms.CharField(label='new parol', widget=forms.PasswordInput)
    confirm_pass = forms.CharField(label='parolni tasdiqlang', widget=forms.PasswordInput)
    code = forms.CharField(label='emailga yuborilgan kod', max_length=6)

    def clean(self):
        cleaned_data = super().clean()
        new_pass = self.cleaned_data['new_pass']
        confirm_pass = self.cleaned_data['confirm_pass']
        if new_pass!=confirm_pass:
            raise forms.ValidationError('parollar mos emas')
        return cleaned_data


class ResetPassForm(forms.ModelForm):
    password = forms.CharField(label='yangi parol',  widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='parolni tasdiqlang',  widget=forms.PasswordInput)
    code = forms.CharField(label='tasdiqlash kodini kiriting',  max_length=6)

    def clean(self):
        cleaned_data = super().clean()
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']
        if password!=password_confirm:
            raise forms.ValidationError('parollar mos emas')
        return cleaned_data















