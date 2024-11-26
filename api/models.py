from django.db import models
from django.utils import timezone

class Company(models.Model):
    COMPANY_TYPES = [
        ('IT', 'Information Technology'),
        ('NON_IT', 'Non IT'),
        ('MOBILE', 'Mobile Development'),
        ('WEB', 'Web Development'),
        ('AI', 'Artificial Intelligence'),
        ('DATA', 'Data Science'),
    ]
    
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    about = models.TextField()
    type = models.CharField(max_length=20, choices=COMPANY_TYPES)
    added_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    employee_count = models.IntegerField(default=0)
    website = models.URLField(blank=True, null=True)
    founded_date = models.DateField(null=True, blank=True)

    def update_metrics(self):
        self.employee_count = self.employee_set.count()
        self.save()

    def get_department_distribution(self):
        return self.employee_set.values('position').annotate(
            count=models.Count('id')
        )

    def __str__(self):
        return self.name

class Employee(models.Model):
    POSITION_CHOICES = [
        ('MANAGER', 'Manager'),
        ('DEVELOPER', 'Software Developer'),
        ('LEAD', 'Project Leader'),
        ('DESIGNER', 'UI/UX Designer'),
        ('ANALYST', 'Business Analyst'),
        ('DEVOPS', 'DevOps Engineer'),
        ('QA', 'Quality Assurance'),
    ]

    PERFORMANCE_LEVELS = [
        ('EXC', 'Excellent'),
        ('GOOD', 'Good'),
        ('AVG', 'Average'),
        ('BELOW', 'Below Average'),
        ('POOR', 'Poor'),
    ]

    employee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    about = models.TextField()
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    hire_date = models.DateField(auto_now_add=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    performance_rating = models.CharField(
        max_length=5, 
        choices=PERFORMANCE_LEVELS,
        default='AVG'
    )
    projects_completed = models.IntegerField(default=0)
    skills = models.JSONField(default=dict)
    last_review_date = models.DateField(null=True, blank=True)

    def calculate_experience(self):
        if self.hire_date:
            return (timezone.now().date() - self.hire_date).days // 365
        return 0

    def update_performance(self, rating, projects_completed=None):
        self.performance_rating = rating
        if projects_completed is not None:
            self.projects_completed = projects_completed
        self.last_review_date = timezone.now().date()
        self.save()

    def __str__(self):
        return self.name

class Project(models.Model):
    STATUS_CHOICES = [
        ('PLAN', 'Planning'),
        ('PROG', 'In Progress'),
        ('TEST', 'Testing'),
        ('COMP', 'Completed'),
        ('HOLD', 'On Hold'),
    ]

    project_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default='PLAN')
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    team_members = models.ManyToManyField(Employee, related_name='projects')
    technologies = models.JSONField(default=list)
    completion_percentage = models.IntegerField(default=0)

    def get_duration(self):
        if self.end_date:
            return (self.end_date - self.start_date).days
        return (timezone.now().date() - self.start_date).days

    def update_completion(self, percentage):
        self.completion_percentage = percentage
        if percentage == 100:
            self.status = 'COMP'
            self.end_date = timezone.now().date()
        self.save()

    def __str__(self):
        return self.name
