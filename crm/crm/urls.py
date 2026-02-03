from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("users.urls")),
    path("accounts/", include("registration.urls")),
    path("products/", include("products.urls")),
    path("ads/", include("ads.urls")),
    path("leads/", include("leads.urls")),
    path("contracts/", include("contracts.urls")),
    path("customers/", include("customers.urls")),
]

# добавление в urlpatterns шаблонов URL для файлов MEDIA и STATIC (только в DEBUG режиме)
if settings.DEBUG:
    for param in (settings.MEDIA_URL, settings.MEDIA_ROOT), (
        settings.STATIC_URL,
        settings.STATIC_ROOT,
    ):
        urlpatterns.extend(static(param[0], document_root=param[1]))
