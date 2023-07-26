
from django.contrib import admin
import cloudinary
from django.contrib import admin
from event.models import Participant


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


admin.site.register(Participant, ParticipantAdmin)



