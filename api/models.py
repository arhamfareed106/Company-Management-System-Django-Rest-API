from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from django.utils.text import slugify

class Company(models.Model):
    COMPANY_TYPES = [
        ('CORP', 'Corporation'),
        ('LLC', 'Limited Liability Company'),
        ('PART', 'Partnership'),
        ('SOLE', 'Sole Proprietorship'),
    ]

    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=200)
    type = models.CharField(max_length=4, choices=COMPANY_TYPES, default='CORP')
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    website = models.URLField(blank=True)
    established_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ['name']

    def __str__(self):
        return self.name

class Employee(models.Model):
    POSITION_CHOICES = [
        ('MGR', 'Manager'),
        ('DEV', 'Developer'),
        ('DES', 'Designer'),
        ('HR', 'HR'),
        ('SALES', 'Sales'),
        ('OTHER', 'Other'),
    ]

    PERFORMANCE_CHOICES = [
        ('EXC', 'Excellent'),
        ('GOOD', 'Good'),
        ('AVG', 'Average'),
        ('BELOW', 'Below Average'),
        ('POOR', 'Poor'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator(message="Enter a valid email address.")]
    )
    phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    position = models.CharField(max_length=5, choices=POSITION_CHOICES, default='OTHER')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    performance_rating = models.CharField(max_length=5, choices=PERFORMANCE_CHOICES, default='AVG')
    projects_completed = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        unique_together = ['email', 'company']

    def __str__(self):
        return f"{self.name} - {self.company.name}"

class Project(models.Model):
    STATUS_CHOICES = [
        ('PLAN', 'Planning'),
        ('PROG', 'In Progress'),
        ('COMP', 'Completed'),
        ('HOLD', 'On Hold'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    employees = models.ManyToManyField(Employee, related_name='projects')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default='PLAN')
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    completion_percentage = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
