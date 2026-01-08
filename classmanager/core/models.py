from django.db import models


class DynamicClass(models.Model):
    name = models.CharField(max_length=100)
    attributes = models.JSONField(default=list)

    def __str__(self):
        return self.name


class DynamicInstance(models.Model):
    dynamic_class = models.ForeignKey(
        DynamicClass, on_delete=models.CASCADE, related_name="instances"
    )
    values = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.dynamic_class.name} instance {self.pk}"


# Simple credential model
class AppUser(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(
        max_length=128
    )  # store plain for demo; use hashing in real apps

    def __str__(self):
        return self.username
