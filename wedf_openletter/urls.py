from django.urls import include, re_path
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

urlpatterns = [
    re_path(r'openletter/i18n/', include('django.conf.urls.i18n')),
    re_path(r'openletter/admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    re_path(r'openletter/', include('petitions.urls')),
)
