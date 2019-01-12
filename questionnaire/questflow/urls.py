from django.urls import path, include
from .views import index


urlpatterns = [
    path('api/v1/', include('questflow.api.urls')),
    path('', index),
]
