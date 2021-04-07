import datetime as dt
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import AddProjectForm, RateProjectForm, CreateProfileForm
from .email import send_signup_email
from .models import Profile, Project
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

def create_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = CreateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
        return HttpResponseRedirect('/')

    else:
        form = CreateProfileForm()
    return render(request, 'user/create_profile.html', {"form": form})

def email(request):
    current_user = request.user
    email = current_user.email
    name = current_user.username
    send_signup_email(name, email)
    return redirect(create_profile)

def home(request):
    title= "awwwards"
    date = dt.date.today()
    projects = Project.display_all_projects()
    projects_scores = projects.order_by('-average_score')
    highest_score = projects_scores[0]
    return render(request, "home.html", {"date": date, "title": title, "projects": projects, "highest":highest_score})

@login_required(login_url='/accounts/login/')
def profile(request, profile_id):
    title = "aWWWards"
    try:
        profile = Profile.objects.get(id =profile_id)
        title = profile.user.username
        projects = Project.get_user_projects(profile.id)
        projects_count = projects.count()
        votes= []
        for project in projects:
            votes.append(project.average_score)
        total_votes = sum(votes)
        average = 0
        if len(projects)> 1:
            average = total_votes / len(projects)
    except Profile.DoesNotExist:
        raise Http404()        
    return render(request, "user/profile.html", {"profile": profile, "projects": projects, "count": projects_count, "votes": total_votes, "average": average})

@login_required(login_url='/accounts/login/')
def project(request, project_id):
    form = RateProjectForm()
    project = Project.objects.get(pk=project_id)
    votes = project.voters.count()
    if votes > 1:
        average = project.average_score / votes
    else:
        average = 0
    voted = False
    if project.voters.filter(id=request.user.id).exists():
        voted = True 
    voters_list =[]
    voters = project.voters
    print(type(voters))
    return render(request, 'project/project.html', {"form": form, "project": project, "votes": votes, "average": average})

@login_required(login_url='/accounts/login/')
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

def rate_project(request,project_id):
    project = Project.objects.get(pk = project_id)
    if request.method == "POST":
        form = RateProjectForm(request.POST)
        if form.is_valid():
            design = form.cleaned_data['design']
            usability = form.cleaned_data['usability']
            content = form.cleaned_data['content']
            profile = Profile.objects.get(user = request.user)
            project.voters.add(profile)

            project.design_score = project.design_score + design
            project.usability_score = project.usability_score + usability
            project.content_score = project.content_score + content
            
            total_voters = project.voters_count()
            if total_voters > 0:
                project.average_design = project.design_score/project.voters_count()
                project.average_usability = project.usability_score/project.voters_count()
                project.average_content = project.content_score/project.voters_count()
            else:
                project.average_design = project.design_score
                project.average_usability = project.usability_score
                project.average_content = project.content_score

            project.average_score = (project.average_design + project.average_usability + project.average_content)/3

            project.save()
            return HttpResponseRedirect(reverse('project', args =[int(project.id)]))

    else:
        form = RateProjectForm()
    return render(request, 'project/project.html', {"form": form})

def search_project(request):
    if "project" in request.GET and request.GET["project"]:
        searched_project = request.GET.get("project")
        try:
            projects = Project.search_project(searched_project)
            message =f"{searched_project}"
            if len(projects) == 1:
                project = projects[0]
                form = RateProjectForm()
                return render(request, 'project/project.html', {"form": form, "project": project})
            return render(request, 'project/search.html', {"projects": projects,"message": message})
        except ObjectDoesNotExist:
            projects = Project.display_all_projects()
            if len(projects)> 1:
                suggestions = projects[:4]
                message= f"Found NO projects titled {searched_project}"
                return render(request, 'project/search.html', {"suggestions":suggestions,"message": message})
    else:
        message = "You haven't searched for any term"
        return render(request,'project/search.html', {"message": message})