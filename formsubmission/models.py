from django.db import models
from django_countries.fields import CountryField

class UserProfile(models.Model):
    """
    Model to represent user information.
    """

    # Fields for user information
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]

    PREFERRED_CONTACT_CHOICES = (
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('none', 'None'),
    )
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    nationality = CountryField()
    date_of_birth = models.DateField()
    education_background = models.TextField()
    preferred_contact = models.CharField(max_length=10, choices=PREFERRED_CONTACT_CHOICES)

    # Additional fields for tracking user status
    is_deleted = models.BooleanField(default=False, verbose_name='Is Deleted')
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Deleted At')

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return self.name