from django.shortcuts import get_object_or_404, render, redirect
from .models import Customer, Pet, Appointment, PetAdoptionApplication, PetCarePayment  # Ensure all models are imported
from .forms import CustomerForm, PetForm, AppointmentForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Value, DecimalField
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Count, Sum
from django.db.models.functions import Concat
from django.db import models
from django.shortcuts import render
from django.db.models import Count, Sum, Value
from django.db.models.functions import TruncMonth, Concat
from .models import Customer, Pet, Appointment, PetCarePayment
from django.shortcuts import render
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.db.models import Value
from django.db.models.functions import Concat
from .models import Customer, Appointment


def statistics(request):
    try:
        # 1. Customers' Full Names
        customer_names = list(
            Customer.objects.annotate(
                full_name=Concat('first_name', Value(' '), 'last_name')
            ).values_list('full_name', flat=True).order_by('first_name', 'last_name')
        )

        # 2. Count Appointments for Each Customer
        appointment_counts = list(
            Customer.objects.annotate(
                appointment_count=Count('pet__appointment', distinct=True)
            ).values_list('appointment_count', flat=True).order_by('first_name', 'last_name')
        )

        # 3. Count Pets for Each Customer
        pet_counts = list(
            Customer.objects.annotate(
                pet_count=Count('pet', distinct=True)
            ).values_list('pet_count', flat=True).order_by('first_name', 'last_name')
        )

        # 4. Appointments by Service Type
        service_types = list(
            Appointment.objects.values('service_type')
            .annotate(count=Count('id'))
            .order_by('service_type')
        )
        service_type_labels = [item['service_type'] for item in service_types]
        service_type_counts = [item['count'] for item in service_types]

        # 5. Appointments Over Time
        monthly_appointments = list(
            Appointment.objects.annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )
        monthly_appointment_labels = [ma['month'].strftime('%B %Y') for ma in monthly_appointments]
        monthly_appointment_data = [ma['count'] for ma in monthly_appointments]

        # 6. Total Payments by Customer
        total_payments = list(
            Customer.objects.annotate(
                total_payment=Sum('pet__petcarepayment__amount')
            ).values_list('total_payment', flat=True).order_by('first_name', 'last_name')
        )
        total_payments = [payment if payment is not None else 0 for payment in total_payments]

        context = {
            'customer_names': customer_names,
            'appointment_counts': appointment_counts,
            'pet_counts': pet_counts,
            'service_types': service_type_labels,
            'service_type_counts': service_type_counts,
            'monthly_appointments': {
                'labels': monthly_appointment_labels,
                'data': monthly_appointment_data,
            },
            'total_payments': total_payments,
        }
        return render(request, 'statistics.html', context)

    except Exception as e:
        # Handle Errors Gracefully
        context = {
            'customer_names': [],
            'appointment_counts': [],
            'pet_counts': [],
            'service_types': [],
            'service_type_counts': [],
            'monthly_appointments': {'labels': [], 'data': []},
            'total_payments': [],
            'error_message': f'Unable to load statistics: {str(e)}',
        }
        return render(request, 'statistics.html', context)


def handle_post_form(request, form, success_url, error_message=''):
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(success_url)
        else:
            if form.errors:
                messages.error(request, error_message)
    return form




# Password Validation
def validate_password(password):
    if (len(password) < 8 or 
        not re.search(r"[A-Z]", password) or 
        not re.search(r"[0-9]", password)):
        raise ValidationError('Password must be at least 8 characters long, include an uppercase letter and a number.')


# Create Account View
def create_account_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use.')
        else:
            try:
                validate_password(password1)
                if password1 == password2:
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    user.save()
                    messages.success(request, 'Account created successfully! You can now log in.')
                    return redirect('login') 
                else:
                    messages.error(request, 'Passwords do not match.')
            except ValidationError as e:
                messages.error(request, e.message)

    return render(request, 'create.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'home')  # Redirect to 'next' or 'home' if 'next' is not provided
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password. If you don\'t have an account, please create one.')
            return redirect('create')
    else:
        return render(request, 'login.html')
    

# Home View
def home_view(request):
    return render(request, 'home.html')  


# Appointments View (secured)

def appointments(request):
    appointments = Appointment.objects.all() 
    return render(request, 'appointments.html', {'appointments': appointments})


# Customers View (secured)
def customers(request):
    customers = Customer.objects.all()
    return render(request, 'customers.html', {'customers': customers})


# Add Customer View
def add_customer(request):
    form = CustomerForm(request.POST or None)
    form = handle_post_form(request, form, 'customers', 'Please correct the errors below.')
    return render(request, 'add_customer.html', {'form': form})


# Edit Customer View
def edit_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    form = CustomerForm(request.POST or None, instance=customer)
    form = handle_post_form(request, form, 'customers', 'Please correct the errors below.')
    return render(request, 'edit_customer.html', {'form': form, 'customer': customer})


# Delete Customer View
def delete_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    if request.method == "POST":
        customer.delete()
        return redirect('customers')
    return render(request, 'confirm_delete.html', {'customer': customer})


# Add Appointment View

def add_appointment(request):
    form = AppointmentForm(request.POST or None)
    form = handle_post_form(request, form, 'appointments', 'Please correct the errors below.')
    return render(request, 'add_appointment.html', {'form': form})
