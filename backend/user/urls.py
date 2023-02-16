from django.urls import path
from .views import RegistrationAPI

urlpatterns = [
    path('register/', RegistrationAPI.as_view(), name='register')
]
