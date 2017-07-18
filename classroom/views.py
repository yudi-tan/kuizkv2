from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.views import generic
from .models import Classroom, Calendar, Anouncements
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate,login, logout
from django.views.generic import View 
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User, Group
from .forms import Createassignmentform, Createannouncementform
from forum.models import Forum
from django.contrib.auth.decorators import user_passes_test


# def index(request):
# 	return render(request, 'classroom/index.html', {})



@login_required

def detail(request, pk):
	instance = get_object_or_404(Classroom, pk=pk)
	students = instance.students.split()
	forum = Forum(classroom=instance)
	calendar = Calendar.objects.filter(classroom=instance)
	anouncements = Anouncements.objects.filter(classroom=instance)
	context = {
	'instance':instance,
	'calendar':calendar,
	'anouncements':anouncements,
	'forum':forum,
	}
	if request.user.username in students:
		return render(request, 'classroom/detail.html', context)
	else:
		raise Http404('You are not enrolled in this class.')

def createassignment(request, pk):
	form = Createassignmentform(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.classroom = get_object_or_404(Classroom, pk=pk)
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
	'form':form
	}
	return render(request, 'classroom/assignmentpostform.html', context)


def createannouncement(request, pk):
	form = Createannouncementform(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.classroom = get_object_or_404(Classroom, pk=pk)
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
	'form':form
	}
	return render(request, 'classroom/assignmentpostform.html', context)

def classmembers(request, pk):
	classroom = get_object_or_404(Classroom, pk=pk)
	members = classroom.students.split()
	owner = classroom.owner
	namelist = []
	names = []
	for member in members:
		name = User.objects.filter(username=member).first()
		if owner != name:
			names.append(name)
			fullname = name.first_name + " " + name.last_name
			namelist.append(fullname)
	xy = zip(namelist,names)
	context = {'namelist':namelist, 'owner':owner, 'names':names, 'xy':xy}
	return render(request, 'classroom/classmembers.html', context)



