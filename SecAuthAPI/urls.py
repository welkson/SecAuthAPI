from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from rest_framework.urlpatterns import format_suffix_patterns
from SecAuthAPI.API import views
from django.conf.urls.static import static
from django.conf import settings

# from rest_framework import routers
# router = routers.DefaultRouter(schema_title="SecAuthAPI")
# router.register(r'policy', views.PolicyViewSet)
# url(r'^', include(router.urls)),

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include_docs_urls(title='SecAuthAPI')),

    # REST API
    url(r'^policy/$', views.policy_list),
    url(r'^policy/(?P<policy_name>\w+)', views.policy_detail),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
