from django.shortcuts import render
from .models import Member, Event

def home(request):
    # Retrieve general information for the home page
    # Render the home template with the information
    return render(request, 'home.html', {})

def contact(request):
    # Retrieve contact information
    # Render the contact template with the information
    return render(request, 'contact.html', {})

def member_list(request):
    # Retrieve all members from the database
    members = Member.objects.all()
    # Render the member list template with the members
    return render(request, 'member_list.html', {'members': members})

def event_list(request):
    # Retrieve all events from the database
    events = Event.objects.all()
    # Render the event list template with the events
    return render(request, 'event_list.html', {'events': events})
