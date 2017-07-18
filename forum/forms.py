from django.contrib.auth.models import User
from django import forms
from .models import Forumpost, Comment


class Forumpostform(forms.ModelForm):
	class Meta:
		model = Forumpost
		fields = [
		'title',
		'summary',
		'text',

		]
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)