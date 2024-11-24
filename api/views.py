from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, related_name='employees', on_delete=models.CASCADE)
    position = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
