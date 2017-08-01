from django.contrib import admin

from SecAuthAPI.Manager.models import Policy


class PolicyAdmin(admin.ModelAdmin):
    pass

admin.site.register(Policy, PolicyAdmin)