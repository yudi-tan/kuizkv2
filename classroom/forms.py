from django.contrib.auth.models import User
from django import forms
from .models import Calendar, Anouncements



class Createassignmentform(forms.ModelForm):
	class Meta:
		model = Calendar
		fields = [
		'lecture',
		'reading',
		'homework',
		'uploads',
		]


class Createannouncementform(forms.ModelForm):
	class Meta:
		model = Anouncements
		fields = [
		'title',
		'content',
		]
