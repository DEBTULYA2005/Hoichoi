from django.db import models

# Create your models here.

class User(models.Model): 
    emailorphone = models.EmailField(max_length=25, unique=True, null=True)
    
    
    def __str__(self):
        return self.emailorphone
