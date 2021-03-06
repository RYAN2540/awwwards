from django.urls import path, re_path
from . import views

urlpatterns=[
    path('',views.home,name = 'home'),
    re_path(r'^email/$',views.email,name = 'email'),
    re_path(r'^create_profile/$',views.create_profile,name = 'create_profile'),
    re_path(r'^profile/(?P<profile_id>\d+)',views.profile,name = 'profile'),
    re_path(r'^project/(?P<project_id>\d+)',views.project,name = 'project'),
    re_path(r'^add_project/$',views.add_project,name = 'add_project'),
    re_path(r'^rate_project/(?P<project_id>\d+)',views.rate_project,name = 'rate_project'),
    re_path(r'^search_project/$',views.search_project,name = 'search_project'),
    re_path(r'^api/projects/$', views.ProjectList.as_view()),
    re_path(r'^api/profiles/$', views.ProfileList.as_view()),
]