
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

    template = get_template('id_template.html')

    id=participant.id_number
    if id:
        id = str(id).zfill(3)
    context = {
        'participant': participant,
        'id':id,
    }

    return render(request, 'id_template.html', context)



from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from xhtml2pdf import pisa
from io import BytesIO
from .models import Participant  # Import the Participant model (adjust the import as per your model location)

def svg_to_pdf(svg_code):
    # Create a PDF buffer
    pdf_buffer = BytesIO()

    # Convert SVG to PDF using xhtml2pdf
    pisa_status = pisa.CreatePDF(svg_code, pdf_buffer)

    print(pisa_status)
    # Check if the PDF generation was successful
    if not pisa_status.err:
        return pdf_buffer.getvalue()
    else:
        return None

def get_id_card(request, id_type, id_number):
    # Fetch the participant based on the id_number
    participant = get_object_or_404(Participant, id_number=id_number)
    id=participant.id_number
    if id:
        id = str(id).zfill(3)
    context = {
        'participant': participant,
        'id':id,
    }
    if id_type == 'own':
        # Render the SVG template with the participant's data
        svg_code = render_to_string('id_participant.html', context)

    elif id_type == 'spouse':
        # Render the SVG template with the spouse's data
        svg_code = render_to_string('id_spouse.html', context)
  
    else:
        return HttpResponse("Invalid id_type")

    # Convert SVG to PDF
    pdf_data = svg_to_pdf(svg_code)

    if pdf_data:
        # Create the HTTP response with PDF content
        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = f'filename="{id_number}_{id_type}_id_card.pdf"'
        return response
    else:
        return HttpResponse("PDF generation failed.")
    




# # -----------------------------------------------------
# import os
# from django.conf import settings
# from django.http import HttpResponse
# from django.template.loader import get_template
# from xhtml2pdf import pisa
# from django.contrib.staticfiles import finders


# def link_callback(uri, rel):
#     """
#     Convert HTML URIs to absolute system paths so xhtml2pdf can access those
#     resources
#     """
#     result = finders.find(uri)
#     if result:
#             if not isinstance(result, (list, tuple)):
#                     result = [result]
#             result = list(os.path.realpath(path) for path in result)
#             path=result[0]
#     else:
#             sUrl = settings.STATIC_URL        # Typically /static/
#             sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
#             mUrl = settings.MEDIA_URL         # Typically /media/
#             mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/
    
#             if uri.startswith(mUrl):
#                     path = os.path.join(mRoot, uri.replace(mUrl, ""))
#             elif uri.startswith(sUrl):
#                     path = os.path.join(sRoot, uri.replace(sUrl, ""))
#             else:
#                     return uri
    
#     # make sure that file exists
#     if not os.path.isfile(path):
#             raise Exception(
#                     'media URI must start with %s or %s' % (sUrl, mUrl)
#             )
#     return path

# def get_id_card(request, id_type, id_number):
#     participant = get_object_or_404(Participant, id_number=id_number)

#     if id_type == 'own':
#         # Render the SVG template with the participant's data
#         template_path = 'id_participant.html'
#         # svg_code = render_to_string('id_participant.html', {'participant': participant})

#     elif id_type == 'spouse':
#         # Render the SVG template with the spouse's data
#         template_path = 'id_spouse.html'
#         # svg_code = render_to_string('id_spouse.html', {'participant': participant})
#     else:
#         return HttpResponse("Invalid id_type")
    
#     context = {'participant': participant}
#     # Create a Django response object, and specify content_type as pdf
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="report.pdf"'
#     # find the template and render it.
#     template = get_template(template_path)
#     html = template.render(context)
#     # print(html)
#     # create a pdf
#     pisa_status = pisa.CreatePDF(
#        html, dest=response, link_callback=link_callback)
#     # if error then show some funny view
#     if pisa_status.err:
#        return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return response





