from django.contrib import admin
from django import forms

from SecAuthAPI.Core.models import Policy
from SecAuthAPI.Core.xacml_util import XacmlUtil
from widgets import HtmlEditor


class PolicyAdminForm(forms.ModelForm):
    model = Policy

    # TODO: XML Formatter
    # Ref: https://stackoverflow.com/questions/11941971/how-to-override-field-value-display-in-django-admin-change-form
    # def __init__(self, *args, **kwargs):
    #    super(PolicyAdminForm, self).__init__(*args, **kwargs)
    #    self.initial['content'] = None or XacmlUtil(content=self.instance.content).xacml_formatter()

    class Meta:
        fields = '__all__'
        widgets = {
            'content': HtmlEditor(attrs={'style': 'width: 90%; height: 100%;'}),
        }


class PolicyAdmin(admin.ModelAdmin):
    form = PolicyAdminForm

    # field name is read-only (captured from xacml file)
    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + ('name', )


admin.site.register(Policy, PolicyAdmin)
admin.site.site_header = 'SecAuthAPI - Dashboard'
