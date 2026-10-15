from django.db import models

# Create your models here.
class Customer(models.Model):
    companyName = models.CharField(max_length=75)
    contactPerson = models.CharField(max_length=75)
    contactEmail = models.EmailField()
    location = models.CharField(max_length=75)
    pojectsNumber = models.IntegerField()
    activeTickets = models.IntegerField()

    def __str__(self):
        return f"{self.companyName}, {self.contactPerson}"