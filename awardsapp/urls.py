from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name = 'home'),
    path('profile/',views.profile,name = 'profile'),
    path('project/',views.project,name = 'project'),
    path('add-project/',views.add_project,name = 'add_project'),
    path('rate-project/',views.rate_project,name = 'rate_project'),
]