from core.models import Todo
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TodoSerializer


class ApiTodoList(APIView):
    def get(self, request, format=None):
        todoList = Todo.objects.all()
        serializer = TodoSerializer(todoList, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiTodoDetail(APIView):
    def get_object(self, id):
        try:
            return Todo.objects.get(pk=id)
        except Todo.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        todo = self.get_object(id)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        todo = self.get_object(request.id)
        serialzer = TodoSerializer(todo, data=request.data)
        if serialzer.is_valid():
            serialzer.save()
            return Response(serialzer.data, status=status.HTTP_201_CREATED)
        return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        todo = self.get_object(id)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
