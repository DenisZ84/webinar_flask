from django.db import models

# Create your models here.
class MyApp(models.Model):
    name = models.CharField(max_length=123)
    name3 = models.CharField(max_length=123)

