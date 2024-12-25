from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Project

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username'] # Changed to username to avoid issues

class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True, default=serializers.CurrentUserDefault()) # Serialize username
    projects = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by','projects']

    def get_projects(self, obj):
         return ProjectSerializer(obj.projects.all(), many=True).data


class ProjectSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    client = serializers.CharField(source='client.client_name', read_only=True)
    created_by = serializers.CharField(source='created_by.username', read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client','users', 'created_at', 'created_by']
