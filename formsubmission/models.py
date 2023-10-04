from django.db import models
from django_countries.fields import CountryField
from django.utils import timezone


class UserProfileManager(models.Manager):
    def get_all_profiles(self):
        return self.only('name', 'gender', 'phone', 'email', 'address', 'nationality',
                         'date_of_birth', 'education_background', 'preferred_contact').all()

    def get_active_profiles(self):
        return self.only('name', 'gender', 'phone', 'email', 'address', 'nationality',
                         'date_of_birth', 'education_background', 'preferred_contact'
                         ).filter(is_deleted=False)


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

    objects = UserProfileManager()

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['-id']

    def __str__(self):
        return self.name

    def mark_as_deleted(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
        return self

    def undelete_users(self):
        self.is_deleted = False
        self.deleted_at = timezone.now()
        self.save()
        return self
