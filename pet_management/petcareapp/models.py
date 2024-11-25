from django.db import models

# Customer model
class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Pet model
class Pet(models.Model):  
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Reference to Customer
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name

# Appointment model
class Appointment(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    service_type = models.CharField(max_length=100)

    def __str__(self):
        return f"Appointment for {self.pet.name} on {self.date} at {self.time}"

# PetAdoptionApplication model
class PetAdoptionApplication(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)  # Reference to the Pet being adopted
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Reference to the customer adopting the pet
    application_date = models.DateField()
    adoption_status = models.CharField(max_length=50)  # e.g., 'Pending', 'Approved', 'Rejected'

    def __str__(self):
        return f"Application for {self.pet.name} by {self.customer.first_name} {self.customer.last_name}"

# PetCarePayment model
class PetCarePayment(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)  # Reference to the pet being cared for
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()

    def __str__(self):
        return f"Payment for {self.pet.name} - {self.amount} on {self.payment_date}"
