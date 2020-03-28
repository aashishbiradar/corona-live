from django.db import models
from django.contrib.postgres.fields import JSONField

class Cache(models.Model):
    cache_key = models.CharField(max_length = 255, primary_key = True)
    data = JSONField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

class Daily(models.Model):
    date = models.DateField()
    confirmed = models.IntegerField()
    active = models.IntegerField()
    recovered = models.IntegerField()
    death = models.IntegerField()
    migrated = models.IntegerField()
    source = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
