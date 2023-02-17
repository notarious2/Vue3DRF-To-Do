from .models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreation(UserCreationForm):
    """Customizing User creation for use in admin panel"""

    class Meta:
        model = User
        fields = "__all__"
