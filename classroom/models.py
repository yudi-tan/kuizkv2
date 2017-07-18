from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator



class Classroom(models.Model):
	owner = models.ForeignKey(settings.AUTH_USER_MODEL)
	school = models.TextField()
	classname = models.TextField()
	session = models.TextField(null = True)
	classtime = models.TextField(null = True)
	passcode = models.IntegerField(validators=[MinValueValidator(100000), MaxValueValidator(999999)])
	created_date = models.DateTimeField(default = timezone.now)
	students = models.TextField(blank=True, null=True)


	def get_absolute_url(self):
		return reverse('classroom:detail', kwargs={'pk':self.pk})

	def __str__(self):
		return self.school + "---" + self.classname

	class Meta:
		permissions = (("can_enter_classroom", "Can enter classroom"),)



class Calendar(models.Model):
	classroom = models.ForeignKey('classroom.Classroom', related_name='calendar')
	date = models.DateField(default=timezone.now)
	lecture = models.TextField()
	reading = models.TextField(null = True)
	homework = models.TextField(null= True)
	uploads = models.FileField(upload_to='uploads/%Y/%m/%d/', null= True)

	def get_absolute_url(self):
		return reverse('classroom:detail', kwargs={'pk':self.classroom.pk})

	def __str__(self):
		return self.lecture

class Anouncements(models.Model):
	date = models.DateField(default=timezone.now)
	title = models.TextField()
	content = models.TextField(null=True)
	classroom = models.ForeignKey('classroom.Classroom', related_name='anouncements', blank=True, null=True)

	def get_absolute_url(self):
		return reverse('classroom:detail', kwargs={'pk':self.classroom.pk})

	def __str__(self):
		return self.title 
