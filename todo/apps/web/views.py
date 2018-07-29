from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Todo, Task
from django.utils.timezone import now, timedelta

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TodoSerializer


@login_required
def todoList(request):
    user = request.user
    task = Task.objects.filter(author=user).last()
    today = now().date() + timedelta(days=0)
    todoList_Today = Todo.objects.filter(author=user, is_do=False, create_date__gte=today).order_by('create_date')
    doList_Today = Todo.objects.filter(author=user, is_do=True, create_date__gte=today).order_by('create_date')
    todoList = Todo.objects.filter(author=user, is_do=False, create_date__lt=today).all()
    doList_page = Todo.objects.filter(author=user, is_do=True, create_date__lt=today).all()

    paginator = Paginator(doList_page, 8)
    page = request.GET.get('page')
    try:
        doList = paginator.page(page)
    except PageNotAnInteger:
        doList = paginator.page(1)
    except EmptyPage:
        doList = paginator.page(paginator.num_pages)
    return render(request, 'Todo/Todo.html', {'todoList_Today': todoList_Today, 'doList_Today': doList_Today,
                                              'todoList': todoList, 'doList': doList, 'task': task})


def todoAdd(request):
    user = request.user
    if request.method == 'POST':
        todo = request.POST.get('Todo')
        Todo.objects.create(author=user, content=todo)

    return redirect('/')


def todoUpdate(request, id):
    todo = Todo.objects.get(pk=id)
    if request.method == 'POST':
        content = request.POST.get('Todo')
        todo.content = content
        todo.save()

    return redirect('/edit/')


def todoFinish(request, id):
    todo = Todo.objects.get(pk=id)
    todo.is_do = True
    todo.save()

    return redirect('/')


def todoUnfinish(request, id):
    todo = Todo.objects.get(pk=id)
    todo.is_do = False
    todo.save()

    return redirect('/')


def todoDelete(request):
    todo_id = request.GET.get('Todo-id')
    todo = Todo.objects.get(pk=todo_id)
    todo.delete()

    return HttpResponse()


def todoTask(request):
    user = request.user
    task_pre = Task.objects.filter(author=user).last()
    if request.method == 'POST':
        task = request.POST.get('task')
        Task.objects.create(author=user, content=task)
        return redirect('/')

    todoList_all = Todo.objects.filter(author=user).all()
    paginator = Paginator(todoList_all, 10)
    page = request.GET.get('page')
    try:
        todoList = paginator.page(page)
    except PageNotAnInteger:
        todoList = paginator.page(1)
    except EmptyPage:
        todoList = paginator.page(paginator.num_pages)
    return render(request, 'Todo/task.html', {'task': task_pre, 'todoList': todoList})


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


from django.shortcuts import render, redirect
from ..web.models import Todo


def search(request):
    search = request.POST.get('value')
    if search:
        results = Todo.objects.filter(content__contains=search).all()
        return render(request, 'search/search.html', {'results': results})
    return redirect('/')


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.generic.base import RedirectView
from urllib.request import urlopen, Request
from urllib.parse import quote_plus
import json

GITHUB_CLIENTID = settings.GITHUB_CLIENTID
GITHUB_CLIENTSECRET = settings.GITHUB_CLIENTSECRET
GITHUB_CALLBACK = settings.GITHUB_CALLBACK


def signup(request):
    if request.method != 'POST':
        return render(request, 'authentication/signup.html', {'form': SignUpForm()})

    form = SignUpForm(request.POST)

    if not form.is_valid():
        return render(request, 'authentication/signup.html', {'form': form})

    username = form.cleaned_data.get('username')
    email = form.cleaned_data.get('email')
    password = form.cleaned_data.get('password')

    User.objects.create_user(username=username, password=password, email=email)

    user = authenticate(username=username, password=password)
    login(request, user)

    return redirect('/')


#
@login_required
def setting(request):
    user = request.user
    username = user.username
    if request.method == 'POST':
        form = ProfileForm(request.POST)

        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()

            message = '修改成功'
            messages.add_message(request, messages.SUCCESS, message)

            new_user = authenticate(username=username, password=new_password)
            login(request, new_user)
    else:
        form = ProfileForm(instance=user)

    return render(request, 'authentication/setting.html', {'form': form})


class GithubOauthView(RedirectView):
    permanent = False
    url = None

    def get_access_token(self):
        code = self.request.GET.get('code')
        url = 'https://github.com/login/oauth/access_token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': GITHUB_CLIENTID,
            'client_secret': GITHUB_CLIENTSECRET,
            'code': code,
            'redirect_uri': GITHUB_CALLBACK,
        }
        data = quote_plus(data)
        req = Request(url, data, headers={'Accept': 'application/json'})
        response = urlopen(req)
        result = response.read()
        result = json.loads(result)
        return result

    def get_user_info(self, access_token):
        url = 'https://api.github.com/user?access_token=%s' % (access_token)
        response = urlopen(url)
        html = response.read()
        data = json.loads(html)
        username = data['login'] + '(github_oauth)'
        email = 'oauth@oauth.com'
        password = '********'
        try:
            user = User.objects.get(username=username)
        except:
            user = User.objects.create_user(username, email, password)
            user.save()
        user = authenticate(username=username, password=password)
        login(self.request, user)

    def get_redirect_url(self, *args, **kwargs):
        self.url = self.request.GET.get('state')
        try:
            access_token_info = self.get_access_token()
            access_token = access_token_info['access_token']
            self.get_user_info(access_token)
        except:
            pass
        return super(GithubOauthView, self).get_redirect_url(*args, **kwargs)
