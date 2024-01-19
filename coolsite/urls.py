from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from coolsite import settings
from women.views import pageNotFound

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('women.urls')),
]
handler404 = pageNotFound

# маршрут к нашим графическим файлам
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls"))
        ]
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
