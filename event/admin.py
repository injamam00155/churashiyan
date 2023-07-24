from django.contrib import admin
from event.models import Participant

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['id_number', 'name', 'spouse_name', 'driver_coming', 'paid_at', 'amount', 'transaction_id', 'is_verified']


admin.site.register(Participant, ParticipantAdmin)
