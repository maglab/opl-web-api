from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class JobInformation(models.Model):
    info_id = models.AutoField(primary_key=True)
    info_title = models.CharField(max_length=50, unique=True)

    class Meta:
        abstract = True


class Organisation(JobInformation):
    def __str__(self) -> str:
        return f"{self.info_title}"


class JobField(JobInformation):
    def __str__(self) -> str:
        return f"{self.info_title}"


class Contact(models.Model):  # For non-auth users for now.
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    job_field = models.ForeignKey(
        JobField, on_delete=models.SET_NULL, null=True, blank=True
    )
    organisation = models.ForeignKey(
        Organisation, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        db_table_comment = "This table contains the contact details of the person who submitted the question"

    def __str__(self):
        return f"{self.first_name} {self.last_name} : {self.email}"


# Need to test how this userprofile would work with open Id.
class UserProfile(models.Model):
    account = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=False, null=False
    )
    firebase_uuid = models.CharField(max_length=50, blank=True, null=True)
    affiliation = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.account.username


# Signal to save or update the user profile whenever the User instance is updated. May not need for now.
# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, **kwargs):
#     UserProfile.objects.get_or_create(account=instance)
#     instance.userprofile.save()
