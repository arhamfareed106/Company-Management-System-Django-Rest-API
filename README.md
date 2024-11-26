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
- Django Template Engine
- Django ORM

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

## Basic Installation

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

## Advanced Setup and Configuration

### Environment Variables
Create a `.env` file in the root directory:
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Custom Database Configuration
For PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### API Authentication
The API supports multiple authentication methods:

1. Token Authentication:
```python
# Add to INSTALLED_APPS
'rest_framework.authtoken',

# Add to REST_FRAMEWORK settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
```

2. JWT Authentication:
```bash
pip install djangorestframework-simplejwt
```

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
```

### API Permissions
```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### Custom Middleware
```python
MIDDLEWARE = [
    # ... other middleware
    'api.middleware.CustomAuthMiddleware',
    'api.middleware.RequestLoggingMiddleware',
]
```

## Advanced Features

### API Rate Limiting
```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}
```

### Caching Configuration
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### Custom Management Commands
```bash
# Generate performance report
python manage.py generate_performance_report

# Cleanup old data
python manage.py cleanup_old_data --days 30

# Export company data
python manage.py export_company_data --format csv
```

### Automated Testing
```bash
# Run all tests
python manage.py test

# Run specific test module
python manage.py test api.tests.test_companies

# Run with coverage
coverage run manage.py test
coverage report
```

## Production Deployment

### Using Docker
1. Create a Dockerfile:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "djangoapi.wsgi:application", "--bind", "0.0.0.0:8000"]
```

2. Docker Compose configuration:
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=djangoapi
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
```

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path/to/your/static/;
    }

    location /media/ {
        alias /path/to/your/media/;
    }
}
```

### Security Considerations
1. Enable HTTPS:
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

2. Set security headers:
```python
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

## Performance Optimization

### Database Optimization
- Use database indexes:
```python
class Company(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    class Meta:
        indexes = [
            models.Index(fields=['created_at', 'type']),
        ]
```

### Caching Strategies
1. View caching:
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def company_list(request):
    # View logic here
```

2. Template fragment caching:
```html
{% load cache %}
{% cache 500 company_sidebar company.id %}
    <!-- Cached content -->
{% endcache %}
```

## Monitoring and Logging

### Logging Configuration
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

### Performance Monitoring
- Integration with Sentry
- New Relic configuration
- Prometheus metrics

## API Documentation

### Swagger/OpenAPI Integration
```python
INSTALLED_APPS = [
    ...
    'drf_yasg',
]

# URLs configuration
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Company API",
        default_version='v1',
    ),
    public=True,
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
]
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Implement the feature
5. Run tests and ensure they pass
6. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Use black for code formatting
- Run flake8 for linting

## License

This project is licensed under the MIT License.
