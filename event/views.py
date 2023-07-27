
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
# import cairosvg
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
import cloudinary


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



import reportlab
from reportlab.graphics import renderPDF
import svglib.svglib as svglib
from io import BytesIO
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.pagesizes import portrait  # Import portrait for custom page size
from reportlab.lib.units import inch  # Import inch to set dimensions in points
from reportlab.lib.pagesizes import letter  # Import your desired page size
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.pagesizes import A4

from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas
from django.templatetags.static import static
from reportlab.graphics.shapes import Path





# PARTLY WORKING


def svg_to_pdf(svg_code,participant, page_size=letter):
    # Create a PDF buffer
    pdf_buffer = BytesIO()
    
    # Convert SVG to PDF using reportlab's svglib
    drawing = svglib.svg2rlg(BytesIO(svg_code.encode('utf-8')))
    pdf_canvas = Canvas(pdf_buffer, pagesize=(485.53, 687))  # Set the page size
    reportlab.graphics.renderPDF.draw(drawing, pdf_canvas, 0, 0)
    
    

    pdf_canvas.drawImage('static/logo1.png', 32, 550, width=100, height=100, mask='auto')
    pdf_canvas.drawImage('static/logo2.png', 352, 550, width=100, height=100, mask='auto')

    # Define the SVG path for the clipping path
    
    # Convert the SVG path to clip path points
    clip_path_points = [
        (0, 325),  # Top-left corner
        (290, 325),  # Top-right corner
        (0, 500),  # Bottom-right corner
        (290, 500)   # Bottom-left corner
]
    # pdf_canvas.saveState()
    # canvas.clipPath(clip_path_points, stroke=1, fill=0, fillMode='FILL_EVEN_ODD')
    # pdf_canvas.drawImage(participant.participant_image.url, 150, 300, width=130, height=130)
    # pdf_canvas.restoreState()
    # Save the PDF to the buffer
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
    pdf_data = svg_to_pdf(svg_code,participant, page_size=letter)  # You can pass other page sizes as needed
    # pdf_data = svg_to_pdf_with_canvas(svg_code, page_size=letter)  # You can pass other page sizes as needed

    if pdf_data:
        # Create the HTTP response with PDF content
        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = f'filename="{id_number}_{id_type}_id_card.pdf"'
        return response
    else:
        return HttpResponse("PDF generation failed.")
