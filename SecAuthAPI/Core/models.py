from __future__ import unicode_literals
from django.db import models
from SecAuthAPI.Util.xacml import Util


class Policy(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100, null=True)
    content = models.TextField()

    class Meta:
        verbose_name = "Policy"
        verbose_name_plural = "Policies"

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = Util.get_policy_name(self.content)  # retrieve policy name from xacml file
        super(Policy, self).save(*args, **kwargs)
