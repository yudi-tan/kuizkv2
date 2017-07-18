

# Create your views here.
from django.http import HttpResponseRedirect, Http404
from django.views import generic
from classroom.models import Classroom
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate,login, logout
from django.views.generic import View 
from .forms import Createclassform, Joinclassform
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User, Group
from forum.models import Forum

def index(request):
	return render(request, 'homepage/index.html', {})

def login(request):
	return render(request, 'homepage/login.html')

@login_required(login_url='/login/')
def loggedin(request):
	all_owned_classes = Classroom.objects.all().filter(owner=request.user)
	user = request.user.username
	all_joined_classes = Classroom.objects.filter(students__icontains=user)
	return render(request, 'homepage/loggedin.html', {'ownedclasses':all_owned_classes, 'joinedclasses':all_joined_classes})


def createclassroom(request):
	form = Createclassform(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.owner = request.user
		instance.students = request.user.username
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
	'form':form
	}
	return render(request, 'homepage/createclassroom.html', context)


def joinclassroom(request):
	form = Joinclassform(request.POST or None, request.FILES or None)
	if form.is_valid():
		form = form.save(commit=False)
		school = form.school
		classname = form.classname
		pin = form.passcode
		requested_class = get_object_or_404(Classroom, school=school, classname=classname)
		if form.passcode == requested_class.passcode:
			students = requested_class.students
			students = students + " " + request.user.username
			requested_class.students = students
			requested_class.save()
			return redirect('homepage:loggedin') 
		else:
			raise Http404("Passcode Incorrect")
	context = {
	'form': form
	}
	return render(request, 'homepage/joinclassroom.html', context)











