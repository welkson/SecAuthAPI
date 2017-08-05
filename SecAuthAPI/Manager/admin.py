from django.contrib import admin
from django import forms

from SecAuthAPI.Manager.models import Policy
from widgets import HtmlEditor


class PolicyAdminForm(forms.ModelForm):
    model = Policy

    class Meta:
        fields = '__all__'
        widgets = {
            'content': HtmlEditor(attrs={'style': 'width: 90%; height: 100%;'}),
        }


class PolicyAdmin(admin.ModelAdmin):
    form = PolicyAdminForm

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('name', )
        return self.readonly_fields

admin.site.register(Policy, PolicyAdmin)
admin.site.site_header = 'SecAuthAPI - Dashboard'
