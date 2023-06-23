from django.contrib import admin
from django.urls import path, include
from django.urls import re_path as url
from Agritherm_data import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Agritherm_data.urls')),
    url(r"^city/$", views.cityView.as_view()),
    url(r"^chatbot/$", views.ChatBotView.as_view())
]
