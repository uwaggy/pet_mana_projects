from django import forms
from .models import Customer, Appointment, Pet

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone_number', 'email']


class AppointmentForm(forms.ModelForm):
    # Define the choices for service type
    SERVICE_CHOICES = [
        ('grooming', 'Grooming'),
        ('vaccination', 'Vaccination'),
        ('checkup', 'Check-up'),
        ('boarding', 'Boarding'),
    ]

    # Define the pet field as a ModelChoiceField
    pet = forms.ModelChoiceField(
        queryset=Pet.objects.all(),  # Display all pets in the database
        required=True,
        label="Select Pet",  # Label for the dropdown
        empty_label="Select a pet",  # Placeholder option
    )

    # Define the service type field as a ChoiceField
    service_type = forms.ChoiceField(
        choices=SERVICE_CHOICES,  # The predefined choices for service type
        required=True,
        label="Service Type",  # Label for the dropdown
    )


    class Meta:
        model = Appointment
        fields = ['pet', 'date', 'time', 'service_type']  


    def __init__(self, *args, **kwargs):
        customer = kwargs.pop('customer', None)  
        super(AppointmentForm, self).__init__(*args, **kwargs)
        
        # If a customer is provided, filter pets to show only those related to that customer
        if customer:
            self.fields['pet'].queryset = Pet.objects.filter(customer=customer)


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'breed', 'age']
