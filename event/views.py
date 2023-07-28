import cloudinary
import reportlab
import cloudinary.api
import requests
import svglib.svglib as svglib


from reportlab.lib.pagesizes import letter,portrait, landscape, A4
from reportlab.lib.units import inch  # Import inch to set dimensions in points
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Path
from reportlab.pdfgen.canvas import Canvas
from PIL import Image
from io import BytesIO
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.http import HttpResponse
from reportlab.lib.utils import ImageReader
from django.db.models import Max
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Count
from django.db.models import Q
from .forms import ParticipantForm
from .models import Participant 
from .models import Participant
from .models import *


def home(request):
    return render(request, 'home.html')


def is_participant_unique(name_arg, spouse_name_arg, contact_number_arg, email_arg):
    # Check if any participant with the same name, spouse name, contact number, and email exists
    existing_participant = Participant.objects.filter(
        Q(name__iexact=name_arg) &
        Q(spouse_name__iexact=spouse_name_arg) &
        Q(contact_number__iexact=contact_number_arg) &
        Q(email__iexact=email_arg)
    ).first()

    return not existing_participant

def registration(request):
    form = ParticipantForm()

    if request.method == 'POST':
        form = ParticipantForm(request.POST, request.FILES)
        if form.is_valid():
            participant = form.save(commit=False)

            # Check if the participant information is unique
            if is_participant_unique(participant.name, participant.spouse_name, participant.contact_number, participant.email):
                # Get the maximum id_number from the Participant table
                max_id_number = Participant.objects.aggregate(Max('id_number'))['id_number__max']

                if max_id_number is None:
                    max_id_number = 1

                # Generate the new id_number by incrementing the maximum value
                participant.id_number = max_id_number + 1

                participant.save()
                messages.success(request, 'Registration successful!')
                return redirect('participants')
            else:
                # Display an error message if participant information is not unique
                messages.error(request, 'Participant with the same name, spouse name, contact number, and email already exists!')
                return redirect('registration')

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
    participants = Participant.objects.all().order_by('id_number')
    context = {'participants': participants}
    return render(request, 'participants.html', context)


def view_id_card(request, id_number):
    participant = get_object_or_404(Participant, id_number=id_number)
    school_length=len(str(participant.school_name))
    font_size=17
    font_top=272

    if school_length > 23:
        font_size -= (school_length - 23) // 7
        font_top -= ((school_length - 23) // 7)*0.1

    # print(school_length)
    # print(font_size)
    # print(font_top)

    template = 'id_template.html'

    id=participant.id_number
    if id:
        id = str(id).zfill(3)
    context = {
        'participant': participant,
        'id':id,
        'font_size':font_size,
        'font_top':font_top,
    }

    return render(request, template, context)






# PARTLY WORKING


def svg_to_pdf(svg_code,participant,id_type, page_size=letter):
    # Create a PDF buffer
    pdf_buffer = BytesIO()
    drawing = svglib.svg2rlg(BytesIO(svg_code.encode('utf-8')))
    pdf_canvas = Canvas(pdf_buffer, pagesize=(485.53,687 ))  # Set the page size
    

    if(id_type=='own'):
        image_url=participant.participant_image.url
    elif(id_type=='spouse'):
        # Render the SVG template with the spouse's data
        image_url=participant.spouse_image.url

    split_url = image_url.split("v1/")

    if len(split_url) > 1:
        image_id = split_url[1]
    else:
        print("Invalid URL format")


    # Download the image from the URL
    image_info = cloudinary.api.resource(image_id)

    # print(image_info)
    image_url = image_info['url']
    image_width = image_info['width']
    image_height = image_info['height']

    # Calculate the scaling factor to maintain the aspect ratio
    scaling_factor = min(220 / image_width, 220 / image_height)

    # Calculate the scaled width and height
    scaled_width = image_width * scaling_factor
    scaled_height = image_height * scaling_factor
    print(scaled_width,scaled_height)
    # Calculate the position to center the image on the canvas
    center_x = (485.53 - scaled_width) / 2
    center_y = (687 - scaled_height) / 2

    pdf_canvas.drawImage(image_url, center_x, center_y, width=scaled_width, height=scaled_height)

    reportlab.graphics.renderPDF.draw(drawing, pdf_canvas, 0, 0)
    

    pdf_canvas.drawImage('static/logo1.png', 32, 550, width=100, height=100, mask='auto')
    pdf_canvas.drawImage('static/logo2.png', 352, 550, width=100, height=100, mask='auto')



    pdf_canvas.save()

    # Return the PDF buffer
    return pdf_buffer.getvalue()


# ... (other imports and code)

def get_id_card(request, id_type, id_number):
    participant = get_object_or_404(Participant, id_number=id_number)
    school_length=len(str(participant.school_name))
    font_size=17
    font_top=272

    if school_length > 23:
        font_size -= (school_length - 23) // 7
        font_top -= ((school_length - 23) // 7)*0.1

    # print(school_length)
    # print(font_size)
    # print(font_top)

    template = 'id_template.html'

    id=participant.id_number
    if id:
        id = str(id).zfill(3)

    context = {
        'participant': participant,
        'id':id,
        'font_size':font_size,
        'font_top':font_top,

    }

    if(id_type=='own'):
        # Render the SVG template with the participant's data
        svg_code = render_to_string('id_participant.html', context)
    elif(id_type=='spouse'):
        # Render the SVG template with the spouse's data
        svg_code = render_to_string('id_spouse.html', context)

    # Convert SVG to PDF with the desired page size (e.g., letter)
    pdf_data = svg_to_pdf(svg_code,participant,id_type, page_size=letter)  # You can pass other page sizes as needed
    # pdf_data = svg_to_pdf_with_canvas(svg_code, page_size=letter)  # You can pass other page sizes as needed

    if pdf_data:
        # Create the HTTP response with PDF content
        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = f'filename="{id_number}_{id_type}_id_card.pdf"'
        return response
    else:
        return HttpResponse("PDF generation failed.")
