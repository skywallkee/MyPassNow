from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Password(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    website = models.CharField(max_length=256)
    username = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    password_db_key = models.CharField(max_length=256)

    def __str__(self):
        return self.website + " " + self.username

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)