# from django.contrib import admin
from django.urls import include, path
from django.contrib import admin
from .admin import ParticipantAdmin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('event.urls')),
    path('admin/', admin.site.urls),
    path('admin/verify/', ParticipantAdmin.verify, name='verify'),
    # path('admin/verify/', ParticipantAdmin.verify, name='verify'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)