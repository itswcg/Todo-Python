from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.todoList, name='home'),
    path('login/', auth_views.login, {'template_name': 'web/login.html'}, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/login/'}, name='logout'),
    path('signup', views.signup, name='signup'),
    path('add/', views.todoAdd, name='todoAdd'),
    path('del/', views.todoDelete, name='todoDel'),
    path('<int:id>/do/', views.todoFinish, name='todoFinish'),
    path('<int:id>/undo/', views.todoUnfinish, name='todoUnfinish'),
    path('<int:id>/update/', views.todoUpdate, name='todoUpdate'),
    path('edit/', views.todoTask, name='todoTask'),
    path('search/', views.search, name='search'),
    path('setting', views.setting, name='setting'),
    path('captcha', include('captcha.urls')),
]
