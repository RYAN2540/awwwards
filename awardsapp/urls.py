from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name = 'home'),
    path('email/',views.email,name = 'email'),
    path('create_profile/',views.create_profile,name = 'create_profile'),
    path('profile/',views.profile,name = 'profile'),
    path('project/(?P<project_id>\d+)',views.project,name = 'project'),
    path('add_project/',views.add_project,name = 'add_project'),
    path('rate_project/(?P<project_id>\d+)',views.rate_project,name = 'rate_project'),
    path('search_project/',views.search_project,name = 'search_project'),
]