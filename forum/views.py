from django.http import HttpResponseRedirect, Http404
from django.views import generic
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
from .models import Forumpost, Forum, Comment
from django.views.generic.detail import DetailView
from .forms import Forumpostform, CommentForm
from classroom.models import Classroom
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ForumpostSerializer, CommentSerializer, ForumSerializer



def index(request, pk, pk2):
	forum = get_object_or_404(Forum, pk=pk2)
	classroom = get_object_or_404(Classroom, pk=pk)
	all_forumposts = Forumpost.objects.filter(classroom_id=pk, forum_id=pk2, posted_date__lte=timezone.now()).order_by('posted_date')
	if forum.classroom == classroom:
		return render(request, 'forum/index.html', {'all_forumposts': all_forumposts, 'pk':pk, 'pk2':pk2})
	else:
		raise Http404("Forum does not exist")

def detail(request, pk, pk2, pk3):
	detailpost = get_object_or_404(Forumpost, classroom_id=pk, forum_id=pk2, id=pk3)
	context = {
	'detailpost':detailpost,
	'comments':detailpost.comments.all().order_by('-created_date'),
	'pk':pk,
	'pk2':pk2,
	'pk3':pk3
	}
	return render(request, 'forum/detail.html', context)

def createforumpost(request, pk, pk2):
	form = Forumpostform(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.writer = request.user
		instance.forum = get_object_or_404(Forum, pk=pk2)
		instance.classroom = get_object_or_404(Classroom, pk=pk)
		instance.save()
		return redirect('classroom:forum:detail', pk=instance.classroom.pk, pk2=instance.forum.pk, pk3=instance.pk)
	context = {
	'form':form
	}
	return render(request, 'forum/createforumpost.html', context)


def createcomment(request, pk, pk2, pk3):
	post = get_object_or_404(Forumpost, pk=pk3)
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.writer = request.user
			comment.classroom = get_object_or_404(Classroom, pk=pk)
			comment.forum = get_object_or_404(Forum, pk=pk2)
			comment.save()
			return redirect('classroom:forum:detail', pk=comment.classroom.pk, pk2=comment.forum.pk, pk3=comment.post.pk)
	else:
		form = CommentForm()
	return render(request, 'forum/createcomment.html', {'form': form})



class ForumpostList(APIView):

	def get(self, request, pk, pk2):
		posts = Forumpost.objects.all()
		serializer = ForumpostSerializer(posts, many=True)
		return Response(serializer.data)

	def post(self, request, pk):
		serializer = ForumpostSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentList(APIView):

	def get(self, request, pk):
		comments = Comment.objects.all()
		serializer = CommentSerializer(comments, many=True)
		return Response(serializer.data)

	def post(self, request, pk):
		serializer = CommentSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForumList(APIView):

	def get(self, request, pk):
		forums = Forum.objects.all()
		serializer = ForumSerializer(forums, many=True)
		return Response(serializer.data)

	def post(self, request, pk):
		serializer = ForumpostSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_posts(request, pk, pk2, pk3):
	post = Forumpost.objects.filter(classroom_id=pk, forum_id=pk2, id=pk3)
	response_data ={}
	try:
		response_data['result'] = 'Success'
		response_data['message'] = post.title
	except:
		response_data['result'] = 'Not found!'
		response_data['message'] = 'Failed!'
	return HttpResponse(json.dumps(response_data), content_type="application/json")


