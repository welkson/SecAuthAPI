# -*- coding: utf-8 -*
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_swagger.views import get_swagger_view
from SecAuthAPI.API import views
from django.conf.urls.static import static
from django.conf import settings


schema_view = get_swagger_view(title=u'SecAuthAPI Documentation')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^$', schema_view),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # REST API
    url(r'^policy/$', views.policy_list),
    url(r'^policy/(?P<policy_name>\w+)/$', views.policy_detail),
    url(r'^policy/(?P<policy_name>\w+)/(?P<rule_name>\w+)/$', views.policy_attribute),
    url(r'^clear_cache/$', views.clear_cache),

    # OAuth
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
