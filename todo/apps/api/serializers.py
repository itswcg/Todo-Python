from rest_framework import serializers
from core.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'author', 'content', 'create_date', 'is_do')
