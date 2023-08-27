# from django.contrib import admin
from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from event import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from event.admin import custom_admin_site




urlpatterns = [
    path('', include('event.urls')),
    path('superadmin/', admin.site.urls),
    path('admin/', custom_admin_site.urls),
]

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

