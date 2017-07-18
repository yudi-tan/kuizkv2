from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate,login, logout
from django.views.generic import View 
from .forms import UserForm, Userprofileform
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User, Group
from .models import Profile

@login_required
def index(request):
	return render(request, 'circle/index.html')

class register(View):
	form_class = UserForm
	template_name = 'circle/signup.html'


	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})



	def post(self, request):
		form = self.form_class(request.POST)


		if form.is_valid():


			user = form.save(commit=False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()

			user = authenticate(username=username, password=password)

			if user is not None:

				if user.is_active:
					login(request, user)
					return redirect('homepage:loggedin')
					
		return render(request, self.template_name, {'form': form})

# def updateprofile(request):
# 	return render(request, 'circle/updateprofile.html')

def updateprofile(request):
    if request.method == 'POST':
        form = Userprofileform(request.POST, instance=request.user)
        if form.is_valid():
            profile = Profile.objects.get(user=request.user)
            if profile.organization != request.POST['organization'] and request.POST['organization'] != "":
            	profile.organization = request.POST['organization']
            if profile.bio != request.POST['bio'] and request.POST['bio'] != "":
            	profile.bio = request.POST['bio']
            if profile.stack != request.POST['stack'] and request.POST['stack'] != "":
            	profile.stack = request.POST['stack']
            if profile.year_of_grad != request.POST['year_of_grad'] and request.POST['year_of_grad'] != "":
            	profile.year_of_grad = request.POST['year_of_grad']
            if profile.upload != request.POST['upload'] and request.POST['upload'] != "":
            	profile.upload = request.POST['upload']
            profile.save()
            return redirect('homepage:loggedin')
    else:
        form = Userprofileform()
        return render(request,'circle/updateprofile.html',
                          {'form': form})

def profile(request, pk):
	user = User.objects.get(pk=pk)
	context = {
	"profiles": Profile.objects.all(),
	"user": user,
	}
	return render(request, 'circle/profile.html', context)
