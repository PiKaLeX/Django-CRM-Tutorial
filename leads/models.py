from django.db import models
from django.contrib.auth.models import AbstractUser

# Creating our own User class for future upgrade. 
class User(AbstractUser):
    pass

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username},{self.user.email}"

class Lead(models.Model):
    # Basic fields
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)

    # Foreign Key
    agent = models.ForeignKey("Agent", on_delete=models.CASCADE)

    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    # Just for learning purpose for different field available.

    # SOURCE_CHOICES = (
    #     ("Youtube", "Youtube"), # First is actual word in DB, second is the text to display. 
    #     ("Google", "Google"),
    #     ("Newsletter", "Newsletter"),
        
    # )

    #phoned = models.BooleanField(default=False)
    #source = models.CharField(choices=SOURCE_CHOICES, max_length=100)

    #profile_picture = models.ImageField(blank=True, null=True)
    #special_files = models.FileField(blank=True, null=True)



