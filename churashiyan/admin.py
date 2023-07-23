from django.contrib import admin
from event.models import Participant

# Define your admin classes
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('id_number', 'name', 'district', 'contact_number', 'is_verified')
    list_filter = ('is_verified',)
    actions = ['verify_transactions']

    def verify(self, request, queryset):
        # Your action method logic here
        queryset.update(is_verified=True)
        self.message_user(request, "Selected transactions have been verified.")

# Register the admin classes
admin.site.register(Participant, ParticipantAdmin)
