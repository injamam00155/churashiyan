
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
import svglib.svglib as svglib
from io import BytesIO
from reportlab.lib.pagesizes import portrait  # Import portrait for custom page size
from reportlab.lib.units import inch  # Import inch to set dimensions in points
from django.template.loader import render_to_string
from reportlab.lib.pagesizes import letter  # Import your desired page size



def svg_to_pdf(svg_code, page_size=letter):
    # Create a PDF buffer
    pdf_buffer = BytesIO()

    # Convert SVG to PDF using reportlab's svglib
    drawing = svglib.svg2rlg(BytesIO(svg_code.encode('utf-8')))
    pdf_canvas = reportlab.pdfgen.canvas.Canvas(pdf_buffer, pagesize=page_size)  # Set the page size
    reportlab.graphics.renderPDF.draw(drawing, pdf_canvas, 0, 0)

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
        svg_code = render_to_string('sample.html', context)
    elif(id_type=='spouse'):
        # Render the SVG template with the spouse's data
        svg_code = render_to_string('sample.html', context)

    # Convert SVG to PDF with the desired page size (e.g., letter)
    pdf_data = svg_to_pdf(svg_code, page_size=letter)  # You can pass other page sizes as needed

    if pdf_data:
        # Create the HTTP response with PDF content
        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = f'filename="{id_number}_{id_type}_id_card.pdf"'
        return response
    else:
        return HttpResponse("PDF generation failed.")


# ... (other imports and code)

# def svg_to_pdf(svg_code, page_size):
#     # Create a PDF buffer
#     pdf_buffer = BytesIO()

#     # Convert SVG to PDF using reportlab's svglib
#     drawing = svglib.svg2rlg(BytesIO(svg_code.encode('utf-8')))
#     pdf_canvas = reportlab.pdfgen.canvas.Canvas(pdf_buffer, pagesize=page_size)  # Set the custom page size
#     reportlab.graphics.renderPDF.draw(drawing, pdf_canvas, 0, 0)

#     # Save the PDF to the buffer
#     pdf_canvas.save()

#     # Return the PDF buffer
#     return pdf_buffer.getvalue()

# def get_id_card(request, id_type, id_number):
#     # Fetch the participant based on the id_number
#     participant = get_object_or_404(Participant, id_number=id_number)
#     id = str(participant.id_number).zfill(3)

#     context = {
#         'participant': participant,
#         'id': id,
#     }

#     # Render the SVG template with the participant's data
#     svg_code = render_to_string('sample.html', context)

#     # Set the custom page size (e.g., 3.5x5 inches)
#     custom_page_width = 3.5 * inch
#     custom_page_height = 5 * inch
#     custom_page_size = (custom_page_width, custom_page_height)

#     # Convert SVG to PDF with the custom page size
#     pdf_data = svg_to_pdf(svg_code, page_size=custom_page_size)

#     if pdf_data:
#         # Create the HTTP response with PDF content
#         response = HttpResponse(pdf_data, content_type='application/pdf')
#         response['Content-Disposition'] = f'filename="{id_number}_{id_type}_id_card.pdf"'
#         return response
#     else:
#         return HttpResponse("PDF generation failed.")
