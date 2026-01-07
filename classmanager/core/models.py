from django.db import models


class DynamicClass(models.Model):
    name = models.CharField(max_length=100)
    attributes = models.JSONField(default=list)  # list of attribute names

    def __str__(self):
        return self.name


class DynamicInstance(models.Model):
    dynamic_class = models.ForeignKey(
        DynamicClass, on_delete=models.CASCADE, related_name="instances"
    )
    values = models.JSONField(default=dict)  # dict of attr -> value

    def __str__(self):
        return f"{self.dynamic_class.name} instance {self.pk}"
