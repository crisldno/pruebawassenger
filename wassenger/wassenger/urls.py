
from django.conf import settings
from django.conf.urls.static import static 
from django.urls import path
from .views import webhook_handler,procesar_webhook
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('webhook/', webhook_handler, name='webhook_handler'),
    path('procesar-webhook/', procesar_webhook, name='procesar_webhook'),
]
if settings.DEBUG:     
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)     
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    