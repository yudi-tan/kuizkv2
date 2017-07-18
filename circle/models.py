from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import signals

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='relate_profile')
    organization = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    stack = models.TextField(null=True, blank=True)
    year_of_grad = models.CharField(max_length = 4, null=True, blank=True)
    upload = models.FileField(null=True, blank=True)
    

    def __str__(self):
    	return self.user.username


def create_profile(sender, instance, created, **kwargs):
    """Create ModelB for every new ModelA."""
    if created:
        Profile.objects.create(user=instance)

signals.post_save.connect(create_profile, sender=User, weak=False,
                          dispatch_uid='models.create_profile')

class Person(models.Model):
    name = models.CharField(max_length=100)
    relationships = models.ManyToManyField('self', through='Relationship',
                                           symmetrical=False,
                                           related_name='related_to')

    def add_relationship(self, person, status):
        relationship, created = Relationship.objects.get_or_create(
        from_person=self,
        to_person=person,
        status=status)
        return relationship

    def remove_relationship(self, person, status):
        Relationship.objects.filter(
        from_person=self,
        to_person=person,
        status=status).delete()
        return

    def get_relationships(self, status):
        return self.relationships.filter(
        to_people__status=status,
        to_people__from_person=self)

    def get_related_to(self, status):
        return self.related_to.filter(
        from_people__status=status,
        from_people__to_person=self)

    def get_following(self):
        return self.get_relationships(RELATIONSHIP_FOLLOWING)

    def get_followers(self):
        return self.get_related_to(RELATIONSHIP_FOLLOWING)

    def get_friends(self):
        return self.relationships.filter(
        to_people__status=RELATIONSHIP_FOLLOWING,
        to_people__from_person=self,
        from_people__status=RELATIONSHIP_FOLLOWING,
        from_people__to_person=self)
        
    def __unicode__(self):
        return self.name

RELATIONSHIP_FOLLOWING = 1
RELATIONSHIP_BLOCKED = 2
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_FOLLOWING, 'Following'),
    (RELATIONSHIP_BLOCKED, 'Blocked'),
)

class Relationship(models.Model):
    from_person = models.ForeignKey(Person, related_name='from_people')
    to_person = models.ForeignKey(Person, related_name='to_people')
    status = models.IntegerField(choices=RELATIONSHIP_STATUSES)














