from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Company, Employee, Project
import random
from datetime import timedelta
import json

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Company.objects.all().delete()
        
        # Sample company data
        companies = [
            {
                'name': 'TechCorp Solutions',
                'type': 'IT',
                'revenue': 5000000,
                'location': 'Silicon Valley',
            },
            {
                'name': 'MobileApp Innovations',
                'type': 'MOBILE',
                'revenue': 2500000,
                'location': 'New York',
            },
            {
                'name': 'WebDev Masters',
                'type': 'WEB',
                'revenue': 1500000,
                'location': 'Austin',
            },
            {
                'name': 'AI Research Labs',
                'type': 'AI',
                'revenue': 3500000,
                'location': 'Boston',
            },
            {
                'name': 'DataScience Pro',
                'type': 'DATA',
                'revenue': 2000000,
                'location': 'Seattle',
            }
        ]

        # Create companies
        created_companies = []
        for company_data in companies:
            company = Company.objects.create(
                name=company_data['name'],
                type=company_data['type'],
                revenue=company_data['revenue'],
                location=company_data['location'],
                about=f"Leading provider of {company_data['type']} solutions",
                website=f"https://www.{company_data['name'].lower().replace(' ', '')}.com",
                founded_date=timezone.now().date() - timedelta(days=random.randint(365, 3650))
            )
            created_companies.append(company)

        # Sample skills for different positions
        skills_by_position = {
            'MANAGER': ['Leadership', 'Strategy', 'Team Building', 'Project Management', 'Agile', 'Budget Management'],
            'DEVELOPER': ['Python', 'JavaScript', 'React', 'Django', 'Node.js', 'AWS', 'Docker'],
            'LEAD': ['Architecture', 'Team Leadership', 'Code Review', 'Agile', 'System Design', 'Mentoring'],
            'DESIGNER': ['UI/UX', 'Figma', 'Adobe XD', 'Wireframing', 'User Research', 'Design Systems'],
            'ANALYST': ['Data Analysis', 'SQL', 'Python', 'Tableau', 'Business Intelligence', 'Statistics'],
            'DEVOPS': ['Docker', 'Kubernetes', 'AWS', 'CI/CD', 'Jenkins', 'Terraform', 'Linux'],
            'QA': ['Testing', 'Automation', 'Selenium', 'Test Planning', 'Bug Tracking', 'API Testing']
        }

        # Sample names for more realistic data
        first_names = ['James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph',
                      'Thomas', 'Charles', 'Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth',
                      'Barbara', 'Susan', 'Jessica', 'Sarah', 'Karen']
        
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
                     'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson']

        # Create employees with realistic distribution
        for company in created_companies:
            # Define department distribution for 50 employees
            department_distribution = {
                'DEVELOPER': 20,  # 40% developers
                'QA': 7,         # 14% QA
                'ANALYST': 5,    # 10% analysts
                'DESIGNER': 5,   # 10% designers
                'DEVOPS': 5,     # 10% devops
                'LEAD': 5,       # 10% team leads
                'MANAGER': 3     # 6% managers
            }
            
            # Create employees for each department
            for position, count in department_distribution.items():
                for i in range(count):
                    name = f"{random.choice(first_names)} {random.choice(last_names)}"
                    email = f"{name.lower().replace(' ', '.')}.{position.lower()}.{random.randint(100, 999)}@{company.name.lower().replace(' ', '')}.com"
                    
                    # Experience and salary calculation
                    experience_years = random.randint(1, 15)
                    base_salary = {
                        'MANAGER': 120000,
                        'LEAD': 110000,
                        'DEVELOPER': 95000,
                        'DESIGNER': 85000,
                        'ANALYST': 80000,
                        'DEVOPS': 100000,
                        'QA': 75000
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
                    
                    # Projects completed based on experience and performance
                    base_projects = experience_years * 2
                    performance_multiplier = {'EXC': 1.5, 'GOOD': 1.2, 'AVG': 1.0, 'BELOW': 0.8, 'POOR': 0.6}
                    projects_completed = int(base_projects * performance_multiplier[performance_rating])
                    
                    employee = Employee.objects.create(
                        name=name,
                        email=email,
                        address=f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Maple', 'Cedar', 'Pine'])} {random.choice(['Street', 'Avenue', 'Road', 'Boulevard'])}",
                        phone=f"+1-{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                        about=f"Experienced {position.lower()} with {experience_years} years of experience in {company.type} technologies",
                        position=position,
                        company=company,
                        salary=salary,
                        performance_rating=performance_rating,
                        projects_completed=projects_completed,
                        skills=json.dumps(random.sample(skills_by_position[position], min(5, len(skills_by_position[position])))),
                        hire_date=timezone.now().date() - timedelta(days=int(experience_years * 365))
                    )

        # Create projects
        project_types = [
            'Mobile App Development', 'Cloud Migration', 'E-commerce Platform',
            'AI Integration', 'Data Analytics Dashboard', 'Security Upgrade',
            'Infrastructure Modernization', 'Customer Portal', 'API Gateway'
        ]
        
        for company in created_companies:
            num_projects = random.randint(5, 8)
            for i in range(num_projects):
                start_date = timezone.now().date() - timedelta(days=random.randint(30, 365))
                project_type = random.choice(project_types)
                
                # Project budget based on type and company revenue
                base_budget = random.randint(100000, 500000)
                revenue_factor = company.revenue / 2000000
                budget = int(base_budget * revenue_factor)
                
                project = Project.objects.create(
                    name=f"{company.name} - {project_type}",
                    description=f"Strategic {project_type.lower()} project aimed at enhancing {company.name}'s capabilities",
                    company=company,
                    start_date=start_date,
                    status=random.choice(['PLAN', 'PROG', 'TEST', 'COMP', 'HOLD']),
                    budget=budget,
                    technologies=json.dumps(random.sample([
                        'Python', 'JavaScript', 'React', 'Django', 'Docker', 'AWS',
                        'Kubernetes', 'MongoDB', 'PostgreSQL', 'Redis', 'GraphQL'
                    ], 4)),
                    completion_percentage=random.randint(0, 100)
                )
                
                # Add team members with appropriate roles
                employees = list(company.employee_set.all())
                
                # Ensure project has required roles
                required_roles = ['MANAGER', 'LEAD', 'DEVELOPER', 'QA']
                team_members = []
                
                for role in required_roles:
                    role_employees = [e for e in employees if e.position == role]
                    if role_employees:
                        team_members.append(random.choice(role_employees))
                
                # Add additional team members
                remaining_employees = [e for e in employees if e not in team_members]
                additional_members = random.randint(3, 7)
                if remaining_employees:
                    team_members.extend(random.sample(remaining_employees, min(additional_members, len(remaining_employees))))
                
                project.team_members.add(*team_members)

        self.stdout.write(self.style.SUCCESS('Successfully populated database with enhanced sample data'))
