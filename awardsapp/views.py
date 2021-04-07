import datetime as dt
from django.shortcuts import render
from .forms import AddProjectForm, RateProjectForm

def home(request):
    date = dt.date.today()
    return render(request, "user/profile.html", {"date": date})

def profile(request):
    return render(request, "user/profile.html")

def project(request):
    form = RateProjectForm()
    return render(request, 'project/project.html', {"form": form})

def add_project(request):
    if request.method == "POST":
        form = AddProjectForm(request.POST, request.FILES)
        current_user = request.user
        try:
            profile = Profile.objects.get(user = current_user)
        except Profile.DoesNotExist:
            raise Http404()
        if form.is_valid():
            project = form.save(commit= False)
            project.profile = profile
            project.save()

        return redirect("home")
    else:
        form = AddProjectForm()
    return render(request, 'project/add_project.html', {"form": form})

def rate_project(request,id):
    project = Project.objects.get(pk = id)
    if request.method == "POST":
        form = RateProjectForm(request.POST)
        if form.is_valid():
            design = form.cleaned_data['design']
            usability = form.cleaned_data['usability']
            content = form.cleaned_data['content']

            project.design_score = project.design_score + design
            project.usability_score = project.usability_score + usability
            project.content_score = project.content_score + content

            project.average_design = project.design_score/project.voters_count()
            project.average_usability = project.usability_score/project.voters_count()
            project.average_content = project.content_score/project.voters_count()

            project.average_score = (project.average_design + project.average_usability + project.average_content)/3

            project.save()
            return HttpResponseRedirect(reverse('project'))

    else:
        form = RateProjectForm()
    return render(request, 'project/project.html', {"form": form})