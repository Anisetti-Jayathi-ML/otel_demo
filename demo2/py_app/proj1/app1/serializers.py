from rest_framework import serializers
from .models import ProjectModel,AppModel

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectModel
        fields = '__all__'

class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppModel
        fields = '__all__'
