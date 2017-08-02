from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from SecAuthAPI.API import views
from django.conf.urls.static import static
from django.conf import settings


router = routers.DefaultRouter(schema_title="SecAuthAPI")
router.register(r'policy', views.PolicyViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include_docs_urls(title='SecAuthAPI')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

print settings.STATIC_ROOT
