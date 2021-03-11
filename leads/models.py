from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

# Creating our own User class for future upgrade. 
class User(AbstractUser):
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username}"

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey("UserProfile", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}"

class Lead(models.Model):
    # Basic fields
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)

    # Foreign Key
    organisation = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)

    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

def post_user_created_signals(sender, instance, created, **kwargs):
    print(f"{sender=}")
    print(f"{instance=}")
    print(f"{created=}")
    print(f"{kwargs=}")
    if created:
        # Create a new UserProfile
        UserProfile.objects.create(user=instance)

post_save.connect(post_user_created_signals, sender=User)