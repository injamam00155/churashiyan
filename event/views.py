
from django.shortcuts import render
from .models import Participant  # Import your Participant model
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.template.loader import get_template
from .models import Participant
from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Count
from .forms import ParticipantForm
from .models import *
from django.db.models import Max


def home(request):
    return render(request, 'home.html')


def registration(request):
    form = ParticipantForm()

    if request.method == 'POST':
        form = ParticipantForm(request.POST, request.FILES)
        if form.is_valid():
            participant = form.save(commit=False)

            # Get the maximum id_number from the Participant table
            max_id_number = Participant.objects.aggregate(Max('id_number'))['id_number__max']

            if max_id_number is None:
                max_id_number = 0

            # Generate the new id_number by incrementing the maximum value
            participant.id_number = max_id_number + 1

            participant.save()
            messages.success(request, 'Registration successful!')
            return redirect('participants')

    return render(request, 'registration.html', {'form': form})



# Custom decorator to check if the user is an admin
def is_user_admin(user):
    return user.is_authenticated and user.is_superuser

# Apply the custom decorator to the view function
@user_passes_test(is_user_admin)
def admin_verify_participants(request):
    participants = Participant.objects.all()
    return render(request, 'verify.html', {'participants': participants})


def participants(request):
    participants = Participant.objects.all()
    context = {'participants': participants}
    return render(request, 'participants.html', context)

def view_id_card(request, id_number):
    participant = get_object_or_404(Participant, id_number=id_number)

    template = get_template('id_card.html')

    context = {
        'participant': participant,
    }

    return render(request, 'id_card.html', context)


def get_id_card(request, id_number):
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
