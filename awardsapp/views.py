import datetime as dt
import statistics
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import AddProjectForm, RateProjectForm, CreateProfileForm
from .email import send_signup_email
from django.contrib.auth.models import User
from .models import Profile, Project, Vote
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProjectSerializer,ProfileSerializer

def create_profile(request):
    current_user = request.user
    title = "Create Profile"
    if request.method == 'POST':
        form = CreateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
        return HttpResponseRedirect('/')

    else:
        form = CreateProfileForm()
    return render(request, 'user/create_profile.html', {"form": form, "title": title})

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
    highest_score = None
    if len(projects) >= 1:
        highest_score = projects_scores[0]
        votes = Vote.get_project_votes(highest_score.id)
        highest_votes = votes[:3]    

    return render(request, "home.html", {"date": date, "title": title, "projects": projects, "highest":highest_score, "votes": highest_votes})

@login_required(login_url='/accounts/login/')
def profile(request, profile_id):
    title = "aWWWards"
    try:
        user = User.objects.get(pk = profile_id)
        profile = Profile.objects.get(user = user)
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
    return render(request, "user/profile.html", {"profile": profile, "projects": projects, "count": projects_count, "votes": total_votes, "average": average, "title": title})

@login_required(login_url='/accounts/login/')
def project(request, project_id):
    form = RateProjectForm()
    project = Project.objects.get(pk=project_id)
    title = project.name.title()
    votes = Vote.get_project_votes(project.id)
    total_votes = votes.count()
    
    voters_list =[]
    average_list = []
    content_list = []
    design_list = []
    usability_list = []
    for vote in votes:
        voters_list.append(vote.voter.id)
        average_summation = vote.design + vote.content + vote.usability
        average = average_summation/3
        average_list.append(average)
        content_list.append(vote.content)
        design_list.append(vote.design)
        usability_list.append(vote.usability)
    voted = False
    if request.user.id-1 in voters_list or request.user.id == project.profile.id:
        voted = True
    else:
        voted = False
    print("IDS")
    print(request.user.id)
    print(voters_list[0])
    print(voters_list[1])
    print(project.profile.id)
    average_score = sum(average_list) / len(average_list)
    average_design = sum(design_list) / total_votes
    average_content = sum(content_list) / total_votes
    average_usability = sum(usability_list) / total_votes   

    project.average_score = average_score
    project.average_design = average_design
    project.average_content =average_content
    project.average_usability = average_usability
    project.save()  

    return render(request, 'project/project.html', {"title": title, "form": form, "project": project, "votes": votes, "voted": voted, "total_votes":total_votes})

@login_required(login_url='/accounts/login/')
def add_project(request):
    title = "Add a project"
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
    return render(request, 'project/add_project.html', {"form": form, "title":title})

@login_required(login_url='/accounts/login/')
def rate_project(request,project_id):
    if request.method == "POST":
        form = RateProjectForm(request.POST)
        project = Project.objects.get(pk = project_id)
        current_user = request.user
        try:
            user = User.objects.get(pk = current_user.id)
            profile = Profile.objects.get(user = user)
        except Profile.DoesNotExist:
            raise Http404()

            if form.is_valid():
                vote = form.save(commit= False)
                vote.voter = profile
                vote.project = project
                vote.save_vote()
                return HttpResponseRedirect(reverse('project', args =[int(project.id)]))
    else:
        form = RateProjectForm()
    return render(request, 'project/project.html', {"form": form})

@login_required(login_url='/accounts/login/')
def search_project(request):
    if "project" in request.GET and request.GET["project"]:
        searched_project = request.GET.get("project")
        title = "aWWWards | search"
        try:
            projects = Project.search_project(searched_project)
            count = projects.count()
            message =f"{searched_project}"
            if len(projects) == 1:
                project = projects[0]
                form = RateProjectForm()
                title = project.name.upper()
                votes = Vote.get_project_votes(project.id)
                voters = project.voters

                voters_list =[]
                for vote in votes:
                    voters_list.append(vote.voter.id)
                voted = True
                if request.user.id-1 in voters_list or request.user.id == project.profile.user.id:
                    voted = False
                else:
                    voted = True
                return render(request, 'project/project.html', {"form": form, "project": project, "voted": voted, "votes": votes, "title": title})
            return render(request, 'project/search.html', {"projects": projects,"message": message, "count":count, "title": title})
        except ObjectDoesNotExist:
            suggestions = Project.display_all_projects()
            message= f"Found NO projects titled {searched_project}"
            return render(request, 'project/search.html', {"suggestions":suggestions,"message": message, "title": title})
    else:
        message = "You haven't searched for any term"
        return render(request,'project/search.html', {"message": message, "title": title})

class ProjectList(APIView):
    def get(self,request,format = None):
        projects =  Project.objects.all()
        serializers = ProjectSerializer(projects, many=True)
        return Response(serializers.data)  

class ProfileList(APIView):
    def get(self,request,format = None):
        profiles =  Profile.objects.all()
        serializers = ProfileSerializer(profiles, many=True)
        return Response(serializers.data)