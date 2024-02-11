from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .models import Students
from .models import Sessions
from django import forms
from .forms import SessionForm
from datetime import datetime
now = datetime.now()

#Définir des fonctions

def student_list(request):
    students = Students.objects.all()
    return render(request, 'student_list.html', {'students':students})

def accueil(request):
    return render(request,'accueil.html', context=None)

def sessions(request):
    sessions = Sessions.objects.all()

    #current_date = now.strftime("%d/%m/%Y")
    #current_time = now.strftime("%H:%M:%S")
    #current_datetime = current_date + " " + current_time

    return render(request,'sessions.html', context={'sessions':sessions,})


def create_sessions(request: HttpRequest) -> HttpResponse:
    #last_session = Sessions.objects.latest('closing_time')
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            date: datetime.date = form.cleaned_data["date"]
            opening_hour: datetime.date = form.cleaned_data["opening_hour"]
            closing_hour: datetime.date = form.cleaned_data["closing_hour"]
            #date_output = date.strftime("%d/%m/%Y")
            #opening_hour_output = opening_hour.strftime("%H:%M")
            #closing_hour_output = closing_hour.strftime("%H:%M")
            form.save()
            #return redirect('sessions')
            #return HttpResponse(f"The submitted date is: {date} + {opening_hour} +{closing_hour} ")
    else:
        form = SessionForm()
    return render(request, 'sessions.html', {'form':form,})


def derniers_resultats(request):
    return render(request,'derniers_resultats.html', context=None)