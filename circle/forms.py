from django.contrib.auth.models import User
from django import forms
from .models import Profile


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['first_name','last_name','email','username', 'password',]


class Userprofileform(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['organization', 'bio', 'stack', 'year_of_grad', 'upload',]