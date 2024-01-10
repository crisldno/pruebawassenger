from django.urls import path
from .views import recibir_mensaje
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recibir_mensaje/', recibir_mensaje, name='recibir_mensaje'),

]