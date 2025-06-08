from django.db import models

# Create your models here.

class User(models.Model): 
    email = models.EmailField(unique=True, null=False)
    phone = models.CharField(max_length=10, unique=True, null=True)
    
    def __str__(self):
        return self.email, self.phone
