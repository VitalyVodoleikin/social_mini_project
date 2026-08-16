from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import handler404
from django.urls import path, include


handler404 = 'django.views.defaults.page_not_found'

urlpatterns = [
    path("admin/", admin.site.urls),

    # URL приложений
    # path("posts/", include("posts.urls", namespace="posts")),
    path("", include("posts.urls", namespace="posts")),
    path("users/", include("users.urls", namespace="users")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
