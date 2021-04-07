from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name = 'home'),
    path('profile/',views.profile,name = 'profile'),
    path('project/',views.project,name = 'project'),
    path('add_project/',views.add_project,name = 'add_project'),
    path('rate_project/(?P<image_id>\d+)',views.rate_project,name = 'rate_project'),
    path('search_project/(?P<image_id>\d+)',views.search_project,name = 'search_project'),
]