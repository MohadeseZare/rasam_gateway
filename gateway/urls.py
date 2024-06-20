from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('gatewaya/admin/', admin.site.urls),
    path('gatewaya/', include('logs.urls')),
    path('gatewaya/packaging/', include('packaging.api.urls')),
]
