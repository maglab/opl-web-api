from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


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
