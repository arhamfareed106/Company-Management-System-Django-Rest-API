from django.contrib import admin
from django.urls import path, include
from .views import home_page

urlpatterns = [
    # Admin page URL
    path('admin/', admin.site.urls),
    path('home/', home_page),
    path('', include('api.urls')),  # Including the URLs from the 'api' app
]
