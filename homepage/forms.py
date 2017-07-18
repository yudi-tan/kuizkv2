from django.contrib.auth.models import User
from django import forms
from classroom.models import Classroom




class Createclassform(forms.ModelForm):
	class Meta:
		model = Classroom
		fields = [
		'school',
		'classname',
		'session',
		'classtime',
		'passcode',
		]

class Joinclassform(forms.ModelForm):
	class Meta:
		model = Classroom
		fields = [
		'school',
		'classname',
		'passcode',
		]