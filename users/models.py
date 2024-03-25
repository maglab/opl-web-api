from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


# Make one to one copy or change field names ??
class User(AbstractUser):
    firebase_uid = models.CharField(max_length=50, blank=True, null=True)
    job_role = models.CharField(max_length=100, blank=True, null=True)
    affiliation = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "auth_user"
