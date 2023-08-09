
from django.contrib import admin
import cloudinary
from django.contrib import admin
from event.models import Participant
from django.db.models import Q





# Override the site header, browser tab title, and index page title
admin.site.site_header = "পিরোজপুর চুরাশিয়ান মিলনমেলা"
admin.site.site_title = "পিরোজপুর চুরাশিয়ান মিলনমেলা"
admin.site.index_title = "Pirojpur Churashiyan Admin "


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['id_number', 'name', 'spouse_name', 'spouse_coming', 'driver_coming', 'paid_at', 'amount', 'transaction_id', 'is_verified']
    actions = ['mark_verified', 'mark_unverified']  # Add custom actions to set 'is_verified'
    list_filter = ['is_verified', 'paid_at']
    
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





admin.site.register(Participant, ParticipantAdmin)


