from rest_framework import serializers
from core.models import Todo, Task, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        models = User
        fields = '__all__'


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('author', 'content', 'create_date', 'is_do')
