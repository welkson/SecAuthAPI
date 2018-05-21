from __future__ import unicode_literals

from django.db import models

from SecAuthAPI.Core.xacml_util import XacmlUtil


class Policy(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100, null=True)
    content = models.TextField()
    version = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name = "Policy"
        verbose_name_plural = "Policies"

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = XacmlUtil(content=self.content).get_policy_name()  # retrieve policy name from xacml file
        self.version += 1                                              # increment policy version
        super(Policy, self).save(*args, **kwargs)
