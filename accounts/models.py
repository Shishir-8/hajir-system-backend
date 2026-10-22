from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

# if i don't write this line then i can't create super_user and user if i remove username = None

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        # Normalize the email (convert domain to lowercase)
        email = self.normalize_email(email)
        
        # Create the user instance
        user = self.model(email=email, **extra_fields)
        
        # Hash the password (never store plain text passwords!)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Force superuser flags to True
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):

    class RoleChoices(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        MANAGER = "MANAGER", 'Manager'
        EMPLOYEE = 'EMPLOYEE', 'Employee'

    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(choices=RoleChoices.choices, default=RoleChoices.EMPLOYEE)
    
    # Required Django permission & status flags
    is_active = models.BooleanField(default=True)  # Can the user log in?
    is_staff = models.BooleanField(default=False)   # Can access Django Admin?
    date_joined = models.DateTimeField(auto_now_add=True)

    # Link the manager we wrote above
    objects = CustomUserManager()

    # 1. What field does the user type in to log in?
    USERNAME_FIELD = 'email' 
    # 2. What fields are requested when running `python manage.py createsuperuser`?
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email





    

