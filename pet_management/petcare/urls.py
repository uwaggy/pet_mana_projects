# main_project/urls.py
from django.contrib import admin
from django.urls import path, include  # Make sure to include 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('petcareapp.urls')),  # Include your app URLs
]
