import datetime as dt
from django.shortcuts import render

def home(request):
    date = dt.date.today()
    return render(request, "user/profile.html", {"date": date})