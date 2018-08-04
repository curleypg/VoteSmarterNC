from django.db import models

# Create your models here.
class Bill(models.Model):
    number = models.IntegerField()
    chamber = models.CharField(max_length=8, default='')
    session = models.CharField(max_length=32, default='')
    session_id = models.CharField(max_length=8, default='')
    title = models.CharField(max_length=255, default='')
    passed_house = models.BooleanField(default=False)
    passed_senate = models.BooleanField(default=False)
    is_ratified = models.BooleanField(default=False)
    is_law = models.BooleanField(default=False)
