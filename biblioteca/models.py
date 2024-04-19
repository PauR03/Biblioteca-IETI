from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    SUPERADMIN = 1
    ADMIN = 2
    USER = 3

    ROLE_CHOICES = (
        (SUPERADMIN, 'superadmin'),
        (ADMIN, 'admin'),
        (USER, 'user'),
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()

class UserProfile(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    center = models.CharField(max_length=100)
    cycle = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)