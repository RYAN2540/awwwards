from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name = 'home'),
    path('profile/',views.profile,name = 'profile'),
    path('project/',views.project,name = 'project'),
]