from django.shortcuts import render, redirect
from .forms import ParticipantForm
from .models import *

def home(request):
    return render(request, 'home.html')

from .forms import ParticipantForm

def registration(request):
    form = ParticipantForm()

    if request.method == 'POST':
        form = ParticipantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect or perform any other actions after successful form submission

    return render(request, 'registration.html', {'form': form})

def participants(request):
    participants = Participant.objects.all()
    context = {'participants': participants}
    return render(request, 'participants.html', context)
