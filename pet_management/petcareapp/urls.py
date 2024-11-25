from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static  # Correct import for static()
from .views import (
    home_view, 
    create_account_view,
    login_view,
    appointments,
    customers,
    add_customer,
    edit_customer,     
    delete_customer, 
    add_appointment,
    
    
)

urlpatterns = [
    path('', home_view, name='home'),
    path('create/', create_account_view, name='create'),
    path('customers/', customers, name='customers'),
    path('add-customer/', add_customer, name='add_customer'),
    path('edit-customer/<int:id>/', edit_customer, name='edit_customer'),  # Edit customer path
    path('delete-customer/<int:id>/', delete_customer, name='delete_customer'),  # Delete customer path
    path('add-appointment/', add_appointment, name='add_appointment'),
    path('login/', login_view, name='login'), 
    path('appointments/', appointments, name='appointments'),
    path('statistics /', views.statistics, name='statistics'), 

]

# Serve media files in development when DEBUG is True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
