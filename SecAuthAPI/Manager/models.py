from __future__ import unicode_literals

from django.db import models


class Policy(models.Model):
    name = models.CharField(max_length=30, unique=True)
    content = models.TextField()

    def __str__(self):
        return self.name