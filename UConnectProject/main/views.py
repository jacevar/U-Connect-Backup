from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse
from main.models import Route
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from django.contrib import messages
from .models import *

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView

import folium
import json
import random
import datetime
from .forms import routesForms
from . import getroute

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def unsafe(request):
    return render(request, 'Unsafe.html')

def login(request):
    return render(request,'login.html')

def chat(request,id,username):
    context = {
        'id':id,
        'username':username
    }
    return render(request, 'chat.html',context=context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created succesfully')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request,'register.html', {'form':form})


def profile(request):
    return render(request, 'profile.html')

def myRoutes(request):
    routes = Route.objects.filter()
    myroutes = []
    lastroutes = []
    currRoutes = []
    waitingRoutes = []
    for i in routes:
        r = json.loads(i.participants)
        if (i.startdate < datetime.date.today()):
            lastroutes.append(i.data())
        elif (i.Owner == request.user.username):
            if (i.data()[5]):
                myroutes.append(i.data())
            else:
                lastroutes.append(i.data())
        elif (request.user.username in r["waiting"]):
            waitingRoutes.append(i.data())
        elif (request.user.username in r["accepted"]):
            currRoutes.append(i.data())
    context = {
        'myRoutes': myroutes,
        'currRoutes': currRoutes,
        'waitingRoutes': waitingRoutes,
        'lastRoutes': lastroutes
    }
    return render(request, 'myRoutes.html',context=context)

def myRoute(request,id):
    if (request.method == 'GET'):
        route = Route.objects.get(id = id)
        time =  ("%02d:%02d" % (route.startTime.hour,route.startTime.minute)) 
        f = routesForms({'route':route.route,
                        'description':route.description,
                        'petfriendly':route.petfriendly,
                        'startdate':route.startdate,
                        'startTime':time}
                        )
        figure = getroute.getRouteFigure(json.loads(route.route))
        context = {
            'form':f,
            'id':route.id,
            'map':figure,
        }
        return render(request, 'myRoute.html',context=context)
    

def deleteRoute(request,id):
    route = Route.objects.get(id = id)
    route.delete()
    return redirect('myRoutes')

def infoRoute(request,id):
    route = Route.objects.filter(id = id)
    context = {}
    if (request.method == 'GET'):
        figure = getroute.getRouteFigure(json.loads(route[0].route))
        context["map"] = figure
        context["startdate"] = route[0].startdate
        context["startTime"] = route[0].startTime
        context["description"] = route[0].description
        context["petfriendly"] = route[0].petfriendly
        return render(request, 'infoRoute.html',context=context)
    elif (request.method == 'POST'):
        users = json.loads(route[0].participants)
        users["waiting"] = [user for user in users["waiting"] if user!=request.user.username]
        users["accepted"] = [user for user in users["accepted"] if user!=request.user.username]
        route.update(participants = json.dumps(users))
        return redirect('../')
    

def participants(request,id):
    route = Route.objects.filter(id = id)
    users = json.loads(route[0].participants)
    context = {}
    pList = []
    if (request.method == 'POST'):
        if ("deny" in request.POST):
            users["waiting"] = [user for user in users["waiting"] if user!=request.POST["deny"]]
            route.update(participants = json.dumps(users))
        elif ("accept" in request.POST):
            users["waiting"] = [user for user in users["waiting"] if user!=request.POST["accept"]]
            users["accepted"].append(request.POST["accept"])
            route.update(participants = json.dumps(users))
        elif ("delete" in request.POST):
            users["accepted"] = [user for user in users["accepted"] if user!=request.POST["delete"]]
            route.update(participants = json.dumps(users))
    
    for participant in users["waiting"]:
        p = get_object_or_404(User,username=participant)
        stars = random.randint(0,5)
        pList.append([participant,p.first_name,p.last_name,("★"*stars)+("☆"*(5-stars))])
    context["waiting"] = pList

    pList = []
    for participant in users["accepted"]:
        p = get_object_or_404(User,username=participant)
        stars = random.randint(0,5)
        pList.append([participant,p.first_name,p.last_name,("★"*stars)+("☆"*(5-stars))])
    context["accepted"] = pList
    print(context)
    return render(request, 'participants.html',context=context)

def reviews(request,id):
    route = Route.objects.filter(id = id)
    users = json.loads(route[0].participants)
    context = {}
    pList = []
    for participant in users["accepted"]:
        p = get_object_or_404(User,username=participant)
        pList.append([participant,p.first_name,p.last_name])
    context["Participants"] = pList
    return render(request, 'reviews.html',context=context)

def showmap(request):
    return render(request,'showmap.html')

def updateRoute(request,id):    
    if request.method == 'POST':
        route = Route.objects.filter(id = id)
        route.update(Owner=request.user.username,
                            route=request.POST["route"].replace('\\\"',"\""),
                            startdate=request.POST["startdate"],
                            startTime=request.POST["startTime"],
                            description=request.POST["description"],
                            petfriendly = True if ("petfriendly" in request.POST) else False)
        
    return redirect('../../myRoutes')

def createRoute(request):
    if request.method == 'POST':
        print(type(json.loads(request.POST["route"])))
        color = "#%06x" % random.randint(0, 0xFFFFFF)
        Route.objects.create(Owner=request.user.username,
                            route=request.POST["route"],
                            startdate=request.POST["startdate"],
                            startTime=request.POST["startTime"],
                            description=request.POST["description"],
                            petfriendly = True if ("petfriendly" in request.POST) else False,
                            color = color)
        
    return redirect('../myRoutes')

def showroute(request,lat1,long1,lat2,long2):
    #figure = folium.Figure()
    lat1,long1,lat2,long2=float(lat1),float(long1),float(lat2),float(long2)

    route=getroute.get_route(long1,lat1,long2,lat2)

    figure = getroute.getRouteFigure(route=route)
    f = routesForms({'route':json.dumps(route)})
    context={
        'map':figure,
        'form':f}
  
    return render(request,'showroute.html',context)

def joinRoute(request,id):
    route = Route.objects.filter(id = id)
    users = json.loads(route[0].participants)
    users["waiting"].append(request.user.username)
    route.update(participants = json.dumps(users))
    return redirect('../myRoutes')

def generatePopPup(route):
    p = get_object_or_404(User,username=route.Owner)
    stars = random.randint(0,5)
    iframe = ("Name: "+p.first_name+" "+p.last_name
           +"<br> Reputation: "+("★"*stars)+("☆"*(5-stars))
           +"<br> StartDate: "+str(route.startdate)
           +"<br> StartTime: "+str(route.startTime)
           +"<br> PetFriendly: "+str(route.petfriendly)
           +"<br> Description: "+route.description
           +"<br> <a href=\"./joinRoute/"+str(route.id)+"\">Join</a>")
    popup = folium.Popup(iframe, min_width=200,max_width=200)
    return popup

def showRoutes(request):
    routes = Route.objects.all()
    figure = folium.Figure()
    m = folium.Map(location=[6.1997147,-75.5814568], zoom_start=15)

    aux = 0
    for i in routes:
        r = i.data()

        route = json.loads(r[0])
        
        folium.PolyLine(route['route'],weight=8,color=i.color,opacity=1,popup=generatePopPup(i)).add_to(m)
        folium.Marker(location=route['start_point'],icon=folium.Icon(color='green')).add_to(m)
        folium.Marker(location=route['end_point'],icon=folium.Icon(color='red')).add_to(m)
        aux += 1
    m.add_to(figure)
    m._id = "map"
    figure.render()
    #print(figure.html.render())
    #print(figure.script.render())
    #print("=================================")
    #print(figure.header.render())
    context={'map':figure}
    return render(request,'showAllRoutes.html',context)

