from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    CustomUser model representing a user in the system.
    
    Attributes:
        - email (EmailField): The email address of the user.
        - birth_date (DateField): The birth date of the user.
        - about_me (TextField): A short description about the user.
        - document_number (CharField): The document number of the user.
    
    Attributes inherits from AbstractUser:
        - username (CharField): The username of the user.
        - first_name (CharField): The first name of the user.
        - last_name (CharField): The last name of the user.
        - is_staff (BooleanField): Designates whether the user can access the admin site.
        - is_active (BooleanField): Designates whether the user account is active.
        - date_joined (DateTimeField): The date and time when the user account was created.
        
    Custom Manager:
        - objects (CustomUserManager): Custom manager for the CustomUser model.
    
    Methods:
        - __str__: Returns a string representation of the user.
        - clean: Validates the document number and birth date of the user.
        - save: Overrides the save method to set the username as 'first_name last_name' when saving the user.
    """
    email = models.EmailField(help_text='User email', unique=True)
    birth_date = models.DateField()
    about_me = models.TextField(max_length=500, blank=True, verbose_name='About me section')
    document_number = models.CharField(max_length=8, verbose_name='Document number')
    # profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True) TODO: add profile picture
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = CustomUserManager()
    
    def __str__(self) -> str:
        return self.email
    
    def clean(self):
        super.clean()
        
        if len(self.document_number) != 8:
            raise ValueError('Document number must be 8 characters long.')
        if int(self.document_number) <= 0:
            raise ValueError('Document number must be a positive number.')
        if not self.document_number.isdigit():
            raise ValueError('Document number must be a number.') 
        
        if self.birth_date.year - datetime.today.year < 18:
            raise ValueError('User must be at least 18 years old.')
        if self.birth_date.year - datetime.today.year > 100:
            raise ValueError('User birth date is invalid.')
    
    def save(self, *args, **kwargs):
        self.username = f"{self.first_name} {self.last_name}"
        super().save(*args, **kwargs)