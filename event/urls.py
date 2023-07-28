from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registration/', views.registration, name='registration'),
    path('participants/', views.participants, name='participants'),
    path('view-id-card/<int:id_number>/', views.view_id_card, name='view_id_card'),
    path('get-id-card/<int:id_number>/<str:id_type>/', views.get_id_card, name='get_id_card'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
