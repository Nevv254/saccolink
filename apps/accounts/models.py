from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom user model for SaccoLink — single source of truth for authentication/roles
class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STAFF = "STAFF", "Staff"
        MEMBER = "MEMBER", "Member"

    # Use email as unique identifier for login
    email = models.EmailField(unique=True)

    # Optional contact info
    phone = models.CharField(max_length=15, blank=True, null=True)

    # Role field controls permission logic in the app
    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.MEMBER)

    # Date user joined, for accounting/registration workflows
    date_joined = models.DateTimeField(auto_now_add=True)

    # Email is used to authenticate instead of username
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  # keep username required for display

    def __str__(self):
        return f"{self.username} ({self.role})"
