from rest_framework import serializers
from .models import Forumpost, Comment, Forum

class ForumpostSerializer(serializers.ModelSerializer):

	class Meta:
		model = Forumpost
		fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):

	class Meta:
		model = Comment
		fields = '__all__'


class ForumSerializer(serializers.ModelSerializer):

	class Meta:
		model = Forum
		fields = '__all__'