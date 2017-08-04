from __future__ import unicode_literals

from django.db import models


class Policy(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100, null=True)
    content = models.TextField()

    class Meta:
        verbose_name = "Policy"
        verbose_name_plural = "Policies"

    def __unicode__(self):
        return self.name



