
from django.http import HttpResponse
from django.template.loader import get_template
from .models import Participant
from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Count
from .forms import ParticipantForm
from .models import *


def home(request):
    return render(request, 'home.html')


def registration(request):
    form = ParticipantForm()

    if request.method == 'POST':
        form = ParticipantForm(request.POST, request.FILES)
        if form.is_valid():
            participant = form.save(commit=False)
            # Get the total number of rows in the Participant table
            total_rows = Participant.objects.aggregate(total=Count('id_number'))['total']
            participant.id_number = total_rows + 1
            participant.save()
            messages.success(request, 'Registration successful!')
            return redirect('participants')

    return render(request, 'registration.html', {'form': form})


def participants(request):
    participants = Participant.objects.all()
    context = {'participants': participants}
    return render(request, 'participants.html', context)

def view_id_card(request, id_number):
    participant = get_object_or_404(Participant, id_number=id_number)

    # Generate the ID card PDF using the participant data
    template = get_template('id_card.html')
    context = {
        'participant': participant,
    }
    rendered_template = template.render(context)

    # Generate the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="id_card_{participant.id_number}.pdf"'
    # Use a PDF generation library (e.g., ReportLab) to generate the PDF content here
    # Replace the following line with the actual code to generate the PDF content
    response.write(rendered_template)

    return response
