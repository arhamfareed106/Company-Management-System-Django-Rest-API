# Django REST API - Company Management System

A comprehensive Django-based REST API and web application for managing companies, employees, and projects.

## Features

- **Company Management**
  - Create, read, update, and delete company profiles
  - Track company details including name, location, type, revenue, and more
  - Company types supported: Corporation, LLC, Partnership, Sole Proprietorship

- **Employee Management**
  - Comprehensive employee database
  - Track employee information including position, salary, and performance
  - Multiple position types: Manager, Developer, Designer, HR, Sales, and Others

- **Project Management**
  - Track company projects and their status
  - Assign employees to projects
  - Monitor project budgets and completion percentages

- **Analytics Dashboard**
  - View company performance metrics
  - Employee statistics and distribution
  - Project status overview

## Technical Stack

- Django Web Framework
- Django REST Framework
- SQLite Database
- Bootstrap (Frontend)

## API Endpoints

### Companies
- GET /api/companies/ - List all companies
- POST /api/companies/ - Create a new company
- GET /api/companies/{id}/ - Retrieve company details
- PUT /api/companies/{id}/ - Update company details
- DELETE /api/companies/{id}/ - Delete a company

### Employees
- GET /api/employees/ - List all employees
- POST /api/employees/ - Add a new employee
- GET /api/employees/{id}/ - Retrieve employee details
- PUT /api/employees/{id}/ - Update employee details
- DELETE /api/employees/{id}/ - Remove an employee

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install django djangorestframework
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Web Interface

The application includes a web interface with the following pages:
- Home Dashboard (`/`)
- Company List (`/companies/`)
- Employee List (`/employees/`)
- Analytics Dashboard (`/analytics/`)
- Company Details (`/companies/<id>/`)
- Employee Details (`/employees/<id>/`)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
