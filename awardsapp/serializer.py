from rest_framework import serializers
from .models import Project, Profile

class ProjectSerializer(serializers.ModelSerializer):
    class Meta :
        model = Project
        fields = ('name', 'description','screenshot', 'link', 'profile', 'post_date', 'average_design', 'average_content', 'average_score', 'average_usability')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'bio', 'profile_pic', 'email','location', 'link')