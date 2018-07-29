"""Todo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .authentic import views as signup_views
from .todo import views as todo_views
from .search import views as search_views

from rest_framework import routers, serializers, viewsets
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', todo_views.todoList, name='home'),
    path('login/', auth_views.login, {'template_name': 'authentication/login.html'}, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/login/'}, name='logout'),
    path('signup/', signup_views.signup, name='signup'),
    path('captcha/', include('captcha.urls')),
    path('setting/', include('Todo.authentic.urls')),
    path('add/', todo_views.todoAdd, name='todoAdd'),
    path('del/', todo_views.todoDelete, name='todoDel'),
    path('<int:id>/do/', todo_views.todoFinish, name='todoFinish'),
    path('<int:id>/undo/', todo_views.todoUnfinish, name='todoUnfinish'),
    path('<int:id>/update/', todo_views.todoUpdate, name='todoUpdate'),
    path('edit/', todo_views.todoTask, name='todoTask'),
    path('search/', search_views.search, name='search'),
    path('oauth-github/', signup_views.GithubOauthView.as_view(), name='oauth_github'),
    # path('api/', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls')),
    path('api/todolist/', todo_views.ApiTodoList.as_view()),
    path('api/Todo/<int:id>/', todo_views.ApiTodoDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += staticfiles_urlpatterns()
