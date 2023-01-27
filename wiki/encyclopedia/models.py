from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    pass

class Author(models.Model):
    title = models.CharField(max_length=128)
    d_writer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="writer")

    def __str__(self):
        return self.d_writer.username