# from django.contrib import admin
from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from event import views


urlpatterns = [
    path('', include('event.urls')),
    path('admin/', admin.site.urls),
    path('verify/', views.admin_verify_participants, name='admin_verify_participants'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)