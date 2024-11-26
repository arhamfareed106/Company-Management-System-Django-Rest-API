from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Company, Employee, Project
import random
from datetime import timedelta
import json

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing existing data...')
        Company.objects.all().delete()
        Employee.objects.all().delete()
        Project.objects.all().delete()
        
        # Sample company data
        companies = [
            {
                'name': 'TechCorp Solutions',
                'type': 'CORP',
                'revenue': 5000000,
                'location': 'Silicon Valley',
            },
            {
                'name': 'FinTech Innovations LLC',
                'type': 'LLC',
                'revenue': 2500000,
                'location': 'New York',
            },
            {
                'name': 'HealthCare Partners',
                'type': 'PART',
                'revenue': 1500000,
                'location': 'Boston',
            },
            {
                'name': 'EduTech Ventures',
                'type': 'CORP',
                'revenue': 3500000,
                'location': 'Austin',
            },
            {
                'name': 'Retail Solutions Inc',
                'type': 'CORP',
                'revenue': 2000000,
                'location': 'Seattle',
            }
        ]

        self.stdout.write('Creating companies...')
        created_companies = []
        for company_data in companies:
            company = Company.objects.create(
                name=company_data['name'],
                type=company_data['type'],
                location=company_data['location'],
                website=f"https://www.{company_data['name'].lower().replace(' ', '')}.com",
                established_date=timezone.now().date() - timedelta(days=random.randint(365, 3650)),
                description=f"Leading provider of innovative solutions in {company_data['location']}",
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            created_companies.append(company)
            self.stdout.write(f'Created company: {company.name}')

        # Sample names for more realistic data
        first_names = ['James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph',
                      'Thomas', 'Charles', 'Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth',
                      'Barbara', 'Susan', 'Jessica', 'Sarah', 'Karen']
        
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
                     'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson']

        self.stdout.write('Creating employees...')
        # Create employees for each company
        for company in created_companies:
            # Define department distribution
            department_distribution = {
                'MGR': 3,    # Managers
                'DEV': 20,   # Developers
                'DES': 5,    # Designers
                'HR': 4,     # HR
                'SALES': 8,  # Sales
                'OTHER': 5   # Other roles
            }
            
            # Create employees for each department
            for position, count in department_distribution.items():
                for i in range(count):
                    name = f"{random.choice(first_names)} {random.choice(last_names)}"
                    email = f"{name.lower().replace(' ', '.')}.{random.randint(100, 999)}.{position.lower()}@{company.name.lower().replace(' ', '')}.com"
                    
                    # Experience and salary calculation
                    experience_years = random.randint(1, 15)
                    base_salary = {
                        'MGR': 120000,
                        'DEV': 95000,
                        'DES': 85000,
                        'HR': 65000,
                        'SALES': 75000,
                        'OTHER': 60000
                    }
                    
                    experience_factor = 0.8 + (experience_years * 0.04)
                    salary = int(base_salary[position] * experience_factor)
                    
                    # Performance rating based on experience
                    if experience_years > 10:
                        performance_weights = [('EXC', 0.3), ('GOOD', 0.4), ('AVG', 0.2), ('BELOW', 0.07), ('POOR', 0.03)]
                    elif experience_years > 5:
                        performance_weights = [('EXC', 0.15), ('GOOD', 0.35), ('AVG', 0.35), ('BELOW', 0.1), ('POOR', 0.05)]
                    else:
                        performance_weights = [('EXC', 0.05), ('GOOD', 0.25), ('AVG', 0.45), ('BELOW', 0.15), ('POOR', 0.1)]
                    
                    performance_rating = random.choices(
                        [p[0] for p in performance_weights],
                        weights=[p[1] for p in performance_weights]
                    )[0]

                    hire_date = timezone.now().date() - timedelta(days=int(experience_years * 365))
                    
                    employee = Employee.objects.create(
                        name=name,
                        email=email,
                        phone=f"+1-{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                        position=position,
                        company=company,
                        hire_date=hire_date,
                        salary=salary,
                        performance_rating=performance_rating,
                        projects_completed=random.randint(1, 20),
                        is_active=random.choices([True, False], weights=[0.95, 0.05])[0],
                        created_at=timezone.now(),
                        updated_at=timezone.now()
                    )
                    self.stdout.write(f'Created employee: {employee.name} ({position})')

        self.stdout.write('Creating projects...')
        # Create projects
        project_names = [
            'Mobile App Development', 'Cloud Migration', 'E-commerce Platform',
            'AI Integration', 'Data Analytics', 'Security Upgrade',
            'Infrastructure Update', 'Customer Portal', 'API Gateway'
        ]
        
        for company in created_companies:
            num_projects = random.randint(3, 6)
            employees = list(company.employee_set.all())
            
            for i in range(num_projects):
                project_name = random.choice(project_names)
                status = random.choice(['PLAN', 'PROG', 'COMP', 'HOLD'])
                completion = 100 if status == 'COMP' else (
                    random.randint(0, 20) if status == 'PLAN'
                    else random.randint(20, 90) if status == 'PROG'
                    else random.randint(0, 100)
                )
                
                start_date = timezone.now().date() - timedelta(days=random.randint(30, 365))
                end_date = start_date + timedelta(days=random.randint(90, 365)) if status == 'COMP' else None
                
                project = Project.objects.create(
                    name=f"{company.name} - {project_name}",
                    description=f"Strategic {project_name.lower()} project for {company.name}",
                    company=company,
                    start_date=start_date,
                    end_date=end_date,
                    status=status,
                    budget=random.randint(50000, 500000),
                    completion_percentage=completion,
                    created_at=timezone.now() - timedelta(days=random.randint(30, 365)),
                    updated_at=timezone.now() - timedelta(days=random.randint(0, 30))
                )
                
                # Assign random employees to the project
                num_team_members = random.randint(3, 10)
                project.employees.add(*random.sample(employees, min(num_team_members, len(employees))))
                
                self.stdout.write(f'Created project: {project.name}')

        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample data'))
