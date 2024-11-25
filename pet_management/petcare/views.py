from django.shortcuts import render, redirect
from petcareapp.models import Customer, Pet, Appointment
from petcareapp.forms import CustomerForm, PetForm, AppointmentForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def validate_password(password):
    # Password validation criteria
    if (len(password) < 8 or 
        not re.search(r"[A-Z]", password) or 
        not re.search(r"[0-9]", password)):
        raise ValidationError(_('Password must be at least 8 characters long, include an uppercase letter and a number.'))

def create_account_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Check for existing username or email
        if User.objects.filter(username=username).exists():
            messages.error(request, _('Username already exists.'))
        elif User.objects.filter(email=email).exists():
            messages.error(request, _('Email already in use.'))
        else:
            try:
                validate_password(password1)  # Validate password strength
                if password1 == password2:
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    user.save()
                    messages.success(request, _('Account created successfully! You can now log in.'))
                    return redirect('login')  # Redirect to the login page after successful account creation
                else:
                    messages.error(request, _('Passwords do not match.'))
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
            return redirect('home')  # Redirect to the home page on successful login
        else:
            messages.error(request, _('Invalid username or password. If you don\'t have an account, please create one.'))
            return redirect('create')  # Redirect to create account page if login fails

    return render(request, 'login.html')

@login_required
def home_view(request):
    return render(request, 'home.html')

@login_required
def appointments_view(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointments.html', {'appointments': appointments})

@login_required
def customers_view(request):
    customers = Customer.objects.all()
    return render(request, 'customers.html', {'customers': customers})

@login_required
def add_customer_view(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Customer added successfully!'))
            return redirect('customers')
    else:
        form = CustomerForm()
    return render(request, 'add_customer.html', {'form': form})

@login_required
def add_appointment_view(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Appointment added successfully!'))
            return redirect('appointments')
    else:
        form = AppointmentForm()
    return render(request, 'add_appointment.html', {'form': form})

