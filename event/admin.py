from django.contrib import admin
import cloudinary
from django.db.models import Q
from django.contrib.admin import AdminSite
from django.shortcuts import render
from django.db.models import Count, Sum
from . import models
from event.models import Participant
from django.contrib.auth.models import User, Group
import django.apps
from django.http import HttpResponse
from django.template import loader
from django.db.models import Case, When, Value, IntegerField


models = django.apps.apps.get_models()




# @admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['id_number', 'name', 'spouse_name', 'spouse_coming', 'driver_coming', 'paid_at', 'amount', 'transaction_id', 'is_verified']
    actions = ['mark_verified', 'mark_unverified']  # Add custom actions to set 'is_verified'
    list_filter = ['is_verified', 'paid_at']

    # change_list_template = 'admin/change_list_results.html'
    
    def mark_verified(self, request, queryset):
        # Set 'is_verified' to True for selected instances
        queryset.update(is_verified=True)
    mark_verified.short_description = 'Verify Participant'

    def mark_unverified(self, request, queryset):
        # Set 'is_verified' to False for selected instances
        queryset.update(is_verified=False)
    mark_unverified.short_description = 'Unverify Participant'

    
    def delete_model(self, request, obj):
        # Call the model's delete method to handle associated image deletion
        obj.delete()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            # Delete the associated pictures from Cloudinary
            if obj.participant_image:
                cloudinary.uploader.destroy(obj.participant_image.name)
            if obj.spouse_image:
                cloudinary.uploader.destroy(obj.spouse_image.name)
        
        # Call the model's delete method to handle other aspects of deletion
        queryset.delete()



    def save_model(self, request, obj, form, change):
        # Check if the participant_image has changed
        print(form.cleaned_data['participant_image'].name)
        print(obj.participant_image.name)
        if 'participant_image' in form.changed_data:
            # Delete the old participant image from Cloudinary
            if obj.participant_image:
                print(obj.participant_image.name)  
                cloudinary.uploader.destroy(obj.participant_image.name)

            # Upload and update the participant_image with the new image
            if form.cleaned_data['participant_image']:
                response = cloudinary.uploader.upload(
                    form.cleaned_data['participant_image'].read(),
                    folder='media/',
                    # public_id=f"PP{obj.id_number}"
                )
                obj.participant_image = response['public_id']

        # Similar process for spouse_image
        if 'spouse_image' in form.changed_data:
            if obj.spouse_image:
                cloudinary.uploader.destroy(obj.spouse_image.name)
            
            if form.cleaned_data['spouse_image']:
                response = cloudinary.uploader.upload(
                    form.cleaned_data['spouse_image'].read(),
                    folder='media/',
                    # public_id=f"SP{obj.id_number}"
                )
                obj.spouse_image = response['public_id']


        super().save_model(request, obj, form, change)


admin.site.register(Participant,ParticipantAdmin)


# Define your custom admin site
class CustomAdminSite(admin.AdminSite):
    site_header = "পিরোজপুর চুরাশিয়ান মিলনমেলা"
    site_title = "পিরোজপুর চুরাশিয়ান মিলনমেলা"
    index_title = "Pirojpur Churashiyan Admin"

    def has_permission(self, request):
        # Allow superusers full access to all models
        if request.user.is_superuser:
            return True
        
        # Allow users in 'Admins' group to edit the Participant model
        if request.user.groups.filter(name='Admins').exists():
            return True if request.path.startswith('/admin/event/participant') else False
        
        return False

    def index(self, request, extra_context=None):
        # Calculate statistics for each paid_at name
        stats_queryset = (
            Participant.objects.values('paid_at')
            .annotate(
                participants=Count('id_number'),
                spouses=Count('spouse_name'),
                drivers=Count('id_number', filter=Q(driver_coming='Yes')),
                total_amount=Sum('amount')
            )
            .order_by('-paid_at')
        )

        stats = {
            stat['paid_at'][:-14]: {
                'paid_at': stat['paid_at'][:-14],
                'participants': stat['participants'],
                'spouses': stat['spouses'],
                'drivers': stat['drivers'],
                'total_amount': stat['total_amount'],
            }
            for stat in stats_queryset
        }

        context = dict(
            self.each_context(request),
            stats=stats,
            paid_dates=Participant.objects.order_by('-paid_at').values_list('paid_at', flat=True).distinct(),
            custom_message='This is a custom message from context',  # Additional context
        )
        return render(request, "admin/event/admin_index.html", context)

# Create an instance of the custom admin site
custom_admin_site = CustomAdminSite(name='customadmin')


# Register other models with the custom admin site
custom_admin_site.register(Participant,ParticipantAdmin)
# models_to_exclude = [Participant]  # Add more models if needed

# for model in admin.site._registry:
#     if model not in models_to_exclude:
#         custom_admin_site.register(model)


