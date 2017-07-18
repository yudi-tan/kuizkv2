
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings
from classroom.models import Classroom
from django.db.models import signals


class Forumpost(models.Model):
	writer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
	forum = models.ForeignKey('forum.Forum', related_name='forumpost', blank=True, null=True)
	title = models.CharField(max_length = 200)
	summary = models.TextField()
	text = models.TextField()
	posted_date = models.DateTimeField(default = timezone.now)
	classroom = models.ForeignKey('classroom.Classroom', related_name='classroom', blank=True, null=True)

	def get_absolute_url(self):
		return reverse('classroom:forum:detail', kwargs={'pk':self.pk})

	def __str__(self):
		return self.title

class Forum(models.Model):
	classroom = models.OneToOneField(Classroom, on_delete=models.CASCADE,
        primary_key=True)

	def get_absolute_url(self):
		return reverse('classroom:detail', kwargs={'pk':self.pk})

	def __str__(self):
		return self.classroom.classname + " forum"

def create_forum(sender, instance, created, **kwargs):
    """Create ModelB for every new ModelA."""
    if created:
        Forum.objects.get_or_create(classroom=instance)

signals.post_save.connect(create_forum, sender=Classroom, weak=False,
                          dispatch_uid='models.create_forum')

class Comment(models.Model):
    post = models.ForeignKey('forum.Forumpost', related_name='comments')
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    classroom = models.ForeignKey('classroom.Classroom', related_name='classroomcomments', blank=True, null=True)
    forum = models.ForeignKey('forum.Forum', related_name='forumpostcomments', blank=True, null=True)

    def get_absolute_url(self):
    	return reverse('forum:detail', kwargs={'pk':self.post.pk})

    def __str__(self):
        return self.text
