import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import markdown2
from .models import User, Article, Project

# Create your views here.
def index(request):
    all_articles = Article.objects.all()
    all_articles = all_articles.order_by("-date")
    if all_articles.count() > 0:
        return render(request, "sdg/index.html", {
            "articles": all_articles
        })


    return render(request, "sdg/index.html", {
        "message": "no thing to see here"
    })

def add_article(request):
    user = request.user
    categories = [
        "No Poverty",
        "Zero Hunger", 
        "Good Health and Well-Being",
        "Quality Education",
        "Gender Equality",
        "Clean Water and Sanitation",
        "Affordable and Clean Energy",
        "Decent Work and Economic Growth",
        "Industry, Innovation and Infrastructure",
        "Reduced Inequalities",
        "Sustainable Cities and Communities",
        "Responsible Consumption and Production",
        "Climate Action", 
        "Life Below Water",
        "Life on Land",
        "Peace, Justice and Strong Institutions",
        "Partnerships for the Goals"
    ]
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        Author = request.POST["author"]
        Author = User.objects.get(username = Author)
        category = request.POST["category"]
        #content = markdown2.markdown(content)
        # I now need to first convert the markdown into html then save it.
        # I will have to use markdownII to do this
        article = Article(Author = Author, title = title, content=content, category=category)
        article.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "sdg/addarticle.html", {
            "user": user,
            "categories": categories
        })

def categories(request):
    categories = [
        "No Poverty",
        "Zero Hunger", 
        "Good Health and Well-Being",
        "Quality Education",
        "Gender Equality",
        "Clean Water and Sanitation",
        "Affordable and Clean Energy",
        "Decent Work and Economic Growth",
        "Industry, Innovation and Infrastructure",
        "Reduced Inequalities",
        "Sustainable Cities and Communities",
        "Responsible Consumption and Production",
        "Climate Action", 
        "Life Below Water",
        "Life on Land",
        "Peace, Justice and Strong Institutions",
        "Partnerships for the Goals"
    ]
    return render(request, "sdg/categories.html", {
        "categories": categories
    })

def category_view(request, category_name):
    try:
        articles = Article.objects.filter(category = category_name)
    except Article.DoesNotExist:
        return JsonResponse({"error": "Category not found"})
    articles = articles.order_by("-date").all()
    for article in articles:
        article.content = markdown2.markdown(article.content)
    return JsonResponse([article.serialize() for article in articles], safe=False)

def article_view(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
        article.content = markdown2.markdown(article.content)
    except Article.DoesNotExist:
        return JsonResponse({"error":"Article Not found"})
    return JsonResponse(article.serialize())


def add_project(request):
    user = request.user
    categories = [
        "No Poverty",
        "Zero Hunger", 
        "Good Health and Well-Being",
        "Quality Education",
        "Gender Equality",
        "Clean Water and Sanitation",
        "Affordable and Clean Energy",
        "Decent Work and Economic Growth",
        "Industry, Innovation and Infrastructure",
        "Reduced Inequalities",
        "Sustainable Cities and Communities",
        "Responsible Consumption and Production",
        "Climate Action", 
        "Life Below Water",
        "Life on Land",
        "Peace, Justice and Strong Institutions",
        "Partnerships for the Goals"
    ]
    if request.method == "POST":
        title = request.POST["title"]
        category = request.POST["category"]
        goals = request.POST["goals"]
        user = User.objects.get(username = user)
        project  = Project(title = title, category= category, Incompletegoals = goals,user = user)
        project.save()
        return HttpResponseRedirect(reverse("AddProject"))
    else:
        projects = Project.objects.filter(user = request.user)
        projects = projects.order_by('-date').all()
        all_projects = Project.objects.all()
        all_projects = all_projects.order_by('-date').all()
        for project in projects:
            project.Incompletegoals = project.Incompletegoals.split(',')
            filter_object1 = filter(lambda x: x !='', project.Incompletegoals)
            project.Incompletegoals = list(filter_object1)
            project.Completegoals = project.Completegoals.split(',')
            filter_object = filter(lambda x: x !='', project.Completegoals)
            project.Completegoals = list(filter_object)
        for project in all_projects:
            project.Incompletegoals = project.Incompletegoals.split(',')
            filter_object1 = filter(lambda x: x !='', project.Incompletegoals)
            project.Incompletegoals = list(filter_object1)
            project.Completegoals = project.Completegoals.split(',')
            filter_object = filter(lambda x: x !='', project.Completegoals)
            project.Completegoals = list(filter_object)
        return render(request, "sdg/addproject.html", {
            "categories": categories,
            "projects": projects,
            "allprojects": all_projects
        })
def mark_project(request):
    # put the code here that marks the project goals that have been completed
    if request.method == "POST":
        projectID = request.POST['id']
        projectID = int(projectID)
        project = Project.objects.get(pk=projectID)
        # a list of all the goals
        projectGoals = project.Incompletegoals.split(',')
        projectNum = len(projectGoals)
        str = ""
        # I need to loop through every one of the goals and such to get
        for i in range(projectNum):
            if request.POST.get(f'goal{i + 1}', False):
                completed_goal = request.POST[f'goal{i + 1}']
                projectGoals.remove(completed_goal)
                if i + 1 != projectNum:
                    str += completed_goal + ","
                else:
                    str += completed_goal
            else:
                1 + 1
        incomp_goals_str = "" 
        for i in range(len(projectGoals)):
            if i + 1 != len(projectGoals) and (len(projectGoals) > 0):
                incomp_goals_str += projectGoals[i] + ","
            else:
                incomp_goals_str += projectGoals[i]
        if incomp_goals_str.isspace():
            project.Incompletegoals = ''
        else:
            project.Incompletegoals = incomp_goals_str
            project.Completegoals = project.Completegoals + "," + str
        project.save()

        return HttpResponseRedirect(reverse('AddProject'))
    else:
        return HttpResponse('This url is only meant for post requests')

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "sdg/login.html", {
                "message": "Invalid username and/or password."
            }) 
    else:
        return render(request, "sdg/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "sdg/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "sdg/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "sdg/register.html")