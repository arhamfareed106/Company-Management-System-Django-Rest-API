from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin page URL
    path('admin/', admin.site.urls),
    path('', include('api.urls')),  # Include our api urls at the root
]
