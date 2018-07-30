from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.models import Todo, Task, User
from django.utils.timezone import now, timedelta
from web.forms import ProfileForm, SignUpForm


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
    return render(request, 'web/todo.html', {'todoList_Today': todoList_Today, 'doList_Today': doList_Today,
                                             'todoList': todoList, 'doList': doList, 'task': task})


def todoAdd(request):
    user = request.user
    if request.method == 'POST':
        todo = request.POST.get('todo')
        Todo.objects.create(author=user, content=todo)

    return redirect('/')


def todoUpdate(request, id):
    todo = Todo.objects.get(pk=id)
    if request.method == 'POST':
        content = request.POST.get('todo')
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
    todo_id = request.GET.get('todo-id')
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
    return render(request, 'web/task.html', {'task': task_pre, 'todoList': todoList})


def search(request):
    search = request.POST.get('value')
    if search:
        results = Todo.objects.filter(content__contains=search).all()
        return render(request, 'web/search.html', {'results': results})
    return redirect('/')


def signup(request):
    if request.method != 'POST':
        return render(request, 'web/signup.html', {'form': SignUpForm()})

    form = SignUpForm(request.POST)

    if not form.is_valid():
        return render(request, 'web/signup.html', {'form': form})

    username = form.cleaned_data.get('username')
    email = form.cleaned_data.get('email')
    password = form.cleaned_data.get('password')

    User.objects.create_user(username=username, password=password, email=email)

    user = authenticate(username=username, password=password)
    login(request, user)

    return redirect('/')


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

    return render(request, 'web/setting.html', {'form': form})
